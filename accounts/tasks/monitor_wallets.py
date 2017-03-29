from __future__ import absolute_import
from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from core.models import Transaction, Address
from payments.models import UserCards
from orders.models import Order
from nexchange.utils import check_transaction_uphold, send_email, send_sms
from accounts.utils import UpholdTransactionImporter
from nexchange.utils import get_nexchange_logger
from orders.task_summary import (sell_order_release_invoke,
                                 exchange_order_release_invoke)
from django.db import transaction


def update_pending_transactions():
    logger = get_nexchange_logger(__name__, True, True)
    next_tasks = set()
    for tr in Transaction.objects.\
            filter(Q(is_completed=False) | Q(is_verified=False)):
        order = tr.order
        profile = order.user.profile
        logger.info(
            'Look-up transaction with txid api {} '.format(tr.tx_id_api))
        if tr.address_to.type == Address.WITHDRAW and \
                check_transaction_uphold(tr):
            tr.is_completed = True
            tr.is_verified = True
            tr.save()
            order.status = Order.COMPLETED
            order.save()

        if tr.address_to.type == Address.DEPOSIT and \
                check_transaction_uphold(tr):

            with transaction.atomic():
                tr.is_completed = True
                tr.is_verified = True
                tr.save()
                order.status = Order.PAID
                order.save()
            if not order.exchange:
                next_tasks.add((sell_order_release_invoke, None,))
            else:
                next_tasks.add((exchange_order_release_invoke, tr.pk, ))

            # trigger release
            title = _('Nexchange: Order released')
            if not order.exchange:
                msg = _(
                    'Your order {}:  is PAID. '
                    '\n {} {} were sent to {} {} {}'). format(
                    order.unique_reference,
                    order.amount_quote,
                    order.pair.quote.code,
                    order.payment_preference.payment_method.name,
                    order.payment_preference.identifier,
                    '(' +
                    order.payment_preference.secondary_identifier +
                    ')' if
                    order.payment_preference.secondary_identifier else ''
                )
            else:
                msg = _(
                    'Your order {}:  is PAID. '
                    '\n '
                ). format(order)

            if profile.notify_by_phone and profile.phone:
                phone_to = str(tr.order.user.username)
                sms_result = send_sms(msg, phone_to)

                if settings.DEBUG:
                    logger.info(str(sms_result))

            if profile.notify_by_email and order.user.email:
                email = send_email(tr.order.user.email, title, msg)
                email.send()

            if settings.DEBUG:
                logger.info('Transaction {} is completed'.format(tr.tx_id))

    for task, args in next_tasks:
        if args is not None:
            res = task.apply([args])
        else:
            res = task.apply()
        if res.state != 'SUCCESS':
            logger.error(
                'Task {} returned error traceback: {}'.format(
                    task.name, res.traceback))


def import_transaction_deposit_crypto():
    logger = get_nexchange_logger(__name__, True, True)
    addresses = Address.objects.filter(
        currency__is_crypto=True,
        type=Address.DEPOSIT
    )
    for addr in addresses:
        cards = UserCards.objects.filter(
            address_id=addr.address, user=addr.user, currency=addr.currency)
        if len(cards) > 1:
            logger.error('Deposit Address {} has more then 1 UserCard'.format(
                addr
            ))
            continue
        if len(cards) < 1:
            logger.error('Deposit Address {} has no UserCard'.format(
                addr
            ))
            continue
        importer = UpholdTransactionImporter(
            cards[0], addr
        )
        importer.import_income_transactions()
