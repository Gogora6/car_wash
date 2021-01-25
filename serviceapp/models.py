from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import date


class Location(models.Model):
    address = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=7)

    def __str__(self):
        return f'{self.address}, {self.city}'


class Coupon(models.Model):
    code = models.CharField(max_length=30)
    expiration_date = models.DateTimeField(verbose_name=_('Coupon Expiration Date'))
    discount = models.IntegerField(verbose_name=_('Discount percent'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    def format_percent(self):
        return f'{self.discount}$'

    format_percent.short_description = _('Discount')


class CarType(models.Model):
    name = models.CharField(max_length=45, verbose_name=_('Car Type'), unique=True)  # სედანი, ჯიპი, ჰეჩბექი
    price = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'car_type'


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Company Name'))
    location = models.OneToOneField(to='serviceapp.Location', on_delete=models.PROTECT, related_name='company')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def get_employees_number(self):  # ვიყენებ ადმინ პანელში company-ს სექციაში

        return Employee.objects.filter(company=self.pk).count()

    get_employees_number.short_description = 'Employee Number'


class Employee(models.Model):
    company = models.ForeignKey(to='serviceapp.Company', on_delete=models.CASCADE, related_name='employee')
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    birthdate = models.DateField(verbose_name=_('Birth Date'))
    salary = models.IntegerField(verbose_name=_('salary ($)'))
    phone_number = models.CharField(max_length=50, verbose_name=_('Phone Number'))
    hire_date = models.DateField()

    def get_age(self):
        today = date.today()
        return today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    def __str__(self):
        return f'{self.name} {self.lastname}  {self.get_age()} წლის '

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')


class Booth(models.Model):
    number = models.SmallIntegerField(verbose_name=_('Booth Number'))
    employee = models.OneToOneField(to='serviceapp.Employee', on_delete=models.SET_NULL, null=True,
                                    related_name='booth')
    available = models.BooleanField(default=True)

    # company_id იმიტომ არ ვუწერ რომ Employee ში მაქვს Company-id ია.

    def __str__(self):
        return f'Box Number {self.number}'


class Car(models.Model):
    licence_plate = models.CharField(max_length=20)
    car_type = models.ForeignKey(to='serviceapp.CarType', on_delete=models.SET_NULL, null=True, related_name='cars')

    def __str__(self):
        return self.licence_plate

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class Orders(models.Model):
    car = models.ForeignKey(to='serviceapp.Car', on_delete=models.CASCADE, related_name='orders')
    booth = models.ForeignKey(to='serviceapp.Booth', on_delete=models.PROTECT, related_name='orders')
    time = models.DateTimeField(verbose_name=_('Scheduled time'))
    job_description = models.TextField(null=True, blank=True)
    coupon = models.ManyToManyField(to='serviceapp.Coupon', related_name='orders', null=True, blank=True)

    # through არ ვუწერ რადგან არ მინდა CouponToOrder-ში სხვა ველის დამატება
    def __str__(self):
        return self.car.licence_plate

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

# class CouponToOrders(models.Model):
#     order = models.ForeignKey(to='serviceapp.Orders', on_delete=models.CASCADE, related_name='coupon_to_orders')
#     coupon = models.ForeignKey(to='serviceapp.Coupon', on_delete=models.CASCADE, related_name='coupon_to_orders')
