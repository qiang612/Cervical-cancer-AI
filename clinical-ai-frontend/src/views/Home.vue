<template>
  <div class="h-full flex flex-col">
    <!-- 页面标题 -->
    <div class="p-6 border-b border-gray-200">
      <h1 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-gray-800">临床AI辅助诊断系统</h1>
      <p class="text-gray-600 mt-1">欢迎使用，探索AI辅助诊断的强大功能</p>
    </div>
    
    <!-- 主要内容区 -->
    <div class="flex-1 p-6 overflow-auto">
      <!-- 数据概览卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card title="病例总数" :value="totalCases" icon="fa-file-text-o" color="blue" />
        <Card title="AI诊断准确率" :value="accuracyRate" icon="fa-check-circle-o" color="green" />
        <Card title="今日新增病例" :value="todayCases" icon="fa-plus-circle" color="purple" />
        <Card title="待处理病例" :value="pendingCases" icon="fa-clock-o" color="orange" />
      </div>
      
      <!-- 功能区域 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- 病例管理 -->
        <div class="bg-white rounded-xl shadow p-6 hover:shadow-md transition-shadow border border-gray-100">
          <div class="flex items-center mb-4">
            <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-3">
              <i class="fa fa-stethoscope text-xl"></i>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">病例管理</h3>
          </div>
          <p class="text-gray-600 mb-4">管理、查看和分析所有临床病例数据，支持高级搜索和筛选</p>
          <button @click="$router.push('/cases')" class="text-blue-600 hover:text-blue-800 font-medium flex items-center">
            进入管理 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- AI诊断 -->
        <div class="bg-white rounded-xl shadow p-6 hover:shadow-md transition-shadow border border-gray-100">
          <div class="flex items-center mb-4">
            <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-green-600 mr-3">
              <i class="fa fa-brain text-xl"></i>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">AI辅助诊断</h3>
          </div>
          <p class="text-gray-600 mb-4">上传病例数据，获取AI辅助诊断结果和专业建议</p>
          <button @click="$router.push('/ai-diagnosis')" class="text-green-600 hover:text-green-800 font-medium flex items-center">
            开始诊断 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- 数据分析 -->
        <div class="bg-white rounded-xl shadow p-6 hover:shadow-md transition-shadow border border-gray-100">
          <div class="flex items-center mb-4">
            <div class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 mr-3">
              <i class="fa fa-bar-chart text-xl"></i>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">数据分析</h3>
          </div>
          <p class="text-gray-600 mb-4">查看诊断数据统计和趋势分析，辅助临床决策</p>
          <button @click="$router.push('/analytics')" class="text-purple-600 hover:text-purple-800 font-medium flex items-center">
            查看分析 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- 系统设置 -->
        <div class="bg-white rounded-xl shadow p-6 hover:shadow-md transition-shadow border border-gray-100">
          <div class="flex items-center mb-4">
            <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-600 mr-3">
              <i class="fa fa-cog text-xl"></i>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">系统设置</h3>
          </div>
          <p class="text-gray-600 mb-4">管理系统参数、用户权限和诊断模型配置</p>
          <button @click="$router.push('/settings')" class="text-gray-600 hover:text-gray-800 font-medium flex items-center">
            进入设置 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- 诊断历史 -->
        <div class="bg-white rounded-xl shadow p-6 hover:shadow-md transition-shadow border border-gray-100">
          <div class="flex items-center mb-4">
            <div class="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 mr-3">
              <i class="fa fa-history text-xl"></i>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">诊断历史</h3>
          </div>
          <p class="text-gray-600 mb-4">查看和管理所有历史诊断记录，支持导出和分享</p>
          <button @click="$router.push('/history')" class="text-orange-600 hover:text-orange-800 font-medium flex items-center">
            查看历史 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- 帮助中心 -->
        <div class="bg-white rounded-xl shadow p-6 hover:shadow-md transition-shadow border border-gray-100">
          <div class="flex items-center mb-4">
            <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center text-red-600 mr-3">
              <i class="fa fa-question-circle text-xl"></i>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">帮助中心</h3>
          </div>
          <p class="text-gray-600 mb-4">查看系统使用指南、常见问题和视频教程</p>
          <button @click="$router.push('/help')" class="text-red-600 hover:text-red-800 font-medium flex items-center">
            获取帮助 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Card from '../components/Card.vue'; // 假设已存在此组件

// 模拟数据
const totalCases = ref('12,458');
const accuracyRate = ref('97.3%');
const todayCases = ref('42');
const pendingCases = ref('8');
</script>
