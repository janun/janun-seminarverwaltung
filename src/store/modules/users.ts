// tslint:disable:no-shadowed-variable

import api from "@/services/api";
import { User } from "@/types";
import Vue from "vue";
import { ActionTree, GetterTree, Module, MutationTree } from "vuex";

interface UserState {
  users: User[];
}

const state: UserState = {
  users: []
};

const getters: GetterTree<UserState, {}> = {
  all(state): User[] {
    return state.users;
  },
  byPk(state): (pk: User["pk"]) => User | undefined {
    return (pk) => state.users.find((user) => user.pk === pk);
  }
};

const mutations: MutationTree<UserState> = {
  setAll(state, users: User[]) {
    Vue.set(state, "users", users);
  },
  add(state, user: User) {
    state.users.unshift(user);
  },
  update(state, user: User) {
    const idx = state.users.findIndex((obj) => obj.pk === user.pk);
    if (idx > -1) {
      Vue.set(state.users, idx, user);
    }
  },
  delete(state, pk: User["pk"]) {
    const idx = state.users.findIndex((obj) => obj.pk === pk);
    if (idx > -1) {
      state.users.splice(idx, 1);
    }
  }
};

const actions: ActionTree<UserState, {}> = {
  async create({ commit }, payload: User): Promise<User> {
    const response = await api.post("users/", payload);
    commit("add", response.data);
    return response.data;
  },
  async fetchAll({ commit }): Promise<User[]> {
    const response = await api.get("users/");
    commit("setAll", response.data);
    return response.data;
  },
  async fetchSingle({ commit, getters }, pk: User["pk"]): Promise<User> {
    const response = await api.get(`users/${pk}/`);
    if (getters.byPk(pk)) {
      commit("update", response.data);
    } else {
      commit("add", response.data);
    }
    return response.data;
  },
  async delete({ commit }, pk: User["pk"]) {
    await api.delete(`users/${pk}/`);
    commit("delete", pk);
  },
  async update({ commit }, { pk, data }: { pk: User["pk"]; data: User }): Promise<User> {
    const response = await api.patch(`users/${pk}/`, data);
    commit("update", response.data);
    return response.data;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
} as Module<UserState, {}>;
