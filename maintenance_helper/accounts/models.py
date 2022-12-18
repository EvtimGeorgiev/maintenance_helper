# accounts/models.py

from enum import Enum

from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models
from maintenance_helper.core.validators import validate_only_chars


class ChoicesEnumMixin(Enum):
    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def max_length(cls):
        return max(len(x) for x, _ in cls.choices())


class Position(ChoicesEnumMixin):
    operator = 'Operator'
    technician = 'Technician'
    maintenance = 'Maintenance'
    manager = 'Manager'


class AppUser(auth_models.AbstractUser):
    MIN_LENGTH_FIRST_NAME = 3
    MAX_LENGTH_FIRST_NAME = 30
    MIN_LENGTH_LAST_NAME = 3
    MAX_LENGTH_LAST_NAME = 30

    username = models.CharField(
        verbose_name='trigram',
        unique=True,
        null=False,
        blank=False,
        max_length=3,
        validators=(
            validators.MinLengthValidator(3),
            validate_only_chars,
        ),
    )

    first_name = models.CharField(
        verbose_name='First Name',
        null=False,
        blank=False,
        max_length=MAX_LENGTH_FIRST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_FIRST_NAME),
            validate_only_chars,
        ),
    )

    last_name = models.CharField(
        verbose_name='Last Name',
        null=False,
        blank=False,
        max_length=MAX_LENGTH_LAST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LENGTH_LAST_NAME),
            validate_only_chars
        ),
    )

    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
    )

    position = models.CharField(
        null=False,
        blank=False,
        choices=Position.choices(),
        max_length=Position.max_length()
    )

    image_url = models.URLField(
        null=True,
        blank=True,
    )


