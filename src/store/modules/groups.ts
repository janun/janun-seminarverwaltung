// tslint:disable:no-shadowed-variable

import Vue from 'vue';
import { Module, GetterTree, MutationTree, ActionTree } from 'vuex';
import { Group } from '@/types';

import api from '@/services/api';

interface GroupState {
  groups: Group[];
}

const state: GroupState = {
  groups: []
};

const getters: GetterTree<GroupState, {}> = {
  all(state) {
    return state.groups;
  },
  byPk(state): (pk: number) => Group | undefined {
    return (pk) => state.groups.find((group) => group.pk === pk);
  }
};

const mutations: MutationTree<GroupState> = {
  setAll(state, groups: Group[]) {
    Vue.set(state, 'groups', groups);
  },
  add(state, group: Group) {
    state.groups.unshift(group);
  },
  update(state, group: Group) {
    const idx = state.groups.findIndex((obj) => obj.pk === group.pk);
    if (idx > -1) {
      Vue.set(state.groups, idx, group);
    }
  },
  delete(state, pk: Group['pk']) {
    const idx = state.groups.findIndex((obj) => obj.pk === pk);
    if (idx > -1) {
      state.groups.splice(idx, 1);
    }
  }
};

const actions: ActionTree<GroupState, {}> = {
  async create({ commit }, payload: Group): Promise<Group> {
    const response = await api.post('groups/', payload);
    commit('add', response.data);
    return response.data;
  },
  async fetchAll({ commit }): Promise<Group[]> {
    const response = await api.get('groups/');
    commit('setAll', response.data);
    return response.data;
  },
  async fetchSingle({ commit, getters }, pk: Group['pk']): Promise<Group> {
    const response = await api.get(`groups/${pk}/`);
    if (getters.byPk(pk)) {
      commit('update', response.data);
    } else {
      commit('add', response.data);
    }
    return response.data;
  },
  async delete({ commit }, pk: Group['pk']) {
    await api.delete(`groups/${pk}/`);
    commit('delete', pk);
  },
  async update({ commit }, { pk, data }: { pk: Group['pk']; data: Group }): Promise<Group> {
    const response = await api.patch(`groups/${pk}/`, data);
    commit('update', response.data);
    return response.data;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
} as Module<GroupState, {}>;
