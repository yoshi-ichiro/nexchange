from unittest.mock import patch

from django.conf import settings
from payments.tasks.generic.payeer import PayeerPaymentChecker

from core.tests.base import WalletBaseTestCase
from orders.models import Order
from payments.models import Payment, PaymentPreference
from payments.tasks.generic.ok_pay import OkPayPaymentChecker
from core.tests.utils import get_ok_pay_mock


class WalletAPITestCase(WalletBaseTestCase):
    @patch('orders.models.Order.convert_coin_to_cash')
    @patch('nexchange.utils.OkPayAPI.get_date_time')
    @patch('nexchange.utils.OkPayAPI._get_transaction_history')
    def test_confirm_order_payment_with_okpay_celery(self, history, datetime,
                                                     convert_to_cash):
        history.return_value = get_ok_pay_mock()
        datetime.return_value = '2017-01-11-10:00'
        convert_to_cash.return_value = None
        order = Order(**self.okpay_order_data)
        order.save()
        import_okpay_payments = OkPayPaymentChecker()
        import_okpay_payments.run()

        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            reference=order.unique_reference
        )
        self.assertEqual(1, len(p))
        pref = PaymentPreference.objects.filter(payment=p[0])
        self.assertEqual(1, len(pref))
        self.assertEqual(pref[0].identifier, 'dobbscoin@gmail.com')
        self.assertEqual(pref[0].secondary_identifier, 'OK487565544')
        # apply second time - should not create another payment
        import_okpay_payments.run()

        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            reference=order.unique_reference
        )
        self.assertEqual(1, len(p))
        # check that pref is intact
        pref = PaymentPreference.objects.filter(payment=p[0])
        self.assertEqual(1, len(pref))
        self.assertEqual(pref[0].identifier, 'dobbscoin@gmail.com')
        self.assertEqual(pref[0].secondary_identifier, 'OK487565544')

    @patch('nexchange.utils.PayeerAPIClient.history_of_transactions')
    @patch('orders.models.Order.convert_coin_to_cash')
    def test_import_payeer__invalid_wallet(self, convert_to_cash, trans_hist):
        convert_to_cash.return_value = None
        sender = 'zaza'
        # TODO: get fixutre
        trans_hist.return_value = {
            '1': {
                'id': '1',
                'type': 'transfer',
                'status': 'success',
                'creditedCurrency': self.EUR.code,
                'creditedAmount': str(self.payeer_order_data['amount_cash']),
                'to': 'tata',
                'shopOrderId': self.payeer_order_data['unique_reference'],
                'comment': self.payeer_order_data['unique_reference'],
                'from': sender
            }
        }
        order = Order(**self.payeer_order_data)
        order.save()
        import_payeer_payments = PayeerPaymentChecker()
        import_payeer_payments.run()
        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            reference=order.unique_reference
        )
        self.assertEqual(0, len(p))
        # assert payment pref is created correctly

    @patch('nexchange.utils.PayeerAPIClient.history_of_transactions')
    @patch('orders.models.Order.convert_coin_to_cash')
    def test_import_payeer_invalid_status(self, convert_to_cash, trans_hist):
        convert_to_cash.return_value = None
        sender = 'zaza'
        # TODO: get fixutre
        trans_hist.return_value = {
            '1': {
                'id': '1',
                'type': 'transfer',
                'status': 'None',
                'creditedCurrency': self.EUR.code,
                'creditedAmount': str(self.payeer_order_data['amount_cash']),
                'to': 'tata',
                'shopOrderId': self.payeer_order_data['unique_reference'],
                'comment': self.payeer_order_data['unique_reference'],
                'from': sender
            }
        }
        order = Order(**self.payeer_order_data)
        order.save()
        import_payeer_payments = PayeerPaymentChecker()
        import_payeer_payments.run()
        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            reference=order.unique_reference
        )
        self.assertEqual(0, len(p))
        # assert payment pref is created correctly

    @patch('nexchange.utils.PayeerAPIClient.history_of_transactions')
    @patch('orders.models.Order.convert_coin_to_cash')
    def test_confirm_order_payment_with_payeer_celery(self, convert_to_cash,
                                                      trans_hist):
        convert_to_cash.return_value = None
        sender = 'zaza'
        # TODO: get fixutre
        trans_hist.return_value = {
            '1': {
                'id': '1',
                'type': 'transfer',
                'status': 'success',
                'creditedCurrency': self.EUR.code,
                'creditedAmount': str(self.payeer_order_data['amount_cash']),
                'to': settings.PAYEER_ACCOUNT,
                'shopOrderId': self.payeer_order_data['unique_reference'],
                'comment': self.payeer_order_data['unique_reference'],
                'from': sender
            }
        }
        order = Order(**self.payeer_order_data)
        order.save()
        import_payeer_payments = PayeerPaymentChecker()
        import_payeer_payments.run()
        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            reference=order.unique_reference
        )
        self.assertEqual(1, len(p))
        # assert payment pref is created correctly
        pref = PaymentPreference.objects.filter(payment=p[0])
        self.assertEqual(1, len(pref))

        self.assertEquals(pref[0].identifier,
                          sender)

        # apply second time - should not create another payment\payment
        # preference
        import_payeer_payments.run()
        p = Payment.objects.filter(
            amount_cash=order.amount_cash,
            currency=order.currency,
            reference=order.unique_reference
        )
        self.assertEqual(1, len(p))
        pref = PaymentPreference.objects.filter(payment=p[0])
        self.assertEqual(1, len(pref))

        self.assertEquals(pref[0].identifier,
                          sender)
