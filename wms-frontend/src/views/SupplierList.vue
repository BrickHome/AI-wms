<template>
  <div class="supplier-list">
    <el-card>
      <div class="card-header">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索供应商名称或编码" 
          class="search-input"
          @keyup.enter="fetchSuppliers"
        >
          <template #append>
            <el-button @click="fetchSuppliers">
              <Search />
            </el-button>
          </template>
        </el-input>
        <el-button type="primary" @click="openAddModal">
          <Plus /> 添加供应商
        </el-button>
      </div>
      <el-table :data="suppliers" border>
        <el-table-column prop="code" label="供应商编码" />
        <el-table-column prop="name" label="供应商名称" />
        <el-table-column prop="contact" label="联系人" />
        <el-table-column prop="phone" label="联系电话" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="editSupplier(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteSupplier(scope.row.id)">删除</el-button>
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

    <el-dialog :title="isEdit ? '编辑供应商' : '添加供应商'" :visible.sync="modalVisible">
      <el-form :model="form" label-width="100px">
        <el-form-item label="供应商编码" prop="code">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="供应商名称" prop="name">
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
        <el-button type="primary" @click="saveSupplier">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const suppliers = ref([])
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

const fetchSuppliers = async () => {
  try {
    const response = await axios.get(`/api/suppliers/?page=${currentPage.value}&page_size=${pageSize.value}`)
    suppliers.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取供应商列表失败:', error)
  }
}

const openAddModal = () => {
  isEdit.value = false
  form.value = { id: null, code: '', name: '', contact: '', phone: '', email: '', address: '' }
  modalVisible.value = true
}

const editSupplier = (row) => {
  isEdit.value = true
  form.value = { ...row }
  modalVisible.value = true
}

const saveSupplier = async () => {
  try {
    if (isEdit.value) {
      await axios.put(`/api/suppliers/${form.value.id}/`, form.value)
    } else {
      await axios.post('/api/suppliers/', form.value)
    }
    modalVisible.value = false
    fetchSuppliers()
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
    console.error('保存供应商失败:', error)
  }
}

const deleteSupplier = async (id) => {
  try {
    await axios.delete(`/api/suppliers/${id}/`)
    fetchSuppliers()
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
    console.error('删除供应商失败:', error)
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchSuppliers()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchSuppliers()
}

onMounted(() => {
  fetchSuppliers()
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