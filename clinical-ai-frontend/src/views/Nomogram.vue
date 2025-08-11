<template>
  <el-row :gutter="20" style="height: 100%;">
    <el-col :span="6">
      <el-card class="box-card" style="height: 100%;">
        <template #header>
          <span>参数设置</span>
        </template>
        <el-form label-position="top">
            <el-form-item label="输出格式">
              <el-radio-group v-model="outputFormat">
                <el-radio-button label="PNG" />
                <el-radio-button label="PDF" />
                <el-radio-button label="JPEG" />
              </el-radio-group>
            </el-form-item>
             <el-form-item label="图像宽度">
                <el-input-number v-model="imageWidth" :min="400" :max="2000" />
            </el-form-item>
             <el-form-item label="图像高度">
                <el-input-number v-model="imageHeight" :min="300" :max="1500" />
            </el-form-item>
        </el-form>
      </el-card>
    </el-col>

    <el-col :span="18">
       <el-card class="box-card" style="height: 100%;">
        <template #header>
          <div class="card-header">
            <span>列线图 (Nomogram)</span>
             <el-button class="button" type="primary" link>
              <el-icon style="vertical-align: middle; margin-right: 4px;"><Download /></el-icon>
              下载
            </el-button>
          </div>
        </template>
        <Chart :option="chartOption" :style="{height: 'calc(100vh - 205px)'}" />
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref } from 'vue';
import Chart from '../components/Chart.vue';

const outputFormat = ref('PNG');
const imageWidth = ref(800);
const imageHeight = ref(600);

// 这是根据ECharts能力虚构的列线图配置，用于1:1仿照界面
// 注意：用ECharts实现一个功能完全正确的医学列线图非常复杂
// 这里的代码主要是为了【视觉还原】，让界面看起来一模一样
const chartOption = ref({
    grid: {
        top: 80,
        bottom: 120
    },
    xAxis: {
        type: 'value',
        min: 0,
        max: 100,
        splitLine: { show: true },
        axisLabel: { show: true },
        axisLine: { show: true },
        name: 'Points',
        nameLocation: 'center',
        nameGap: 30
    },
    yAxis: {
        type: 'category',
        data: ['age', 'BMI', 'BL', 'DDimer', 'ToS', 'EKG', 'PF', 'Total Points', 'Diagnostic Possibility'],
        axisLine: { show: false },
        axisTick: { show: false },
    },
    visualMap: [
      {
        show: false,
        dimension: 0,
        seriesIndex: 0,
        min: 0,
        max: 100,
        inRange: {
            color: ['#333']
        }
      }
    ],
    series: [
        {
            type: 'line',
            symbol: 'none',
            data: [[0,0], [100,0], [0,1], [100,1], [0,2], [100,2], [0,3], [100,3], [0,4], [100,4], [0,5], [100,5], [0,6], [100,6], [0,7], [100,7], [0,8], [100,8]]
        }
    ]
});
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.box-card {
  display: flex;
  flex-direction: column;
}
:deep(.el-card__body) {
  flex-grow: 1;
}
</style>