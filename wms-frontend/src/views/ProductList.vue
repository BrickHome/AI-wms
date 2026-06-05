<template>
  <div class="product-list">
    <el-card>
      <div class="card-header">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索商品名称或编码" 
          class="search-input"
          @keyup.enter="fetchProducts"
        >
          <template #append>
            <el-button @click="fetchProducts">
              <Search />
            </el-button>
          </template>
        </el-input>
        <el-button type="primary" @click="openAddModal">
          <Plus /> 添加商品
        </el-button>
      </div>
      <el-table :data="products" border>
        <el-table-column prop="code" label="商品编码" />
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="sku" label="SKU" />
        <el-table-column prop="barcode" label="条码" />
        <el-table-column prop="category" label="分类" />
        <el-table-column prop="unit" label="单位" />
        <el-table-column prop="price" label="单价" />
        <el-table-column prop="min_stock" label="最低库存" />
        <el-table-column prop="max_stock" label="最高库存" />
        <el-table-column prop="is_active" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'warning'">
              {{ scope.row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="editProduct(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteProduct(scope.row.id)">删除</el-button>
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

    <el-dialog :title="isEdit ? '编辑商品' : '添加商品'" :visible.sync="modalVisible">
      <el-form :model="form" label-width="100px">
        <el-form-item label="商品编码" prop="code">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="SKU" prop="sku">
          <el-input v-model="form.sku" />
        </el-form-item>
        <el-form-item label="条码" prop="barcode">
          <el-input v-model="form.barcode" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-input v-model="form.category" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="form.unit" />
        </el-form-item>
        <el-form-item label="重量(kg)" prop="weight">
          <el-input type="number" step="0.001" v-model="form.weight" />
        </el-form-item>
        <el-form-item label="体积(m³)" prop="volume">
          <el-input type="number" step="0.001" v-model="form.volume" />
        </el-form-item>
        <el-form-item label="单价" prop="price">
          <el-input type="number" step="0.01" v-model="form.price" />
        </el-form-item>
        <el-form-item label="最低库存" prop="min_stock">
          <el-input type="number" v-model="form.min_stock" />
        </el-form-item>
        <el-form-item label="最高库存" prop="max_stock">
          <el-input type="number" v-model="form.max_stock" />
        </el-form-item>
        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="form.is_active" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="form.description" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="modalVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProduct">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const products = ref([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const modalVisible = ref(false)
const isEdit = ref(false)
const form = ref({
  id: null,
  code: '',
  name: '',
  sku: '',
  barcode: '',
  category: '',
  unit: '件',
  weight: 0,
  volume: 0,
  price: 0,
  min_stock: 0,
  max_stock: 0,
  is_active: true,
  description: ''
})

const fetchProducts = async () => {
  try {
    const response = await axios.get(`/api/products/?page=${currentPage.value}&page_size=${pageSize.value}`)
    products.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取商品列表失败:', error)
  }
}

const openAddModal = () => {
  isEdit.value = false
  form.value = { id: null, code: '', name: '', sku: '', barcode: '', category: '', unit: '件', weight: 0, volume: 0, price: 0, min_stock: 0, max_stock: 0, is_active: true, description: '' }
  modalVisible.value = true
}

const editProduct = (row) => {
  isEdit.value = true
  form.value = { ...row }
  modalVisible.value = true
}

const saveProduct = async () => {
  try {
    if (isEdit.value) {
      await axios.put(`/api/products/${form.value.id}/`, form.value)
    } else {
      await axios.post('/api/products/', form.value)
    }
    modalVisible.value = false
    fetchProducts()
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
    console.error('保存商品失败:', error)
  }
}

const deleteProduct = async (id) => {
  try {
    await axios.delete(`/api/products/${id}/`)
    fetchProducts()
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
    console.error('删除商品失败:', error)
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchProducts()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchProducts()
}

onMounted(() => {
  fetchProducts()
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