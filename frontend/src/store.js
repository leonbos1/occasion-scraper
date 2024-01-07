import { createStore } from 'vuex';

export default createStore({
  state: {
    token: '',
    role: '0',
  },
  mutations: {
    setToken(state, value) {
      state.token = value;
    },
    setRole(state, value) {
      state.role = value;
    },
  },
});