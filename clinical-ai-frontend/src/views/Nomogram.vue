<template>
  <div class="p-4 sm:p-6 md:p-8 bg-slate-100 min-h-full">
    <div class="max-w-screen-2xl mx-auto">

      <div class="bg-white p-5 rounded-xl shadow-md mb-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-center">
          
          <div class="lg:col-span-1">
            <label for="patient-id" class="block text-base font-bold text-slate-800 mb-2">
              第一步: 输入患者编号
            </label>
            <div class="flex rounded-lg shadow-sm">
              <input 
                v-model="patientId"
                type="text" 
                name="patient-id" 
                id="patient-id" 
                class="block w-full rounded-none rounded-l-lg border-slate-300 px-4 py-2.5 text-slate-800 placeholder-slate-400 focus:border-indigo-500 focus:ring-indigo-500"
                placeholder="例如: 1"
                @keyup.enter="fetchPatientImage"
              />
              <button 
                @click="fetchPatientImage"
                type="button" 
                class="relative -ml-px inline-flex items-center space-x-2 rounded-r-lg border border-slate-300 bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <span>查找切片</span>
              </button>
            </div>
          </div>
          
          <div class="lg:col-span-2 flex items-center h-full pt-2 md:pt-8">
             <button 
                @click="runModelPrediction"
                :disabled="!originalImageUrl || isLoading"
                class="inline-flex items-center justify-center rounded-lg border border-transparent bg-indigo-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors">
                第二步: 开始诊断
            </button>
            <div class="ml-6 flex items-center text-slate-600">
              <div v-if="isLoading">
                <svg class="animate-spin h-6 w-6 mr-3 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>神经网络模型正在运行...</span>
              </div>
              <div v-if="!isLoading && diagnosisResult" class="flex items-center font-semibold text-green-600">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-6 h-6 mr-2"><path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z" clip-rule="evenodd" /></svg>
                <span>运行已结束</span>
              </div>
            </div>
          </div>

        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <div class="bg-white p-6 rounded-xl shadow-md flex flex-col">
          <h3 class="text-xl font-bold text-slate-800 mb-1">原始检测切片</h3>
          <p class="text-slate-500 mb-4">从样本库中找到患者对应的检测切片</p>
          <div class="mt-auto w-full h-96 xl:h-[500px] bg-slate-50 rounded-lg overflow-hidden flex items-center justify-center">
            <img v-if="originalImageUrl" :src="originalImageUrl" alt="患者原始切片" class="w-full h-full object-contain">
            <div v-else class="border-2 border-dashed border-slate-300 rounded-lg w-full h-full flex flex-col items-center justify-center text-center p-4">
              <svg class="w-16 h-16 text-slate-400 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
              </svg>
              <p class="text-slate-500 font-semibold">此处显示原始图片</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-xl shadow-md flex flex-col">
          <h3 class="text-xl font-bold text-slate-800 mb-1">AI 分析结果</h3>
          <p class="text-slate-500 mb-4">经过神经网络模型处理后的带标注图像和诊断</p>
          <div class="mt-auto w-full h-96 xl:h-[500px] bg-slate-50 rounded-lg overflow-hidden flex items-center justify-center">
            <img v-if="processedImageUrl" :src="processedImageUrl" alt="处理后的切片" class="w-full h-full object-contain">
            <div v-else class="border-2 border-dashed border-slate-300 rounded-lg w-full h-full flex flex-col items-center justify-center text-center p-4">
              <svg class="w-16 h-16 text-slate-400 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                 <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456Z" />
              </svg>
              <p class="text-slate-500 font-semibold">此处显示带有候选框的图片</p>
            </div>
          </div>
          <div v-if="diagnosisResult || isLoading" class="mt-6 border-t border-slate-200 pt-6">
            <dl class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
              <div class="p-4 bg-slate-50 rounded-lg">
                <dt class="text-sm font-medium text-slate-500">诊断结果</dt>
                <dd class="mt-1 text-2xl font-bold" :class="diagnosisResult.includes('阳性') ? 'text-red-600' : 'text-green-700'">
                  {{ diagnosisResult || '...' }}
                </dd>
              </div>
              <div class="p-4 bg-slate-50 rounded-lg">
                <dt class="text-sm font-medium text-slate-500">判断依据</dt>
                <dd class="mt-1 text-sm text-slate-700">
                  {{ judgmentBasis || '...' }}
                </dd>
              </div>
            </dl>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

// 后端API服务器地址
const API_BASE_URL = 'http://127.0.0.1:5000';

const patientId = ref('');
const originalImageUrl = ref(null);
const processedImageUrl = ref(null);
const diagnosisResult = ref('');
const judgmentBasis = ref('');
const isLoading = ref(false);

// 1. 根据患者ID获取原始图片
const fetchPatientImage = async () => {
    if (!patientId.value) {
        alert('请输入患者编号!');
        return;
    }
    isLoading.value = true;
    // 重置状态
    originalImageUrl.value = null;
    processedImageUrl.value = null;
    diagnosisResult.value = '';
    judgmentBasis.value = '';
    
    try {
        const response = await axios.get(`${API_BASE_URL}/patient_image/${patientId.value}`, { responseType: 'blob' });
        originalImageUrl.value = URL.createObjectURL(response.data);
    } catch (error) {
        console.error('获取图片失败:', error);
        alert(`无法找到编号为 ${patientId.value} 的患者图片，请确认编号是否正确以及后端服务是否开启。`);
        originalImageUrl.value = null;
    } finally {
        isLoading.value = false;
    }
};

// 2. 点击按钮，运行模型进行预测
const runModelPrediction = async () => {
    if (!originalImageUrl.value) {
        alert('请先查找并加载患者切片。');
        return;
    }

    isLoading.value = true;
    processedImageUrl.value = null;
    diagnosisResult.value = '运行中...';
    judgmentBasis.value = '模型正在分析切片，请稍候...';

    try {
        const response = await axios.post(`${API_BASE_URL}/predict/${patientId.value}`);
        const data = response.data;

        diagnosisResult.value = data.diagnosis;
        judgmentBasis.value = data.basis;
        processedImageUrl.value = `data:image/jpeg;base64,${data.processed_image}`;

    } catch (error) {
        console.error('模型预测失败:', error);
        diagnosisResult.value = '错误';
        judgmentBasis.value = `模型运行出错: ${error.message}。请检查后端服务。`;
    } finally {
        isLoading.value = false;
    }
};
</script>