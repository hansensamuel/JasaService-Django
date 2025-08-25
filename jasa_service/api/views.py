from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.serializers import (
    RegisterUserSerializer, LoginSerializer, ServiceDeviceSerializer,
    CustomerSerializer, TechnicianSerializer, DeviceSerializer,
    OrderSerializer, ServiceTypeSerializer, SparePartSerializer,
    InventorySerializer, PaymentSerializer
)
from jasa_service_app.models import (
    User, ServiceDevice, Customer, Technician, Device,
    Order, ServiceType, SparePart, Inventory, Payment
)


class RegisterUserAPIView(APIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Selamat anda telah terdaftar...',
                'data': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'status': 200,
            'message': 'Login berhasil.',
            'data': {
                'token': token.key,
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_active': user.is_active,
                'is_admin_service': user.is_admin_service,
                'is_technician': user.is_technician,
            }
        })


class ServiceDeviceListApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        devices = ServiceDevice.objects.all()
        serializer = ServiceDeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ServiceDeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Data perangkat berhasil ditambahkan.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDeviceDetailApiView(APIView):
    def get_object(self, id):
        try:
            return ServiceDevice.objects.get(id=id)
        except ServiceDevice.DoesNotExist:
            return None

    def get(self, request, id):
        device = self.get_object(id)
        if not device:
            return Response({'status': 404, 'message': 'Data tidak ditemukan.'}, status=404)
        serializer = ServiceDeviceSerializer(device)
        return Response({'status': 200, 'message': 'Data ditemukan.', 'data': serializer.data})

    def put(self, request, id):
        device = self.get_object(id)
        if not device:
            return Response({'status': 404, 'message': 'Data tidak ditemukan.'}, status=404)
        serializer = ServiceDeviceSerializer(device, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, 'message': 'Data berhasil diperbarui.', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        device = self.get_object(id)
        if not device:
            return Response({'status': 404, 'message': 'Data tidak ditemukan.'}, status=404)
        device.delete()
        return Response({'status': 200, 'message': 'Data berhasil dihapus.'})



class BaseModelListCreateView(APIView):
    model_class = None
    serializer_class = None
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = self.model_class.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseModelDetailView(APIView):
    model_class = None
    serializer_class = None
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return self.model_class.objects.get(id=id)
        except self.model_class.DoesNotExist:
            return None

    def get(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=404)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def put(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=404)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        obj = self.get_object(id)
        if not obj:
            return Response({'message': 'Data tidak ditemukan.'}, status=404)
        obj.delete()
        return Response({'message': 'Data berhasil dihapus.'}, status=200)


class CustomerListCreateView(BaseModelListCreateView):
    model_class = Customer
    serializer_class = CustomerSerializer

class CustomerDetailView(BaseModelDetailView):
    model_class = Customer
    serializer_class = CustomerSerializer

class TechnicianListCreateView(BaseModelListCreateView):
    model_class = Technician
    serializer_class = TechnicianSerializer

class TechnicianDetailView(BaseModelDetailView):
    model_class = Technician
    serializer_class = TechnicianSerializer

class DeviceListCreateView(BaseModelListCreateView):
    model_class = Device
    serializer_class = DeviceSerializer

class DeviceDetailView(BaseModelDetailView):
    model_class = Device
    serializer_class = DeviceSerializer

class OrderListCreateView(BaseModelListCreateView):
    model_class = Order
    serializer_class = OrderSerializer

class OrderDetailView(BaseModelDetailView):
    model_class = Order
    serializer_class = OrderSerializer

class ServiceTypeListCreateView(BaseModelListCreateView):
    model_class = ServiceType
    serializer_class = ServiceTypeSerializer

class ServiceTypeDetailView(BaseModelDetailView):
    model_class = ServiceType
    serializer_class = ServiceTypeSerializer

class SparePartListCreateView(BaseModelListCreateView):
    model_class = SparePart
    serializer_class = SparePartSerializer

class SparePartDetailView(BaseModelDetailView):
    model_class = SparePart
    serializer_class = SparePartSerializer

class InventoryListCreateView(BaseModelListCreateView):
    model_class = Inventory
    serializer_class = InventorySerializer

class InventoryDetailView(BaseModelDetailView):
    model_class = Inventory
    serializer_class = InventorySerializer

class PaymentListCreateView(BaseModelListCreateView):
    model_class = Payment
    serializer_class = PaymentSerializer

class PaymentDetailView(BaseModelDetailView):
    model_class = Payment
    serializer_class = PaymentSerializer