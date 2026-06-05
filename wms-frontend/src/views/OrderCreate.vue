<template>
  <div class="order-create">
    <el-card>
      <el-form :model="form" label-width="100px">
        <el-form-item label="订单类型" prop="order_type">
          <el-select v-model="form.order_type">
            <el-option label="入库单" value="IN" />
            <el-option label="出库单" value="OUT" />
          </el-select>
        </el-form-item>
        <el-form-item label="订单编号" prop="order_no">
          <el-input v-model="form.order_no" />
        </el-form-item>
        <el-form-item label="仓库" prop="warehouse">
          <el-select v-model="form.warehouse">
            <el-option v-for="warehouse in warehouses" :key="warehouse.id" :label="warehouse.name" :value="warehouse.id" />
          </el-select>
        </el-form-item>
        <el-form-item :label="form.order_type === 'IN' ? '供应商' : '客户'" :prop="form.order_type === 'IN' ? 'supplier' : 'customer'">
          <el-select v-model="form.order_type === 'IN' ? form.supplier : form.customer">
            <el-option v-for="item in (form.order_type === 'IN' ? suppliers : customers)" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="订单明细">
          <el-button type="primary" size="small" @click="addItem">添加商品</el-button>
          <el-table :data="form.items" border style="margin-top: 10px;">
            <el-table-column prop="product" label="商品">
              <template #default="scope">
                <el-select v-model="scope.row.product">
                  <el-option v-for="product in products" :key="product.id" :label="product.name" :value="product.id" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量">
              <template #default="scope">
                <el-input type="number" v-model="scope.row.quantity" />
              </template>
            </el-table-column>
            <el-table-column prop="unit_price" label="单价">
              <template #default="scope">
                <el-input type="number" step="0.01" v-model="scope.row.unit_price" />
              </template>
            </el-table-column>
            <el-table-column prop="batch_no" label="批次号">
              <template #default="scope">
                <el-input v-model="scope.row.batch_no" />
              </template>
            </el-table-column>
            <el-table-column prop="location" label="库位" v-if="form.order_type === 'IN'">
              <template #default="scope">
                <el-select v-model="scope.row.location">
                  <el-option v-for="location in locations" :key="location.id" :label="location.code" :value="location.id" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button size="small" type="danger" @click="removeItem(scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="form.remark" />
        </el-form-item>
      </el-form>
      <div class="button-group">
        <router-link to="/orders">
          <el-button>取消</el-button>
        </router-link>
        <el-button type="primary" @click="saveOrder">保存订单</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const form = ref({
  order_no: '',
  order_type: 'IN',
  warehouse: null,
  supplier: null,
  customer: null,
  remark: '',
  items: []
})

const warehouses = ref([])
const suppliers = ref([])
const customers = ref([])
const products = ref([])
const locations = ref([])

const generateOrderNo = () => {
  const now = new Date()
  const type = form.value.order_type === 'IN' ? 'IN' : 'OUT'
  return `${type}${now.getFullYear()}${String(now.getMonth()+1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}${String(Date.now()).slice(-6)}`
}

const addItem = () => {
  form.value.items.push({
    product: null,
    quantity: 0,
    unit_price: 0,
    batch_no: '',
    location: null
  })
}

const removeItem = (index) => {
  form.value.items.splice(index, 1)
}

const fetchWarehouses = async () => {
  try {
    const response = await axios.get('/api/warehouses/')
    warehouses.value = response.data.results
  } catch (error) {
    console.error('获取仓库列表失败:', error)
  }
}

const fetchSuppliers = async () => {
  try {
    const response = await axios.get('/api/suppliers/')
    suppliers.value = response.data.results
  } catch (error) {
    console.error('获取供应商列表失败:', error)
  }
}

const fetchCustomers = async () => {
  try {
    const response = await axios.get('/api/customers/')
    customers.value = response.data.results
  } catch (error) {
    console.error('获取客户列表失败:', error)
  }
}

const fetchProducts = async () => {
  try {
    const response = await axios.get('/api/products/')
    products.value = response.data.results
  } catch (error) {
    console.error('获取商品列表失败:', error)
  }
}

const fetchLocations = async () => {
  try {
    const response = await axios.get('/api/locations/')
    locations.value = response.data.results
  } catch (error) {
    console.error('获取库位列表失败:', error)
  }
}

const saveOrder = async () => {
  if (!form.value.order_no) {
    form.value.order_no = generateOrderNo()
  }
  
  try {
    const data = { ...form.value }
    if (form.value.order_type === 'IN') {
      delete data.customer
    } else {
      delete data.supplier
    }
    
    await axios.post('/api/orders/', data)
    ElMessage.success('订单创建成功')
    window.location.href = '/orders'
  } catch (error) {
    ElMessage.error('订单创建失败')
    console.error('订单创建失败:', error)
  }
}

onMounted(() => {
  fetchWarehouses()
  fetchSuppliers()
  fetchCustomers()
  fetchProducts()
  fetchLocations()
  form.value.order_no = generateOrderNo()
})
</script>

<style scoped>
.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>