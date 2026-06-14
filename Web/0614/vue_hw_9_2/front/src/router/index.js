import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ArticleCreateView from '../views/ArticleCreateView.vue'
import SignUpView from '../views/SignUpView.vue'
import SignInView from '../views/SignInView.vue'


const onlyGuest = function (to, from) {
  const auth = JSON.parse(localStorage.getItem('auth'))

  if (auth?.isAuthenticated) {
    return { name: 'home' }
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/create',
      name: 'create',
      component: ArticleCreateView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      beforeEnter: onlyGuest
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignInView,
      beforeEnter: onlyGuest
    }

  ]
})

export default router
