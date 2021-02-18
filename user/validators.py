from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validate_birthdate(birthdate: str) -> None:
    if birthdate > datetime.date.today():
        raise ValidationError(
            _('Birthdate cannot be in the past!'),
        )
