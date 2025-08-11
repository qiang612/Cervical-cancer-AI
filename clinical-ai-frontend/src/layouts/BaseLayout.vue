<template>
  <el-container class="layout-container">
    <el-aside width="240px" class="sidebar">
      <div class="logo-container">
        <h1 class="logo-title">临床预测模型 V2.0.2</h1>
      </div>

      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        router
        background-color="#222D32"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-sub-menu index="/system">
          <template #title>
            <el-icon><Monitor /></el-icon>
            <span>登录系统</span>
          </template>
          <el-menu-item index="/system/login">
            <el-icon><DArrowRight /></el-icon>
            <span>登录界面</span>
          </el-menu-item>
          <el-menu-item index="/system/intro">
            <el-icon><DArrowRight /></el-icon>
            <span>软件介绍</span>
          </el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/sample-size-calculation">
          <el-icon><DataAnalysis /></el-icon> <span>样本量计算</span>
        </el-menu-item>

        <el-sub-menu index="/data-cleaning">
          <template #title>
            <el-icon><Filter /></el-icon>
            <span>数据清洗</span>
          </template>
          <el-menu-item index="/data-cleaning/missing-value"><el-icon><DArrowRight /></el-icon>缺失值处理</el-menu-item>
          <el-menu-item index="/data-cleaning/psm"><el-icon><DArrowRight /></el-icon>倾向性评分</el-menu-item>
          <el-menu-item index="/data-cleaning/random-sampling"><el-icon><DArrowRight /></el-icon>随机对照抽样</el-menu-item>
          <el-menu-item index="/data-cleaning/smote"><el-icon><DArrowRight /></el-icon>Smote样本扩增</el-menu-item>
          <el-menu-item index="/data-cleaning/cutoff"><el-icon><DArrowRight /></el-icon>查找截断值</el-menu-item>
          <el-menu-item index="/data-cleaning/rcs"><el-icon><DArrowRight /></el-icon>限制性立方样条RCS</el-menu-item>
          <el-menu-item index="/data-cleaning/non-numeric"><el-icon><DArrowRight /></el-icon>非数值列检测</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/data-preparation">
          <el-icon><DocumentChecked /></el-icon>
          <span>数据准备</span>
        </el-menu-item>

        <el-menu-item index="/baseline-analysis">
          <el-icon><Grid /></el-icon>
          <span>基线分析</span>
        </el-menu-item>

        <el-sub-menu index="/variable-selection">
          <template #title>
            <el-icon><MagicStick /></el-icon>
            <span>自变量筛选</span>
          </template>
           <el-menu-item index="/variable-selection/diff-analysis"><el-icon><DArrowRight /></el-icon>差异性分析</el-menu-item>
           <el-menu-item index="/variable-selection/univariate-analysis"><el-icon><DArrowRight /></el-icon>单因素分析</el-menu-item>
           <el-menu-item index="/variable-selection/lasso"><el-icon><DArrowRight /></el-icon>Lasso法</el-menu-item>
           <el-menu-item index="/variable-selection/best-subset"><el-icon><DArrowRight /></el-icon>最优子集法</el-menu-item>
           <el-menu-item index="/variable-selection/random-forest"><el-icon><DArrowRight /></el-icon>随机森林法</el-menu-item>
           <el-menu-item index="/variable-selection/boruta"><el-icon><DArrowRight /></el-icon>Boruta特征筛选</el-menu-item>
           <el-menu-item index="/variable-selection/mrmr"><el-icon><DArrowRight /></el-icon>最大相关最小冗余</el-menu-item>
           <el-menu-item index="/variable-selection/icc"><el-icon><DArrowRight /></el-icon>组内相关系数ICC</el-menu-item>
           <el-menu-item index="/variable-selection/imaging-features"><el-icon><DArrowRight /></el-icon>影像特征筛选</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/multivariate-analysis">
          <el-icon><DataLine /></el-icon>
          <span>多因素分析</span>
        </el-menu-item>

        <el-sub-menu index="/model-evaluation">
          <template #title>
            <el-icon><Trophy /></el-icon>
            <span>模型评价</span>
          </template>
          <el-menu-item index="/model-evaluation/nomogram"><el-icon><DArrowRight /></el-icon>列线图</el-menu-item>
          <el-menu-item index="/model-evaluation/discrimination"><el-icon><DArrowRight /></el-icon>区分度分析</el-menu-item>
          <el-menu-item index="/model-evaluation/calibration"><el-icon><DArrowRight /></el-icon>校准度分析</el-menu-item>
          <el-menu-item index="/model-evaluation/dca"><el-icon><DArrowRight /></el-icon>决策曲线分析</el-menu-item>
          <el-menu-item index="/model-evaluation/rationality"><el-icon><DArrowRight /></el-icon>合理性分析</el-menu-item>
          <el-menu-item index="/model-evaluation/nri-idi"><el-icon><DArrowRight /></el-icon>NRI & IDI</el-menu-item>
          <el-menu-item index="/model-evaluation/multi-model-comparison"><el-icon><DArrowRight /></el-icon>多模型比较</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="/cross-validation">
          <template #title>
            <el-icon><Refresh /></el-icon>
            <span>交叉验证</span>
          </template>
          <el-menu-item index="/cross-validation/simple"><el-icon><DArrowRight /></el-icon>简单交叉验证</el-menu-item>
          <el-menu-item index="/cross-validation/k-fold"><el-icon><DArrowRight /></el-icon>K折交叉验证</el-menu-item>
          <el-menu-item index="/cross-validation/leave-one-out"><el-icon><DArrowRight /></el-icon>留一法交叉验证</el-menu-item>
          <el-menu-item index="/cross-validation/bootstrap"><el-icon><DArrowRight /></el-icon>Boot自助法</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="/machine-learning">
          <template #title>
            <el-icon><Cpu /></el-icon>
            <span>AI算法</span>
          </template>
          <el-menu-item index="/machine-learning/神经网络模型"><el-icon><DArrowRight /></el-icon>神经网络模型</el-menu-item>
          <el-menu-item index="/machine-learning/lightgbm"><el-icon><DArrowRight /></el-icon>LightGBM</el-menu-item>
          <el-menu-item index="/machine-learning/catboost"><el-icon><DArrowRight /></el-icon>CatBoost</el-menu-item>
          <el-menu-item index="/machine-learning/decision-tree"><el-icon><DArrowRight /></el-icon>决策树</el-menu-item>
          <el-menu-item index="/machine-learning/random-forest-ml"><el-icon><DArrowRight /></el-icon>随机森林</el-menu-item>
          <el-menu-item index="/machine-learning/svm"><el-icon><DArrowRight /></el-icon>SVM</el-menu-item>
          <el-menu-item index="/machine-learning/knn"><el-icon><DArrowRight /></el-icon>KNN</el-menu-item>
          <el-menu-item index="/machine-learning/ensemble"><el-icon><DArrowRight /></el-icon>机器集成</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="/advanced-topics">
          <template #title>
            <el-icon><Collection /></el-icon>
            <span>复杂专题</span>
          </template>
          <el-menu-item index="/advanced-topics/interaction-model"><el-icon><DArrowRight /></el-icon>交互模型</el-menu-item>
          <el-menu-item index="/advanced-topics/multi-dataset"><el-icon><DArrowRight /></el-icon>多数据集验证</el-menu-item>
        </el-sub-menu>
        
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item>{{ $route.meta.parentTitle }}</el-breadcrumb-item>
          <el-breadcrumb-item v-if="$route.meta.title !== $route.meta.parentTitle">{{ $route.meta.title }}</el-breadcrumb-item>
        </el-breadcrumb>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.layout-container {
  height: 100vh;
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif;
}
.sidebar {
  background-color: #222D32;
  transition: width 0.28s;
}
.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
  background-color: #367FA9;
}
.logo-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
}
.el-menu {
  border-right: none;
}
.header {
  background-color: #3A86B2;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #d8dce5;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}
.main-content {
  background-color: #f0f2f5;
  padding: 5px;
  height: calc(100vh - 60px); 
  overflow-y: auto;
}

.el-menu-item.is-active {
  background-color: #001528 !important;
}

:deep(.el-sub-menu__title:hover) {
    background-color: #001528 !important;
}

:deep(.el-breadcrumb__inner) {
  color: #ffffff !important;
}

:deep(.el-breadcrumb__separator) {
  color: #ffffff !important;
}
</style>