import { createRouter, createWebHistory } from 'vue-router'
import StudentViews from '@/views/StudentViews.vue'
import MainPage from '@/views/MainPage.vue'
import OtherView from '@/views/OtherView.vue';
import StudentDetailView from '@/views/StudentDetailView.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
     path: '/students',
     name: 'students',
     component: StudentViews
    },
    {
     path: '/',
     name: 'mainpage',
     component: MainPage
    },
    {
     path: '/other',
     name: 'other',
     component: OtherView
    },
    {
      path: '/students/:name',
      name: 'studentDetail',
      component: StudentDetailView
    }
    
  ]
})

export default router
