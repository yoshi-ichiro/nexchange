
from decimal import Decimal

from core.tests.base import OrderBaseTestCase, UserBaseTestCase
from orders.models import Order
from payments.models import Payment, PaymentPreference, PaymentMethod
from nexchange.tasks import check_okpay_payments, check_payeer_payments
from unittest.mock import patch
from django.conf import settings


class WalletAPITestCase(UserBaseTestCase, OrderBaseTestCase):

    def setUp(self):
        super(WalletAPITestCase, self).setUp()
        self.payment_method = PaymentMethod(name='Okpay')
        self.payment_method.save()
        pref_data = {
            'user': self.user,
            'comment': 'Just testing',
            'payment_method': self.payment_method
        }
        pref = PaymentPreference(**pref_data)
        pref.save()
        # look at:
        # nexchange/tests/fixtures/transaction_history.xml self.order_data
        # matches first transaction from the XML file
        self.order_data = {
            'amount_cash': 85.85,
            'amount_btc': Decimal(0.01),
            'currency': self.EUR,
            'user': self.user,
            'admin_comment': 'tests Order',
            'unique_reference': '12345',
            'payment_preference': pref,
        }

    @patch('orders.models.Order.convert_coin_to_cash')
    @patch('nexchange.utils.OkPayAPI.get_date_time')
    @patch('nexchange.utils.OkPayAPI._get_transaction_history')
    def test_confirm_order_payment_with_okpay_celery(self, history, datetime,
                                                     convert_to_cash):
        with open('nexchange/tests/fixtures/transaction_history.xml') as f:
            history.return_value = str.encode(f.read().replace('\n', ''))
        datetime.return_value = '2017-01-11-10:00'
        convert_to_cash.return_value = None
        order = Order(**self.order_data)
        order.save()
        check_okpay_payments.apply()
        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            order=order,
            reference=order.unique_reference
        )
        self.assertEqual(1, len(p))
        # apply second time - should not create another payment
        check_okpay_payments.apply()
        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            order=order,
            reference=order.unique_reference
        )
        self.assertEqual(1, len(p))

    @patch('nexchange.utils.PayeerAPIClient.history_of_transactions')
    @patch('orders.models.Order.convert_coin_to_cash')
    def test_confirm_order_payment_with_payeer_celery(self, convert_to_cash,
                                                      trans_hist):
        convert_to_cash.return_value = None
        trans_hist.return_value = [{
            'type': 'transfer',
            'status': 'success',
            'creditedCurrency': self.EUR.code,
            'creditedAmount': str(self.order_data['amount_cash']),
            'to': settings.PAYEER_ACCOUNT,
            'shopOrderId': self.order_data['unique_reference'],
            'comment': self.order_data['unique_reference']
        }]
        order = Order(**self.order_data)
        order.save()
        check_payeer_payments.apply()
        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            order=order,
            reference=order.unique_reference
        )
        self.assertEqual(1, len(p))
        # apply second time - should not create another payment
        check_payeer_payments.apply()
        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            order=order,
            reference=order.unique_reference
        )
        self.assertEqual(1, len(p))
