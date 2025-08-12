import axios from 'axios';
import { ElMessage } from 'element-plus';
import store from '@/store'; // 导入 store 以便在拦截器中 dispatch actions

// 创建Axios实例
const instance = axios.create({
  // Vite 环境变量格式，建议提供一个默认的 /api 前缀
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api', 
  timeout: 30000, // 30秒超时
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 【修正】直接从 localStorage 获取 token
    // 这是最稳定可靠的方式，因为它不依赖 Vue 实例的生命周期
    const token = localStorage.getItem('token');
    
    if (token) {
      // 如果 token 存在，则添加到请求头中
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // 对请求错误做些什么
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    // 我们只关心响应体中的 `data` 部分
    return response.data;
  },
  (error) => {
    if (error.response) {
      const status = error.response.status;
      // 后端返回的数据通常在 error.response.data
      const data = error.response.data;
      let message = data.msg || data.message || '发生未知错误';

      switch (status) {
        case 401:
          message = '登录已过期或认证失败，请重新登录';
          // 调用 Vuex 的 logout action 来清理状态并重定向
          // 使用 store.dispatch 来确保能访问到 Vuex
          store.dispatch('user/logout');
          break;
        case 403:
          message = '您没有权限执行此操作';
          break;
        case 404:
          message = '请求的资源不存在';
          break;
        case 500:
          message = '服务器内部错误';
          break;
        default:
          message = `请求失败: ${message} (状态码: ${status})`;
      }
      ElMessage.error(message);
    } else if (error.request) {
      ElMessage.error('服务器无响应，请检查您的网络连接');
    } else {
      ElMessage.error('请求发送失败: ' + error.message);
    }
    return Promise.reject(error);
  }
);

export default instance;
