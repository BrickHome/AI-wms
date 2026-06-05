<template>
  <div class="inventory-list">
    <el-card>
      <div class="card-header">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索商品名称或编码" 
          class="search-input"
          @keyup.enter="fetchInventories"
        >
          <template #append>
            <el-button @click="fetchInventories">
              <Search />
            </el-button>
          </template>
        </el-input>
        <el-button type="warning" @click="openAdjustModal">
          <Refresh /> 库存调整
        </el-button>
      </div>
      <el-table :data="inventories" border>
        <el-table-column prop="product_code" label="商品编码" />
        <el-table-column prop="product_name" label="商品名称" />
        <el-table-column prop="warehouse_code" label="仓库" />
        <el-table-column prop="location_code" label="库位" />
        <el-table-column prop="quantity" label="库存数量" />
        <el-table-column prop="batch_no" label="批次号" />
        <el-table-column prop="expiry_date" label="有效期" />
        <el-table-column prop="created_at" label="更新时间" />
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

    <el-dialog title="库存调整" :visible.sync="adjustModalVisible">
      <el-form :model="adjustForm" label-width="100px">
        <el-form-item label="调整类型" prop="adjustment_type">
          <el-select v-model="adjustForm.adjustment_type">
            <el-option label="盘盈" value="INCREASE" />
            <el-option label="盘亏" value="DECREASE" />
            <el-option label="调拨" value="TRANSFER" />
          </el-select>
        </el-form-item>
        <el-form-item label="商品" prop="product">
          <el-select v-model="adjustForm.product">
            <el-option v-for="product in products" :key="product.id" :label="product.name" :value="product.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="库位" prop="location">
          <el-select v-model="adjustForm.location">
            <el-option v-for="location in locations" :key="location.id" :label="location.code" :value="location.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="调整数量" prop="quantity">
          <el-input type="number" v-model="adjustForm.quantity" />
        </el-form-item>
        <el-form-item label="调整原因" prop="reason">
          <el-input type="textarea" v-model="adjustForm.reason" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="adjustModalVisible = false">取消</el-button>
        <el-button type="primary" @click="saveAdjustment">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Refresh } from '@element-plus/icons-vue'
import axios from 'axios'

const inventories = ref([])
const products = ref([])
const locations = ref([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const adjustModalVisible = ref(false)
const adjustForm = ref({
  adjustment_no: '',
  adjustment_type: 'INCREASE',
  product: null,
  location: null,
  quantity: 0,
  reason: ''
})

const fetchInventories = async () => {
  try {
    const response = await axios.get(`/api/inventories/?page=${currentPage.value}&page_size=${pageSize.value}`)
    inventories.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取库存列表失败:', error)
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

const openAdjustModal = () => {
  adjustForm.value = {
    adjustment_no: '',
    adjustment_type: 'INCREASE',
    product: null,
    location: null,
    quantity: 0,
    reason: ''
  }
  adjustModalVisible.value = true
}

const saveAdjustment = async () => {
  try {
    const now = new Date()
    adjustForm.value.adjustment_no = `ADJ${now.getFullYear()}${String(now.getMonth()+1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}${String(Date.now()).slice(-6)}`
    await axios.post('/api/adjustments/', adjustForm.value)
    adjustModalVisible.value = false
    fetchInventories()
    ElMessage.success('调整成功')
  } catch (error) {
    ElMessage.error('调整失败')
    console.error('库存调整失败:', error)
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchInventories()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchInventories()
}

onMounted(() => {
  fetchInventories()
  fetchProducts()
  fetchLocations()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}
</style>