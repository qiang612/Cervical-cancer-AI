<template>
  <div class="bg-white p-6 rounded-lg shadow-lg">
    <div class="flex flex-wrap justify-between items-center pb-4 border-b mb-6 gap-4">
      <div class="flex items-center">
        <input v-if="isEditingName" v-model="editableName" @blur="saveName" @keyup.enter="saveName"
               class="text-2xl font-bold text-gray-800 border-b-2 border-blue-500 focus:outline-none" ref="nameInputRef"/>
        <h2 v-else @click="editName" class="text-2xl font-bold text-gray-800 mr-2 cursor-pointer" :title="dataset.name">{{ dataset.name }}</h2>
        <button @click="editName" class="text-gray-500 hover:text-blue-600">
            <FilePenLine class="h-5 w-5"/>
        </button>
      </div>
      <div class="flex items-center space-x-2">
        <button @click="handleBatchImport" class="btn-primary">
          <Upload class="h-4 w-4 mr-2" /> 批量导入
        </button>
        <button @click="$emit('migrateDataset', dataset.id)" class="btn-secondary">
          <GitBranch class="h-4 w-4 mr-2" /> 数据集迁移
        </button>
        <button @click="$emit('shareDataset', dataset.id)" class="btn-secondary">
          <Share2 class="h-4 w-4 mr-2" /> 分享
        </button>
        <button @click="$emit('deleteDataset', dataset.id)" class="btn-danger">
          <Trash2 class="h-4 w-4 mr-2" /> 删除数据集
        </button>
      </div>
    </div>

    <div class="mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
        <div class="col-span-1 md:col-span-2">
          <label for="search-image" class="block text-sm font-medium text-gray-700 mb-1">搜索图片</label>
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input type="text" id="search-image" v-model="imageSearchTerm"
              class="pl-10 w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500"
              placeholder="按图片名称搜索...">
          </div>
        </div>
        <div>
          <label for="image-format" class="block text-sm font-medium text-gray-700 mb-1">图像格式</label>
          <select id="image-format" v-model="imageFormatFilter"
            class="w-full border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500">
            <option value="">所有格式</option>
            <option v-for="format in allFormats" :key="format" :value="format">{{ format }}</option>
          </select>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="text-center py-10">
      <LoaderCircle class="h-10 w-10 text-blue-600 animate-spin mx-auto" />
      <p class="mt-3 text-gray-500">图片加载中...</p>
    </div>
     <div v-else-if="filteredImages.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4">
        <div v-for="image in filteredImages" :key="image.id" class="relative group aspect-square border rounded-lg overflow-hidden shadow-sm">
            <img :src="image.url" :alt="image.name" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-300 flex flex-col justify-between p-2">
                <div class="flex justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                    <button @click="deleteImage(image.id)" class="p-1.5 bg-red-600 text-white rounded-full hover:bg-red-700">
                        <Trash2 class="h-4 w-4" />
                    </button>
                </div>
                <p class="text-white text-xs font-semibold truncate bg-black/50 p-1 rounded-sm">{{ image.name }}</p>
            </div>
        </div>
    </div>
    <div v-else class="text-center py-20 border-2 border-dashed rounded-lg">
        <ImageOff class="h-16 w-16 text-gray-400 mx-auto" />
        <h3 class="mt-4 text-xl font-semibold text-gray-700">此数据集为空</h3>
        <p class="mt-2 text-gray-500">点击“批量导入”开始添加影像数据。</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { Upload, GitBranch, Share2, Trash2, FilePenLine, Search, LoaderCircle, ImageOff } from 'lucide-vue-next';

const props = defineProps({
  dataset: {
    type: Object,
    required: true
  }
});
const emit = defineEmits(['update:datasetName', 'deleteDataset', 'shareDataset', 'migrateDataset']);

// --- State for Image Grid ---
const images = ref([]);
const loading = ref(true);
const imageSearchTerm = ref('');
const imageFormatFilter = ref('');

// --- State for editing name ---
const isEditingName = ref(false);
const editableName = ref(props.dataset.name);
const nameInputRef = ref(null);

// --- Mock API for images ---
const imageApi = {
    getImages: async (datasetId) => {
        console.log(`Fetching images for dataset ${datasetId}`);
        await new Promise(resolve => setTimeout(resolve, 800));
        // Generate mock images
        const formats = ['jpg', 'png', 'tiff', 'dcm'];
        return Array.from({length: props.dataset.imageCount}, (_, i) => {
            const format = formats[i % formats.length];
            return {
                id: i + 1,
                name: `image_${i + 1}.${format}`,
                url: `https://source.unsplash.com/random/200x200?sig=${i + props.dataset.id}`,
                format: format.toUpperCase()
            }
        });
    },
    deleteImage: async (imageId) => {
        await new Promise(resolve => setTimeout(resolve, 300));
        return imageId;
    }
}

onMounted(async () => {
    images.value = await imageApi.getImages(props.dataset.id);
    loading.value = false;
})

const allFormats = computed(() => {
    const formats = new Set(images.value.map(img => img.format));
    return Array.from(formats).sort();
})

const filteredImages = computed(() => {
    return images.value.filter(image => {
        const nameMatch = image.name.toLowerCase().includes(imageSearchTerm.value.toLowerCase());
        const formatMatch = !imageFormatFilter.value || image.format === imageFormatFilter.value;
        return nameMatch && formatMatch;
    })
})


// --- Methods ---
const editName = async () => {
    isEditingName.value = true;
    await nextTick();
    nameInputRef.value?.focus();
}
const saveName = () => {
    isEditingName.value = false;
    if (editableName.value && editableName.value !== props.dataset.name) {
        // TODO: Call API to update the name on the backend
        emit('update:datasetName', editableName.value);
    } else {
        editableName.value = props.dataset.name;
    }
}

const handleBatchImport = () => {
    // TODO: Implement batch import logic, e.g., open a file dialog
    alert('功能开发中：批量导入图片...');
}

const deleteImage = async (imageId) => {
    if (confirm('你确定要删除这张图片吗?')) {
        // TODO: Call API to delete the image from the backend
        const deletedId = await imageApi.deleteImage(imageId);
        images.value = images.value.filter(img => img.id !== deletedId);
    }
}

</script>

<style scoped>
/* 基础容器容器样式 */
.bg-white {
  background-color: #ffffff;
}

.p-6 {
  padding: 1.5rem;
}

.rounded-lg {
  border-radius: 0.5rem;
}

.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
}

/* 顶部头部样式 */
.flex {
  display: flex;
}

.flex-wrap {
  flex-wrap: wrap;
}

.justify-between {
  justify-content: space-between;
}

.items-center {
  align-items: center;
}

.pb-4 {
  padding-bottom: 1rem;
}

.border-b {
  border-bottom-width: 1px;
  border-bottom-color: #e5e7e9;
}

.mb-6 {
  margin-bottom: 1.5rem;
}

.gap-4 {
  gap: 1rem;
}

/* 标题编辑区域 */
.text-2xl {
  font-size: 1.5rem;
  line-height: 2rem;
}

.font-bold {
  font-weight: 600;
}

.text-gray-800 {
  color: #1f2937;
}

.mr-2 {
  margin-right: 0.5rem;
}

.cursor-pointer {
  cursor: pointer;
}

/* 输入框样式 */
.border-b-2 {
  border-bottom-width: 2px;
}

.border-blue-500 {
  border-color: #3b82f6;
}

.focus\:outline-none:focus {
  outline: none;
}

/* 按钮样式 */
.btn-primary {
  @apply flex flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg shadow-sm hover:bg-blue-700 transition-all duration-200 text-sm font-medium;
}

.btn-secondary {
  @applyapply flex flex items-center bg-gray-100 text-gray-700 px-4 py-2 rounded-md shadow-sm hover:bg-gray-200 transition-all duration-200 text-sm font-medium;
}

.btn-danger {
  @apply flex items-center bg-red-600 text-white px-4 py-2 rounded-md shadow-sm hover:bg-red-700 transition-all duration-200 text-sm font-medium;
}

/* 按钮图标标样式 */
.h-4 {
  height: 1rem;
}

.w-4 {
  width: 1rem;
}

.mr-2 {
  margin-right: 0.5rem;
}

/* 搜索和筛选区域 */
.grid {
  display: grid;
}

.grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

.md\:grid-cols-3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.gap-4 {
  gap: 1rem;
}

.items-end {
  align-items: end;
}

.col-span-1 {
  grid-column: span 1 / span 1;
}

.md\:col-span-2 {
  grid-column: span 2 / span 2;
}

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

.mb-1 {
  margin-bottom: 0.25rem;
}

.relative {
  position: relative;
}

.pl-10 {
  padding-left: 2.5rem;
}

.w-full {
  width: 100%;
}

.border-gray-300 {
  border-color: #d1d5db;
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.focus\:ring-blue-500:focus {
  ring-color: #3b82f6;
  ring-width: 2px;
  ring-offset-width: 0px;
}

.focus\:border-blue-500:focus {
  border-color: #3b82f6;
}

.placeholder\:text-gray-400::placeholder {
  color: #9ca3af;
}

/* 图片网格区域 */
.mb-6 {
  margin-bottom: 1.5rem;
}

.text-center {
  text-align: center;
}

.py-10 {
  padding-top: 2.5rem;
  padding-bottom: 2.5rem;
}

.h-10 {
  height: 2.5rem;
}

.w-10 {
  width: 2.5rem;
}

.text-blue-600 {
  color: #3b82f6;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.mt-3 {
  margin-top: 0.75rem;
}

.text-gray-500 {
  color: #6b7280;
}

/* 图片网格布局 */
.sm\:grid-cols-3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.md\:grid-cols-4 {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.lg\:grid-cols-6 {
  grid-template-columns: repeat(6, minmax(0, 1fr));
}

.xl\:grid-cols-8 {
  grid-template-columns: repeat(8, minmax(0, 1fr));
}

.gap-4 {
  gap: 1rem;
}

/* 图片卡片样式 */
.relative {
  position: relative;
}

.group {
  transition: all 0.3s ease;
}

.aspect-square {
  aspect-ratio: 1 / 1;
}

.border {
  border-width: 1px;
  border-color: #e2e8f0;
}

.overflow-hidden {
  overflow: hidden;
}

/* 图片卡片悬停效果 */
.group:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-color: #cbd5e1;
}

/* 图片样式 */
.object-cover {
  object-fit: cover;
  transition: transform 0.4s ease;
}

.group:hover .object-cover {
  transform: scale(1.08);
}

/* 图片覆盖层 */
.absolute {
  position: absolute;
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

.bg-opacity-0 {
  background-opacity: 0;
}

.group-hover\:bg-opacity-40:hover {
  background-opacity: 0.4;
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

.flex-col {
  flex-direction: column;
}

.justify-between {
  justify-content: space-between;
}

.p-2 {
  padding: 0.5rem;
}

/* 图片操作按钮 */
.justify-end {
  justify-content: flex-end;
}

.opacity-0 {
  opacity: 0;
}

.group-hover\:opacity-100:hover {
  opacity: 1;
}

.transition-opacity {
  transition-property: opacity;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

.p-1.5 {
  padding: 0.375rem;
}

.bg-red-600 {
  background-color: #dc2626;
}

.text-white {
  color: #ffffff;
}

.rounded-full {
  border-radius: 9999px;
}

.hover\:bg-red-700:hover {
  background-color: #b91c1c;
}

/* 图片名称标签 */
.text-xs {
  font-size: 0.75rem;
  line-height: 1rem;
}

.font-semibold {
  font-weight: 600;
}

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bg-black\/50 {
  background-color: rgba(0, 0, 0, 0.5);
}

.p-1 {
  padding: 0.25rem;
}

.rounded-sm {
  border-radius: 0.125rem;
}

/* 空状态样式 */
.py-20 {
  padding-top: 5rem;
  padding-bottom: 5rem;
}

.border-2 {
  border-width: 2px;
}

.border-dashed {
  border-style: dashed;
}

.h-16 {
  height: 4rem;
}

.w-16 {
  width: 4rem;
}

.text-gray-400 {
  color: #9ca3af;
}

.mt-4 {
  margin-top: 1rem;
}

.text-xl {
  font-size: 1.25rem;
  line-height: 1.75rem;
}

.mt-2 {
  margin-top: 0.5rem;
}

/* 动画效果 */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .lg\:grid-cols-6 {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .md\:grid-cols-4 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  
  .md\:col-span-2 {
    grid-column: span 1 / span 1;
  }
  
  .md\:grid-cols-3 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .sm\:grid-cols-3 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
  .xl\:grid-cols-8 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
  .flex-wrap button {
    width: 100%;
    justify-content: center;
  }
}

</style>