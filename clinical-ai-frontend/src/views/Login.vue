<template>
  <!-- 外层容器，使内容全屏居中 -->
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <!-- 登录卡片容器 -->
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg overflow-hidden">
      <!-- 卡片头部 -->
      <div class="bg-blue-600 p-6 text-white text-center">
        <h2 class="text-2xl font-bold">临床AI辅助诊断系统</h2>
        <p class="mt-1 opacity-90">请登录以继续使用</p>
      </div>
      
      <!-- 登录表单 -->
      <div class="p-6">
        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- 用户名输入 -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-500">
                <i class="fa fa-user"></i>
              </div>
              <input
                type="text"
                id="username"
                v-model="username"
                required
                placeholder="请输入用户名"
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out"
              >
            </div>
          </div>
          
          <!-- 密码输入 -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">密码</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-500">
                <i class="fa fa-lock"></i>
              </div>
              <input
                type="password"
                id="password"
                v-model="password"
                required
                placeholder="请输入密码"
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out"
              >
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500 hover:text-gray-700"
              >
                <i :class="showPassword ? 'fa fa-eye-slash' : 'fa fa-eye'"></i>
              </button>
            </div>
          </div>
          
          <!-- 记住密码和忘记密码 -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember"
                type="checkbox"
                v-model="rememberMe"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              >
              <label for="remember" class="ml-2 block text-sm text-gray-700">
                记住密码
              </label>
            </div>
            <a href="#" class="text-sm text-blue-600 hover:text-blue-800">
              忘记密码?
            </a>
          </div>
          
          <!-- 登录按钮 -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <span v-if="isLoading" class="flex items-center">
              <i class="fa fa-spinner fa-spin mr-2"></i> 登录中...
            </span>
            <span v-else>登录</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// 表单数据
const username = ref('');
const password = ref('');
const rememberMe = ref(true);
const showPassword = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

const router = useRouter();

// 登录处理
const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  
  try {
    // 模拟登录API调用
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 这里应该是实际的登录验证逻辑
    if (username.value && password.value) {
      // 存储登录状态
      localStorage.setItem('token', 'dummy-token');
      if (!rememberMe.value) {
        // 如果不记住密码，可以设置短期存储
        sessionStorage.setItem('username', username.value);
      } else {
        localStorage.setItem('username', username.value);
      }
      
      // 登录成功，重定向到首页
      router.push('/home');
    } else {
      errorMessage.value = '请输入用户名和密码';
    }
  } catch (err) {
    errorMessage.value = '登录失败，请检查用户名和密码';
    console.error('登录错误:', err);
  } finally {
    isLoading.value = false;
  }
};

// 页面加载时恢复用户名（如果记住密码）
const initForm = () => {
  const savedUsername = rememberMe.value ? localStorage.getItem('username') : sessionStorage.getItem('username');
  if (savedUsername) {
    username.value = savedUsername;
  }
};

// 初始化表单
initForm();
</script>
    