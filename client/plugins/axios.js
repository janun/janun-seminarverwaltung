// logout on 401 and 403 errors
// i.e. with expired tokens
export default function({ $axios, app }) {
  $axios.onError(error => {
    const code = parseInt(error.response && error.response.status)

    if ([401, 403].includes(code)) {
      app.$auth.logout()
    }

    return Promise.reject(error)
  })
}
