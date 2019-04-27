import Vue from 'vue';
import Router from 'vue-router';
import store from '@/store/index';
import routes from './routes';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { x: 0, y: 0 };
    }
  }
});

// title tag
router.afterEach((to, from) => {
  Vue.nextTick(() => {
    if (to.meta.title) {
      document.title = to.meta.title;
    } else {
      document.title = 'JANUN Seminarverwaltung';
    }
  });
});

// access control
router.beforeEach((to, from, next) => {
  const isPublic = to.matched.some((record) => record.meta.public);
  const onlyWhenLoggedOut = to.matched.some((record) => record.meta.onlyWhenLoggedOut);
  const loggedIn = store.getters['auth/isAuthenticated'];

  if (!isPublic && !loggedIn) {
    return next({
      path: '/login',
      query: { redirect: to.fullPath }
    });
  }
  if (loggedIn && onlyWhenLoggedOut) {
    return next('/');
  }
  next();
});

export default router;
