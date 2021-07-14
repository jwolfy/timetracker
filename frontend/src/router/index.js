import Vue from 'vue'
import VueRouter from 'vue-router'
import Tasks from '@/views/Tasks.vue'
import Issues from '@/views/Issues.vue'
import Settings from '@/views/Settings.vue'
import Login from '@/views/Login.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'tasks',
    component: Tasks,
    meta: {layout: 'main', requiresAuth: true},
  },
  {
    path: '/issues',
    name: 'issues',
    component: Issues,
    meta: {layout: 'main', requiresAuth: true},
  },
  {
    path: '/settings',
    name: 'settings',
    component: Settings,
    meta: {layout: 'main', requiresAuth: true},
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {layout: 'empty'},
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (localStorage.getItem('token') == null) {
      console.log('null token');
      // next({
      //   path: '/login',
      //   params: { nextUrl: to.fullPath },
      // })
      next()
    } else {
      next()
    }
  } else {
    next();
  }
})

export default router
