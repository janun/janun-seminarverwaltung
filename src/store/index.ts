import Vue from 'vue';
import Vuex from 'vuex';
import auth from './modules/auth';
import groups from './modules/groups';
import seminars from './modules/seminars';
import toasts from './modules/toasts';
import users from './modules/users';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    toasts,
    users,
    groups,
    seminars
  }
});
