from rest_framework import serializers
from jasa_service_app.models import (
    User, ServiceDevice, Customer, Technician, Device, 
    Order, ServiceType, SparePart, Inventory, Payment
)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


# 🔐 Serializer untuk Registrasi User
class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
                  'is_active', 'is_admin_service', 'is_technician', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Kata sandi dan ulangi kata sandi tidak cocok.'
            })
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
            is_admin_service=validated_data['is_admin_service'],
            is_technician=validated_data['is_technician'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


# Serializer untuk Login User
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise ValidationError({'message': 'Akun pengguna tidak aktif.'})
            else:
                raise ValidationError({'message': 'Nama pengguna atau kata sandi salah.'})
        else:
            raise ValidationError({'message': 'Mohon isi nama pengguna dan kata sandi.'})
        return data


# Serializer untuk Data Service Perangkat
class ServiceDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDevice
        fields = (
            'id', 'code', 'customer_name', 'device_type',
            'brand', 'damage_description', 'service_status',
            'status', 'created_on', 'last_modified'
        )

# 👤 Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


# 🧑‍🔧 Teknisi
class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = '__all__'


# 📟 Perangkat
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


# 📋 Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# 🔧 Jenis Layanan
class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'


# 🛠 Spare Part
class SparePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SparePart
        fields = '__all__'


# 📦 Inventory
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


# 💰 Pembayaran
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'