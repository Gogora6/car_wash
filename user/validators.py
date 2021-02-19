from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validate_birthdate(value: datetime) -> None:
    if value > datetime.date.today():
        raise ValidationError(
            _('Birthdate cannot be in the past!'),
        )
