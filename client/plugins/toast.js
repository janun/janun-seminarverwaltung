export default ({ store }, inject) => {
  inject('toast', toast => store.dispatch('toasts/toast', toast))
}
