import App from '@/App.vue';
import router from '@/router/index';
import store from '@/store/index';
import { formatDate, formatEuro, formatNumber, formatDatetime } from '@/utils/formatters.ts';
import Vue from 'vue';
import Vuelidate from 'vuelidate';
import vuelidateErrorExtractor from 'vuelidate-error-extractor';

Vue.use(Vuelidate);
Vue.use(vuelidateErrorExtractor, {
  messages: { required: 'Erforderlich' }
});

Vue.filter('date', (value: string) => {
  return value ? formatDate(value) : '';
});
Vue.filter('datetime', (value: string) => {
  return value ? formatDatetime(value) : '';
});
Vue.filter('euro', formatEuro);
Vue.filter('number', formatNumber);

store.dispatch('auth/init');

Vue.config.productionTip = false;

Vue.prototype.$toast = (text: string, options: object) => {
  store.dispatch('toasts/toast', { text, ...options });
};

new Vue({
  router,
  store,
  render: (h) => h(App)
}).$mount('#app');
