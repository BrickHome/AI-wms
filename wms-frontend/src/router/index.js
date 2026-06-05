import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/warehouses',
    name: 'WarehouseList',
    component: () => import('../views/WarehouseList.vue')
  },
  {
    path: '/locations',
    name: 'LocationList',
    component: () => import('../views/LocationList.vue')
  },
  {
    path: '/products',
    name: 'ProductList',
    component: () => import('../views/ProductList.vue')
  },
  {
    path: '/inventories',
    name: 'InventoryList',
    component: () => import('../views/InventoryList.vue')
  },
  {
    path: '/orders',
    name: 'OrderList',
    component: () => import('../views/OrderList.vue')
  },
  {
    path: '/orders/create',
    name: 'OrderCreate',
    component: () => import('../views/OrderCreate.vue')
  },
  {
    path: '/suppliers',
    name: 'SupplierList',
    component: () => import('../views/SupplierList.vue')
  },
  {
    path: '/customers',
    name: 'CustomerList',
    component: () => import('../views/CustomerList.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router