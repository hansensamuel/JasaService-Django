from django.contrib import admin
from jasa_service_app.models import (
    User, ServiceDevice, Customer, Technician, Device,
    Order, ServiceType, SparePart, Inventory, Payment
)
from django import forms

admin.site.register(User)

@admin.register(ServiceDevice)
class ServiceDeviceAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'customer',      
        'device_type',   
        'brand',         
        'service_status',
        'status',
        'created_on',
    )
    list_filter = ('service_status', 'status')
    search_fields = ('code', 'customer__name', 'device__brand')
    ordering = ('-created_on',)
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'device', 'technician',
        'service_type', 'status', 'priority', 'created_on'
    )
    list_filter = ('status', 'priority', 'created_on')
    search_fields = ('customer__name', 'device__model', 'service_type__name')



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer_type', 'contact', 'email')
    search_fields = ('name', 'contact', 'email')



@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'brand', 'model', 'serial_number')
    search_fields = ('brand', 'model', 'serial_number')



@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'specialization')
    search_fields = ('user__username', 'specialization')



@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty', 'price')
    list_filter = ('category', 'difficulty')
    search_fields = ('name',)



@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)



@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('spare_part', 'stock', 'low_stock_threshold', 'is_low_stock')



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hanya tampilkan order yang belum pernah dipilih pada payment
        used_orders = Payment.objects.values_list('order_id', flat=True)
        self.fields['order'].queryset = Order.objects.exclude(id__in=used_orders)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    list_display = ('id', 'order', 'amount', 'method', 'paid_on')
    list_filter = ('method', 'paid_on')
    search_fields = ('order__id',)
    

admin.site.site_header = 'Sistem Informasi Jasa Service PC dan Laptop'
admin.site.site_title = 'Admin Service'
admin.site.index_title = 'Manajemen Data Service Perangkat'
