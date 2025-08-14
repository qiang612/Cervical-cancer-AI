<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>软件介绍</span>
      </div>
    </template>
    <div class="welcome-content">
      <h2>欢迎使用临床预测模型数据分析软件</h2>
      <el-divider />
      <p>
        临床预测模型数据分析软件是一款专为医疗健康领域医护、研究人员和学生设计的高效的人工智能大数据分析软件,它极大地简化了复杂的数据分析流程,您无需具备专业的语言编程知识,仅需通过直观的图形界面操作,点击几次鼠标,就能轻松完成临床预测模型的构建与验证,助您快速发文。 
      </p>
    </div>
  </el-card>
</template>

<style scoped>
.box-card {
  height: 100%;
}
.welcome-content {
  line-height: 1.8;
  font-size: 16px;
  color: #606266;
}
.welcome-content h2 {
  text-align: center;
  color: #303133;
  font-weight: 600;
}
</style>