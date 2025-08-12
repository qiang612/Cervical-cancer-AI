import axios from 'axios';
import { ElMessage } from 'element-plus';
// Vuex 导入方式
import { useStore } from 'vuex';

// 创建Axios实例
const instance = axios.create({
  // Vite 环境变量格式
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 30000, // 30秒超时
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 从 Vuex 中获取 token
    const store = useStore();
    const token = store.state.user.token;
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    ElMessage.error('请求错误: ' + error.message);
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          ElMessage.error('登录已过期，请重新登录');
          // 调用 Vuex 的 logout action
          const store = useStore();
          store.dispatch('user/logout');
          break;
        case 403:
          ElMessage.error('没有操作权限');
          break;
        case 404:
          ElMessage.error('请求的资源不存在');
          break;
        case 500:
          ElMessage.error('服务器内部错误');
          break;
        default:
          ElMessage.error(`请求失败: ${error.response.data.message || '未知错误'}`);
      }
    } else if (error.request) {
      ElMessage.error('服务器无响应，请稍后再试');
    } else {
      ElMessage.error('请求错误: ' + error.message);
    }
    return Promise.reject(error);
  }
);

export default instance;
