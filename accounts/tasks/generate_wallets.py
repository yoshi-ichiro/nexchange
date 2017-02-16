from __future__ import absolute_import
from django.conf import settings
from nexchange.utils import CreateUpholdCard
from payments.models import UserCards
import logging


def renew_cards_reserve():
    if settings.DEBUG:
        logging.info(
            settings.CARDS_RESERVE_COUNT,
            settings.API1_USER,
            settings.API1_PASS
        )
    api = CreateUpholdCard(settings.API1_IS_TEST)
    api.auth_basic(settings.API1_USER, settings.API1_PASS)
    currency = {
        'BTC': 'bitcoin',
        'LTC': 'litecoin',
        'ETH': 'ethereum'
    }
    for key, value in currency.items():
        count = UserCards.objects.filter(user=None, currency=key).count()
        while count < settings.CARDS_RESERVE_COUNT:
            new_card = api.new_card(key)
            logging.info(
                "new card currency: {}, card: {}".format(
                    new_card, key))
            address = api.add_address(new_card['id'], value)
            card = UserCards(card_id=new_card['id'],
                             currency=new_card['currency'],
                             address_id=address['id'])
            card.save()
            count = UserCards.objects.filter(user=None, currency=key).count()
