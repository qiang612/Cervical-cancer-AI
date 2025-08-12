import axios from '@/utils/axios'; // 我们将在这里调用登录API
import router from '@/router';

// 封装一个独立的登录API请求函数
function loginApi(loginData) {
  // 注意：这里的 URL 应该和你后端的登录路由完全一致
  return axios.post('/auth/login', loginData);
}

const state = {
  // 应用初始化时，尝试从 localStorage 获取 token
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
  // 【优化】登录 action 现在会自己调用 API
  async login({ commit }, loginForm) {
    try {
      // 1. 调用后端登录接口
      const response = await loginApi(loginForm);
      
      // 2. 从响应中解构出 token 和用户信息
      //    请根据你后端实际返回的字段来修改这里！
      //    例如: const { access_token, user } = response;
      const { access_token } = response; // 假设后端返回 { "access_token": "..." }
      
      if (!access_token) {
        throw new Error('未能从响应中获取Token');
      }

      // 3. 提交 mutation 来更新 state 和 localStorage
      commit('SET_TOKEN', access_token);
      // commit('SET_USER_INFO', user); // 如果后端返回了用户信息，也一并存储

      // 4. 登录成功后跳转到主页
      router.push('/');
      return Promise.resolve(); // 表示登录成功
    } catch (error) {
      // 登录失败时，确保 token 被清空
      commit('SET_TOKEN', null);
      commit('SET_USER_INFO', null);
      return Promise.reject(error); // 将错误继续抛出，以便组件可以捕获
    }
  },

  // 登出
  logout({ commit }) {
    commit('SET_TOKEN', null);
    commit('SET_USER_INFO', null);
    // 跳转到登录页，并强制刷新页面以确保所有状态都被重置
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
