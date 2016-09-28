from __future__ import absolute_import

from celery import shared_task
import logging
from core.models import Payment, Order, Transaction
from django.conf import settings
from twilio.rest import TwilioRestClient
from twilio.exceptions import TwilioException
from django.utils.translation import ugettext_lazy as _

logging.basicConfig(filename='payment_release.log', level=logging.INFO)


@shared_task
def payment_release():
    for o in Order.objects.filter(is_paid=True, is_released=False):
        print("Look order {} ".format(o.unique_reference))
        p = Payment.objects.filter(user=o.user,
                                   amount_cash=o.amount_cash,
                                   payment_preference=o.payment_preference,
                                   is_complete=False,
                                   currency=o.currency).first()
        if p is not None:
            print("release the bitcoins")
            print("id={}, unique_reference={}".format(o.id,
                                                      o.unique_reference))
            o.is_released = True
            o.save()

            # send sms depending on notification settings in profile
            msg = _("Your order %s:") + ' is released' % o.unique_reference
            phone_to = str(o.user.username)

            try:
                client = TwilioRestClient(
                    settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=msg, to=phone_to, from_=settings.TWILIO_PHONE_FROM)
                return message
            except TwilioException as err:
                return err
            # email
        else:
            print('payment not found ')


@shared_task
def checker_transactions():
    for tr in Transaction.objects.all():
        print("Look transaction {} ".format(tr.tx_id))
