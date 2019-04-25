// tslint:disable:no-shadowed-variable

import { Toast } from '@/types';
import { ActionTree, GetterTree, Module, MutationTree } from 'vuex';

interface ToastsState {
  toasts: Toast[];
}

export const state: ToastsState = {
  toasts: []
};

const getters: GetterTree<ToastsState, {}> = {
  all(state): Toast[] {
    return state.toasts;
  }
};

const mutations: MutationTree<ToastsState> = {
  add(state, toast: Toast) {
    state.toasts.push(toast);
  },

  delete(state, id: number) {
    const index = state.toasts.findIndex((t) => t.id === id);
    state.toasts.splice(index, 1);
  }
};

const actions: ActionTree<ToastsState, {}> = {
  toast({ commit }, newToast: Toast | string) {
    if (typeof newToast === 'string') {
      newToast = { text: newToast };
    }

    if (!newToast.duration) {
      newToast.duration = 2000;
    }

    const id = Date.now();
    newToast.id = id;

    setTimeout(() => {
      commit('delete', id);
    }, newToast.duration);

    commit('add', newToast);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
} as Module<ToastsState, {}>;
