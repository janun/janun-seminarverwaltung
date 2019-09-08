// Populate stores
export default function({ store }) {
  if (store.state.auth.loggedIn) {
    store.dispatch('seminars/fetch')
    store.dispatch('groups/fetch')

    if (store.state.auth.user.has_staff_role) {
      store.dispatch('users/fetch')
    }
  }
}
