import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '../views/SearchView.vue'
import VideoDetailView from '../views/VideoDetailView.vue'
import SavedView from '../views/SavedView.vue'
import ChannelsView from '../views/ChannelsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/search', name: 'search', component: SearchView },
    { path: '/video/:id', name: 'video-detail', component: VideoDetailView },
    { path: '/saved', name: 'saved', component: SavedView },
    { path: '/channels', name: 'channels', component: ChannelsView },
  ],
})

export default router
