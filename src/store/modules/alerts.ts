// tslint:disable:no-shadowed-variable

import { Alert } from "@/types";
import { ActionTree, GetterTree, Module, MutationTree } from "vuex";

interface AlertsState {
  alerts: Alert[];
}

export const state: AlertsState = {
  alerts: []
};

const getters: GetterTree<AlertsState, {}> = {
  all(state): Alert[] {
    return state.alerts;
  }
};

const mutations: MutationTree<AlertsState> = {
  add(state, alert: Alert) {
    alert.id = Date.now();
    state.alerts.push(alert);
  },
  delete(state, index: number) {
    state.alerts.splice(index, 1);
  }
};

const actions: ActionTree<AlertsState, {}> = {};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
} as Module<AlertsState, {}>;
