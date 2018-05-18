from rest_framework import serializers
from core.serializers import NestedAddressSerializer,\
    NestedReadOnlyAddressSerializer, NestedPairSerializer, \
    TransactionSerializer
from referrals.serializers import ReferralCodeSerializer
from ticker.serializers import RateSerializer

from orders.models import Order
from core.models import Address, Pair

from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as RestValidationError
from django.utils.translation import ugettext_lazy as _
from core.validators import get_validator, validate_xmr_payment_id


BASE_FIELDS = ('amount_base', 'is_default_rule', 'unique_reference',
               'payment_id', 'amount_quote', 'pair', 'withdraw_address')
READABLE_FIELDS = ('deposit_address', 'created_on', 'from_default_rule',
                   'unique_reference', 'deposit_address',
                   'payment_window', 'payment_deadline', 'kyc_deadline',
                   'status_name', 'transactions', 'referral_code',
                   'withdrawal_fee', 'withdrawal_fee_quote',
                   'user_provided_amount')
RATE_FIELDS = ('amount_usd', 'amount_btc', 'amount_eur', 'price',
               'amount_quote_fee')
UPDATE_FIELDS = ('refund_address',)
CREATE_FIELDS = ('payment_url', 'token')
FIAT_FIELDS = ('payment_url',)
TOKEN_FIELDS = ('token',)


class MetaOrder:
    model = Order
    fields = BASE_FIELDS
    read_only_fields = READABLE_FIELDS


class MetaFlatOrder(MetaOrder):
    fields = MetaOrder.fields + READABLE_FIELDS


class OrderSerializer(serializers.ModelSerializer):
    referral_code = ReferralCodeSerializer(many=True, read_only=True,
                                           source='user.referral_code')
    pair = NestedPairSerializer(many=False, read_only=False)
    deposit_address = NestedReadOnlyAddressSerializer(many=False,
                                                      read_only=True)
    withdraw_address = NestedAddressSerializer(many=False,
                                               read_only=False, partial=True)
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta(MetaFlatOrder):
        fields = MetaFlatOrder.fields


class OrderDetailSerializer(OrderSerializer):

    price = RateSerializer(many=False, read_only=True)

    class Meta(MetaFlatOrder):
        fields = MetaFlatOrder.fields + RATE_FIELDS + FIAT_FIELDS


class UpdateOrderSerializer(OrderSerializer):
    refund_address = NestedAddressSerializer(many=False,
                                             read_only=False, partial=True)

    class Meta(MetaOrder):
        fields = UPDATE_FIELDS

    def validate(self, data):
        if self.instance.refund_address:
            raise ValidationError(_(
                'Order {} already has refund address'.format(
                    self.instance.unique_reference
                )
            ))
        currency = self.instance.pair.quote.code
        validate_address = get_validator(currency)
        validate_address(data['refund_address']['address'])
        return super(UpdateOrderSerializer, self).validate(data)

    def update(self, instance, validated_data):
        refund_address = validated_data.pop('refund_address')
        addr_list = Address.objects.filter(address=refund_address['address'])
        if not addr_list:
            address = Address(**refund_address)
            address.type = Address.WITHDRAW
            address.currency = instance.pair.quote
            address.save()
        else:
            address = addr_list[0]
        instance.refund_address = address
        instance.save()
        return instance


class CreateOrderSerializer(OrderSerializer):
    class Meta(MetaOrder):
        # hack to allow seeing needed fields in
        # response from post (lines 47:51)
        fields = BASE_FIELDS + READABLE_FIELDS + FIAT_FIELDS + TOKEN_FIELDS

    def validate(self, data):
        # TODO: custom validation based on order.pair.base
        pair = data['pair']['name']
        try:
            pair_obj = Pair.objects.get(name=pair, disabled=False)
            self.pair = pair_obj
        except Pair.DoesNotExist:
            raise ValidationError(_('%(value)s is not'
                                    ' currently a supported Pair'),
                                  params={'value': pair})
        if all(['amount_base' not in data, 'amount_quote' not in data]):
            raise ValidationError(
                _('One of amount_quote and amount_base is required.'))

        currency = pair_obj.base.code
        validate_address = get_validator(currency)
        validate_address(data['withdraw_address']['address'])
        if 'payment_id' in data:
            validate_xmr_payment_id(data['payment_id'])

        return super(CreateOrderSerializer, self).validate(data)

    def create(self, validated_data):
        for field in READABLE_FIELDS:
            validated_data.pop(field, None)
        withdraw_address = validated_data.pop('withdraw_address')

        validated_data.pop('pair')
        # Just making sure
        addr_list = Address.objects.filter(address=withdraw_address['address'])
        order = Order(pair=self.pair, **validated_data)
        if not addr_list:
            address = Address(**withdraw_address)
            address.type = Address.WITHDRAW
            address.currency = order.pair.base
            address.save()
        else:
            address = addr_list[0]

        order.withdraw_address = address
        if validated_data.get('payment_id'):
            order.payment_id = validated_data.pop('payment_id')
        try:
            order.save()
            # get post_save stuff in sync
            order.refresh_from_db()
            return order
        except ValidationError as e:
            raise RestValidationError({'non_field_errors': [e.message]})

    def update(self, instance, validated_data):
        # Forbid updating after creation
        return instance
