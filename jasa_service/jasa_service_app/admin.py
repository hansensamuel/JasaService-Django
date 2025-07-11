from django.contrib import admin
from jasa_service_app.models import (
    User, ServiceDevice, Customer, Technician, Device,
    Order, ServiceType, SparePart, Inventory, Payment
)

# Register your models here
admin.site.register(User)
admin.site.register(ServiceDevice)
admin.site.register(Customer)
admin.site.register(Technician)
admin.site.register(Device)
admin.site.register(Order)
admin.site.register(ServiceType)
admin.site.register(SparePart)
admin.site.register(Inventory)
admin.site.register(Payment)

# Admin branding
admin.site.site_header = 'Sistem Informasi Jasa Service PC dan Laptop'
admin.site.site_title = 'Admin Service'
admin.site.index_title = 'Manajemen Data Service Perangkat'
