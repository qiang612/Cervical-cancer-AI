<template>
  <!-- 外层容器，使内容全屏居中 -->
  <div class="login-container">
    <!-- 登录卡片容器 -->
    <div class="login-card">
      <!-- 卡片头部 -->
      <div class="card-header">
        <h2>临床AI辅助诊断系统</h2>
        <p>请登录以继续使用</p>
      </div>
      
      <!-- 登录表单 -->
      <div class="card-body">
        <form @submit.prevent="handleLogin" class="login-form">
          <!-- 错误提示 -->
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          
          <!-- 用户名输入 -->
          <div class="form-group">
            <label for="username">用户名</label>
            <div class="input-wrapper">
              <i class="fa fa-user icon"></i>
              <input
                type="text"
                id="username"
                v-model="username"
                required
                placeholder="请输入用户名"
                class="form-input"
              >
            </div>
          </div>
          
          <!-- 密码输入 -->
          <div class="form-group">
            <label for="password">密码</label>
            <div class="input-wrapper">
              <i class="fa fa-lock icon"></i>
              <input
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="password"
                required
                placeholder="请输入密码"
                class="form-input"
              >
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="toggle-btn"
              >
                <i :class="showPassword ? 'fa fa-eye-slash' : 'fa fa-eye'"></i>
              </button>
            </div>
          </div>
          
          <!-- 记住密码和忘记密码 -->
          <div class="form-actions">
            <div class="remember-me">
              <input
                id="remember"
                type="checkbox"
                v-model="rememberMe"
                class="checkbox"
              >
              <label for="remember">记住密码</label>
            </div>
            <a href="#" class="forgot-link">忘记密码?</a>
          </div>
          
          <!-- 登录按钮 -->
          <button
            type="submit"
            :disabled="isLoading"
            class="login-btn"
          >
            <span v-if="isLoading" class="loading-indicator">
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

<style scoped>
/* 基础样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 登录容器 - 全屏居中 */
.login-container {
  min-height: 100vh;
  background-color: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* 登录卡片样式 */
.login-card {
  width: 100%;
  max-width: 400px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* 卡片头部样式 */
.card-header {
  background-color: #2563eb;
  padding: 30px 20px;
  text-align: center;
  color: white;
}

.card-header h2 {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 8px;
}

.card-header p {
  opacity: 0.9;
  font-size: 14px;
}

/* 卡片主体样式 */
.card-body {
  padding: 30px 20px;
}

/* 表单样式 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 表单组样式 */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #4b5563;
}

/* 输入框容器 */
.input-wrapper {
  position: relative;
  width: 100%;
}

/* 输入框样式 */
.form-input {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.15s ease-in-out;
}

.form-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}

/* 图标样式 */
.icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  font-size: 16px;
}

/* 密码切换按钮 */
.toggle-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  font-size: 16px;
  transition: color 0.15s ease-in-out;
}

.toggle-btn:hover {
  color: #4b5563;
}

/* 表单操作区 */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
}

/* 记住密码 */
.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox {
  width: 16px;
  height: 16px;
  color: #2563eb;
  border-color: #d1d5db;
  border-radius: 4px;
}

.remember-me label {
  font-size: 13px;
  color: #4b5563;
}

/* 忘记密码链接 */
.forgot-link {
  font-size: 13px;
  color: #2563eb;
  text-decoration: none;
  transition: color 0.15s ease-in-out;
}

.forgot-link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  padding: 12px;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-btn:hover {
  background-color: #1d4ed8;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background-color: #2563eb;
}

/* 加载指示器 */
.loading-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 错误消息 */
.error-message {
  color: #dc2626;
  font-size: 13px;
  padding: 8px 12px;
  background-color: #fee2e2;
  border-radius: 6px;
  text-align: center;
}
</style>
    