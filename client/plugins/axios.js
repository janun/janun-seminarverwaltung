// logout on 401 error
// i.e. with expired tokens
export default function({ $axios, app }) {
  $axios.onError(error => {
    const code = parseInt(error.response && error.response.status)

    if (code === 401) {
      app.$auth.logout()
    }

    return Promise.reject(error)
  })
}
