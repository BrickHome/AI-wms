<template>
  <div class="customer-list">
    <el-card>
      <div class="card-header">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索客户名称或编码" 
          class="search-input"
          @keyup.enter="fetchCustomers"
        >
          <template #append>
            <el-button @click="fetchCustomers">
              <Search />
            </el-button>
          </template>
        </el-input>
        <el-button type="primary" @click="openAddModal">
          <Plus /> 添加客户
        </el-button>
      </div>
      <el-table :data="customers" border>
        <el-table-column prop="code" label="客户编码" />
        <el-table-column prop="name" label="客户名称" />
        <el-table-column prop="contact" label="联系人" />
        <el-table-column prop="phone" label="联系电话" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="editCustomer(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteCustomer(scope.row.id)">删除</el-button>
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

    <el-dialog :title="isEdit ? '编辑客户' : '添加客户'" :visible.sync="modalVisible">
      <el-form :model="form" label-width="100px">
        <el-form-item label="客户编码" prop="code">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="客户名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact">
          <el-input v-model="form.contact" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input type="textarea" v-model="form.address" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="modalVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCustomer">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const customers = ref([])
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
  contact: '',
  phone: '',
  email: '',
  address: ''
})

const fetchCustomers = async () => {
  try {
    const response = await axios.get(`/api/customers/?page=${currentPage.value}&page_size=${pageSize.value}`)
    customers.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取客户列表失败:', error)
  }
}

const openAddModal = () => {
  isEdit.value = false
  form.value = { id: null, code: '', name: '', contact: '', phone: '', email: '', address: '' }
  modalVisible.value = true
}

const editCustomer = (row) => {
  isEdit.value = true
  form.value = { ...row }
  modalVisible.value = true
}

const saveCustomer = async () => {
  try {
    if (isEdit.value) {
      await axios.put(`/api/customers/${form.value.id}/`, form.value)
    } else {
      await axios.post('/api/customers/', form.value)
    }
    modalVisible.value = false
    fetchCustomers()
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
    console.error('保存客户失败:', error)
  }
}

const deleteCustomer = async (id) => {
  try {
    await axios.delete(`/api/customers/${id}/`)
    fetchCustomers()
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
    console.error('删除客户失败:', error)
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchCustomers()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchCustomers()
}

onMounted(() => {
  fetchCustomers()
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