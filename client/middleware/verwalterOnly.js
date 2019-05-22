export default function({ store, redirect }) {
  if (!store.state.auth.user.has_verwalter_role) {
    return redirect('/')
  }
}
