<template>
  <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100 hover:shadow-md transition-shadow">
    <div class="flex justify-between items-start">
      <div>
        <p class="text-gray-500 font-medium">{{ title }}</p>
        <h3 class="text-2xl font-bold mt-1 text-gray-800">{{ value }}</h3>
      </div>
      <div :class="`w-10 h-10 rounded-full flex items-center justify-center text-${color}-600 bg-${color}-100`">
        <i :class="`fa ${icon}`"></i>
      </div>
    </div>
    <div class="mt-4 flex items-center text-sm">
      <span class="text-green-500 flex items-center" v-if="trend === 'up'">
        <i class="fa fa-arrow-up mr-1"></i> {{ trendValue }}
      </span>
      <span class="text-red-500 flex items-center" v-if="trend === 'down'">
        <i class="fa fa-arrow-down mr-1"></i> {{ trendValue }}
      </span>
      <span class="text-gray-500" v-if="!trend">较上期持平</span>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

// 定义组件属性
const props = defineProps({
  // 卡片标题
  title: {
    type: String,
    required: true
  },
  // 卡片数值
  value: {
    type: String,
    required: true
  },
  // 图标类名（Font Awesome）
  icon: {
    type: String,
    required: true
  },
  // 颜色主题（blue, green, purple, orange 等）
  color: {
    type: String,
    required: true
  },
  // 趋势方向（up, down 或不提供）
  trend: {
    type: String,
    default: ''
  },
  // 趋势数值
  trendValue: {
    type: String,
    default: ''
  }
});
</script>
