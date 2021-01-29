from .models import Car, Company, Coupon, Orders, Location, Booth, Employee, CarType
from django.contrib import admin
from datetime import date


class EmployeeInline(admin.TabularInline):
    model = Employee


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'address', 'city', 'zip_code')


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'get_employees_number')
    inlines = [EmployeeInline, ]

    def get_employees_number(self, obj):
        return Employee.objects.filter(company=obj.pk).count()

    get_employees_number.short_description = 'Employee Number'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'company', 'name', 'phone_number', 'salary', 'get_age', 'hire_date']

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


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['car', 'booth', 'time']

    readonly_fields = ('price',)
    fieldsets = [
        ('Car Details', {'fields': ['car']}),
        ('Order Details', {'fields': ['booth', 'employee', readonly_fields, 'time', 'job_description', 'coupons']}),
    ]
