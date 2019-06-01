export const state = () => ({
  messages: []
})

export const mutations = {
  add(state, message) {
    state.messages.push(message)
  },

  delete(state, id) {
    const index = state.messages.findIndex(t => t.id === id)
    state.messages.splice(index, 1)
  }
}

export const actions = {
  message({ commit }, newMessage) {
    if (typeof newMessage === 'string') {
      newMessage = { text: newMessage }
    }

    const id = Date.now()
    newMessage.id = id

    commit('add', newMessage)
  }
}
