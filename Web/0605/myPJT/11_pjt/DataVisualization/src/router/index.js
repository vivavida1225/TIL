import { createRouter, createWebHistory } from 'vue-router'

import SportView from '@/views/SportView.vue';
import CustomDataView from '@/views/CustomDataView.vue';

const routes = [
  {
    // 사용자가 처음 진입했을 때(/) 스포츠 대시보드로 자동 리다이렉트
    path: '/',
    redirect: '/sport'
  },
  {
    path: '/sport',
    name: 'sport',
    component: SportView
  },
  {
    path: '/custom',
    name: 'custom',
    component: CustomDataView
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router
