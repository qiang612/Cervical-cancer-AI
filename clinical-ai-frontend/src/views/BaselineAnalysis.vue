<template>
  <el-row :gutter="20" style="height: 100%;">
    <el-col :span="6">
      <el-card class="box-card" style="height: 100%;">
        <template #header>
          <div class="card-header">
            <span>参数设置</span>
          </div>
        </template>
        <el-form label-position="top">
          <el-form-item label="因变量">
            <el-select v-model="dependentVar" placeholder="请选择">
              <el-option label="group" value="group"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="自变量">
            <el-select v-model="independentVars" multiple placeholder="请选择" style="width: 100%">
               <el-checkbox v-model="selectAllVars" @change="handleSelectAll" style="padding-left: 10px;">全选</el-checkbox>
              <el-option v-for="item in allVars" :key="item" :label="item" :value="item"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="小数位数">
            <el-input-number v-model="decimalPlaces" :min="1" :max="5" />
          </el-form-item>
          <el-button type="primary" @click="generateTable" :loading="loading">
            <el-icon style="vertical-align: middle; margin-right: 4px;"><CaretRight /></el-icon>
            生成表格
          </el-button>
        </el-form>
      </el-card>
    </el-col>

    <el-col :span="18">
      <el-card class="box-card" style="height: 100%;">
        <template #header>
          <div class="card-header">
            <span>基线特征表</span>
            <el-button class="button" type="primary" link>
              <el-icon style="vertical-align: middle; margin-right: 4px;"><Download /></el-icon>
              下载
            </el-button>
          </div>
        </template>
        <el-table :data="tableData" stripe style="width: 100%" border height="calc(100vh - 205px)">
          <el-table-column prop="variable" label="Variables" width="220" />
          <el-table-column prop="all" label="[ALL] N=680" />
          <el-table-column prop="group0" label="0 (n=544)" />
          <el-table-column prop="group1" label="1 (n=136)" />
          <el-table-column prop="p" label="P" />
          <el-table-column prop="statistic" label="Statistic" />
        </el-table>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref } from 'vue';

const dependentVar = ref('group');
const allVars = ['age', 'BMI', 'ToS', 'BL', 'DDimer', 'CA153', 'CDU', 'EKG'];
const independentVars = ref(['age', 'BMI', 'ToS']); // 默认选中几个
const selectAllVars = ref(false);
const decimalPlaces = ref(2);
const loading = ref(false);

// 这是后端返回的固定数据 (Mock Data)
const mockData = [
  { variable: 'age, Median (Q1,Q3)', all: '63 (55, 68)', group0: '61 (53, 67)', group1: '66 (61, 70)', p: '<0.001', statistic: '25479' },
  { variable: 'BMI, Mean ± SD', all: '23.8±3.14', group0: '23.48±3.15', group1: '25.11±2.76', p: '<0.001', statistic: '-5.978' },
  { variable: 'ToS, Median (Q1,Q3)', all: '120 (90.75, 156.25)', group0: '115 (90, 147.25)', group1: '155 (115, 190.25)', p: '<0.001', statistic: '22988' },
  { variable: 'BL, Median (Q1,Q3)', all: '50 (50, 100)', group0: '50 (50, 50)', group1: '100 (50, 150)', p: '<0.001', statistic: '21390' },
  { variable: 'DDimer, Median (Q1,Q3)', all: '138 (102, 215.25)', group0: '134 (99.75, 184)', group1: '218.5 (110, 390.75)', p: '<0.001', statistic: '27055.5' },
];
const tableData = ref([]);

const handleSelectAll = (val) => {
  independentVars.value = val ? [...allVars] : [];
};

const generateTable = () => {
  loading.value = true;
  // 模拟调用后端API进行数据分析
  setTimeout(() => {
    tableData.value = mockData; // 将固定数据填充到表格中
    loading.value = false;
  }, 800);
};

// 页面加载时就执行一次分析
generateTable();
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.el-select, .el-input-number {
  width: 100%;
}
.box-card {
  display: flex;
  flex-direction: column;
}
:deep(.el-card__body) {
  flex-grow: 1;
}
</style>