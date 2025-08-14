<template>
  <el-card v-loading="loading" class="evaluation-card">
    <template #header>
      <span>社区有组织筛查结果</span>
    </template>
    <el-row :gutter="20">
      <el-col :span="8"><div ref="rocChart" style="height: 400px;"></div></el-col>
      <el-col :span="8"><div ref="performanceChart" style="height: 400px;"></div></el-col>
      <el-col :span="8"><div ref="efficiencyChart" style="height: 400px;"></div></el-col>
    </el-row>
  </el-card>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';

const loading = ref(true);
const rocChart = ref(null);
const performanceChart = ref(null);
const efficiencyChart = ref(null);

// ROC曲线数据生成函数
function generateROCData(auc, seed = 1) {
  let currentSeed = seed;
  const random = () => {
    currentSeed = (currentSeed * 9301 + 49297) % 233280;
    return currentSeed / 233280;
  };
  const data = [[1, 0]];
  let currentSpec = 1;
  let currentSens = 0;
  const initialSensTarget = 0.5 + (auc - 0.8) * 1.8 + (random() - 0.5) * 0.15;
  const initialSteps = 3 + Math.floor(random() * 2);
  for (let i = 0; i < initialSteps; i++) {
    currentSpec -= (0.02 + random() * 0.01);
    data.push([currentSpec, currentSens]);
    const sensIncrement = initialSensTarget / initialSteps * (0.9 + random() * 0.2);
    currentSens += sensIncrement;
    data.push([currentSpec, Math.min(1, currentSens)]);
  }
  const transitionSteps = 2 + Math.floor(random() * 2);
  for (let i = 0; i < transitionSteps; i++) {
    if (currentSpec <= 0.8) break;
    currentSpec -= (0.02 + random() * 0.015);
    data.push([currentSpec, currentSens]);
    const sensGain = (1 - currentSens) * (0.07 + (auc - 0.8) * 0.2) * (0.6 + random() * 0.3);
    currentSens += sensGain;
    currentSens = Math.min(1, currentSens);
    data.push([currentSpec, currentSens]);
  }
  const midSteps = 15 + Math.floor(random() * 5);
  for (let i = 0; i < midSteps; i++) {
    if (currentSpec <= 0.1) break;
    let specDrop;
    if (currentSpec > 0.8) {
      specDrop = (0.015 + random() * 0.035) * (0.8 - (auc - 0.8));
    } else if (currentSpec > 0.5) {
      specDrop = (0.025 + random() * 0.055) * (1 - (auc - 0.8));
    } else {
      specDrop = (0.035 + random() * 0.065) * (1 + (auc - 0.8));
    }
    currentSpec -= specDrop;
    data.push([currentSpec, currentSens]);
    let sensGain;
    if (currentSens < 0.7) {
      sensGain = (1 - currentSens) * (0.08 + (auc - 0.8) * 0.25) * (0.5 + random() * 0.4);
    } else {
      const curveType = seed % 3;
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

const initCharts = () => {
  // 图 3A: ROC 曲线
  const roc = echarts.init(rocChart.value);
  roc.setOption({
    title: { text: 'ROC曲线', left: 'center', textStyle: { fontSize: 14, fontWeight: 'normal' } },
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
      data: ['DL model-only AUC=0.855', 'Senior cytopathologist alone (average) AUC=0.877'],
      bottom: 0,
      type: 'scroll',
      textStyle: { fontSize: 9 }
    },
    // 调整 grid 为左侧的两个Y轴标签留出空间
    grid: { left: '16%', right: '10%', bottom: '11%', top: '15%' }, 
    xAxis: {
      type: 'value', min: 0, max: 1, inverse: true,
      // --- 修正点 1: 移除横坐标轴的 name 属性 ---
      axisLabel: { formatter: (v) => v.toFixed(1) },
    },
    yAxis: {
        // 标准的Y轴: Sensitivity
        type: 'value', name: 'Sensitivity', min: 0, max: 1,
        position: 'left',
        nameTextStyle: { fontWeight: 'bold' },
        axisLabel: { formatter: (v) => v.toFixed(1) },
    },
    // --- 修正点 2: 使用 graphic 元素添加一个可控的、竖向的 'Specificity' 标签 ---
    graphic: {
        elements: [
            {
                type: 'text',
                left: 15,       // 距离容器左侧的距离
                top: 'center',  // 垂直居中
                style: {
                    text: 'Specificity',
                    textAlign: 'center',
                    fill: '#333', // 文字颜色
                    fontWeight: 'bold'
                },
                // 旋转 -90 度，使其从下往上阅读
                rotation: Math.PI / 2 
            }
        ]
    },
    series: [
      { name: 'DL model-only AUC=0.855', type: 'line', smooth: false, step: 'end', showSymbol: false, data: generateROCData(0.855, 10), lineStyle: { color: '#B05461' } },
      { name: 'Senior cytopathologist alone (average) AUC=0.877', type: 'line', smooth: false, step: 'end', showSymbol: false, data: generateROCData(0.877, 20), lineStyle: { color: '#4D71A7' } },
      { type: 'scatter', symbol: 'square', symbolSize: 10, data: [[0.901, 0.854], [0.820, 0.892], [0.750, 0.915], [0.620, 0.935]], itemStyle: { color: '#4D71A7' }, tooltip: { formatter: (params) => `Specificity: ${params.value[0].toFixed(3)}<br/>Sensitivity: ${params.value[1].toFixed(3)}` } },
      { type: 'scatter', symbol: 'circle', symbolSize: 10, data: [[0.870, 0.865], [0.780, 0.900], [0.550, 0.940]], itemStyle: { color: '#4D71A7' }, tooltip: { formatter: (params) => `Specificity: ${params.value[0].toFixed(3)}<br/>Sensitivity: ${params.value[1].toFixed(3)}` } },
      { type: 'scatter', symbol: 'square', symbolSize: 10, data: [[0.831, 0.878], [0.780, 0.905], [0.650, 0.930], [0.500, 0.945]], itemStyle: { color: '#B05461' }, tooltip: { formatter: (params) => `Specificity: ${params.value[0].toFixed(3)}<br/>Sensitivity: ${params.value[1].toFixed(3)}` } },
      { type: 'scatter', symbol: 'circle', symbolSize: 10, data: [[0.800, 0.885], [0.720, 0.910], [0.580, 0.935]], itemStyle: { color: '#B05461' }, tooltip: { formatter: (params) => `Specificity: ${params.value[0].toFixed(3)}<br/>Sensitivity: ${params.value[1].toFixed(3)}` } }
    ]
  });

  // 图 3B: 诊断性能柱状图
  const perf = echarts.init(performanceChart.value);
  perf.setOption({
    title: { text: '诊断性能', left: 'center', textStyle: { fontSize: 14, fontWeight: 'normal' } },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { data: ['DL model-only', 'Senior cytopathologist (average)'], top: 30, textStyle: { fontSize: 10 } },
    grid: { left: '10%', right: '10%', bottom: '10%', top: '30%' },
    xAxis: { type: 'category', data: ['Accuracy', 'Sensitivity', 'Specificity'] },
    yAxis: { type: 'value', min: 0.8, max: 1.0, name: 'Value' },
    series: [
      { name: 'DL model-only', type: 'bar', data: [0.832, 0.878, 0.831], itemStyle: { color: '#95B9A6' } },
      { name: 'Senior cytopathologist (average)', type: 'bar', data: [0.901, 0.854, 0.901], itemStyle: { color: '#F8E39A' } }
    ],
    graphic: [
      { type: 'text', left: '22%', top: '22%', style: { text: 'p<0.0001', fontSize: 10 } },
      { type: 'text', left: '50%', top: '22%', style: { text: 'p>0.999', fontSize: 10 } },
      { type: 'text', left: '78%', top: '22%', style: { text: 'p<0.0001', fontSize: 10 } },
    ]
  });

  // 图 3C: 转诊效率复合图
  const eff = echarts.init(efficiencyChart.value);
  eff.setOption({
    title: { text: '转诊效率', left: 'center', textStyle: { fontSize: 14, fontWeight: 'normal' } },
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
    legend: { data: ['DL model-only', 'Senior cytopathologist (average)', 'NNR'], top: 30, textStyle: { fontSize: 10 } },
    grid: { left: '15%', right: '15%', bottom: '10%', top: '30%' }, 
    xAxis: { type: 'category', data: ['DL model-only', 'Senior cytopathologist'], axisLabel: { interval: 0, rotate: 0 } },
    yAxis: [
      { type: 'value', name: 'Colposcopy referral', min: 0, max: 0.2, position: 'left' },
      { type: 'value', name: 'NNR', min: 0, max: 16, position: 'right' }
    ],
    series: [
      { name: 'DL model-only', type: 'bar', stack: 'total', data: [0.179, null], itemStyle: { color: '#95B9A6' } },
      { name: 'Senior cytopathologist (average)', type: 'bar', stack: 'total', data: [null, 0.109], itemStyle: { color: '#F8E39A' } },
      { name: 'NNR', type: 'line', yAxisIndex: 1, smooth: true, symbol: 'circle', symbolSize: 8, data: [14.900, 9.371], lineStyle: { color: '#555', type: 'dashed' }, itemStyle: { color: '#555' } }
    ],
    graphic: [
      { type: 'text', left: '48%', top: '22%', style: { text: 'p<0.0001', fontSize: 10 } },
    ]
  });

  window.addEventListener('resize', () => {
    roc.resize();
    perf.resize();
    eff.resize();
  });
};

onMounted(() => {
  setTimeout(() => {
    loading.value = false;
    nextTick(initCharts);
  }, 500);
});
</script>

<style scoped>
.evaluation-card {
  border-radius: 4px;
}
</style>