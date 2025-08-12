const state = {
  token: localStorage.getItem('token') || null,
  userInfo: JSON.parse(localStorage.getItem('userInfo')) || null
};

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token;
    localStorage.setItem('token', token);
  },
  SET_USER_INFO(state, userInfo) {
    state.userInfo = userInfo;
    localStorage.setItem('userInfo', JSON.stringify(userInfo));
  },
  CLEAR_USER_STATE(state) {
    state.token = null;
    state.userInfo = null;
    localStorage.removeItem('token');
    localStorage.removeItem('userInfo');
  }
};

const actions = {
  // 登录
  login({ commit }, { token, userInfo }) {
    commit('SET_TOKEN', token);
    commit('SET_USER_INFO', userInfo);
  },
  // 登出
  logout({ commit }) {
    commit('CLEAR_USER_STATE');
  }
};

const getters = {
  isAuthenticated: state => !!state.token,
  currentUser: state => state.userInfo
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
