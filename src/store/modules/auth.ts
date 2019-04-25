// tslint:disable:no-shadowed-variable

import router from '@/router';
import api from '@/services/api';
import { LoginData, User, UserRole } from '@/types';
import { ActionTree, GetterTree, Module, MutationTree } from 'vuex';

function setAuthToken(token: string) {
  api.defaults.headers.common.Authorization = `Token ${token}`;
}
function delAuthToken() {
  delete api.defaults.headers.common.Authorization;
}

interface AuthState {
  token: string | null;
  user: User | null;
}

export const state: AuthState = {
  token: localStorage.getItem('user-token'),
  user: JSON.parse(localStorage.getItem('user') as string) // JSON.parse can cope with null
};

const getters: GetterTree<AuthState, {}> = {
  isAuthenticated(state): boolean {
    return !!state.token && !!state.user;
  },
  user(state): User | null {
    return state.user;
  },
  isStaff(state, getters): boolean {
    const staffRoles: UserRole[] = [UserRole.Prüfer_in, UserRole.Verwalter_in];
    return getters.isAuthenticated && getters.user && staffRoles.includes(getters.user.role);
  }
};

const mutations: MutationTree<AuthState> = {
  setToken: (state, token: string) => {
    state.token = token;
    localStorage.setItem('user-token', token);
    setAuthToken(token);
  },
  logout: (state) => {
    state.token = '';
    state.user = null;
    localStorage.removeItem('user');
    localStorage.removeItem('user-token');
    delAuthToken();
  },
  setUser: (state, user: User) => {
    localStorage.setItem('user', JSON.stringify(user));
    state.user = user;
  }
};

const actions: ActionTree<AuthState, {}> = {
  async signup({ commit, dispatch }, formData: User): Promise<User> {
    try {
      const response = await api.post('auth/registration/', formData);
      commit('setToken', response.data.key);
      return await dispatch('fetchUser');
    } catch (error) {
      commit('logout');
      throw error;
    }
  },
  async login({ commit }, formData: LoginData): Promise<User> {
    try {
      const response = await api.post('auth/login/', formData);
      commit('setToken', response.data.token.key);
      commit('setUser', response.data.user);
      return response.data.user;
    } catch (error) {
      commit('logout');
      throw error;
    }
  },
  async logout({ commit }) {
    try {
      await api.post('auth/logout/');
    } finally {
      commit('logout');
      router.push('/login');
    }
  },
  async init({ state, dispatch }) {
    if (state.token) {
      setAuthToken(state.token);
      if (!state.user) {
        await dispatch('fetchUser');
      }
    }
  },
  async fetchUser({ commit }): Promise<User> {
    try {
      const response = await api.get('auth/user/');
      commit('setUser', response.data);
      return response.data;
    } catch (error) {
      commit('logout');
      throw error;
    }
  },
  async patchUser({ commit }, payload): Promise<User> {
    const response = await api.patch('auth/user/', payload);
    commit('setUser', response.data);
    return response.data;
  },
  async usernameExists(_, payload): Promise<boolean> {
    try {
      const response = await api.get('auth/username-exists/?username=' + payload);
      return response.data.exists;
    } catch (error) {
      return false;
    }
  },
  async emailExists(_, payload): Promise<boolean> {
    try {
      const response = await api.get('auth/email-exists/?email=' + payload);
      return response.data.exists;
    } catch (error) {
      return false;
    }
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
} as Module<AuthState, {}>;
