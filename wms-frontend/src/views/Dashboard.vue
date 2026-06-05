<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon warehouse">
            <Building />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.total_warehouses }}</div>
            <div class="stat-label">仓库总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon location">
            <MapLocation />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.total_locations }}</div>
            <div class="stat-label">库位总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon product">
            <Package />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.total_products }}</div>
            <div class="stat-label">商品种类</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon inventory">
            <Storage />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.total_inventory }}</div>
            <div class="stat-label">库存总量</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon supplier">
            <User />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.total_suppliers }}</div>
            <div class="stat-label">供应商数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon customer">
            <Users />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.total_customers }}</div>
            <div class="stat-label">客户数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon pending">
            <Clock />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.pending_orders }}</div>
            <div class="stat-label">待处理订单</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon today">
            <Calendar />
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ overview.today_in_orders + overview.today_out_orders }}</div>
            <div class="stat-label">今日订单</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card title="今日订单统计">
          <el-row :gutter="10">
            <el-col :span="12">
              <div class="chart-item">
                <div class="chart-value in">{{ overview.today_in_orders }}</div>
                <div class="chart-label">入库订单</div>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-item">
                <div class="chart-value out">{{ overview.today_out_orders }}</div>
                <div class="chart-label">出库订单</div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card title="快速操作">
          <el-button type="primary" style="margin-right: 10px; margin-bottom: 10px;">
            <Plus /> 创建入库单
          </el-button>
          <el-button type="success" style="margin-right: 10px; margin-bottom: 10px;">
            <Plus /> 创建出库单
          </el-button>
          <el-button type="warning" style="margin-bottom: 10px;">
            <RefreshCw /> 库存盘点
          </el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  Building, MapLocation, Package, Storage, 
  User, Users, Clock, Calendar, Plus, RefreshCw 
} from '@element-plus/icons-vue'
import axios from 'axios'

const overview = ref({
  total_warehouses: 0,
  total_locations: 0,
  total_products: 0,
  total_inventory: 0,
  total_suppliers: 0,
  total_customers: 0,
  pending_orders: 0,
  today_in_orders: 0,
  today_out_orders: 0
})

const fetchOverview = async () => {
  try {
    const response = await axios.get('/api/dashboard/overview/')
    overview.value = response.data
  } catch (error) {
    console.error('获取概览数据失败:', error)
  }
}

onMounted(() => {
  fetchOverview()
})
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-right: 20px;
}

.stat-icon.warehouse {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon.location {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-icon.product {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-icon.inventory {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.stat-icon.supplier {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
}

.stat-icon.customer {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #333;
}

.stat-icon.pending {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  color: white;
}

.stat-icon.today {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  color: #333;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #2d3748;
}

.stat-label {
  font-size: 14px;
  color: #718096;
  margin-top: 4px;
}

.chart-item {
  text-align: center;
  padding: 20px;
  background: #f7fafc;
  border-radius: 8px;
}

.chart-value {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 8px;
}

.chart-value.in {
  color: #42b983;
}

.chart-value.out {
  color: #f56c6c;
}

.chart-label {
  font-size: 14px;
  color: #718096;
}
</style>