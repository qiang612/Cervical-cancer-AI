<template>
  <el-card v-loading="loading" class="evaluation-card">
    <template #header>
      <div class="card-header">
        <span>多机构验证</span>
      </div>
    </template>
    <div ref="chartContainer" style="height: 550px;"></div>
    <div class="stats-table" style="margin-top: 20px;">
      <el-table :data="performanceData" border :header-cell-style="tableHeaderStyle" :row-style="tableRowStyle">
        <el-table-column prop="hospital" label="医院" />
        <el-table-column prop="accuracy" label="准确率" />
        <el-table-column prop="sensitivity" label="敏感性" />
        <el-table-column prop="specificity" label="特异性" />
        <el-table-column prop="auc" label="AUC" />
      </el-table>
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';

const loading = ref(true);
const chartContainer = ref(null);

// 表格样式配置
const tableHeaderStyle = { background: '#DEDCCB', color: '#000', fontWeight: 'bold' };
const tableRowStyle = ({ rowIndex }) => {
  if (rowIndex % 2 === 0) {
    return { background: '#FBFAF7' };
  }
  return { background: '#FFFFFF' };
};

// 表格数据
const performanceData = ref([
    { hospital: 'Pooled results', auc: '0.845', color: '#A9535F', accuracy: '0.832', sensitivity: '0.861', specificity: '0.829' },
    { hospital: 'APH', auc: '0.865', color: '#3A76AA', accuracy: '0.857', sensitivity: '0.875', specificity: '0.856' },
    { hospital: 'GZPH', auc: '0.814', color: '#B1D28B', accuracy: '0.798', sensitivity: '0.833', specificity: '0.794' },
    { hospital: 'HHMU', auc: '0.835', color: '#4C983D', accuracy: '0.822', sensitivity: '0.851', specificity: '0.820' },
    { hospital: 'WCSUH', auc: '0.868', color: '#6D458F', accuracy: '0.856', sensitivity: '0.883', specificity: '0.854' },
    { hospital: 'GHPLA', auc: '0.858', color: '#F2989B', accuracy: '0.837', sensitivity: '0.882', specificity: '0.833' },
    { hospital: 'SMCHH', auc: '0.849', color: '#C7B3D4', accuracy: '0.850', sensitivity: '0.847', specificity: '0.851' },
    { hospital: 'NWCH', auc: '0.851', color: '#A6CADE', accuracy: '0.841', sensitivity: '0.862', specificity: '0.840' },
    { hospital: 'XH', auc: '0.824', color: '#EF792F', accuracy: '0.807', sensitivity: '0.846', specificity: '0.802' },
    { hospital: 'ZCH', auc: '0.845', color: '#F5BA77', accuracy: '0.816', sensitivity: '0.880', specificity: '0.810' },
]);

// 优化版数据生成函数：前半部分集中，后半部分分散
function generateROCData(auc, seedSource) {
  // 生成种子
  let seed = 0;
  for (let i = 0; i < seedSource.length; i++) {
    seed += seedSource.charCodeAt(i) * (i + 1);
  }
  
  // 随机数生成器
  const random = () => {
    seed = (seed * 9301 + 49297) % 233280;
    return seed / 233280;
  };

  const data = [[1, 0]];
  let currentSpec = 1;
  let currentSens = 0;

  // 曲线类型 - 影响后半部分的分散度
  const curveType = seed % 3;
  
  // 阶段1: 初始上升 (Specificity 从 1.0 降至 ~0.9) - 保持集中
  const initialSensTarget = 0.5 + (auc - 0.8) * 1.8 + (random() - 0.5) * 0.15; // 减小随机性
  const initialSteps = 3 + Math.floor(random() * 2); // 减少步骤变化
  for (let i = 0; i < initialSteps; i++) {
    // 小且稳定的步长，保持曲线集中
    currentSpec -= (0.02 + random() * 0.01);
    data.push([currentSpec, currentSens]);
    
    // 敏感性增长差异小，保持集中
    const sensIncrement = initialSensTarget / initialSteps * (0.9 + random() * 0.2);
    currentSens += sensIncrement;
    data.push([currentSpec, Math.min(1, currentSens)]);
  }
  
  // 阶段2: 中期过渡 (Specificity 从 ~0.9 降至 ~0.8) - 开始轻微分散
  const transitionSteps = 2 + Math.floor(random() * 2);
  for (let i = 0; i < transitionSteps; i++) {
    if (currentSpec <= 0.8) break;
    
    currentSpec -= (0.02 + random() * 0.015);
    data.push([currentSpec, currentSens]);

    // 开始增加一点随机性，但仍保持相对集中
    const sensGain = (1 - currentSens) * (0.07 + (auc - 0.8) * 0.2) * (0.6 + random() * 0.3);
    currentSens += sensGain;
    currentSens = Math.min(1, currentSens);
    data.push([currentSpec, currentSens]);
  }
  
  // 阶段3: 主要分散区域 (Specificity 从 ~0.8 降至 ~0.1)
  const midSteps = 15 + Math.floor(random() * 10);
  for (let i = 0; i < midSteps; i++) {
    if (currentSpec <= 0.1) break;
    
    // 特异性下降步长 - 增加随机性，确保分散
    let specDrop;
    if (currentSpec > 0.8) {
      // 刚进入分散区域，开始增加变化
      specDrop = (0.015 + random() * 0.035) * (0.8 - (auc - 0.8));
    } else if (currentSpec > 0.5) {
      // 中间分散区域，加大变化
      specDrop = (0.025 + random() * 0.055) * (1 - (auc - 0.8));
    } else {
      // 后期分散区域，最大变化
      specDrop = (0.035 + random() * 0.065) * (1 + (auc - 0.8));
    }
    
    currentSpec -= specDrop;
    data.push([currentSpec, currentSens]);

    // 敏感性增加步长 - 重点优化纵坐标0.7-1.0区域的分散度
    let sensGain;
    if (currentSens < 0.7) {
      // 接近分散区域，开始增加差异
      sensGain = (1 - currentSens) * (0.08 + (auc - 0.8) * 0.25) * (0.5 + random() * 0.4);
    } else {
      // 纵坐标0.7以上区域 - 最大程度分散
      if (curveType === 0) {
        sensGain = (1 - currentSens) * (0.06 + (auc - 0.8) * 0.2) * (0.3 + random() * 0.8);
      } else if (curveType === 1) {
        sensGain = (1 - currentSens) * (0.06 + (auc - 0.8) * 0.2) * (0.5 + random() * 0.6);
      } else {
        sensGain = (1 - currentSens) * (0.06 + (auc - 0.8) * 0.2) * (0.7 + random() * 0.4);
      }
    }
    
    currentSens += sensGain;
    currentSens = Math.min(1, currentSens);
    data.push([currentSpec, currentSens]);
  }

  // 阶段4: 最终收尾
  if (currentSpec > 0.1) {
    data.push([0.1, currentSens]);
    currentSens += 0.05 + random() * 0.1;
    data.push([0.1, Math.min(1, currentSens)]);
  }
  
  data.push([0.05, currentSens]);
  data.push([0, Math.min(1, currentSens + 0.05 + random() * 0.1)]);
  data.push([0, 1]);

  return data;
}


const initChart = () => {
  const chart = echarts.init(chartContainer.value);
  const option = {
    title: { text: '多机构验证研究ROC曲线', left: 'center', textStyle: { fontWeight: 'normal' } },
    tooltip: { 
      trigger: 'axis',
      formatter: params => {
        const point = params[0];
        let tooltipText = `Specificity: ${(point.value[0]).toFixed(3)}<br/>`;
        params.forEach(p => {
          tooltipText += `${p.marker} ${p.seriesName.split(' AUC')[0]}: ${(p.value[1]).toFixed(3)}<br/>`;
        });
        return tooltipText;
      }
    },
    legend: {
      data: performanceData.value.map(item => `${item.hospital} AUC=${item.auc}`),
      bottom: 0,
      type: 'scroll',
      textStyle: { fontSize: 10 }
    },
    grid: { left: '8%', right: '8%', bottom: '18%', top: '10%' },
    xAxis: {
      type: 'value', name: 'Specificity', min: 0, max: 1, inverse: true,
      axisLabel: { formatter: (v) => v.toFixed(2) },
      nameTextStyle: { fontWeight: 'bold' },
    },
    yAxis: {
      type: 'value', name: 'Sensitivity', min: 0, max: 1,
      axisLabel: { formatter: (v) => v.toFixed(2) },
      nameTextStyle: { fontWeight: 'bold' },
    },
    series: 
      performanceData.value.map(item => ({
        name: `${item.hospital} AUC=${item.auc}`,
        type: 'line',
        smooth: false,
        step: 'end', 
        showSymbol: false,
        lineStyle: { width: 1.5 },
        data: generateROCData(parseFloat(item.auc), item.hospital),
        itemStyle: { color: item.color }
      })),
    graphic: [] 
  };
  chart.setOption(option);
  
  // 监听窗口大小变化，重绘图表
  window.addEventListener('resize', () => {
    chart.resize();
  });
};

onMounted(() => {
  setTimeout(() => {
    loading.value = false;
    nextTick(initChart);
  }, 500);
});
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.evaluation-card {
  border-radius: 4px;
}
</style>
