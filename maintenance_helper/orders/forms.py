from django import forms

from maintenance_helper.orders.models import OrderedItem
from maintenance_helper.spares.models import SparePart


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = OrderedItem
        fields = ('part_number', 'quantity')
