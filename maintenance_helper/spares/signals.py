from django.db.models import signals
from django.dispatch import receiver

from maintenance_helper.spares.models import SparePart, Stock


@receiver(signals.post_save, sender=SparePart)
def create_stock_item_on_part_creation(instance, created, *args, **kwargs):
    if created:
        Stock.objects.create(
            pk=instance.pk,
            description=instance.description
        )
    else:
        Stock.objects.filter(pk=instance.pk).update(description=instance.description)
