from django.contrib import admin

from .models import Car, Company, Coupon, Orders, Location, Booth, CarType, Employee


class EmployeeInline(admin.TabularInline):
    model = Employee


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'address', 'city', 'zip_code')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'get_employees_number')
    inlines = [EmployeeInline, ]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'company', 'name', 'phone_number', 'salary', 'hire_date']
    filter = ('company', 'salary', 'hire_date')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'format_percent', 'expiration_date']


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Booth)
class BoothAdmin(admin.ModelAdmin):
    list_display = ['number', 'employee', 'available']
    filter = ('available',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['licence_plate', 'car_type']


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['car', 'booth', 'time', 'get_car_type']

    readonly_fields = ('get_car_type',)

    fieldsets = [
        ('Car Details', {'fields': ['car', readonly_fields]}),
        ('Order Details', {'fields': ['booth', 'time', 'job_description', 'coupon']}),
    ]

    def get_car_type(self, obj):
        return obj.car.type

    get_car_type.short_description = 'Car Type'
