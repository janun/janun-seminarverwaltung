import Vue from 'vue';
import Vuex from 'vuex';
import auth from './modules/auth';
import groups from './modules/groups';
import seminars from './modules/seminars';
import toasts from './modules/toasts';
// import alerts from './modules/alerts';
import users from './modules/users';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    // alerts,
    toasts,
    users,
    groups,
    seminars
  }
});
