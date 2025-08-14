<template>
  <el-card v-loading="loading" class="evaluation-card">
    <template #header>
      <span>诊断效率分析</span>
    </template>
    
    <div ref="chartContainer" style="height: 600px;"></div>

    <el-descriptions :column="2" border style="margin-top: 0;" :header-cell-style="tableHeaderStyle" :cell-style="tableRowStyle">
      <el-descriptions-item label="平均阅读时间(无AI)">218秒/例</el-descriptions-item>
      <el-descriptions-item label="平均阅读时间(有AI)">30秒/例</el-descriptions-item>
      <el-descriptions-item label="时间缩短比例">86.2%</el-descriptions-item>
      <el-descriptions-item label="统计显著性">p &lt; 0.0001</el-descriptions-item>
    </el-descriptions>
  </el-card>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';

const loading = ref(true);
const chartContainer = ref(null);
const tableHeaderStyle = { background: '#DEDCCB', color: '#000', fontWeight: 'bold' };
const tableRowStyle = { background: '#FBFAF7' };

const initChart = () => {
  const chart = echarts.init(chartContainer.value);
  
  const withoutCamsData = [
    [158, 198, 218, 248, 288], // 全体
    [175, 215, 245, 285, 325], // 初级
    [130, 160, 180, 200, 230]  // 高级
  ];
  const withCamsData = [
    [25, 35, 45, 65, 85],   // 全体
    [30, 40, 55, 75, 95],   // 初级
    [20, 30, 40, 55, 70]    // 高级
  ];

  const option = {
    title: { 
      text: 'AI辅助前后阅读时间对比', 
      left: 'center', 
      textStyle: { fontWeight: 'normal' },
      top: 10
    },
    tooltip: { 
      trigger: 'item', 
      axisPointer: { type: 'shadow' },
      // --- 修正点: 将字符串模板改为回调函数 ---
      formatter: (params) => {
        // params.value 就是箱线图的数据数组，例如 [158, 198, 218, 248, 288]
        const data = params.value;
        const seriesName = params.seriesName;

        // 使用模板字符串构建HTML内容
        return `
          ${seriesName}<br/>
          最小值: ${data[0]}s<br/>
          下四分位: ${data[1]}s<br/>
          中位数: ${data[2]}s<br/>
          上四分位: ${data[3]}s<br/>
          最大值: ${data[4]}s
        `;
      }
    },
    legend: {
      data: [
        {
          name: 'Without CAMS',
          itemStyle: { color: '#4B6A96' }
        },
        {
          name: 'With CAMS',
          itemStyle: { color: '#CE6C3F' }
        }
      ],
      top: 40,
      itemGap: 30,
    },
    grid: { 
      left: '10%', 
      right: '10%', 
      bottom: '15%', 
      top: '25%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['All cytopathologists', 'Junior cytopathologists', 'Senior cytopathologists'],
      axisLabel: {
        interval: 0,
        rotate: 0
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: '#666666',
          type: 'dashed'
        }
      }
    },
    yAxis: { 
      type: 'value', 
      name: 'Time (s)', 
      max: 350,
      nameTextStyle: { fontWeight: 'bold' },
      interval: 50
    },
    series: [
      { 
        name: 'Without CAMS', 
        type: 'boxplot', 
        data: withoutCamsData,
        boxWidth: [20, 40],
        itemStyle: {
          color: '#4B6A96',
          borderColor: '#666666',
          borderWidth: 1.5
        }
      },
      { 
        name: 'With CAMS', 
        type: 'boxplot', 
        data: withCamsData,
        boxWidth: [20, 40],
        itemStyle: {
          color: '#CE6C3F',
          borderColor: '#666666',
          borderWidth: 1.5
        }
      }
    ],
    graphic: [
      { type: 'text', left: '26%', top: '18%', style: { text: 'p<0.0001', textAlign: 'center', fontSize: 12 } },
      { type: 'text', left: '50%', top: '18%', style: { text: 'p<0.0001', textAlign: 'center', fontSize: 12 } },
      { type: 'text', left: '74%', top: '18%', style: { text: 'p<0.0001', textAlign: 'center', fontSize: 12 } },
    ]
  };
  chart.setOption(option);

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
.evaluation-card {
  border-radius: 4px;
}
</style>