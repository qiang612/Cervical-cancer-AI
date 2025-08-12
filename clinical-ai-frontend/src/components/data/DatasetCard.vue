<template>
  <div class="group bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300 flex flex-col cursor-pointer overflow-hidden"
       @click.self="$emit('click')">
    <div class="relative" @click.self="$emit('click')">
      <img :src="dataset.preview || 'https://images.unsplash.com/photo-1581091222233-10989a3b8a6e?w=400&q=80'" alt="Dataset preview" class="h-40 w-full object-cover">
      <div class="absolute top-2 right-2">
        <div class="relative">
          <button @click.stop="toggleMenu" class="p-1.5 bg-white/70 backdrop-blur-sm rounded-full text-gray-700 hover:bg-white transition">
            <MoreVertical class="h-5 w-5" />
          </button>
          <transition name="fade">
            <div v-if="isMenuOpen" v-click-outside="closeMenu"
                 class="absolute right-0 mt-2 w-40 bg-white rounded-md shadow-lg z-10 py-1">
              <a @click.stop="$emit('edit')" class="flex items-center w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                <FilePenLine class="h-4 w-4 mr-2" /> 编辑
              </a>
              <a @click.stop="$emit('copy')" class="flex items-center w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                <Copy class="h-4 w-4 mr-2" /> 复制
              </a>
               <a @click.stop="$emit('share')" class="flex items-center w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                <Share2 class="h-4 w-4 mr-2" /> 分享
              </a>
              <div class="border-t my-1"></div>
              <a @click.stop="$emit('delete')" class="flex items-center w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50">
                <Trash2 class="h-4 w-4 mr-2" /> 删除
              </a>
            </div>
          </transition>
        </div>
      </div>
    </div>

    <div class="p-4 flex-grow flex flex-col" @click.self="$emit('click')">
      <h3 class="font-bold text-lg text-gray-800 truncate" :title="dataset.name">{{ dataset.name }}</h3>
      <div class="flex-grow mt-2 text-sm text-gray-500 space-y-1">
          <div class="flex items-center">
             <Layers class="h-4 w-4 mr-2 text-gray-400"/> <span>任务类型: {{ taskTypeMap[dataset.taskType] || '未知' }}</span>
          </div>
          <div class="flex items-center">
              <Shield class="h-4 w-4 mr-2 text-gray-400"/> <span>影像类型: {{ dataset.imageType }}</span>
          </div>
      </div>
      <div class="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center text-sm text-gray-600">
        <span class="font-medium">{{ dataset.imageCount }} 张影像</span>
        <div class="flex -space-x-1 overflow-hidden">
            <span v-for="fmt in dataset.format.slice(0, 3)" :key="fmt"
                  class="inline-block h-6 w-6 rounded-full bg-gray-200 text-gray-600 text-xs flex items-center justify-center font-semibold ring-2 ring-white">
              {{ fmt.slice(0,3) }}
            </span>
            <span v-if="dataset.format.length > 3"
                class="inline-block h-6 w-6 rounded-full bg-gray-300 text-gray-700 text-xs flex items-center justify-center font-semibold ring-2 ring-white">
              +{{ dataset.format.length - 3 }}
            </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { MoreVertical, FilePenLine, Copy, Share2, Trash2, Layers, Shield } from 'lucide-vue-next';

defineProps({
  dataset: {
    type: Object,
    required: true
  }
});

defineEmits(['click', 'edit', 'copy', 'share', 'delete']);

const isMenuOpen = ref(false);

const taskTypeMap = {
  classification: '图像分类',
  detection: '目标检测',
  segmentation: '图像分割'
};

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
    isMenuOpen.value = false;
}

// v-click-outside directive
const vClickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.body.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent);
  },
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>