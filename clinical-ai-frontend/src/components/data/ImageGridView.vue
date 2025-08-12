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
.btn-primary {
    @apply flex items-center bg-blue-600 text-white px-3 py-2 rounded-md shadow-sm hover:bg-blue-700 transition text-sm;
}
.btn-secondary {
    @apply flex items-center bg-gray-200 text-gray-700 px-3 py-2 rounded-md shadow-sm hover:bg-gray-300 transition text-sm;
}
.btn-danger {
    @apply flex items-center bg-red-600 text-white px-3 py-2 rounded-md shadow-sm hover:bg-red-700 transition text-sm;
}
</style>