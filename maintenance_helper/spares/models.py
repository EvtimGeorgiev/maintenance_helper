# spares/models.py

from django.core import validators
from django.db import models


class SparePart(models.Model):
    SPARE_PART_MAX_LENGTH = 12

    class Meta:
        ordering = ['part_number']

    part_number = models.CharField(
        primary_key=True,
        max_length=SPARE_PART_MAX_LENGTH,
        blank=False,
        null=False,
        validators=[validators.RegexValidator(
            r'^\d{2}\.\d{4}\.\d{4}$',
            message='Part number must be in the format xx.xxxx.xxxx')
        ],

    )

    description = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )

    price = models.FloatField(
        blank=False,
        null=False,
    )

    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='image'
    )

    def __str__(self):
        return self.part_number

    @property
    def qty_on_stock(self):
        return Stock.objects.get(part_number=self.part_number).quantity


class Stock(models.Model):
    part_number = models.OneToOneField(
        SparePart,
        primary_key=True,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    description = models.CharField(
        max_length=30,
        blank=False,
        null=False,
    )

    quantity = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0,
    )

    min_stock_qty = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0,
    )

    @staticmethod
    def add_to_stock(part_number, quantity):
        stock_item = Stock.objects.get(part_number=part_number)
        stock_item.quantity += quantity
        stock_item.save()
