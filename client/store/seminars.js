import Vue from 'vue'

export const state = () => ({
  seminars: []
})

export const mutations = {
  set(state, seminars) {
    state.seminars = seminars
  },
  update(state, seminar) {
    const idx = state.seminars.findIndex(obj => obj.uuid === seminar.uuid)
    if (idx > -1) {
      Vue.set(state.seminars, idx, seminar)
    }
  },
  delete(state, uuid) {
    const idx = state.seminars.findIndex(obj => obj.uuid === uuid)
    if (idx > -1) {
      state.seminars.splice(idx, 1)
    }
  }
}

export const actions = {
  async fetch({ commit }) {
    const data = await this.$axios.$get(`/seminars/?year=2019`) // TODO: this+next year
    commit('set', data)
  }
}
