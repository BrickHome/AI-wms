<template>
  <div class="order-list">
    <el-card>
      <div class="card-header">
        <el-select v-model="orderType" class="type-select">
          <el-option label="全部订单" value="ALL" />
          <el-option label="入库单" value="IN" />
          <el-option label="出库单" value="OUT" />
        </el-select>
        <el-select v-model="status" class="status-select">
          <el-option label="全部状态" value="ALL" />
          <el-option label="待处理" value="PENDING" />
          <el-option label="处理中" value="PROCESSING" />
          <el-option label="已完成" value="COMPLETED" />
          <el-option label="已取消" value="CANCELLED" />
        </el-select>
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索订单编号" 
          class="search-input"
          @keyup.enter="fetchOrders"
        >
          <template #append>
            <el-button @click="fetchOrders">
              <Search />
            </el-button>
          </template>
        </el-input>
        <router-link to="/orders/create">
          <el-button type="primary">
            <Plus /> 创建订单
          </el-button>
        </router-link>
      </div>
      <el-table :data="orders" border>
        <el-table-column prop="order_no" label="订单编号" />
        <el-table-column prop="order_type" label="订单类型">
          <template #default="scope">
            <el-tag :type="scope.row.order_type === 'IN' ? 'success' : 'primary'">
              {{ scope.row.order_type === 'IN' ? '入库单' : '出库单' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusName(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="warehouse_name" label="仓库" />
        <el-table-column prop="supplier_name" label="供应商" />
        <el-table-column prop="customer_name" label="客户" />
        <el-table-column prop="total_amount" label="总金额" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="viewOrder(scope.row)">查看</el-button>
            <el-button v-if="scope.row.status === 'PENDING'" size="small" type="success" @click="processOrder(scope.row.id)">处理</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination 
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50]"
        :page-size="pageSize"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
      />
    </el-card>

    <el-dialog :title="orderDetail.order_no" :visible.sync="detailModalVisible" width="800px">
      <el-form :model="orderDetail" label-width="100px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="订单类型">
              <el-tag :type="orderDetail.order_type === 'IN' ? 'success' : 'primary'">
                {{ orderDetail.order_type === 'IN' ? '入库单' : '出库单' }}
              </el-tag>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-tag :type="getStatusType(orderDetail.status)">
                {{ getStatusName(orderDetail.status) }}
              </el-tag>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="仓库">{{ orderDetail.warehouse_name }}</el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="供应商">{{ orderDetail.supplier_name || '-' }}</el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="客户">{{ orderDetail.customer_name || '-' }}</el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="总金额">{{ orderDetail.total_amount }}</el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="备注">{{ orderDetail.remark || '-' }}</el-form-item>
        <el-form-item label="订单明细">
          <el-table :data="orderDetail.items" border>
            <el-table-column prop="product_name" label="商品名称" />
            <el-table-column prop="quantity" label="数量" />
            <el-table-column prop="actual_quantity" label="实际数量" />
            <el-table-column prop="unit_price" label="单价" />
            <el-table-column prop="batch_no" label="批次号" />
            <el-table-column prop="location_code" label="库位" />
          </el-table>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailModalVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const orders = ref([])
const orderDetail = ref({})
const orderType = ref('ALL')
const status = ref('ALL')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const detailModalVisible = ref(false)

const statusNames = {
  'PENDING': '待处理',
  'PROCESSING': '处理中',
  'COMPLETED': '已完成',
  'CANCELLED': '已取消'
}

const statusTypes = {
  'PENDING': 'warning',
  'PROCESSING': 'primary',
  'COMPLETED': 'success',
  'CANCELLED': 'danger'
}

const getStatusName = (status) => {
  return statusNames[status] || status
}

const getStatusType = (status) => {
  return statusTypes[status] || 'info'
}

const fetchOrders = async () => {
  let url = `/api/orders/?page=${currentPage.value}&page_size=${pageSize.value}`
  if (orderType.value !== 'ALL') {
    url += `&order_type=${orderType.value}`
  }
  if (status.value !== 'ALL') {
    url += `&status=${status.value}`
  }
  try {
    const response = await axios.get(url)
    orders.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取订单列表失败:', error)
  }
}

const viewOrder = async (order) => {
  try {
    const response = await axios.get(`/api/orders/${order.id}/`)
    orderDetail.value = response.data
    detailModalVisible.value = true
  } catch (error) {
    console.error('获取订单详情失败:', error)
  }
}

const processOrder = async (id) => {
  try {
    await axios.post(`/api/orders/${id}/process/`)
    fetchOrders()
    ElMessage.success('订单处理成功')
  } catch (error) {
    ElMessage.error('订单处理失败')
    console.error('订单处理失败:', error)
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchOrders()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchOrders()
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.type-select, .status-select {
  width: 120px;
}

.search-input {
  width: 250px;
}
</style>