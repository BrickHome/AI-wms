<template>
  <div class="location-list">
    <el-card>
      <div class="card-header">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索库位编码或名称" 
          class="search-input"
          @keyup.enter="fetchLocations"
        >
          <template #append>
            <el-button @click="fetchLocations">
              <Search />
            </el-button>
          </template>
        </el-input>
        <el-button type="primary" @click="openAddModal">
          <Plus /> 添加库位
        </el-button>
      </div>
      <el-table :data="locations" border>
        <el-table-column prop="code" label="库位编码" />
        <el-table-column prop="name" label="库位名称" />
        <el-table-column prop="warehouse_name" label="所属仓库" />
        <el-table-column prop="location_type" label="库位类型">
          <template #default="scope">
            {{ getLocationTypeName(scope.row.location_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="capacity" label="容量" />
        <el-table-column prop="current_qty" label="当前数量" />
        <el-table-column prop="is_available" label="是否可用">
          <template #default="scope">
            <el-tag :type="scope.row.is_available ? 'success' : 'danger'">
              {{ scope.row.is_available ? '可用' : '不可用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="editLocation(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteLocation(scope.row.id)">删除</el-button>
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

    <el-dialog :title="isEdit ? '编辑库位' : '添加库位'" :visible.sync="modalVisible">
      <el-form :model="form" label-width="100px">
        <el-form-item label="库位编码" prop="code">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="库位名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="所属仓库" prop="warehouse">
          <el-select v-model="form.warehouse">
            <el-option v-for="warehouse in warehouses" :key="warehouse.id" :label="warehouse.name" :value="warehouse.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="库位类型" prop="location_type">
          <el-select v-model="form.location_type">
            <el-option label="货架" value="SHELF" />
            <el-option label="货位" value="BIN" />
            <el-option label="区域" value="AREA" />
            <el-option label="地面" value="FLOOR" />
          </el-select>
        </el-form-item>
        <el-form-item label="容量" prop="capacity">
          <el-input type="number" v-model="form.capacity" />
        </el-form-item>
        <el-form-item label="是否可用" prop="is_available">
          <el-switch v-model="form.is_available" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="form.description" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="modalVisible = false">取消</el-button>
        <el-button type="primary" @click="saveLocation">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const locations = ref([])
const warehouses = ref([])
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
  warehouse: null,
  location_type: 'SHELF',
  capacity: 0,
  is_available: true,
  description: ''
})

const locationTypeNames = {
  'SHELF': '货架',
  'BIN': '货位',
  'AREA': '区域',
  'FLOOR': '地面'
}

const getLocationTypeName = (type) => {
  return locationTypeNames[type] || type
}

const fetchLocations = async () => {
  try {
    const response = await axios.get(`/api/locations/?page=${currentPage.value}&page_size=${pageSize.value}`)
    locations.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取库位列表失败:', error)
  }
}

const fetchWarehouses = async () => {
  try {
    const response = await axios.get('/api/warehouses/')
    warehouses.value = response.data.results
  } catch (error) {
    console.error('获取仓库列表失败:', error)
  }
}

const openAddModal = () => {
  isEdit.value = false
  form.value = { id: null, code: '', name: '', warehouse: null, location_type: 'SHELF', capacity: 0, is_available: true, description: '' }
  modalVisible.value = true
}

const editLocation = (row) => {
  isEdit.value = true
  form.value = { ...row, warehouse: row.warehouse }
  modalVisible.value = true
}

const saveLocation = async () => {
  try {
    if (isEdit.value) {
      await axios.put(`/api/locations/${form.value.id}/`, form.value)
    } else {
      await axios.post('/api/locations/', form.value)
    }
    modalVisible.value = false
    fetchLocations()
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
    console.error('保存库位失败:', error)
  }
}

const deleteLocation = async (id) => {
  try {
    await axios.delete(`/api/locations/${id}/`)
    fetchLocations()
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
    console.error('删除库位失败:', error)
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchLocations()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchLocations()
}

onMounted(() => {
  fetchLocations()
  fetchWarehouses()
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