from typing import Union

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Coupon


def validate_coupon(value: Union[str, None]) -> None:
    """
        ვამოწმებთ არსებობს თუ არა კუპონი რომელიც შეიყვანა
        თუ არ არსებობს ვაბრუნებთ ერორს.
        თუ არსებობს ვამოწმებთ ვადას თუ ვადა გასული აქვს მაშინაც ვისვრით ერორს.

    """
    if value:
        coupon = Coupon.objects.filter(code=value)

        if not coupon.exists():
            raise ValidationError(
                _('%(value)s is not an valid Coupon'),
                params={'value': value},
            )
        else:
            valid_coupon = coupon.filter(expiration_date__gt=timezone.datetime.now())
            if not valid_coupon.exists():
                raise ValidationError(
                    _('The coupon is expired')
                )
