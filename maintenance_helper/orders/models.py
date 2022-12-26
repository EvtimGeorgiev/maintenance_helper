import datetime

from django.core import validators
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from maintenance_helper.spares.models import SparePart


class Order(models.Model):
    ORDER_NUMBER_MAX_LENGTH = 15
    ORDER_NUMBER_MIN_LENGTH = 12
    order_number = models.CharField(
        max_length=ORDER_NUMBER_MAX_LENGTH,
        validators=[
            validators.MaxLengthValidator(ORDER_NUMBER_MIN_LENGTH),
        ],
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
    )

    total_price = models.FloatField(
        null=False,
        blank=False,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
    )

    received_on = models.DateTimeField(
        blank=True,
        null=True,
    )

    @classmethod
    def get_next_order_number(cls):
        last_order_number = ''
        try:
            last_order_number = cls.objects.latest('created_on').order_number
        except ObjectDoesNotExist:
            pass

        if last_order_number == '' or (str(datetime.date.today()) != last_order_number.split('_')[0]):
            return f'{datetime.date.today()}_1'

        else:
            return f'{datetime.date.today()}_{int(last_order_number.split("_")[1]) + 1}'

    def __str__(self):
        return f'Order No: {self.order_number}'


class OrderedItem(models.Model):
    order_number = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT,
    )

    part_number = models.ForeignKey(
        SparePart,
        on_delete=models.RESTRICT,
        blank=False,
        null=False
    )

    description = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        default='NA',
    )

    quantity = models.PositiveIntegerField(
        blank=False,
        null=False,
    )

    price = models.FloatField(
        blank=False,
        null=False,
    )

    @property
    def total_items_price(self):
        return self.quantity * self.price


class Cart(models.Model):
    part_number = models.CharField(
        primary_key=True,
        max_length=12,
        blank=True,
        null=False,
    )

    description = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        default='NA'
    )

    quantity = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1, message='Minimum order value is 1'),
        ]
    )

    class Meta:
        verbose_name_plural = 'Cart'

    @property
    def price(self):
        return SparePart.objects.get(part_number=self.part_number).price

    @property
    def item_cart_total(self):
        return self.price * self.quantity

    @classmethod
    def add_to_cart(cls, part_number, qty):
        item = None
        try:
            item = cls.objects.get(part_number=part_number)
        except ObjectDoesNotExist:
            pass

        if item:
            item.quantity += qty
        else:
            description = SparePart.objects.get(part_number=part_number).description
            item = cls.objects.create(part_number=part_number, description=description, quantity=qty)
        item.save()

    @staticmethod
    def get_total_price():
        total_price = 0
        items = Cart.objects.all()
        for item in items:
            price = SparePart.objects.get(part_number=item.part_number).price
            quantity = item.quantity
            total_price += quantity * price

        return total_price

    @classmethod
    def empty_cart(cls):
        cls.objects.all().delete()
