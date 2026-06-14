import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ArticleCreateView from '../views/ArticleCreateView.vue'
import SignUpView from '../views/SignUpView.vue'
import SignInView from '../views/SignInView.vue'

const publicPages = ['signin', 'signup']  // 비로그인도 접근가능

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

// 전역 가드
router.beforeEach((to, from) => {
  const auth = JSON.parse(localStorage.getItem('auth'))

  const isAuthenticated = auth?.isAuthenticated
  const isPublicPage = publicPages.includes(to.name)

  if (!isAuthenticated && !isPublicPage) {
    return { name: 'signin' }
  }
})


export default router
