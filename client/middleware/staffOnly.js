export default function({ store, redirect }) {
  if (!store.state.auth.user.has_staff_role) {
    return redirect('/')
  }
}
