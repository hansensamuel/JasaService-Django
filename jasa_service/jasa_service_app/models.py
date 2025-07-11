from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import AbstractUser

# User dengan role teknisi atau admin
class User(AbstractUser):
    is_admin_service = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} {self.first_name} {self.last_name}'


# Model perangkat yang diservice
class ServiceDevice(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    )
    service_status_choices = (
        ('Masuk', 'Masuk'),               # Baru datang
        ('Proses', 'Proses'),             # Dalam proses perbaikan
        ('Selesai', 'Selesai'),           # Sudah diperbaiki
        ('Diambil', 'Diambil'),           # Sudah diambil oleh pelanggan
    )

    code = models.CharField(max_length=20, help_text="Kode unik perangkat")
    customer_name = models.CharField(max_length=100, help_text="Nama pelanggan")
    device_type = models.CharField(max_length=50, help_text="Jenis perangkat (PC, Laptop, dll)")
    brand = models.CharField(max_length=50, help_text="Merek perangkat")
    damage_description = models.TextField(help_text="Deskripsi kerusakan")
    service_status = models.CharField(max_length=20, choices=service_status_choices, default='Masuk')
    status = models.CharField(max_length=15, choices=status_choices, default='Aktif')

    user_create = models.ForeignKey(User, related_name='user_create_service_device', blank=True, null=True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(User, related_name='user_update_service_device', blank=True, null=True, on_delete=models.SET_NULL)

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.customer_name}"

class Customer(models.Model):
    CUSTOMER_TYPES = (
        ('Individual', 'Individual'),
        ('Business', 'Business'),
        ('Government', 'Government'),
    )
    name = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    contact = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Technician(models.Model):
    LEVEL_CHOICES = (
        ('Junior', 'Junior'),
        ('Intermediate', 'Intermediate'),
        ('Senior', 'Senior'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.level}"


class Device(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    specs = models.TextField()

    def __str__(self):
        return f"{self.brand} {self.model}"


class ServiceType(models.Model):
    CATEGORY_CHOICES = (
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Network', 'Network'),
    )
    DIFFICULTY_LEVEL = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVEL)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Normal', 'Normal'),
        ('High', 'High'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"


class SparePart(models.Model):
    name = models.CharField(max_length=100)
    compatible_models = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    spare_part = models.OneToOneField(SparePart, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    low_stock_threshold = models.PositiveIntegerField(default=5)

    def is_low_stock(self):
        return self.stock <= self.low_stock_threshold

    def __str__(self):
        return f"{self.spare_part.name} - Stock: {self.stock}"


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('Cash', 'Cash'),
        ('Transfer', 'Transfer'),
        ('E-Wallet', 'E-Wallet'),
        ('Credit Card', 'Credit Card'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.method}"
