<template>
  <div class="dashboard-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>临床AI辅助诊断系统</h1>
      <p>欢迎使用，探索AI辅助诊断的强大功能</p>
    </div>
    
    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 数据概览卡片 -->
      <div class="stats-container">
        <Card title="病例总数" :value="totalCases" icon="fa-file-text-o" color="blue" />
        <Card title="AI诊断准确率" :value="accuracyRate" icon="fa-check-circle-o" color="green" />
        <Card title="今日新增病例" :value="todayCases" icon="fa-plus-circle" color="purple" />
        <Card title="待处理病例" :value="pendingCases" icon="fa-clock-o" color="orange" />
      </div>
      
      <!-- 功能区域 -->
      <div class="features-grid">
        <!-- 病例管理 -->
        <div class="feature-card">
          <div class="feature-icon blue-bg">
            <i class="fa fa-stethoscope"></i>
          </div>
          <h3>病例管理</h3>
          <p>管理、查看和分析所有临床病例数据，支持高级搜索和筛选</p>
          <button @click="$router.push('/cases')" class="feature-button blue-text">
            进入管理 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- AI诊断 -->
        <div class="feature-card">
          <div class="feature-icon green-bg">
            <i class="fa fa-brain"></i>
          </div>
          <h3>AI辅助诊断</h3>
          <p>上传病例数据，获取AI辅助诊断结果和专业建议</p>
          <button @click="$router.push('/ai-diagnosis')" class="feature-button green-text">
            开始诊断 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- 数据分析 -->
        <div class="feature-card">
          <div class="feature-icon purple-bg">
            <i class="fa fa-bar-chart"></i>
          </div>
          <h3>数据分析</h3>
          <p>查看诊断数据统计和趋势分析，辅助临床决策</p>
          <button @click="$router.push('/analytics')" class="feature-button purple-text">
            查看分析 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- 系统设置 -->
        <div class="feature-card">
          <div class="feature-icon gray-bg">
            <i class="fa fa-cog"></i>
          </div>
          <h3>系统设置</h3>
          <p>管理系统参数、用户权限和诊断模型配置</p>
          <button @click="$router.push('/settings')" class="feature-button gray-text">
            进入设置 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- 诊断历史 -->
        <div class="feature-card">
          <div class="feature-icon orange-bg">
            <i class="fa fa-history"></i>
          </div>
          <h3>诊断历史</h3>
          <p>查看和管理所有历史诊断记录，支持导出和分享</p>
          <button @click="$router.push('/history')" class="feature-button orange-text">
            查看历史 <i class="fa fa-arrow-right ml-2"></i>
          </button>
        </div>
        
        <!-- 帮助中心 -->
        <div class="feature-card">
          <div class="feature-icon red-bg">
            <i class="fa fa-question-circle"></i>
          </div>
          <h3>帮助中心</h3>
          <p>查看系统使用指南、常见问题和视频教程</p>
          <button @click="$router.push('/help')" class="feature-button red-text">
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

<style scoped>
/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 容器样式 */
.dashboard-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

/* 页面标题区域 */
.page-header {
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.page-header h1 {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.page-header p {
  color: #6b7280;
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #f9fafb;
}

/* 数据概览卡片容器 */
.stats-container {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 32px;
}

/* 功能区域网格 */
.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

/* 响应式布局 */
@media (min-width: 768px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* 功能卡片样式 */
.feature-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  padding: 24px;
  border: 1px solid #f3f4f6;
  transition: box-shadow 0.2s ease-in-out;
}

.feature-card:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
}

/* 功能图标样式 */
.feature-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  margin-bottom: 16px;
  font-size: 20px;
}

.blue-bg {
  background-color: #eff6ff;
  color: #2563eb;
}

.green-bg {
  background-color: #ecfdf5;
  color: #10b981;
}

.purple-bg {
  background-color: #f5f3ff;
  color: #7c3aed;
}

.gray-bg {
  background-color: #f3f4f6;
  color: #4b5563;
}

.orange-bg {
  background-color: #fff7ed;
  color: #f97316;
}

.red-bg {
  background-color: #fee2e2;
  color: #ef4444;
}

/* 功能卡片标题 */
.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
}

/* 功能卡片描述 */
.feature-card p {
  color: #6b7280;
  margin-bottom: 16px;
  line-height: 1.5;
}

/* 功能按钮样式 */
.feature-button {
  display: inline-flex;
  align-items: center;
  background: none;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s ease-in-out;
  padding: 0;
}

.blue-text {
  color: #2563eb;
}

.blue-text:hover {
  color: #1d4ed8;
}

.green-text {
  color: #10b981;
}

.green-text:hover {
  color: #059669;
}

.purple-text {
  color: #7c3aed;
}

.purple-text:hover {
  color: #6d28d9;
}

.gray-text {
  color: #4b5563;
}

.gray-text:hover {
  color: #1f2937;
}

.orange-text {
  color: #f97316;
}

.orange-text:hover {
  color: #ea580c;
}

.red-text {
  color: #ef4444;
}

.red-text:hover {
  color: #dc2626;
}
</style>
    