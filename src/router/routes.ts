import { Route } from "vue-router";

import Dashboard from "@/views/Dashboard.vue";
import Login from "@/views/Login.vue";
// import Signup from "@/views/Signup.vue";
// import PasswordReset from "@/views/PasswordReset.vue";
// import Profile from "@/views/Profile.vue";
// import ApplyWizard from "@/views/ApplyWizard.vue";
import GroupList from "@/views/GroupList.vue";
// import GroupDetail from '@/views/GroupDetail.vue'
import SeminarList from "@/views/SeminarList.vue";
import SeminarDetail from "@/views/SeminarDetail.vue";
import UserList from "@/views/UserList.vue";
// import UserDetail from '@/views/UserDetail.vue'
// import NotFound from "@/views/NotFound.vue";

const parsePk = (route: Route) => {
  const pk = Number.parseInt(route.params.pk, 10);
  if (Number.isNaN(pk)) {
    return 0;
  }
  return { pk };
};

export default [
  { path: "/", name: "Dashboard", component: Dashboard },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: {
      public: true,
      onlyWhenLoggedOut: true
    }
  },
  // {
  //   path: "/signup",
  //   name: "signup",
  //   component: Signup,
  //   meta: {
  //     public: true
  //   }
  // },
  // {
  //   path: "/password-reset",
  //   name: "password-reset",
  //   component: PasswordReset,
  //   meta: {
  //     public: true,
  //     onlyWhenLoggedOut: true
  //   }
  // },

  {
    path: "/seminare/",
    name: "SeminarList",
    component: SeminarList
  },
  // { path: "/seminare/anmelden", name: "seminar-apply", component: ApplyWizard },
  {
    path: "/seminare/:pk",
    name: "SeminarDetail",
    component: SeminarDetail,
    props: parsePk
  },

  { path: "/groups", name: "GroupList", component: GroupList },
  // // { path: '/gruppen/:pk', name: 'group-detail', component: GroupDetail, props: true },

  // { path: "/profil", name: "profile", component: Profile },
  { path: "/users", name: "UserList", component: UserList }
  // // { path: '/users/:pk', name: 'user-detail', component: UserDetail, props: True },

  // {
  //   path: "*",
  //   name: "404",
  //   component: NotFound,
  //   meta: {
  //     public: true
  //   }
  // }
];
