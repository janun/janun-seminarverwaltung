import axios from "axios";
import store from "@/store/index";

const api = axios.create({
  baseURL: "/api",
  timeout: 5000,
  validateStatus(status) {
    return status >= 200 && status < 400;
  }
});

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response.status === 401) {
      store.dispatch("auth/logout");
    }
    return Promise.reject(error);
  }
);

export default api;
