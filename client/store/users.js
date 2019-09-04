// import Vue from 'vue'

export const state = () => ({
  users: []
})

export const mutations = {
  set(state, users) {
    state.users = users
  }
}

export const actions = {
  async fetch({ commit }) {
    const data = await this.$axios.$get('/users/')
    commit('set', data)
  }
}
