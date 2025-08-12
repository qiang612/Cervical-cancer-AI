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
  animation: scale-in 0.2s ease-out forwards;
}
</style>