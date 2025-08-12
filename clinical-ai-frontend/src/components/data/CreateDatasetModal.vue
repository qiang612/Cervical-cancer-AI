<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 z-40 flex justify-center items-center" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-lg p-6 m-4 transform transition-all" :class="{'animate-scale-in': true}">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">{{ isEditMode ? '编辑数据集' : '创建新数据集' }}</h2>
      
      <form @submit.prevent="submitForm">
        <div class="space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">数据集名称</label>
            <input type="text" id="name" v-model="form.name" required
                   class="mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
          </div>
          <div>
            <label for="taskType" class="block text-sm font-medium text-gray-700">任务类型</label>
            <select id="taskType" v-model="form.taskType" required
                    class="mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
              <option disabled value="">请选择...</option>
              <option value="classification">图像分类</option>
              <option value="detection">目标检测</option>
              <option value="segmentation">图像分割</option>
            </select>
          </div>
          <div>
            <label for="imageType" class="block text-sm font-medium text-gray-700">影像类型</label>
            <select id="imageType" v-model="form.imageType" required
                    class="mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
               <option disabled value="">请选择...</option>
               <option value="细胞学">细胞学</option>
               <option value="病理学">病理学</option>
               <option value="其他">其他</option>
            </select>
          </div>
        </div>
        
        <div class="mt-8 flex justify-end space-x-3">
          <button type="button" @click="$emit('close')"
                  class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition">
            取消
          </button>
          <button type="submit"
                  class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition">
            {{ isEditMode ? '保存更改' : '创建' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  datasetToEdit: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['close', 'save']);

const isEditMode = computed(() => !!props.datasetToEdit);

const form = ref({
  name: '',
  taskType: '',
  imageType: ''
});

watch(() => props.datasetToEdit, (newVal) => {
  if (newVal) {
    form.value.name = newVal.name;
    form.value.taskType = newVal.taskType;
    form.value.imageType = newVal.imageType;
  } else {
    form.value.name = '';
    form.value.taskType = '';
    form.value.imageType = '';
  }
}, { immediate: true });

const submitForm = () => {
  emit('save', { ...form.value });
};
</script>

<style scoped>
/* 背景遮罩 */
.fixed {
  position: fixed;
}

.inset-0 {
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.bg-black {
  background-color: #000000;
}

.bg-opacity-50 {
  background-opacity: 0.5;
}

.z-40 {
  z-index: 40;
}

.flex {
  display: flex;
}

.justify-center {
  justify-content: center;
}

.items-center {
  align-items: center;
}

/* 对话框容器 */
.bg-white {
  background-color: #ffffff;
}

.rounded-lg {
  border-radius: 0.5rem;
}

.shadow-xl {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.w-full {
  width: 100%;
}

.max-w-lg {
  max-width: 32rem;
}

.p-6 {
  padding: 1.5rem;
}

.m-4 {
  margin: 1rem;
}

.transform {
  transform: translateZ(0);
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* 标题样式 */
.text-2xl {
  font-size: 1.5rem;
  line-height: 2rem;
}

.font-bold {
  font-weight: 700;
}

.text-gray-800 {
  color: #1f2937;
}

.mb-6 {
  margin-bottom: 1.5rem;
}

/* 表单样式 */
.space-y-4 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-y-reverse: 0;
  margin-top: calc(1rem * calc(1 - var(--tw-space-y-reverse)));
  margin-bottom: calc(1rem * var(--tw-space-y-reverse));
}

/* 标签样式 */
.block {
  display: block;
}

.text-sm {
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.font-medium {
  font-weight: 500;
}

.text-gray-700 {
  color: #374151;
}

/* 输入框和选择项样式 */
.mt-1 {
  margin-top: 0.25rem;
}

.border-gray-300 {
  border-color: #d1d5db;
}

.rounded-md {
  border-radius: 0.375rem;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.focus\:ring-blue-500:focus {
  --tw-ring-opacity: 1;
  --tw-ring-color: rgba(59, 130, 246, var(--tw-ring-opacity));
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.focus\:border-blue-500:focus {
  border-color: #3b82f6;
}

/* 按钮区域 */
.mt-8 {
  margin-top: 2rem;
}

.justify-end {
  justify-content: flex-end;
}

.space-x-3 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 0;
  margin-right: calc(0.75rem * var(--tw-space-x-reverse));
  margin-left: calc(0.75rem * calc(1 - var(--tw-space-x-reverse)));
}

/* 按钮样式 */
.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.bg-gray-200 {
  background-color: #e5e7eb;
}

.text-gray-800 {
  color: #1f2937;
}

.hover\:bg-gray-300:hover {
  background-color: #d1d5db;
}

.bg-blue-600 {
  background-color: #2563eb;
}

.text-white {
  color: #ffffff;
}

.hover\:bg-blue-700:hover {
  background-color: #1d4ed8;
}

/* 动画效果 */
@keyframes scale-in {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.animate-scale-in {
  animation: scale-in 0.25s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

/* 表单元素交互样式 */
input, select {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

input:focus, select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

input:invalid:not(:focus):not(:placeholder-shown),
select:invalid:not(:focus):not(:placeholder-shown) {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

button {
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s ease-in-out;
}

button[type="submit"] {
  background-color: #2563eb;
  color: white;
}

button[type="submit"]:hover {
  background-color: #1d4ed8;
  transform: translateY(-1px);
}

button[type="button"]:hover {
  transform: translateY(-1px);
}

/* 响应式调整 */
@media (max-width: 640px) {
  .max-w-lg {
    max-width: 100%;
  }
  
  .p-6 {
    padding: 1rem;
  }
  
  .text-2xl {
    font-size: 1.25rem;
  }
  
  .space-x-3 {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .space-x-3 button {
    width: 100%;
  }
}
</style>