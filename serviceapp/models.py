from django.utils.translation import ugettext_lazy as _
from django.db import models


class CarType(models.Model):
    name = models.CharField(max_length=45, verbose_name=_('Car Type'), unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'car_type'


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    expiration_date = models.DateTimeField(verbose_name=_('Coupon Expiration Date'))
    discount = models.IntegerField(verbose_name=_('Discount'), help_text='%')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')


class WashType(models.Model):
    name = models.CharField(max_length=45, verbose_name=_('Car Type'), unique=True)
    percentage = models.IntegerField(verbose_name=_("Percentage of base price"), default=100)

    def __str__(self):
        return self.name


class Booth(models.Model):
    number = models.SmallIntegerField(verbose_name=_('Booth Number'))

    def __str__(self):
        return f'Box Number {self.number}'


class Car(models.Model):
    licence_plate = models.CharField(max_length=20)
    car_type = models.ForeignKey(
        to='serviceapp.CarType',
        on_delete=models.SET_NULL,
        null=True,
        related_name='cars')

    def __str__(self):
        return self.licence_plate

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class Order(models.Model):
    car = models.ForeignKey(
        to='serviceapp.Car',
        on_delete=models.CASCADE,
        related_name='order')
    booth = models.ForeignKey(to='serviceapp.Booth', on_delete=models.PROTECT, related_name='order')
    start_date = models.DateTimeField(verbose_name=_('Scheduled time'))
    end_date = models.DateTimeField(verbose_name=_('End time'), null=True, blank=True)

    wash_type = models.ForeignKey(
        to='serviceapp.WashType',
        related_name='orders',
        on_delete=models.PROTECT,
    )

    note = models.TextField(null=True, blank=True, verbose_name=_('Note'))

    coupon = models.ForeignKey(
        to='serviceapp.Coupon', related_name='orders',
        on_delete=models.PROTECT,
        null=True, blank=True,
    )
    employee = models.ForeignKey(
        to='user.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order')

    price = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.car} using {self.wash_type}'

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.car.car_type.price * self.wash_type.percentage / 100
        super(Order, self).save(*args, **kwargs)
