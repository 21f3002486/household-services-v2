import { createStore } from 'vuex'

export default createStore({
  state: {
    is_logged_in: false,
    role: '',
    token: ''
  },
  getters: {
  },
  mutations: {
    loginUser: function(state, role, token){
      state.is_logged_in = true;
      state.role = role;
      state.token = token;
    },
    logoutUser: function(state){
      state.is_logged_in = false;
      state.role = '';
      state.token = '';
    }
  },
  actions: {
  },
  modules: {
  }
})
