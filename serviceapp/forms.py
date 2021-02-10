from django.forms import ModelChoiceField, CharField, Textarea, DateTimeInput
from django.core.validators import MaxLengthValidator
from django import forms

from user.models import User
from .models import Order, Car, WashType

from user.choices import Status

from .valdators import validate_coupon


class OrderForm(forms.ModelForm):
    car = ModelChoiceField(empty_label='Choice Car', queryset=Car.objects.all(),
                           widget=forms.Select(attrs={'class': 'form-control'}))
    wash_type = ModelChoiceField(empty_label='Choice Wash Type',
                                 widget=forms.Select(attrs={'class': 'form-control'}), queryset=WashType.objects.all())
    employee = ModelChoiceField(empty_label='Choice Washer', widget=forms.Select(attrs={'class': 'form-control'}),
                                queryset=User.objects.filter(status=Status.washer.value).all())
    note = CharField(widget=Textarea(attrs={'class': 'input100'}), validators=[MaxLengthValidator(150)], required=False)
    coupon = CharField(validators=[validate_coupon],
                       required=False, empty_value=None)  # ვამოწმებთ კუპინი არსებობს თუ არა ან ვადა ხომ არ აქვს გასული
    start_date = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input100'}))

    class Meta:
        model = Order
        fields = ('car', 'employee', 'wash_type',  'note', 'start_date', 'coupon')
