import axios from '@/utils/axios';

/**
 * 用户登录接口
 * @param {object} loginData - 包含 username 和 password 的对象
 * @returns {Promise}
 */
export function login(loginData) {
  // 确保这里的 URL '/api/auth/login' 和你后端蓝图的路由完全匹配
  return axios.post('/api/auth/login', loginData);
}

/**
 * 获取用户信息接口
 * @returns {Promise}
 */
export function getUserProfile() {
  return axios.get('/api/auth/profile');
}
