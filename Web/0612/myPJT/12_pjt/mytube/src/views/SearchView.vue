<template>
  <div>
    <router-link to="/" class="back-btn">
      <i class="fa-solid fa-arrow-left"></i> 뒤로가기
    </router-link>

    <h2 class="fw-bold mb-3">비디오 검색</h2>

    <!-- Search Bar -->
    <div class="input-group mb-4" style="max-width: 600px;">
      <input
        v-model="query"
        @keyup.enter="searchVideos"
        type="text"
        class="form-control form-control-lg"
        placeholder="검색어를 입력하세요"
      />
      <button @click="searchVideos" class="btn btn-danger px-4" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
        <i v-else class="fa-solid fa-magnifying-glass me-1"></i>찾기
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="alert alert-danger">
      <i class="fa-solid fa-circle-exclamation me-2"></i>{{ error }}
    </div>

    <!-- Results Grid -->
    <div v-if="videos.length" class="row g-3">
      <div
        v-for="video in videos"
        :key="video.id.videoId"
        class="col-12 col-sm-6 col-md-4 col-lg-3"
      >
        <VideoCard :video="video" @click="goToDetail(video.id.videoId)" />
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="searched && !loading" class="text-center text-muted py-5">
      <i class="fa-solid fa-circle-xmark fs-1 mb-3"></i>
      <p>검색 결과가 없습니다.</p>
    </div>

    <!-- Initial State -->
    <div v-else-if="!searched" class="text-center text-muted py-5">
      <i class="fa-solid fa-magnifying-glass fs-1 mb-3 text-secondary opacity-50"></i>
      <p>키워드를 입력하고 검색해 보세요.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import VideoCard from '../components/VideoCard.vue'

const router = useRouter()
const query = ref('')
const videos = ref([])
const loading = ref(false)
const searched = ref(false)
const error = ref('')

const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

async function searchVideos() {
  if (!query.value.trim()) return
  loading.value = true
  searched.value = true
  error.value = ''
  videos.value = []

  try {
    const res = await axios.get('https://www.googleapis.com/youtube/v3/search', {
      params: {
        key: API_KEY,
        q: query.value,
        part: 'snippet',
        type: 'video',
        maxResults: 12,
      },
    })
    videos.value = res.data.items
  } catch (err) {
    error.value = 'API 호출 중 오류가 발생했습니다. API 키를 확인해 주세요.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function goToDetail(videoId) {
  router.push({ name: 'video-detail', params: { id: videoId } })
}
</script>
