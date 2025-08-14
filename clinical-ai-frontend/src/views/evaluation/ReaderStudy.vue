<template>
  <el-card v-loading="loading" class="evaluation-card">
    <template #header>
      <span>多读者多案例研究</span>
    </template>
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="DL vs 医生" name="vs">
        <el-row :gutter="20">
          <el-col :span="12"><div ref="vsJuniorChart" style="height: 450px;"></div></el-col>
          <el-col :span="12"><div ref="vsSeniorChart" style="height: 450px;"></div></el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="DL辅助性能提升" name="improvement">
        <div ref="improvementChart" style="height: 500px;"></div>
      </el-tab-pane>
      <el-tab-pane label="ROC曲线对比" name="roc">
        <div ref="rocChart" style="height: 500px;"></div>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';

const loading = ref(true);
const activeTab = ref('vs');
const vsJuniorChart = ref(null);
const vsSeniorChart = ref(null);
const improvementChart = ref(null);
const rocChart = ref(null);

let chartsInitialized = { vs: false, improvement: false, roc: false };

// --- 为图例定义精确的SVG路径，防止拉伸 ---
const icons = {
  circle: 'path://M512 85.333a426.667 426.667 0 1 0 0 853.334 426.667 426.667 0 0 0 0-853.334z',
  rect: 'path://M128 128h768v768H128z',
  diamond: 'path://M512 29.867L955.733 473.6l-443.733 443.734L68.267 473.6z',
  triangle: 'path://M512 85.333L66.987 896h890.026z',
};

// --- 数据模拟 ---
const juniorData = Array(16).fill(0).map(() => ({
  withoutAI: { spec: 0.746 + (Math.random() - 0.5) * 0.15, sens: 0.719 + (Math.random() - 0.5) * 0.2 },
  withAI: { spec: 0.815 + (Math.random() - 0.5) * 0.1, sens: 0.858 + (Math.random() - 0.5) * 0.1 }
}));
const seniorData = Array(12).fill(0).map(() => ({
  withoutAI: { spec: 0.888 + (Math.random() - 0.5) * 0.1, sens: 0.854 + (Math.random() - 0.5) * 0.1 },
  withAI: { spec: 0.903 + (Math.random() - 0.5) * 0.08, sens: 0.897 + (Math.random() - 0.5) * 0.08 }
}));

// --- ROC曲线生成函数 ---
function generateROCData(auc, seedSource) {
  let seed = 0;
  for (let i = 0; i < seedSource.length; i++) {
    seed += seedSource.charCodeAt(i) * (i + 1);
  }
  const random = () => {
    seed = (seed * 9301 + 49297) % 233280;
    return seed / 233280;
  };
  const data = [[1, 0]];
  let currentSpec = 1;
  let currentSens = 0;
  const curveType = seed % 3;
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
  const midSteps = 15 + Math.floor(random() * 10);
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

const initVsCharts = () => {
  const commonVsOption = {
    title: { left: 'center', textStyle: { fontSize: 14, fontWeight: 'normal' } },
    tooltip: { trigger: 'item' },
    legend: {
      top: 40,
      textStyle: { fontSize: 10 },
    },
    xAxis: { name: 'Specificity', inverse: true, nameTextStyle: { fontWeight: 'bold' } },
    yAxis: { name: 'Sensitivity', nameTextStyle: { fontWeight: 'bold' } },
    grid: { left: 60, right: 40, top: 100, bottom: 40 },
  };

  const juniorChart = echarts.init(vsJuniorChart.value);
  juniorChart.setOption({
    ...commonVsOption,
    title: { ...commonVsOption.title, text: 'DL vs. 初级医生' },
    xAxis: { ...commonVsOption.xAxis, min: 0.65, max: 1.0 },
    yAxis: { ...commonVsOption.yAxis, min: 0.6, max: 1.0 },
    legend: {
      ...commonVsOption.legend,
      data: [
        { name: 'DL model-only AUC=0.836', icon: icons.diamond },
        { name: 'Junior (individual)', icon: icons.circle },
        { name: 'Junior (average) AUC=0.733', icon: icons.rect }
      ]
    },
    series: [
      { name: 'DL model-only AUC=0.836', type: 'scatter', symbol: 'diamond', symbolSize: 12, data: [[0.822, 0.850]], itemStyle: { color: '#A9535F' } },
      { name: 'Junior (individual)', type: 'scatter', symbol: 'circle', symbolSize: 8, data: juniorData.map(d => [d.withoutAI.spec, d.withoutAI.sens]), itemStyle: { color: '#728AB7' } },
      { name: 'Junior (average) AUC=0.733', type: 'scatter', symbol: 'rect', symbolSize: 12, data: [[0.746, 0.719]], itemStyle: { color: '#456793' } }
    ]
  });

  const seniorChart = echarts.init(vsSeniorChart.value);
  seniorChart.setOption({
    ...commonVsOption,
    title: { ...commonVsOption.title, text: 'DL vs. 高级医生' },
     xAxis: { ...commonVsOption.xAxis, min: 0.75, max: 1.0 },
    yAxis: { ...commonVsOption.yAxis, min: 0.75, max: 1.0 },
    legend: {
       ...commonVsOption.legend,
      data: [
        { name: 'DL model-only AUC=0.851', icon: icons.diamond },
        { name: 'Senior (individual)', icon: icons.circle },
        { name: 'Senior (average) AUC=0.871', icon: icons.rect }
      ]
    },
    series: [
      { name: 'DL model-only AUC=0.851', type: 'scatter', symbol: 'diamond', symbolSize: 12, data: [[0.834, 0.867]], itemStyle: { color: '#A9535F' } },
      { name: 'Senior (individual)', type: 'scatter', symbol: 'circle', symbolSize: 8, data: seniorData.map(d => [d.withoutAI.spec, d.withoutAI.sens]), itemStyle: { color: '#728AB7' } },
      { name: 'Senior (average) AUC=0.871', type: 'scatter', symbol: 'rect', symbolSize: 12, data: [[0.888, 0.854]], itemStyle: { color: '#456793' } }
    ]
  });
};

const initImprovementChart = () => {
  const chart = echarts.init(improvementChart.value);
  const allData = [...juniorData, ...seniorData];
  chart.setOption({
    title: { text: 'DL辅助对医生诊断性能的影响', left: 'center', textStyle: { fontWeight: 'normal' } },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: {
        top: 40,
        data: [
            { name: '无AI辅助', icon: icons.circle },
            { name: '有AI辅助', icon: icons.triangle }
        ]
    },
    grid: { left: 60, right: 40, top: 100, bottom: 40 },
    xAxis: { type: 'category', data: allData.map((_, i) => i < 16 ? `J${i+1}` : `S${i-15}`), name: '医生编号' },
    yAxis: { name: '敏感性', min: 0.6, max: 1.0 },
    series: [
      { name: '无AI辅助', type: 'scatter', symbol: 'circle', symbolSize: 8, data: allData.map(d => d.withoutAI.sens), itemStyle: { color: '#728AB7' } },
      { name: '有AI辅助', type: 'scatter', symbol: 'triangle', symbolSize: 8, data: allData.map(d => d.withAI.sens), itemStyle: { color: '#E88F5D' } },
    ]
  });
};

const initRocChart = () => {
  const chart = echarts.init(rocChart.value);
  
  const legendAndSeriesNames = {
    dlModel: 'DL Model (AUC 0.850)',
    juniorAvgNoDl: 'Junior w/o DL (Avg AUC 0.733)',
    juniorAvgDl: 'Junior w/ DL (Avg AUC 0.841)',
    seniorAvgNoDl: 'Senior w/o DL (Avg AUC 0.871)',
    seniorAvgDl: 'Senior w/ DL (Avg AUC 0.885)',
    juniorIndNoDl: 'Junior w/o DL (Ind.)',
    juniorIndDl: 'Junior w/ DL (Ind.)',
    seniorIndNoDl: 'Senior w/o DL (Ind.)',
    seniorIndDl: 'Senior w/ DL (Ind.)'
  };

  chart.setOption({
    title: { text: '各组平均ROC曲线与个体性能分布', left: 'center', textStyle: { fontWeight: 'normal' } },
    tooltip: { trigger: 'axis' },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      type: 'scroll',
      textStyle: { fontSize: 10 },
      data: [
          { name: legendAndSeriesNames.dlModel },
          { name: legendAndSeriesNames.juniorAvgNoDl },
          { name: legendAndSeriesNames.juniorAvgDl },
          { name: legendAndSeriesNames.seniorAvgNoDl },
          { name: legendAndSeriesNames.seniorAvgDl },
          { name: legendAndSeriesNames.juniorIndNoDl, icon: icons.circle },
          { name: legendAndSeriesNames.juniorIndDl, icon: icons.circle },
          { name: legendAndSeriesNames.seniorIndNoDl, icon: icons.rect },
          { name: legendAndSeriesNames.seniorIndDl, icon: icons.rect }
      ],
    },
    xAxis: { name: 'Specificity', min: 0, max: 1, inverse: true, nameTextStyle: { fontWeight: 'bold' } },
    yAxis: { name: 'Sensitivity', min: 0, max: 1, nameTextStyle: { fontWeight: 'bold' } },
    grid: { left: 60, right: 220, top: 80, bottom: 40 },
    series: [
      { name: legendAndSeriesNames.dlModel, type: 'line', step: 'end', showSymbol: false, lineStyle: { width: 1.5 }, data: generateROCData(0.850, 'DL-model'), itemStyle: { color: '#A8535F' } },
      { name: legendAndSeriesNames.juniorAvgNoDl, type: 'line', step: 'end', showSymbol: false, lineStyle: { width: 1.5 }, data: generateROCData(0.733, 'Junior-no-DL'), itemStyle: { color: '#4D71A7' } },
      { name: legendAndSeriesNames.juniorAvgDl, type: 'line', step: 'end', showSymbol: false, lineStyle: { width: 1.5 }, data: generateROCData(0.841, 'Junior-with-DL'), itemStyle: { color: '#E2703B' } },
      { name: legendAndSeriesNames.seniorAvgNoDl, type: 'line', step: 'end', showSymbol: false, lineStyle: { width: 1.5 }, data: generateROCData(0.871, 'Senior-no-DL'), itemStyle: { color: '#5A945A' } },
      { name: legendAndSeriesNames.seniorAvgDl, type: 'line', step: 'end', showSymbol: false, lineStyle: { width: 1.5 }, data: generateROCData(0.885, 'Senior-with-DL'), itemStyle: { color: '#8A6EB5' } },
      
      { name: legendAndSeriesNames.juniorIndNoDl, type: 'scatter', symbol: 'circle', symbolSize: 6, data: juniorData.map(d => [d.withoutAI.spec, d.withoutAI.sens]), itemStyle: { color: 'rgba(114, 138, 183, 0.7)' } },
      { name: legendAndSeriesNames.juniorIndDl, type: 'scatter', symbol: 'circle', symbolSize: 6, data: juniorData.map(d => [d.withAI.spec, d.withAI.sens]), itemStyle: { color: 'rgba(232, 143, 93, 0.7)' } },
      { name: legendAndSeriesNames.seniorIndNoDl, type: 'scatter', symbol: 'rect', symbolSize: 6, data: seniorData.map(d => [d.withoutAI.spec, d.withoutAI.sens]), itemStyle: { color: 'rgba(139, 195, 74, 0.7)' } },
      { name: legendAndSeriesNames.seniorIndDl, type: 'scatter', symbol: 'rect', symbolSize: 6, data: seniorData.map(d => [d.withAI.spec, d.withAI.sens]), itemStyle: { color: 'rgba(179, 157, 219, 0.7)' } }
    ]
  });
};

const handleTabChange = (tabName) => {
  nextTick(() => {
    if (tabName === 'vs') {
      if (!chartsInitialized.vs) { initVsCharts(); chartsInitialized.vs = true; }
      echarts.getInstanceByDom(vsJuniorChart.value)?.resize();
      echarts.getInstanceByDom(vsSeniorChart.value)?.resize();
    }
    if (tabName === 'improvement') {
      if (!chartsInitialized.improvement) { initImprovementChart(); chartsInitialized.improvement = true; }
      echarts.getInstanceByDom(improvementChart.value)?.resize();
    }
    if (tabName === 'roc') {
      if (!chartsInitialized.roc) { initRocChart(); chartsInitialized.roc = true; }
      echarts.getInstanceByDom(rocChart.value)?.resize();
    }
  });
};

onMounted(() => {
  setTimeout(() => {
    loading.value = false;
    nextTick(() => {
      initVsCharts();
      chartsInitialized.vs = true;
    });
  }, 500);
});
</script>

<style scoped>
.evaluation-card {
  border-radius: 4px;
}
</style>