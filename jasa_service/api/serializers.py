from rest_framework import serializers
from jasa_service_app.models import (
    User, ServiceDevice, Customer, Technician, Device, 
    Order, ServiceType, SparePart, Inventory, Payment
)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


# Serializer untuk Registrasi User
class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(write_only=True,
        required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'is_active', 'is_admin_service', 'is_technician',
            'first_name', 'last_name'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Kata sandi dan Ulang kata sandi tidak sama.'
            })
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
            is_admin_service=validated_data.get('is_admin_service', False),
            is_technician=validated_data.get('is_technician', False),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


# Serializer untuk Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise ValidationError({'message': 'Status pengguna tidak aktif.'})
            else:
                raise ValidationError({'message': 'Username atau password salah.'})
        else:
            raise ValidationError({'message': 'Mohon isi nama pengguna dan kata sandi.'})

        return data

# Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# Perangkat
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


# Serializer untuk Data Service Perangkat
class ServiceDeviceSerializer(serializers.ModelSerializer):
    # Menampilkan informasi customer & device dengan readable format
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )

    device = DeviceSerializer(read_only=True)
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(), source='device', write_only=True
    )

    class Meta:
        model = ServiceDevice
        fields = (
            'id', 'code',
            'customer', 'customer_id',  # relasi
            'device', 'device_id',      # relasi
            'brand', 'damage_description',
            'service_status', 'status',
            'created_on', 'last_modified'
        )

# Teknisi
class TechnicianSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Technician
        fields = ['id', 'user', 'level', 'specialization']

    def get_user(self, obj):
        return obj.user.get_full_name() if obj.user else ''
    
# Jenis Layanan
class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

# Order
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )
    device = DeviceSerializer(read_only=True)
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(), source='device', write_only=True
    )
    technician = TechnicianSerializer(read_only=True)
    technician_id = serializers.PrimaryKeyRelatedField(
        queryset=Technician.objects.all(), source='technician', write_only=True, required=False, allow_null=True
    )
    service_type = ServiceTypeSerializer(read_only=True)
    service_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceType.objects.all(), source='service_type', write_only=True
    )
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_id', 'device', 'device_id',
            'technician', 'technician_id', 'service_type', 'service_type_id',
            'status', 'priority', 'created_on', 'updated_on'
        ]


# Spare Part
class SparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePart
        fields = '__all__'


# Inventory
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


# Pembayaran
class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )
    class Meta: 
        model = Payment
        fields = ['id', 'order', 'order_id', 'amount', 'method', 'paid_on']