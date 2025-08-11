<template>
  <div class="page-container">
    <!-- 左右布局容器 -->
    <div class="layout-row">
      <!-- 左侧：患者切片分析 -->
      <div class="section left-section">
        <h2 class="section-title">患者切片分析</h2>
        <div class="content-wrapper">
          <div class="form-group">
            <label class="label" for="patientId">请输入患者编号 (例如: 1-100):</label>
            <div class="input-group">
              <input 
                v-model="patientId"
                type="text" 
                id="patientId" 
                placeholder="例如: 1"
                class="input"
              />
              <button 
                @click="fetchPatientImage"
                class="button"
              >查找切片</button>
            </div>
            <p class="hint">从样本库中找到患者对应的检测切片图片</p>
          </div>
          <!-- 图片区域 -->
          <div class="image-container">
            <div 
              v-if="!originalImageUrl" 
              class="image-placeholder"
            ></div>
            <img 
              v-else 
              :src="originalImageUrl" 
              alt="患者切片" 
              class="display-image"
            >
          </div>
        </div>
      </div>

      <!-- 右侧：AI诊断结果 -->
      <div class="section right-section">
        <h2 class="section-title">AI诊断结果</h2>
        <div class="content-wrapper">
          <button 
            @click="runModelPrediction"
            :disabled="!originalImageUrl || isLoading"
            class="button start-diagnose"
          >开始诊断</button>
          <p class="hint">经过神经网络模型处理后的图片 (带候选框标注)</p>
          <!-- 图片区域 -->
          <div class="image-container">
            <div v-if="isLoading" class="loading-hint">
              <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>神经网络模型正在运行...</span>
            </div>
            <div 
              v-if="!processedImageUrl && !isLoading" 
              class="image-placeholder"
            ></div>
            <img 
              v-else-if="processedImageUrl" 
              :src="processedImageUrl" 
              alt="处理后切片" 
              class="display-image"
            >
          </div>
          <!-- 诊断结果展示 -->
<div class="result-group">
  <!-- 第一行：诊断结果 -->
  <div class="result-row">
    <span class="result-title">诊断结果：</span>
    <span 
      class="result-value" 
      :class="{ positive: diagnosisResult.includes('阳性') }"
    >
      {{ diagnosisResult || '待运行' }}
    </span>
  </div>
  <!-- 第二行：判断依据 -->
  <div class="result-row">
    <span class="result-title">判断依据：</span>
    <span class="result-value">
      {{ judgmentBasis || '待运行' }}
    </span>
  </div>
</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

const patientId = ref('');
const originalImageUrl = ref('');
const processedImageUrl = ref('');
const diagnosisResult = ref('');
const judgmentBasis = ref('');
const isLoading = ref(false);

const fetchPatientImage = async () => {
  if (!patientId.value.trim()) {
    alert('请输入患者编号！');
    return;
  }
  try {
    // 调用后端接口获取患者图片
    const response = await axios.get(`${API_BASE_URL}/patient_image/${patientId.value}`, { 
      responseType: 'blob' 
    });
    originalImageUrl.value = URL.createObjectURL(response.data);
    processedImageUrl.value = '';
    diagnosisResult.value = '';
    judgmentBasis.value = '';
  } catch (error) {
    console.error('获取图片失败:', error);
    alert('获取患者切片失败，请检查编号或后端服务！');
  }
};

const runModelPrediction = async () => {
  if (!originalImageUrl.value) {
    alert('请先加载患者切片！');
    return;
  }
  isLoading.value = true;
  try {
    // 调用后端预测接口
    const response = await axios.post(`${API_BASE_URL}/predict/${patientId.value}`);
    
    // 更新诊断结果和处理后的图片
    diagnosisResult.value = response.data.diagnosis;
    judgmentBasis.value = response.data.basis;
    
    // 处理后图片是 base64 编码，需要转换为可显示的 URL
    processedImageUrl.value = `data:image/jpeg;base64,${response.data.processed_image}`;
  } catch (error) {
    console.error('诊断失败:', error);
    alert('AI诊断失败，请检查后端服务！');
    diagnosisResult.value = '诊断失败';
    judgmentBasis.value = error.message;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 页面容器 */
.page-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
  padding: 5px;
  min-height: 100vh;
  box-sizing: border-box;
}

/* 左右布局容器 */
.layout-row {
  display: flex;
  gap: 24px;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  flex-wrap: wrap;
}

/* 卡片通用样式 */
.section {
  background-color: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  flex: 1;
  min-width: 400px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column; /* 让内容垂直排列 */
  position: relative; 
  height:870px;
}

/* 内容包裹器 */
.content-wrapper {
  display: flex;
  flex-direction: column;
  flex: 1; /* 让内容区域占满卡片高度 */
}

/* 模块标题 */
.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #2d3748;
  padding-bottom: 12px;
  border-bottom: 1px solid #edf2f7;
}

/* 表单组 */
.form-group {
  margin-bottom: 24px;
}

/* 标签 */
.label {
  display: block;
  margin-bottom: 8px;
  color: #4a5568;
  font-weight: 500;
}

/* 输入框 + 按钮组 */
.input-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 输入框 */
.input {
  padding: 10px 12px;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  flex: 1;
  font-size: 14px;
  transition: border-color 0.2s;
}
.input:focus {
  outline: none;
  border-color: #63b3ed;
  box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.1);
}

/* 按钮 */
.button {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.start-diagnose {
  background-color: #3182ce;
  color: white;
  margin-bottom: 16px;
}
.start-diagnose:hover {
  background-color: #2b6cb0;
}
.start-diagnose:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 提示文字 */
.hint {
  color: #718096;
  margin: 8px 0 24px;
  font-size: 14px;
  line-height: 1.5;
}

/* 图片容器 */
.image-container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1; /* 让图片区域占满剩余空间，卡片会随内容延伸 */
  margin-bottom: 24px;
  min-height: 500px; /* 确保最小高度，内容多则自动增高 */
  }

/* 图片占位符 */
.image-placeholder {
  width: 100%;
  max-width: 600px;
  height: 510px;
  border: 2px dashed #cbd5e0;
  border-radius: 8px;
  background-color: #f7fafc;
  transition: all 0.2s;
  position: absolute;
  top: 230px; 
  /* 距离父容器顶部 50px */
  left: 45px; 
}
.image-placeholder:hover {
  border-color: #90cdf4;
  background-color: #edf2f7;
}

/* 实际图片展示 */
.display-image {
  width: 100%;
  max-width: 500px;
  height: 400px;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #f7fafc;
  padding: 8px;
  box-sizing: border-box;
}

/* 诊断结果展示 */
.result-group {
  margin-top: 20px; /* 结果区域靠下 */
  padding-top: 18px;
  border-top: 1px solid #edf2f7;
}

.result-title {
  font-weight: 600;
  margin-bottom: 6px;
  color: #2d3748;
  font-size: 15px;
}

.result-value {
  margin-bottom: 14px;
  color: #4a5568;
  line-height: 1.6;
}

/* 加载中提示 */
.loading-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #4a5568;
  height: 100%;
}

/* 阳性结果标红 */
.positive {
  color: #e53e3e;
  font-weight: 600;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .image-container {
    min-height: 300px;
  }
  .image-placeholder,
  .display-image {
    height: 300px;
  }
}
</style>