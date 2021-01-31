from .models import Car, Coupon, Order, Booth, Employee, CarType, WashType
from django.contrib import admin
from datetime import date


class EmployeeInline(admin.TabularInline):
    model = Employee


@admin.register(WashType)
class WashTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage']


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'phone_number', 'salary', 'get_age', 'hire_date']

    def get_age(self, obj):
        today = date.today()
        return today.year - obj.birthdate.year - (
                (today.month, today.day) < (obj.birthdate.month, obj.birthdate.day))

    get_age.short_description = 'Age'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'format_percent', 'expiration_date']

    def format_percent(self, ojb):
        return f'{ojb.discount}$'

    format_percent.short_description = 'Discount'


@admin.register(Booth)
class BoothAdmin(admin.ModelAdmin):
    list_display = ['number']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['licence_plate']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'booth', 'wash_type', 'start_date']

    readonly_fields = ('price',)
    fieldsets = [
        ('Car Details', {'fields': ['car']}),
        ('Order Details',
         {'fields': ['wash_type', 'booth', 'employee', 'start_date', 'end_date', readonly_fields, 'note', 'coupon']}),
    ]
