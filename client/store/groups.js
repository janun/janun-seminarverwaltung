export const state = () => ({
  groups: []
})

export const mutations = {
  set(state, groups) {
    state.groups = groups
  }
}

export const actions = {
  async fetch({ commit }) {
    const data = await this.$axios.$get(`/group_names/`)
    commit('set', data)
  }
}
