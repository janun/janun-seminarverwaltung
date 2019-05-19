export const state = () => ({
  toasts: []
})

export const mutations = {
  add(state, toast) {
    state.toasts.push(toast)
  },

  delete(state, id) {
    const index = state.toasts.findIndex(t => t.id === id)
    state.toasts.splice(index, 1)
  }
}

export const actions = {
  toast({ commit }, newToast) {
    if (typeof newToast === 'string') {
      newToast = { text: newToast }
    }

    if (!newToast.duration) {
      newToast.duration = 4000
    }

    const id = Date.now()
    newToast.id = id

    setTimeout(() => {
      commit('delete', id)
    }, newToast.duration)

    commit('add', newToast)
  }
}
