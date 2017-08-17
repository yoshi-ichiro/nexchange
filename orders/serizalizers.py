from rest_framework import serializers
from core.serializers import NestedAddressSerializer,\
    NestedReadOnlyAddressSerializer, NestedPairSerializer, \
    TransactionSerializer

from orders.models import Order
from core.models import Address, Pair

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


BASE_FIELDS = ('amount_base', 'is_default_rule',
               'unique_reference', 'amount_quote', 'pair', 'withdraw_address')
READABLE_FIELDS = ('deposit_address', 'created_on', 'amount_quote', 'from_default_rule',
                   'unique_reference', 'deposit_address',
                   'payment_window', 'payment_deadline',
                   'status_name', 'transactions')


class MetaOrder:
    model = Order
    fields = BASE_FIELDS
    read_only_fields = READABLE_FIELDS


class MetaFlatOrder(MetaOrder):
    fields = MetaOrder.fields + READABLE_FIELDS


class OrderSerializer(serializers.ModelSerializer):
    pair = NestedPairSerializer(many=False, read_only=False)
    deposit_address = NestedReadOnlyAddressSerializer(many=False,
                                                      read_only=True)
    withdraw_address = NestedAddressSerializer(many=False,
                                               read_only=False, partial=True)
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta(MetaFlatOrder):
        fields = MetaFlatOrder.fields


class CreateOrderSerializer(OrderSerializer):
    class Meta(MetaOrder):
        # hack to allow seeing needed fields in
        # response from post (lines 47:51)
        fields = BASE_FIELDS + READABLE_FIELDS

    def create(self, validated_data):
        for field in READABLE_FIELDS:
            validated_data.pop(field, None)
        withdraw_address = validated_data.pop('withdraw_address')
        pair = validated_data.pop('pair')
        try:
            pair_obj = Pair.objects.get(name=pair.get('name'))
        except Pair.DoesNotExist:
            raise ValidationError(_('The pair you have entered is'
                                    ' currently not supported'))

        # Just making sure
        addr_list = Address.objects.filter(address=withdraw_address['address'])
        order = Order(pair=pair_obj, **validated_data)
        if not addr_list:
            address = Address(**withdraw_address)
            address.type = Address.WITHDRAW
            address.currency = order.pair.base
            address.save()
        else:
            address = addr_list[0]

        order.withdraw_address = address
        order.save()
        # get post_save stuff in sync
        order.refresh_from_db()
        return order

    def update(self, instance, validated_data):
        # Forbid updating after creation
        return instance
