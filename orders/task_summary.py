from .tasks.generic.buy_order_release import BuyOrderReleaseByRule,\
    BuyOrderReleaseByWallet, BuyOrderReleaseByReference
from .tasks.generic.exchange_order_release import ExchangeOrderRelease
from orders.tasks.generic.retry_release import RetryOrderRelease
from django.conf import settings
from celery import shared_task
from payments.models import Payment
from orders.models import Order, LimitOrder
from core.models import Transaction
from .decorators import get_task
from nexchange.utils import get_nexchange_logger
from nexchange.celery import app
from django.db.models import Q


@shared_task(time_limit=settings.TASKS_TIME_LIMIT)
@get_task(task_cls=BuyOrderReleaseByReference, key='payment__in')
def buy_order_release_by_reference_invoke(payment_id, task=None):
    task.run(payment_id)


@shared_task(time_limit=settings.TASKS_TIME_LIMIT)
@get_task(task_cls=BuyOrderReleaseByRule, key='payment__in')
def buy_order_release_by_rule_invoke(payment_id, task=None):
    task.run(payment_id)


@shared_task(time_limit=settings.TASKS_TIME_LIMIT)
@get_task(task_cls=BuyOrderReleaseByWallet, key='payment__in')
def buy_order_release_by_wallet_invoke(payment_id, task=None):
    task.run(payment_id)


@shared_task(time_limit=settings.TASKS_TIME_LIMIT)
def buy_order_release_reference_periodic():
    logger = get_nexchange_logger('Periodic Buy Order Release')
    for payment in Payment.objects.filter(
        is_success=True,
        is_redeemed=False,
        flagged=False,
        order__status=Order.PAID
    ):
        try:
            order = payment.order
            if order.coverable:
                buy_order_release_by_reference_invoke.apply_async([payment.pk])
            else:
                logger.warning('Not enough funds to release order {}'.format(
                    order.unique_reference))
        except Exception as e:
            logger.warning(e)


@shared_task(time_limit=settings.TASKS_TIME_LIMIT)
@get_task(task_cls=ExchangeOrderRelease, key='transactions__in')
def exchange_order_release_invoke(transaction_id, task=None):
    task.run(transaction_id)


@shared_task(time_limit=settings.TASKS_TIME_LIMIT)
def exchange_order_release_periodic():
    logger = get_nexchange_logger('Periodic Exchange Order Release')
    dep_txs = Transaction.objects.filter(type=Transaction.DEPOSIT,
                                         flagged=False)
    txs = dep_txs.filter(
        Q(
            order__exchange=True, order__status=Order.PAID,
            order__withdraw_address__isnull=False) |
        Q(
            limit_order__status=LimitOrder.PAID,
            limit_order__withdraw_address__isnull=False)
    )
    for tx in txs:
        try:
            order = tx.order if tx.order else tx.limit_order
            if order.coverable:
                exchange_order_release_invoke.apply_async([tx.pk])
            else:
                logger.warning('Not enough funds to release order {}'.format(
                    order.unique_reference))
        except Exception as e:
            logger.warning(e)


@shared_task(time_limit=settings.TASKS_TIME_LIMIT)
@get_task(task_cls=RetryOrderRelease, key='transactions__in')
def release_retry(transaction_id, task=None):
    res = task.run(transaction_id)
    return res


@app.task(bind=True)
def release_retry_invoke(self, transaction_id):
    task_info = release_retry.apply([transaction_id])
    res = task_info.result
    if res.get('retry'):
        self.retry(countdown=settings.RETRY_RELEASE_TIME,
                   max_retries=settings.RETRY_RELEASE_MAX_RETRIES)


@shared_task(time_limit=settings.TASKS_TIME_LIMIT)
def cancel_unpaid_order_periodic():
    orders = Order.objects.filter(
        status=Order.INITIAL,
        flagged=False
    ).order_by('pk')[:settings.MAX_NUMBER_CANCEL_ORDER]
    for order in orders:
        cancel_unpaid_order.apply_async([order.pk])


@shared_task(time_limit=settings.TASKS_TIME_LIMIT)
def cancel_unpaid_order(order_id):
    order = Order.objects.get(pk=order_id)
    if order.unpaid_order_expired:
        order.cancel()
