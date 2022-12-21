from django.db import models

from maintenance_helper.machines.models import Machine


class Issue(models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.RESTRICT,
        blank=False,
        null=False,
    )
    description = models.TextField(
        blank=False,
        null=False,
    )
    created_by = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )

    closed_by = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
    )

    closed_on = models.DateTimeField(
        blank=True,
        null=True,

    )

    @property
    def short_description(self):
        return f'{self.description[0:40]}...'

    @property
    def status(self):
        if self.closed_on:
            return 'closed'
        return 'open'

    @property
    def create_on_date(self):
        return self.created_on.date()
