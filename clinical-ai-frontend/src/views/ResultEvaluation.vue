<template>
  <div class="result-evaluation-container">
    <el-card class="evaluation-wrapper" shadow="never">
      
      <div class="header-content">
        <h1>深度学习辅助宫颈细胞学检测结果评估</h1>
        <p class="description">
          基于17,397例训练样本和10,826例测试样本的多中心验证结果分析，展示深度学习模型在宫颈癌前病变及癌症检测中的性能表现
        </p>
      </div>

      <el-tabs v-model="activeTab" class="evaluation-tabs" @tab-change="handleTabChange">
        <el-tab-pane 
          v-for="tab in tabList"
          :key="tab.name"
          :label="tab.label"
          :name="tab.name">
        </el-tab-pane>
      </el-tabs>

      <div class="view-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>

    </el-card>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

// 优化4: 将 Tab 数据抽离成数组，便于维护
const tabList = ref([
  { label: '多机构验证', name: 'multi-institution' },
  { label: '多读者研究', name: 'reader-study' },
  { label: '社区筛查应用', name: 'community-screening' },
  { label: '医院筛查应用', name: 'hospital-screening' },
  { label: '效率分析', name: 'efficiency-analysis' },
]);

const activeTab = ref(tabList.value[0].name); // 默认选中第一个
const route = useRoute();
const router = useRouter();

// 计算有效的 tab 名字列表，用于路由监听
const validTabNames = computed(() => tabList.value.map(tab => tab.name));

// 监听路由变化，并用它来更新当前激活的标签页
watch(
  () => route.path,
  (newPath) => {
    const currentTab = newPath.split('/').pop();
    if (validTabNames.value.includes(currentTab)) {
      activeTab.value = currentTab;
    }
  },
  { immediate: true }
);

// 当用户点击标签页时，导航到对应的路由
const handleTabChange = (tabName) => {
  router.push(`/result-evaluation/${tabName}`);
};
</script>

<style scoped>
.result-evaluation-container {
  padding: 20px;
  background-color: #f7f8fa; /* 使用一个更柔和的背景灰 */
}

/* 统一的容器卡片样式 */
.evaluation-wrapper {
  border: none;
  border-radius: 8px; /* 增加圆角，使其更柔和 */
}

/* 头部内容区样式 */
.header-content {
  padding: 10px 20px 20px; /* 增加内边距 */
  display: flex;
  flex-direction: column;
  gap: 12px; /* 标题和描述之间的间距 */
}

.header-content h1 {
  font-size: 26px;
  font-weight: 600; /* 略微加粗 */
  color: #1d2129;
  margin: 0; /* 重置默认 margin */
}

.description {
  font-size: 15px;
  color: #5a6472;
  line-height: 1.7;
  max-width: 1000px;
  margin: 0;
}

/* Tabs 样式定制 */
.evaluation-tabs {
  margin: 0 20px; /* 左右留出内边距 */
}
/* 移除 Tabs 导航条底部的默认边框线，让界面更干净 */
:deep(.el-tabs__nav-wrap::after) {
  display: none;
}

/* 路由视图容器样式 */
.view-content {
  padding: 24px 20px;
  /* 使用一个柔和的顶部边框来分隔 Tabs 和内容 */
  border-top: 1px solid var(--el-border-color-light);
}

/* 切换动画：淡入+向上轻微滑动 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>