from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if value < 1 or value > timezone.now().year:
        raise ValidationError(
            ('%s is not a correct year!' % value)
        )


def raiting_validator(value):
    if value < 1 or value > 10:
        raise ValidationError(
            ('%s is not a caorrect raiting!' % value)
        )
