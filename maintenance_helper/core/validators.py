from django.core import exceptions


def validate_only_chars(value):
    for ch in value:
        if not ch.isalpha():
            raise exceptions.ValidationError('Field must consist of letters only.')


def validate_part_number(value):
    pass
