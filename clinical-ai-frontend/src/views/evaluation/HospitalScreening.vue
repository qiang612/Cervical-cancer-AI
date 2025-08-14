<template>
  <el-card v-loading="loading" class="evaluation-card">
    <template #header>
      <span>医院机会性筛查结果</span>
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
  // 图 3D: ROC 曲线
  const roc = echarts.init(rocChart.value);
  roc.setOption({
    title: { text: 'ROC曲线', left: 'center', textStyle: { fontSize: 14, fontWeight: 'normal' } },
    tooltip: {
      trigger: 'axis',
      formatter: params => {
        if (!params || params.length === 0) return '';
        const point = params[0];
        let tooltipText = `Specificity: ${(point.value[0]).toFixed(3)}<br/>`;
        params.forEach(p => {
          if (p.seriesType === 'line') {
              tooltipText += `${p.marker} ${p.seriesName.split(' AUC')[0]}: ${(p.value[1]).toFixed(3)}<br/>`;
          }
        });
        return tooltipText;
      }
    },
    legend: {
      data: [
        'DL model-only AUC=0.836',
        'Junior cytopathologist without DL assistance (average) AUC=0.697',
        'Junior cytopathologist with DL assistance (average) AUC=0.849'
      ],
      bottom: 0,
      type: 'scroll',
      textStyle: { fontSize: 9 }
    },
    // --- 修正点: 调整 grid，为左侧Y轴标签留出空间 ---
    grid: { left: '16%', right: '10%', bottom: '11%', top: '15%' },
    xAxis: {
      type: 'value', min: 0, max: 1, inverse: true,
      // --- 修正点: 移除 name 属性，删除底部标题 ---
      axisLabel: { formatter: (v) => v.toFixed(1) },
    },
    yAxis: {
      // 标准的Y轴: Sensitivity (保持默认样式，从下往上显示)
      type: 'value', name: 'Sensitivity', min: 0, max: 1,
      axisLabel: { formatter: (v) => v.toFixed(1) },
      nameTextStyle: { fontWeight: 'bold' },
    },
    // --- 修正点: 新增 graphic 元素，绘制左侧的 'Specificity' 标题 ---
    graphic: {
      elements: [
        {
          type: 'text',
          left: 15,       // 距离容器左侧的距离
          top: 'center',  // 垂直居中
          style: {
            text: 'Specificity',
            textAlign: 'center',
            fill: '#333',
            fontWeight: 'bold'
          },
          // 旋转90度，使其从下往上阅读
          rotation: Math.PI / 2
        }
      ]
    },
    series: [
      {
        name: 'DL model-only AUC=0.836',
        type: 'line',
        smooth: false, 
        step: 'end',   
        showSymbol: false,
        data: generateROCData(0.836, 30),
        lineStyle: { color: '#B05461' }
      },
      {
        name: 'Junior cytopathologist without DL assistance (average) AUC=0.697',
        type: 'line',
        smooth: false, 
        step: 'end',   
        showSymbol: false,
        data: generateROCData(0.697, 40),
        lineStyle: { color: '#4D76B1' }
      },
      {
        name: 'Junior cytopathologist with DL assistance (average) AUC=0.849',
        type: 'line',
        smooth: false, 
        step: 'end',   
        showSymbol: false,
        data: generateROCData(0.849, 50),
        lineStyle: { color: '#ED733A' }
      },
      {
        name: 'Junior without DL',
        type: 'scatter',
        symbol: 'diamond',
        symbolSize: 10,
        data: [[0.737, 0.657]],
        itemStyle: { color: '#4D76B1' },
        tooltip: { formatter: (params) => `Junior without DL<br/>Specificity: ${params.value[0].toFixed(3)}<br/>Sensitivity: ${params.value[1].toFixed(3)}` }
      },
      {
        name: 'Junior with DL',
        type: 'scatter',
        symbol: 'diamond',
        symbolSize: 10,
        data: [[0.840, 0.857]],
        itemStyle: { color: '#ED733A' },
        tooltip: { formatter: (params) => `Junior with DL<br/>Specificity: ${params.value[0].toFixed(3)}<br/>Sensitivity: ${params.value[1].toFixed(3)}` }
      }
    ]
  });

  // 图 3E: 诊断性能柱状图
  const perf = echarts.init(performanceChart.value);
  perf.setOption({
    title: { text: '诊断性能', left: 'center', textStyle: { fontSize: 14, fontWeight: 'normal' } },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: {
      data: ['DL model-only', 'Junior cytopathologist without DL assistance (average)', 'Junior cytopathologist with DL assistance (average)'],
      top: 30,
      type: 'scroll',
      textStyle: { fontSize: 9 }
    },
    grid: { left: '10%', right: '10%', bottom: '10%', top: '30%' },
    xAxis: { type: 'category', data: ['Accuracy', 'Sensitivity', 'Specificity'] },
    yAxis: { type: 'value', min: 0.6, max: 0.9, name: 'Value' },
    series: [
      { name: 'DL model-only', type: 'bar', data: [0.841, 0.843, 0.830], itemStyle: { color: '#95B9A6' } },
      { name: 'Junior cytopathologist without DL assistance (average)', type: 'bar', data: [0.733, 0.657, 0.737], itemStyle: { color: '#F8E39A' } },
      { name: 'Junior cytopathologist with DL assistance (average)', type: 'bar', data: [0.841, 0.857, 0.840], itemStyle: { color: '#F4B39E' } }
    ],
    graphic: [
      { type: 'text', left: '22%', top: '22%', style: { text: 'p<0.0001', fontSize: 10 } },
      { type: 'text', left: '50%', top: '22%', style: { text: 'p<0.0001', fontSize: 10 } },
      { type: 'text', left: '78%', top: '22%', style: { text: 'p<0.0001', fontSize: 10 } },
    ]
  });

  // 图 3F: 转诊效率复合图
  const eff = echarts.init(efficiencyChart.value);
  eff.setOption({
    title: { text: '转诊效率', left: 'center', textStyle: { fontSize: 14, fontWeight: 'normal' } },
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
    legend: {
      data: [
          'DL model-only',
          'Junior cytopathologist without DL assistance (average)',
          'Junior cytopathologist with DL assistance (average)',
          'NNR'
      ],
      top: 30,
      type: 'scroll',
      textStyle: { fontSize: 9 }
    },
    grid: { left: '15%', right: '15%', bottom: '10%', top: '35%' },
    xAxis: {
      type: 'category',
      data: ['DL\nmodel-only', 'Junior\nwithout DL', 'Junior\nwith DL'],
      axisLabel: {
          interval: 0,
          rotate: 0
      }
    },
    yAxis: [
      { type: 'value', name: 'Colposcopy referral', min: 0, max: 0.35, position: 'left' },
      { type: 'value', name: 'NNR', min: 0, max: 10, position: 'right' }
    ],
    series: [
      {
        name: 'DL model-only',
        type: 'bar',
        stack: 'total',
        data: [0.282, null, null],
        itemStyle: { color: '#95B9A6' }
      },
      {
        name: 'Junior cytopathologist without DL assistance (average)',
        type: 'bar',
        stack: 'total',
        data: [null, 0.302, null],
        itemStyle: { color: '#F8E39A' }
      },
      {
        name: 'Junior cytopathologist with DL assistance (average)',
        type: 'bar',
        stack: 'total',
        data: [null, null, 0.193],
        itemStyle: { color: '#F4B39E' }
      },
      {
        name: 'NNR',
        type: 'line',
        yAxisIndex: 1,
        smooth: false,
        symbol: 'circle',
        symbolSize: 8,
        data: [9.022, 5.051, 4.733],
        lineStyle: { color: '#888', type: 'dashed' },
        itemStyle: { color: '#888' }
      }
    ],
      graphic: [
      { type: 'text', left: '48%', top: '22%', style: { text: 'p<0.0001', fontSize: 10 } },
    ]
  });
  
   // 监听窗口大小变化，重绘图表
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