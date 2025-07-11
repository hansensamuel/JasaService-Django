from django.urls import path
from api import views
from .views import (
    RegisterUserAPIView, LoginView,
    ServiceDeviceListApiView, ServiceDeviceDetailApiView,
    CustomerListCreateView, CustomerDetailView,
    TechnicianListCreateView, TechnicianDetailView,
    DeviceListCreateView, DeviceDetailView,
    OrderListCreateView, OrderDetailView,
    ServiceTypeListCreateView, ServiceTypeDetailView,
    SparePartListCreateView, SparePartDetailView,
    InventoryListCreateView, InventoryDetailView,
    PaymentListCreateView, PaymentDetailView
)

app_name = 'api'

urlpatterns = [
    # Auth
    path('api/register', RegisterUserAPIView.as_view(), name='register'),
    path('api/login', LoginView.as_view(), name='login'),

    # Service Device (CRUD)
    path('api/service-devices', ServiceDeviceListApiView.as_view(), name='service-device-list'),
    path('api/service-devices/<int:id>', ServiceDeviceDetailApiView.as_view(), name='service-device-detail'),

    # Customer (CRUD)
    path('api/customers', CustomerListCreateView.as_view(), name='customer-list'),
    path('api/customers/<int:id>', CustomerDetailView.as_view(), name='customer-detail'),

    # Technician (CRUD)
    path('api/technicians', TechnicianListCreateView.as_view(), name='technician-list'),
    path('api/technicians/<int:id>', TechnicianDetailView.as_view(), name='technician-detail'),

    # Device (CRUD)
    path('api/devices', DeviceListCreateView.as_view(), name='device-list'),
    path('api/devices/<int:id>', DeviceDetailView.as_view(), name='device-detail'),

    # Order (CRUD)
    path('api/orders', OrderListCreateView.as_view(), name='order-list'),
    path('api/orders/<int:id>', OrderDetailView.as_view(), name='order-detail'),

    # Service Type (CRUD)
    path('api/service-types', ServiceTypeListCreateView.as_view(), name='service-type-list'),
    path('api/service-types/<int:id>', ServiceTypeDetailView.as_view(), name='service-type-detail'),

    # Spare Part (CRUD)
    path('api/spare-parts', SparePartListCreateView.as_view(), name='spare-part-list'),
    path('api/spare-parts/<int:id>', SparePartDetailView.as_view(), name='spare-part-detail'),

    # Inventory (CRUD)
    path('api/inventories', InventoryListCreateView.as_view(), name='inventory-list'),
    path('api/inventories/<int:id>', InventoryDetailView.as_view(), name='inventory-detail'),

    # Payment (CRUD)
    path('api/payments', PaymentListCreateView.as_view(), name='payment-list'),
    path('api/payments/<int:id>', PaymentDetailView.as_view(), name='payment-detail'),
]  
