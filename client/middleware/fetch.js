export default function({ store }) {
  if (store.state.auth.loggedIn) {
    store.dispatch('seminars/fetch')
    store.dispatch('users/fetch')
  }
}
