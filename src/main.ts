import App from "@/App.vue";
import FormGroup from "@/components/FormGroup.vue";
import FormInput from "@/components/FormInput.vue";
import FormTextarea from "@/components/FormTextarea.vue";
import router from "@/router/index";
import store from "@/store/index";
import BootstrapVue from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "bootstrap/dist/css/bootstrap.css";
import Vue from "vue";
import Vuelidate from "vuelidate";
import vuelidateErrorExtractor from "vuelidate-error-extractor";

Vue.use(vuelidateErrorExtractor, {
  // template: templates.singleErrorExtractor.Bootstrap4,
  messages: { required: "Erforderlich" },
  attributes: {
    email: "E-Mail"
  }
});

Vue.use(BootstrapVue);
Vue.use(Vuelidate);

Vue.component("FormGroup", FormGroup);
Vue.component("FormInput", FormInput);
Vue.component("FormTextarea", FormTextarea);

Vue.filter("date", (value: string) => {
  if (!value) {
    return "";
  }
  return new Date(value).toLocaleDateString();
});

Vue.filter("datetime", (value: string) => {
  if (!value) {
    return "";
  }
  const date = new Date(value).toLocaleDateString();
  const time = new Date(value).toLocaleTimeString();
  return `${date} ${time}`;
});

Vue.filter("euro", (value: number) => {
  return value.toLocaleString("de-DE", { style: "currency", currency: "EUR" });
});

Vue.filter("number", (value: number) => {
  return value.toLocaleString("de-DE");
});

store.dispatch("auth/init");

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App)
}).$mount("#app");
