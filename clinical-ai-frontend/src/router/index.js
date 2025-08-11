// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import BaseLayout from '../layouts/BaseLayout.vue'

// --- 修改点 1: 确保 NeuralNetworkModel 组件被正确导入 ---
import NeuralNetworkModel from '../views/ai/NeuralNetworkModel.vue'

// 为所有其他页面创建一个简单的 "开发中" 占位组件引用
const ComingSoon = () => import('../views/ComingSoon.vue')

const routes = [
  {
    path: '/',
    component: BaseLayout,
    redirect: '/system/intro',
    children: [
      // 登录系统
      { path: 'system/login', name: 'Login', component: ComingSoon, meta: { parentTitle: '登录系统', title: '登录界面' } },
      { path: 'system/intro', name: 'SoftwareIntro', component: () => import('../views/Dashboard.vue'), meta: { parentTitle: '登录系统', title: '软件介绍' } },

      // 样本量计算
      { path: 'sample-size-calculation', name: 'SampleSizeCalculation', component: ComingSoon, meta: { parentTitle: '样本量计算', title: '样本量计算' } },

      // 数据清洗
      { path: 'data-cleaning/missing-value', name: 'MissingValue', component: ComingSoon, meta: { parentTitle: '数据清洗', title: '缺失值处理' } },
      { path: 'data-cleaning/psm', name: 'PSM', component: ComingSoon, meta: { parentTitle: '数据清洗', title: '倾向性评分' } },
      { path: 'data-cleaning/random-sampling', name: 'RandomSampling', component: ComingSoon, meta: { parentTitle: '数据清洗', title: '随机对照抽样' } },
      { path: 'data-cleaning/smote', name: 'SMOTE', component: ComingSoon, meta: { parentTitle: '数据清洗', title: 'Smote样本扩增' } },
      { path: 'data-cleaning/cutoff', name: 'Cutoff', component: ComingSoon, meta: { parentTitle: '数据清洗', title: '查找截断值' } },
      { path: 'data-cleaning/rcs', name: 'RCS', component: ComingSoon, meta: { parentTitle: '数据清洗', title: '限制性立方样条RCS' } },
      { path: 'data-cleaning/non-numeric', name: 'NonNumeric', component: ComingSoon, meta: { parentTitle: '数据清洗', title: '非数值列检测' } },

      // 数据准备
      { path: 'data-preparation', name: 'DataPreparation', component: ComingSoon, meta: { parentTitle: '数据准备', title: '数据准备' } },

      // 基线分析
      { path: 'baseline-analysis', name: 'BaselineAnalysis', component: () => import('../views/BaselineAnalysis.vue'), meta: { parentTitle: '基线分析', title: '基线分析' } },

      // 自变量筛选
      { path: 'variable-selection/diff-analysis', name: 'DiffAnalysis', component: ComingSoon, meta: { parentTitle: '自变量筛选', title: '差异性分析' } },
      { path: 'variable-selection/univariate-analysis', name: 'UnivariateAnalysis', component: ComingSoon, meta: { parentTitle: '自变量筛选', title: '单因素分析' } },
      { path: 'variable-selection/lasso', name: 'Lasso', component: ComingSoon, meta: { parentTitle: '自变量筛选', title: 'Lasso法' } },
      { path: 'variable-selection/best-subset', name: 'BestSubset', component: ComingSoon, meta: { parentTitle: '自变量筛选', title: '最优子集法' } },
      { path: 'variable-selection/random-forest', name: 'RandomForest', component: ComingSoon, meta: { parentTitle: '自变量筛选', title: '随机森林法' } },
      { path: 'variable-selection/boruta', name: 'Boruta', component: ComingSoon, meta: { parentTitle: '自变量筛选', title: 'Boruta特征筛选' } },
      { path: 'variable-selection/mrmr', name: 'MRMR', component: ComingSoon, meta: { parentTitle: '自变量筛选', title: '最大相关最小冗余' } },
      { path: 'variable-selection/icc', name: 'ICC', component: ComingSoon, meta: { parentTitle: '自变量筛选', title: '组内相关系数ICC' } },
      { path: 'variable-selection/imaging-features', name: 'ImagingFeatures', component: ComingSoon, meta: { parentTitle: '自变量筛选', title: '影像特征筛选' } },

      // 多因素分析
      { path: 'multivariate-analysis', name: 'MultivariateAnalysis', component: ComingSoon, meta: { parentTitle: '多因素分析', title: '多因素分析' } },

      // 模型评价
      { path: 'model-evaluation/nomogram', name: 'Nomogram', component: () => import('../views/Nomogram.vue'), meta: { parentTitle: '模型评价', title: '列线图' } },
      { path: 'model-evaluation/discrimination', name: 'Discrimination', component: ComingSoon, meta: { parentTitle: '模型评价', title: '区分度分析' } },
      { path: 'model-evaluation/calibration', name: 'Calibration', component: ComingSoon, meta: { parentTitle: '模型评价', title: '校准度分析' } },
      { path: 'model-evaluation/dca', name: 'DCA', component: ComingSoon, meta: { parentTitle: '模型评价', title: '决策曲线分析' } },
      { path: 'model-evaluation/rationality', name: 'Rationality', component: ComingSoon, meta: { parentTitle: '模型评价', title: '合理性分析' } },
      { path: 'model-evaluation/nri-idi', name: 'NriIdi', component: ComingSoon, meta: { parentTitle: '模型评价', title: 'NRI & IDI' } },
      { path: 'model-evaluation/multi-model-comparison', name: 'MultiModelComparison', component: ComingSoon, meta: { parentTitle: '模型评价', title: '多模型比较' } },

      // 交叉验证
      { path: 'cross-validation/simple', name: 'SimpleCV', component: ComingSoon, meta: { parentTitle: '交叉验证', title: '简单交叉验证' } },
      { path: 'cross-validation/k-fold', name: 'KFoldCV', component: ComingSoon, meta: { parentTitle: '交叉验证', title: 'K折交叉验证' } },
      { path: 'cross-validation/leave-one-out', name: 'LeaveOneOutCV', component: ComingSoon, meta: { parentTitle: '交叉验证', title: '留一法交叉验证' } },
      { path: 'cross-validation/bootstrap', name: 'BootstrapCV', component: ComingSoon, meta: { parentTitle: '交叉验证', title: 'Boot自助法' } },

      // AI算法
      // --- 修改点 2: 将下面的路由指向我们创建的组件 ---
      { 
        path: 'ai/neural-network-model', // 使用更符合URL规范的路径
        name: 'NeuralNetworkModel',      // 使用组件名作为路由名
        component: NeuralNetworkModel,  // 将 component 从 ComingSoon 修改为 NeuralNetworkModel
        meta: { parentTitle: 'AI算法', title: '神经网络模型' } 
      },
      { path: 'machine-learning/lightgbm', name: 'LightGBM', component: ComingSoon, meta: { parentTitle: 'AI算法', title: 'LightGBM' } },
      { path: 'machine-learning/catboost', name: 'CatBoost', component: ComingSoon, meta: { parentTitle: 'AI算法', title: 'CatBoost' } },
      { path: 'machine-learning/decision-tree', name: 'DecisionTree', component: ComingSoon, meta: { parentTitle: 'AI算法', title: '决策树' } },
      { path: 'machine-learning/random-forest-ml', name: 'RandomForestML', component: ComingSoon, meta: { parentTitle: 'AI算法', title: '随机森林' } },
      { path: 'machine-learning/svm', name: 'SVM', component: ComingSoon, meta: { parentTitle: 'AI算法', title: 'SVM' } },
      { path: 'machine-learning/knn', name: 'KNN', component: ComingSoon, meta: { parentTitle: 'AI算法', title: 'KNN' } },
      { path: 'machine-learning/ensemble', name: 'Ensemble', component: ComingSoon, meta: { parentTitle: 'AI算法', title: '机器集成' } },

      // 复杂专题
      { path: 'advanced-topics/interaction-model', name: 'InteractionModel', component: ComingSoon, meta: { parentTitle: '复杂专题', title: '交互模型' } },
      { path: 'advanced-topics/multi-dataset', name: 'MultiDataset', component: ComingSoon, meta: { parentTitle: '复杂专题', title: '多数据集验证' } },
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;