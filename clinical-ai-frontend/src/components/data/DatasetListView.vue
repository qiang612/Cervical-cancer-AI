<template>
  <div>
    <div class="mb-6 p-4 bg-white rounded-lg shadow-sm">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
        <div class="col-span-1 md:col-span-2">
          <label for="search" class="block text-sm font-medium text-gray-700 mb-1">搜索数据集</label>
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input type="text" id="search" v-model="localSearchTerm"
              class="pl-10 w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="按名称搜索...">
          </div>
        </div>
        <div>
          <label for="task-type" class="block text-sm font-medium text-gray-700 mb-1">任务类型</label>
          <select id="task-type" v-model="localFilterTaskType"
            class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500">
            <option value="">所有类型</option>
            <option value="classification">图像分类</option>
            <option value="detection">目标检测</option>
            <option value="segmentation">图像分割</option>
          </select>
        </div>
        <div>
          <label for="image-type" class="block text-sm font-medium text-gray-700 mb-1">影像类型</label>
          <select id="image-type" v-model="localFilterImageType"
            class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500">
            <option value="">所有类型</option>
            <option value="细胞学">细胞学</option>
            <option value="病理学">病理学</option>
          </select>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-6">
      <DatasetCard v-for="dataset in filteredData" :key="dataset.id" :dataset="dataset"
        @click="$emit('selectDataset', dataset)" 
        @edit="$emit('editDataset', dataset)"
        @copy="$emit('copyDataset', dataset.id)"
        @share="$emit('shareDataset', dataset.id)"
        @delete="$emit('deleteDataset', dataset.id)"
        />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import DatasetCard from './DatasetCard.vue';
import { Search } from 'lucide-vue-next';

const props = defineProps({
  datasets: {
    type: Array,
    required: true
  }
});

defineEmits(['selectDataset', 'editDataset', 'copyDataset', 'shareDataset', 'deleteDataset']);

const localSearchTerm = ref('');
const localFilterTaskType = ref('');
const localFilterImageType = ref('');

const filteredData = computed(() => {
  return props.datasets.filter(dataset => {
    const nameMatch = dataset.name.toLowerCase().includes(localSearchTerm.value.toLowerCase());
    const taskTypeMatch = !localFilterTaskType.value || dataset.taskType === localFilterTaskType.value;
    const imageTypeMatch = !localFilterImageType.value || dataset.imageType === localFilterImageType.value;
    return nameMatch && taskTypeMatch && imageTypeMatch;
  });
});

</script>