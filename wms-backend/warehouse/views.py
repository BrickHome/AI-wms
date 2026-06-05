from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Sum, Count, F
from datetime import datetime
from .models import (
    Warehouse, Location, Product, Inventory,
    Supplier, Customer, Order, OrderItem, InventoryAdjustment
)
from .serializers import (
    WarehouseSerializer, LocationSerializer, ProductSerializer,
    InventorySerializer, SupplierSerializer, CustomerSerializer,
    OrderSerializer, OrderCreateSerializer, InventoryAdjustmentSerializer
)

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total_inventory = Inventory.objects.aggregate(total=Sum('quantity'))['total'] or 0
        total_products = Product.objects.count()
        low_stock_count = Product.objects.filter(
            id__in=Inventory.objects.values('product').annotate(
                total=Sum('quantity')
            ).filter(total__lt=models.F('product__min_stock')).values('product')
        ).count()
        return Response({
            'total_inventory': total_inventory,
            'total_products': total_products,
            'low_stock_count': low_stock_count
        })

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        order = self.get_object()
        if order.status != 'PENDING':
            return Response({'error': '订单状态不允许处理'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'PROCESSING'
        order.save()
        
        for item in order.items.all():
            if order.order_type == 'IN':
                inventory, created = Inventory.objects.get_or_create(
                    product=item.product,
                    location=item.location,
                    batch_no=item.batch_no or '',
                    defaults={'quantity': item.quantity}
                )
                if not created:
                    inventory.quantity += item.quantity
                    inventory.save()
                item.actual_quantity = item.quantity
            else:
                inventories = Inventory.objects.filter(
                    product=item.product,
                    quantity__gt=0
                ).order_by('expiry_date', 'created_at')
                remaining = item.quantity
                for inv in inventories:
                    if remaining <= 0:
                        break
                    take = min(inv.quantity, remaining)
                    inv.quantity -= take
                    inv.save()
                    remaining -= take
                    item.location = inv.location
                item.actual_quantity = item.quantity - remaining
            item.save()
        
        order.status = 'COMPLETED'
        order.save()
        return Response({'status': 'success'})

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        today = datetime.today().date()
        month_start = today.replace(day=1)
        
        today_orders = Order.objects.filter(created_at__date=today).count()
        month_orders = Order.objects.filter(created_at__date__gte=month_start).count()
        in_orders = Order.objects.filter(order_type='IN').count()
        out_orders = Order.objects.filter(order_type='OUT').count()
        
        return Response({
            'today_orders': today_orders,
            'month_orders': month_orders,
            'in_orders': in_orders,
            'out_orders': out_orders
        })

class InventoryAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = InventoryAdjustment.objects.all()
    serializer_class = InventoryAdjustmentSerializer

    def perform_create(self, serializer):
        adjustment = serializer.save()
        inventory, created = Inventory.objects.get_or_create(
            product=adjustment.product,
            location=adjustment.location,
            defaults={'quantity': 0}
        )
        if adjustment.adjustment_type == 'INCREASE':
            inventory.quantity += adjustment.quantity
        elif adjustment.adjustment_type == 'DECREASE':
            inventory.quantity = max(0, inventory.quantity - adjustment.quantity)
        inventory.save()

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        total_warehouses = Warehouse.objects.count()
        total_locations = Location.objects.count()
        total_products = Product.objects.count()
        total_inventory = Inventory.objects.aggregate(total=Sum('quantity'))['total'] or 0
        total_suppliers = Supplier.objects.count()
        total_customers = Customer.objects.count()
        pending_orders = Order.objects.filter(status='PENDING').count()
        
        today = datetime.today().date()
        today_in_orders = Order.objects.filter(order_type='IN', created_at__date=today).count()
        today_out_orders = Order.objects.filter(order_type='OUT', created_at__date=today).count()

        return Response({
            'total_warehouses': total_warehouses,
            'total_locations': total_locations,
            'total_products': total_products,
            'total_inventory': total_inventory,
            'total_suppliers': total_suppliers,
            'total_customers': total_customers,
            'pending_orders': pending_orders,
            'today_in_orders': today_in_orders,
            'today_out_orders': today_out_orders
        })