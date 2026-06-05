<template>
  <div class="warehouse-list">
    <el-card>
      <div class="card-header">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索仓库名称或编码" 
          class="search-input"
          @keyup.enter="fetchWarehouses"
        >
          <template #append>
            <el-button @click="fetchWarehouses">
              <Search />
            </el-button>
          </template>
        </el-input>
        <el-button type="primary" @click="openAddModal">
          <Plus /> 添加仓库
        </el-button>
      </div>
      <el-table :data="warehouses" border>
        <el-table-column prop="code" label="仓库编码" />
        <el-table-column prop="name" label="仓库名称" />
        <el-table-column prop="address" label="仓库地址" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="editWarehouse(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteWarehouse(scope.row.id)">删除</el-button>
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

    <el-dialog :title="isEdit ? '编辑仓库' : '添加仓库'" :visible.sync="modalVisible">
      <el-form :model="form" label-width="100px">
        <el-form-item label="仓库编码" prop="code">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="仓库名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="仓库地址" prop="address">
          <el-input type="textarea" v-model="form.address" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="form.description" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="modalVisible = false">取消</el-button>
        <el-button type="primary" @click="saveWarehouse">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

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
  address: '',
  description: ''
})

const fetchWarehouses = async () => {
  try {
    const response = await axios.get(`/api/warehouses/?page=${currentPage.value}&page_size=${pageSize.value}&search=${searchQuery.value}`)
    warehouses.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取仓库列表失败:', error)
  }
}

const openAddModal = () => {
  isEdit.value = false
  form.value = { id: null, code: '', name: '', address: '', description: '' }
  modalVisible.value = true
}

const editWarehouse = (row) => {
  isEdit.value = true
  form.value = { ...row }
  modalVisible.value = true
}

const saveWarehouse = async () => {
  try {
    if (isEdit.value) {
      await axios.put(`/api/warehouses/${form.value.id}/`, form.value)
    } else {
      await axios.post('/api/warehouses/', form.value)
    }
    modalVisible.value = false
    fetchWarehouses()
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
    console.error('保存仓库失败:', error)
  }
}

const deleteWarehouse = async (id) => {
  try {
    await axios.delete(`/api/warehouses/${id}/`)
    fetchWarehouses()
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
    console.error('删除仓库失败:', error)
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchWarehouses()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchWarehouses()
}

onMounted(() => {
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