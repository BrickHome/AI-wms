"""
URL configuration for wms_project project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from warehouse.views import (
    WarehouseViewSet, LocationViewSet, ProductViewSet,
    InventoryViewSet, SupplierViewSet, CustomerViewSet,
    OrderViewSet, InventoryAdjustmentViewSet, DashboardViewSet
)

router = routers.DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'products', ProductViewSet)
router.register(r'inventories', InventoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'adjustments', InventoryAdjustmentViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include('rest_framework.urls')),
]
