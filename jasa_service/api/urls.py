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
    path('api/register', RegisterUserAPIView.as_view()),
    path('api/login', LoginView.as_view()),

    # Service Device (CRUD)
    path('api/service_devices', ServiceDeviceListApiView.as_view()),
    path('api/service_devices/<int:id>', ServiceDeviceDetailApiView.as_view()),

    # Customer (CRUD)
    path('api/customers', CustomerListCreateView.as_view()),
    path('api/customers/<int:id>', CustomerDetailView.as_view()),

    # Technician (CRUD)
    path('api/technicians', TechnicianListCreateView.as_view()),
    path('api/technicians/<int:id>', TechnicianDetailView.as_view()),

    # Device (CRUD)
    path('api/devices', DeviceListCreateView.as_view()),
    path('api/devices/<int:id>', DeviceDetailView.as_view()),

    # Order (CRUD)
    path('api/orders', OrderListCreateView.as_view()),
    path('api/orders/<int:id>', OrderDetailView.as_view()),

    # Service Type (CRUD)
    path('api/service_types', ServiceTypeListCreateView.as_view()),
    path('api/service_types/<int:id>', ServiceTypeDetailView.as_view()),

    # Spare Part (CRUD)
    path('api/spare_parts', SparePartListCreateView.as_view()),
    path('api/spare_parts/<int:id>', SparePartDetailView.as_view()),

    # Inventory (CRUD)
    path('api/inventories', InventoryListCreateView.as_view()),
    path('api/inventories/<int:id>', InventoryDetailView.as_view()),

    # Payment (CRUD)
    path('api/payments', PaymentListCreateView.as_view()),
    path('api/payments/<int:id>', PaymentDetailView.as_view()),
]  
