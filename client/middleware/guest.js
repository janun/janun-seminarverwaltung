// useful for login and register views
export default function({ store, redirect }) {
  if (store.state.auth.loggedIn) {
    return redirect('/')
  }
}
