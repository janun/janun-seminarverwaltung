import Vue from "vue";
import Vuex from "vuex";

import auth from "./modules/auth";
import alerts from "./modules/alerts";
import users from "./modules/users";
import groups from "./modules/groups";
import seminars from "./modules/seminars";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    alerts,
    users,
    groups,
    seminars
  }
});
