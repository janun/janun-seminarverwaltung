import { Route } from 'vue-router';

import Dashboard from '@/views/Dashboard.vue';

import GroupList from '@/views/GroupList.vue';
import GroupDetail from '@/views/GroupDetail.vue';
import SeminarList from '@/views/SeminarList.vue';
import SeminarDetail from '@/views/SeminarDetail.vue';
import SeminarApply from '@/views/SeminarApply.vue';

import UserList from '@/views/UserList.vue';
import UserDetail from '@/views/UserDetail.vue';
import UserAdd from '@/views/UserAdd.vue';
import UserProfile from '@/views/UserProfile.vue';
import UserLogin from '@/views/UserLogin.vue';
import UserSignup from '@/views/UserSignup.vue';
import PasswordReset from '@/views/PasswordReset.vue';

import NotFound from '@/views/NotFound.vue';

const parsePk = (route: Route) => {
  const pk = Number.parseInt(route.params.pk, 10);
  if (Number.isNaN(pk)) {
    return 0;
  }
  return { pk };
};

export default [
  { path: '/', name: 'Dashboard', component: Dashboard },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin,
    meta: {
      public: true,
      onlyWhenLoggedOut: true
    }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: UserSignup,
    meta: {
      public: true
    }
  },
  {
    path: '/password-reset',
    name: 'PasswordReset',
    component: PasswordReset,
    meta: {
      public: true,
      onlyWhenLoggedOut: true
    }
  },

  {
    path: '/seminare/',
    name: 'SeminarList',
    component: SeminarList
  },
  {
    path: '/seminare/anmelden',
    name: 'SeminarApply',
    component: SeminarApply,
    meta: { title: 'Seminar anmelden' }
  },
  {
    path: '/seminare/:pk',
    name: 'SeminarDetail',
    component: SeminarDetail,
    props: parsePk
  },

  { path: '/groups', name: 'GroupList', component: GroupList },
  { path: '/gruppen/:pk', name: 'GroupDetail', component: GroupDetail, props: parsePk },

  { path: '/profile', name: 'UserProfile', component: UserProfile },
  { path: '/users', name: 'UserList', component: UserList },
  { path: '/users/add', name: 'UserAdd', component: UserAdd },
  { path: '/users/:pk', name: 'UserDetail', component: UserDetail, props: parsePk },

  {
    path: '*',
    name: '404',
    component: NotFound,
    meta: {
      public: true
    }
  }
];
