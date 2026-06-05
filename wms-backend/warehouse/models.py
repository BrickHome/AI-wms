from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=100, verbose_name='仓库名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='仓库编码')
    address = models.TextField(blank=True, verbose_name='仓库地址')
    description = models.TextField(blank=True, verbose_name='仓库描述')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '仓库'
        verbose_name_plural = '仓库'

class Location(models.Model):
    LOCATION_TYPES = [
        ('SHELF', '货架'),
        ('BIN', '货位'),
        ('AREA', '区域'),
        ('FLOOR', '地面'),
    ]
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='所属仓库')
    code = models.CharField(max_length=50, unique=True, verbose_name='库位编码')
    name = models.CharField(max_length=100, verbose_name='库位名称')
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, verbose_name='库位类型')
    capacity = models.IntegerField(default=0, verbose_name='容量')
    current_qty = models.IntegerField(default=0, verbose_name='当前数量')
    is_available = models.BooleanField(default=True, verbose_name='是否可用')
    description = models.TextField(blank=True, verbose_name='库位描述')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.warehouse.code}-{self.code}"

    class Meta:
        verbose_name = '库位'
        verbose_name_plural = '库位'

class Product(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name='商品编码')
    name = models.CharField(max_length=200, verbose_name='商品名称')
    sku = models.CharField(max_length=100, blank=True, verbose_name='SKU')
    barcode = models.CharField(max_length=100, blank=True, verbose_name='条码')
    category = models.CharField(max_length=100, blank=True, verbose_name='商品分类')
    unit = models.CharField(max_length=20, default='件', verbose_name='单位')
    weight = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name='重量(kg)')
    volume = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name='体积(m³)')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='单价')
    min_stock = models.IntegerField(default=0, verbose_name='最低库存')
    max_stock = models.IntegerField(default=0, verbose_name='最高库存')
    description = models.TextField(blank=True, verbose_name='商品描述')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库位')
    quantity = models.IntegerField(default=0, verbose_name='库存数量')
    batch_no = models.CharField(max_length=100, blank=True, verbose_name='批次号')
    expiry_date = models.DateField(null=True, blank=True, verbose_name='有效期')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.location.code} - {self.quantity}"

    class Meta:
        verbose_name = '库存'
        verbose_name_plural = '库存'
        unique_together = ('product', 'location', 'batch_no')

class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name='供应商名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='供应商编码')
    contact = models.CharField(max_length=100, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=50, blank=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    address = models.TextField(blank=True, verbose_name='地址')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = '供应商'

class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name='客户名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='客户编码')
    contact = models.CharField(max_length=100, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=50, blank=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    address = models.TextField(blank=True, verbose_name='地址')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'

class Order(models.Model):
    ORDER_TYPES = [
        ('IN', '入库单'),
        ('OUT', '出库单'),
    ]
    
    ORDER_STATUS = [
        ('PENDING', '待处理'),
        ('PROCESSING', '处理中'),
        ('COMPLETED', '已完成'),
        ('CANCELLED', '已取消'),
    ]
    
    order_no = models.CharField(max_length=100, unique=True, verbose_name='订单编号')
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, verbose_name='订单类型')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING', verbose_name='订单状态')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='仓库')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='供应商')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='客户')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='总金额')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_no

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(verbose_name='数量')
    actual_quantity = models.IntegerField(default=0, verbose_name='实际数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='单价')
    batch_no = models.CharField(max_length=100, blank=True, verbose_name='批次号')
    expiry_date = models.DateField(null=True, blank=True, verbose_name='有效期')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='库位')

    def __str__(self):
        return f"{self.order.order_no} - {self.product.name}"

    class Meta:
        verbose_name = '订单明细'
        verbose_name_plural = '订单明细'

class InventoryAdjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('INCREASE', '盘盈'),
        ('DECREASE', '盘亏'),
        ('TRANSFER', '调拨'),
    ]
    
    adjustment_no = models.CharField(max_length=100, unique=True, verbose_name='调整单号')
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPES, verbose_name='调整类型')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='库位')
    quantity = models.IntegerField(verbose_name='调整数量')
    reason = models.TextField(blank=True, verbose_name='调整原因')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adjustment_no

    class Meta:
        verbose_name = '库存调整'
        verbose_name_plural = '库存调整'