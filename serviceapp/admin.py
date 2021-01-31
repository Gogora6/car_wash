from .models import Car, Coupon, Order, Booth, CarType, WashType
from django.contrib import admin


@admin.register(WashType)
class WashTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage']


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


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
