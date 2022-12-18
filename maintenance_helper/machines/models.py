# machines/models

from django.db import models


class Machine(models.Model):
    serial_number = models.CharField(
        max_length=30,
        blank=False,
        null=False,
    )

    type = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )

    name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
    )

    image_url = models.URLField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
