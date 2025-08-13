<template>
  <div class="page-container">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="container header-content">
        <div class="logo-container">
          <i class="fa fa-flask logo-icon"></i>
          <div class="logo-text">
            <h1 class="main-title">临床预测模型</h1>
            <p class="version-text">V2.0.2</p>
          </div>
        </div>

        <button v-if="!isAuthenticated" class="login-button" @click="$router.push('/login')">
          登录系统
        </button>
        <div v-else class="user-actions">
          <span class="welcome-text">欢迎, {{ currentUser?.username || '用户' }}</span>
          <button class="logout-button" @click="handleLogout">
            退出登录
          </button>
        </div>

      </div>
    </header>

    <!-- 主横幅 -->
    <section class="hero-section">
      <div class="container hero-content">
        <h2 class="hero-title">临床预测模型分析平台</h2>
        <p class="hero-description">
          一站式医学数据分析与建模解决方案，助力临床研究与决策
        </p>
        <div class="hero-buttons">
          <button class="primary-button" @click="$router.push('/login')">
            立即使用
          </button>
          <button class="secondary-button">
            了解更多
          </button>
        </div>
      </div>
    </section>

    <!-- 软件介绍 -->
    <section class="software-intro">
      <div class="container">
        <h2 class="section-title">软件介绍</h2>
        
        <p class="intro-description">
          临床预测模型V2.0.2是一款专为医学研究人员和临床医生设计的数据分析平台，
          集成了从数据准备到模型构建、评价和验证的全流程功能，帮助用户高效开展临床预测模型研究。
        </p>
        
        <!-- 功能模块 -->
        <div class="features-grid">
          <!-- 数据处理模块 -->
          <div class="feature-card">
            <div class="feature-icon blue-bg">
              <i class="fa fa-database"></i>
            </div>
            <h3 class="feature-title">数据处理</h3>
            <ul class="feature-list">
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>样本量计算</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>数据清洗</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>缺失值处理</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>倾向性评分</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>随机对照抽样</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>Smote样本扩增</span>
              </li>
            </ul>
          </div>
          
          <!-- 特征分析模块 -->
          <div class="feature-card">
            <div class="feature-icon purple-bg">
              <i class="fa fa-search"></i>
            </div>
            <h3 class="feature-title">特征分析</h3>
            <ul class="feature-list">
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>查找截断值</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>限制性立方样条RCS</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>非数值列检测</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>基线分析</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>自变量筛选</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>差异性分析</span>
              </li>
            </ul>
          </div>
          
          <!-- 特征筛选模块 -->
          <div class="feature-card">
            <div class="feature-icon green-bg">
              <i class="fa fa-filter"></i>
            </div>
            <h3 class="feature-title">特征筛选</h3>
            <ul class="feature-list">
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>单因素分析</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>Lasso法</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>最优子集法</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>随机森林法</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>Boruta特征筛选</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>最大相关最小冗余</span>
              </li>
            </ul>
          </div>
          
          <!-- 模型构建模块 -->
          <div class="feature-card">
            <div class="feature-icon orange-bg">
              <i class="fa fa-cogs"></i>
            </div>
            <h3 class="feature-title">模型构建</h3>
            <ul class="feature-list">
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>多因素分析</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>列线图</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>神经网络模型</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>LightGBM & CatBoost</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>决策树 & 随机森林</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>SVM & KNN</span>
              </li>
            </ul>
          </div>
          
          <!-- 模型评价模块 -->
          <div class="feature-card">
            <div class="feature-icon red-bg">
              <i class="fa fa-line-chart"></i>
            </div>
            <h3 class="feature-title">模型评价</h3>
            <ul class="feature-list">
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>区分度分析</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>校准度分析</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>决策曲线分析</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>NRI & IDI</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>多模型比较</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>合理性分析</span>
              </li>
            </ul>
          </div>
          
          <!-- 验证方法模块 -->
          <div class="feature-card">
            <div class="feature-icon teal-bg">
              <i class="fa fa-shield"></i>
            </div>
            <h3 class="feature-title">验证方法</h3>
            <ul class="feature-list">
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>简单交叉验证</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>K折交叉验证</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>留一法交叉验证</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>Boot自助法</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>多数据集验证</span>
              </li>
              <li class="feature-item">
                <i class="fa fa-check text-green"></i>
                <span>机器集成</span>
              </li>
            </ul>
          </div>
        </div>
        
        <!-- 高级功能 -->
        <div class="advanced-features">
          <h3 class="advanced-title">复杂专题功能</h3>
          <div class="advanced-grid">
            <div class="advanced-item">
              <h4 class="advanced-item-title">
                <i class="fa fa-exchange text-blue"></i>
                交互模型
              </h4>
            </div>
            <div class="advanced-item">
              <h4 class="advanced-item-title">
                <i class="fa fa-picture-o text-purple"></i>
                影像特征筛选
              </h4>
            </div>
            <div class="advanced-item">
              <h4 class="advanced-item-title">
                <i class="fa fa-sitemap text-green"></i>
                组内相关系数ICC
              </h4>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 底部区域 -->
    <footer class="footer">
      <div class="container footer-content">
        <div class="footer-left">
          <div class="footer-logo">
            <i class="fa fa-flask footer-icon"></i>
            <span class="footer-title">临床预测模型 V2.0.2</span>
          </div>
          <p class="footer-description">专业的医学数据分析平台</p>
        </div>
        <div class="footer-right">
          <div class="social-links">
            <a href="#" class="social-link">
              <i class="fa fa-question-circle"></i>
            </a>
            <a href="#" class="social-link">
              <i class="fa fa-book"></i>
            </a>
            <a href="#" class="social-link">
              <i class="fa fa-envelope"></i>
            </a>
          </div>
          <p class="copyright">© 2023 临床预测模型软件 版权所有</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

// ## ADDED: 添加完整的脚本逻辑 ##

// 1. 获取 Vuex store 和 router 实例
const store = useStore();
const router = useRouter();

// 2. 创建计算属性，从 Vuex store 中获取登录状态和用户信息
//    'user/isAuthenticated' 和 'user/currentUser' 对应你的 store/modules/user.js 中的 getters
const isAuthenticated = computed(() => store.getters['user/isAuthenticated']);
const currentUser = computed(() => store.getters['user/currentUser']);

// 3. 定义退出登录的处理函数
const handleLogout = () => {
  // 调用 Vuex store 中定义的 logout action
  store.dispatch('user/logout');
};
</script>

<style scoped>
/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

html {
  scroll-behavior: smooth;
}

.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f9fafb;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 顶部导航 */
.header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 16px 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo-icon {
  color: #2563eb;
  font-size: 32px;
  margin-right: 12px;
}

.main-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
}

.version-text {
  font-size: 14px;
  color: #6b7280;
}

.login-button {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.login-button:hover {
  background-color: #1d4ed8;
}

/* 主横幅 */
.hero-section {
  background: linear-gradient(90deg, #2563eb, #1e40af);
  color: white;
  padding: 64px 0;
  text-align: center;
}

.hero-title {
  font-size: 32px;
  margin-bottom: 16px;
  font-weight: 700;
}

@media (min-width: 768px) {
  .hero-title {
    font-size: 40px;
  }
}

.hero-description {
  font-size: 18px;
  max-width: 700px;
  margin: 0 auto 32px;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.primary-button {
  background-color: white;
  color: #1e40af;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.primary-button:hover {
  background-color: #f3f4f6;
}

.secondary-button {
  background-color: transparent;
  color: white;
  border: 2px solid white;
  padding: 10px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.secondary-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* 软件介绍 */
.software-intro {
  padding: 64px 0;
  background-color: white;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  text-align: center;
  margin-bottom: 48px;
}

.intro-description {
  font-size: 18px;
  color: #6b7280;
  line-height: 1.6;
  max-width: 700px;
  margin: 0 auto 64px;
  text-align: center;
}

/* 功能模块网格 */
.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;
  margin-bottom: 64px;
}

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

/* 功能卡片 */
.feature-card {
  background-color: #f9fafb;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #f3f4f6;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  font-size: 24px;
}

.blue-bg {
  background-color: #eff6ff;
  color: #2563eb;
}

.purple-bg {
  background-color: #f5f3ff;
  color: #7c3aed;
}

.green-bg {
  background-color: #ecfdf5;
  color: #10b981;
}

.orange-bg {
  background-color: #fff7ed;
  color: #f97316;
}

.red-bg {
  background-color: #fee2e2;
  color: #ef4444;
}

.teal-bg {
  background-color: #d1fae5;
  color: #059669;
}

.feature-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
}

.feature-list {
  list-style: none;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 8px;
  color: #6b7280;
}

.feature-item i {
  margin-right: 8px;
  margin-top: 4px;
}

.text-green {
  color: #10b981;
}

/* 高级功能 */
.advanced-features {
  background: linear-gradient(90deg, #f9fafb, #f3f4f6);
  border-radius: 12px;
  padding: 32px;
  margin-top: 32px;
}

.advanced-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 24px;
}

.advanced-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 640px) {
  .advanced-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) {
  .advanced-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.advanced-item {
  background-color: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.advanced-item-title {
  font-size: 16px;
  font-weight: 500;
  color: #1f2937;
  display: flex;
  align-items: center;
}

.advanced-item-title i {
  margin-right: 8px;
}

.text-blue {
  color: #2563eb;
}

.text-purple {
  color: #7c3aed;
}

.text-green {
  color: #10b981;
}

/* 底部区域 */
.footer {
  background-color: #1f2937;
  color: white;
  padding: 40px 0;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

@media (min-width: 768px) {
  .footer-content {
    flex-direction: row;
    justify-content: space-between;
  }
}

.footer-left {
  margin-bottom: 24px;
  text-align: center;
}

@media (min-width: 768px) {
  .footer-left {
    margin-bottom: 0;
    text-align: left;
  }
}

.footer-logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (min-width: 768px) {
  .footer-logo {
    justify-content: flex-start;
  }
}

.footer-icon {
  color: #93c5fd;
  font-size: 28px;
  margin-right: 8px;
}

.footer-title {
  font-size: 18px;
  font-weight: 700;
}

.footer-description {
  color: #9ca3af;
  margin-top: 8px;
}

.footer-right {
  text-align: center;
}

@media (min-width: 768px) {
  .footer-right {
    text-align: right;
  }
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 16px;
}

@media (min-width: 768px) {
  .social-links {
    justify-content: flex-end;
  }
}

.social-link {
  color: #9ca3af;
  font-size: 24px;
  transition: color 0.2s ease;
}

.social-link:hover {
  color: white;
}

.copyright {
  color: #9ca3af;
  font-size: 14px;
}

/* 平滑滚动相关 */
section {
  scroll-margin-top: 80px;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.welcome-text {
  font-size: 15px;
  color: #4b5563; /* 深灰色文字 */
  font-weight: 500;
}

.logout-button {
  background-color: transparent;
  color: #6b7280; /* 中灰色文字 */
  border: 1px solid #d1d5db; /* 浅灰色边框 */
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-button:hover {
  color: #1f2937; /* 深色文字 */
  background-color: #f3f4f6; /* 浅灰色背景 */
  border-color: #9ca3af;
}

</style>
    