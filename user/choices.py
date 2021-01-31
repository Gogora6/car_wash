from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class Status(IntegerChoices):
    customer = 1, _("Customer")
    washer = 2, _("Washer")
    manager = 3, _("Manager")
