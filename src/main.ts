import App from '@/App.vue';
import router from '@/router/index';
import store from '@/store/index';
import { formatDate, formatEuro, formatNumber, formatDatetime } from '@/utils/formatters.ts';
import Vue from 'vue';
import Vuelidate from 'vuelidate';
import vuelidateErrorExtractor from 'vuelidate-error-extractor';
import PortalVue from 'portal-vue';
import ModalTransition from '@/components/ModalTransition.vue';

Vue.component('ModalTransition', ModalTransition);

Vue.use(PortalVue);
Vue.use(Vuelidate);
Vue.use(vuelidateErrorExtractor, {
  messages: {
    required: 'Erforderlich',
    minStart: 'Muss nach Start-Datum liegen.',
    minPlannedAttendeesMin: 'Muss größer sein als der Mindestwert.',
    maxDuration: 'Darf nicht größer sein als die Dauer des Seminars ({max} Tage).',
    maxFunding: 'Maximal-Förderung: {maxFunding}',
    minFuture: 'Muss in der Zukunft liegen.'
  }
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
