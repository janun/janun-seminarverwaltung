// tslint:disable:no-shadowed-variable

import api from '@/services/api';
import { Seminar } from '@/types';
import Vue from 'vue';
import { ActionTree, GetterTree, Module, MutationTree } from 'vuex';
import { distinct } from '@/utils/utils.ts';

interface SeminarState {
  seminars: Seminar[];
  listEtag: string;
}

export const state: SeminarState = {
  seminars: [],
  listEtag: ''
};

const getters: GetterTree<SeminarState, {}> = {
  all(state): Seminar[] {
    return state.seminars;
  },
  byPk(state): (pk: Seminar['pk']) => Seminar | undefined {
    return (pk) => state.seminars.find((seminar) => seminar.pk === pk);
  },
  occuringYears(state): number[] {
    return distinct(state.seminars.map((s) => new Date(s.start_date).getFullYear())).sort();
  },
  occuringGroupNames(state): string[] {
    return distinct(state.seminars.map((s) => (s.group ? s.group.name : '- keine -'))).sort();
  }
};

const mutations: MutationTree<SeminarState> = {
  setListEtag(state, etag: string) {
    state.listEtag = etag;
  },
  setAll(state, seminars: Seminar[]) {
    Vue.set(state, 'seminars', seminars);
  },
  add(state, seminar: Seminar) {
    state.seminars.unshift(seminar);
  },
  update(state, seminar: Seminar) {
    const idx = state.seminars.findIndex((obj) => obj.pk === seminar.pk);
    if (idx > -1) {
      Vue.set(state.seminars, idx, seminar);
    }
  },
  delete(state, pk: Seminar['pk']) {
    const idx = state.seminars.findIndex((obj) => obj.pk === pk);
    if (idx > -1) {
      state.seminars.splice(idx, 1);
    }
  }
};

const actions: ActionTree<SeminarState, {}> = {
  async create({ commit }, payload: Seminar): Promise<Seminar> {
    const response = await api.post('seminars/', payload);
    commit('add', response.data);
    return response.data;
  },

  async fetchAll({ state, commit }): Promise<Seminar[]> {
    const headers = state.listEtag ? { 'If-None-Match': state.listEtag } : {};
    const response = await api.get('seminars/', { headers });
    if (response.status === 304) {
      return state.seminars;
    }
    if (response.headers.etag) {
      commit('setListEtag', response.headers.etag);
    }
    commit('setAll', response.data);
    return response.data;
  },

  async fetchSingle({ commit, getters }, pk: Seminar['pk']): Promise<Seminar> {
    const seminar = getters.byPk(pk);
    const headers = seminar ? { 'If-None-Match': seminar.etag } : {};
    const response = await api.get(`seminars/${pk}/`, { headers });
    if (response.status === 304) {
      return seminar;
    }
    if (response.headers.etag) {
      if (seminar) {
        commit('update', { ...response.data, etag: response.headers.etag });
      } else {
        commit('add', { ...response.data, etag: response.headers.etag });
      }
    }
    return response.data;
  },
  async delete({ commit }, pk: Seminar['pk']) {
    await api.delete(`seminars/${pk}/`);
    commit('delete', pk);
  },
  async update({ commit }, { pk, data }: { pk: Seminar['pk']; data: Seminar }) {
    const response = await api.patch(`seminars/${pk}/`, data);
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
} as Module<SeminarState, {}>;
