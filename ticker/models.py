from django.db import models
from django.utils.dateformat import format
from core.common.models import TimeStampedModel


class Price(TimeStampedModel):
    BUY = 'B'
    SELL = 'S'
    BUY_SELL_CHOICES = (
        (BUY, 'BUY'),
        (SELL, 'SELL')
    )
    type = models.CharField(max_length=1, choices=BUY_SELL_CHOICES)
    price_rub = models.FloatField()
    price_usd = models.FloatField()
    rate = models.FloatField()
    better_adds_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.rate:
            self.rate = self.price_rub / self.price_usd
        super(Price, self).save(*args, **kwargs)

    @property
    def unix_time(self):
        return format(self.created_on, 'U')

    @property
    def price_usd_formatted(self):
        return float('{0:.2f}'.format(self.price_usd))

    @property
    def price_rub_formatted(self):
        return float('{0:.2f}'.format(self.price_rub))
