<template>
  <el-container style="height: 100vh;">
    <el-aside width="200px" class="aside">
      <div class="logo">
        <h2>WMS仓储管理</h2>
      </div>
      <el-menu :default-active="$route.path" class="menu" router>
        <el-menu-item path="/">
          <el-icon><Dashboard /></el-icon>
          <span>首页仪表盘</span>
        </el-menu-item>
        <el-sub-menu index="warehouse">
          <template #title>
            <el-icon><Building /></el-icon>
            <span>仓库管理</span>
          </template>
          <el-menu-item path="/warehouses">仓库列表</el-menu-item>
          <el-menu-item path="/locations">库位管理</el-menu-item>
        </el-sub-menu>
        <el-menu-item path="/products">
          <el-icon><Package /></el-icon>
          <span>商品管理</span>
        </el-menu-item>
        <el-menu-item path="/inventories">
          <el-icon><Storage /></el-icon>
          <span>库存管理</span>
        </el-menu-item>
        <el-sub-menu index="order">
          <template #title>
            <el-icon><ShoppingCart /></el-icon>
            <span>订单管理</span>
          </template>
          <el-menu-item path="/orders">订单列表</el-menu-item>
          <el-menu-item path="/orders/create">创建订单</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="partner">
          <template #title>
            <el-icon><Users /></el-icon>
            <span>合作伙伴</span>
          </template>
          <el-menu-item path="/suppliers">供应商</el-menu-item>
          <el-menu-item path="/customers">客户</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <span class="title">{{ pageTitle }}</span>
          <div class="header-right">
            <el-button type="text">退出登录</el-button>
          </div>
        </div>
      </el-header>
      <el-main class="main">
        <router-view @update:title="updateTitle" />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { 
  Dashboard, Building, Package, Storage, 
  ShoppingCart, Users 
} from '@element-plus/icons-vue'

const route = useRoute()
const pageTitle = ref('首页仪表盘')

const titleMap = {
  '/': '首页仪表盘',
  '/warehouses': '仓库列表',
  '/locations': '库位管理',
  '/products': '商品管理',
  '/inventories': '库存管理',
  '/orders': '订单列表',
  '/orders/create': '创建订单',
  '/suppliers': '供应商管理',
  '/customers': '客户管理'
}

watch(() => route.path, (newPath) => {
  pageTitle.value = titleMap[newPath] || 'WMS仓储管理'
})

const updateTitle = (title) => {
  pageTitle.value = title
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.el-container {
  height: 100vh;
}

.aside {
  background: #2d3748;
  color: white;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #4a5568;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
}

.menu {
  border-right: none;
  height: calc(100% - 60px);
}

.menu :deep(.el-menu-item),
.menu :deep(.el-sub-menu__title) {
  color: #a0aec0;
}

.menu :deep(.el-menu-item.is-active),
.menu :deep(.el-sub-menu__title.is-active) {
  color: #4299e1;
  background: #1a202c;
}

.header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.title {
  font-size: 18px;
  font-weight: bold;
  color: #2d3748;
}

.header-right {
  display: flex;
  align-items: center;
}

.main {
  padding: 20px;
  background: #f7fafc;
  overflow-y: auto;
}
</style>