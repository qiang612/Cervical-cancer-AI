import axios from '@/utils/axios';
import router from '@/router';

// 封装一个独立的登录API请求函数
// 我们假设您有一个 api/auth.js 文件来管理这个，或者直接在这里定义
function loginApi(loginData) {
  return axios.post('/api/auth/login', loginData);
}

const state = {
  // 应用初始化时，尝试从 localStorage 获取 token 和 userInfo
  token: localStorage.getItem('token') || null,
  userInfo: JSON.parse(localStorage.getItem('userInfo')) || null,
};

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token;
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  },
  SET_USER_INFO(state, userInfo) {
    state.userInfo = userInfo;
     if (userInfo) {
      localStorage.setItem('userInfo', JSON.stringify(userInfo));
    } else {
      localStorage.removeItem('userInfo');
    }
  },
};

const actions = {
  // ## FIX: 更新 login action 以同时保存 token 和 user info ##
  async login({ commit }, loginForm) {
    try {
      // 1. 调用后端登录接口
      const response = await loginApi(loginForm);
      
      // 2. 从响应中解构出 token 和 user 信息
      //    (根据我们后端 app.py 中定义的 accessToken 和 user 字段)
      const { accessToken, user } = response;
      
      if (!accessToken || !user) {
        throw new Error('未能从响应中获取Token或用户信息');
      }

      // 3. 提交 mutation 来更新 state 和 localStorage
      commit('SET_TOKEN', accessToken);
      commit('SET_USER_INFO', user); // <-- **修正**：提交用户信息

      // 4. 登录成功后跳转到主页
      router.push('/');
      
    } catch (error) {
      // 登录失败时，确保所有信息都被清空
      commit('SET_TOKEN', null);
      commit('SET_USER_INFO', null);
      // 将错误继续抛出，以便登录页面可以捕获并显示错误信息
      return Promise.reject(error);
    }
  },

  // 登出 action (保持不变)
  logout({ commit }) {
    commit('SET_TOKEN', null);
    commit('SET_USER_INFO', null);
    router.push('/login').then(() => {
        window.location.reload();
    });
  },
};

const getters = {
  isAuthenticated: state => !!state.token,
  currentUser: state => state.userInfo,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};