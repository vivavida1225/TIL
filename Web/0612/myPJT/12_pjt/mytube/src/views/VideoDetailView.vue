<template>
  <div>
    <router-link to="/search" class="back-btn">
      <i class="fa-solid fa-arrow-left"></i> 뒤로가기
    </router-link>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-danger" role="status"></div>
      <p class="mt-3 text-muted">영상 정보를 불러오는 중...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="fa-solid fa-circle-exclamation me-2"></i>{{ error }}
    </div>

    <!-- Video Content -->
    <div v-else-if="video">
      <h2 class="fw-bold mb-1">{{ video.snippet.title }}</h2>
      <p class="text-muted mb-3">
        <i class="fa-regular fa-calendar me-1"></i>
        업로드 날짜: {{ formatDate(video.snippet.publishedAt) }}
      </p>

      <!-- Embedded Player -->
      <div class="ratio ratio-16x9 mb-4" style="max-width: 900px;">
        <iframe
          :src="`https://www.youtube.com/embed/${videoId}`"
          allowfullscreen
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        ></iframe>
      </div>

      <!-- Description -->
      <p class="text-muted mb-4" style="white-space: pre-wrap; max-width: 900px;">
        {{ video.snippet.description }}
      </p>

      <!-- Action Buttons -->
      <div class="d-flex gap-2 flex-wrap">
        <button @click="toggleSaveVideo" class="btn btn-lg" :class="isSaved ? 'btn-secondary' : 'btn-dark'">
          <i class="fa-solid me-2" :class="isSaved ? 'fa-bookmark' : 'fa-bookmark'"></i>
          {{ isSaved ? '저장 취소' : '동영상 저장' }}
        </button>
        <button @click="toggleSaveChannel" class="btn btn-lg" :class="isChannelSaved ? 'btn-warning' : 'btn-outline-warning'">
          <i class="fa-solid fa-tv me-2"></i>
          {{ isChannelSaved ? '채널 저장됨' : '채널 저장' }}
        </button>
      </div>

      <!-- Toast Notification -->
      <div v-if="toast.show" class="position-fixed bottom-0 end-0 p-3" style="z-index: 1100;">
        <div class="toast show align-items-center text-white border-0"
             :class="toast.type === 'success' ? 'bg-success' : 'bg-secondary'">
          <div class="d-flex">
            <div class="toast-body">
              <i class="fa-solid fa-circle-check me-2"></i>{{ toast.message }}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto"
                    @click="toast.show = false"></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const videoId = route.params.id
const video = ref(null)
const loading = ref(false)
const error = ref('')
const toast = ref({ show: false, message: '', type: 'success' })

const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

const isSaved = computed(() => {
  const saved = JSON.parse(localStorage.getItem('mytube_saved_videos') || '[]')
  return saved.some(v => v.id === videoId)
})

const isChannelSaved = computed(() => {
  if (!video.value) return false
  const channels = JSON.parse(localStorage.getItem('mytube_saved_channels') || '[]')
  return channels.some(c => c.id === video.value.snippet.channelId)
})

async function fetchVideoDetail() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get('https://www.googleapis.com/youtube/v3/videos', {
      params: {
        key: API_KEY,
        id: videoId,
        part: 'snippet',
      },
    })
    if (res.data.items.length === 0) {
      error.value = '영상 정보를 찾을 수 없습니다.'
    } else {
      video.value = res.data.items[0]
    }
  } catch (err) {
    error.value = '영상 정보를 불러오는 중 오류가 발생했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function toggleSaveVideo() {
  const saved = JSON.parse(localStorage.getItem('mytube_saved_videos') || '[]')
  const idx = saved.findIndex(v => v.id === videoId)
  if (idx === -1) {
    saved.push({
      id: videoId,
      title: video.value.snippet.title,
      thumbnail: video.value.snippet.thumbnails.medium?.url || video.value.snippet.thumbnails.default?.url,
    })
    showToast('나중에 볼 영상에 저장되었습니다.', 'success')
  } else {
    saved.splice(idx, 1)
    showToast('저장이 취소되었습니다.', 'secondary')
  }
  localStorage.setItem('mytube_saved_videos', JSON.stringify(saved))
}

function toggleSaveChannel() {
  if (!video.value) return
  const channels = JSON.parse(localStorage.getItem('mytube_saved_channels') || '[]')
  const channelId = video.value.snippet.channelId
  const channelTitle = video.value.snippet.channelTitle
  const idx = channels.findIndex(c => c.id === channelId)
  if (idx === -1) {
    channels.push({ id: channelId, title: channelTitle })
    showToast(`${channelTitle} 채널이 저장되었습니다.`, 'success')
  } else {
    channels.splice(idx, 1)
    showToast('채널 저장이 취소되었습니다.', 'secondary')
  }
  localStorage.setItem('mytube_saved_channels', JSON.stringify(channels))
}

function showToast(message, type) {
  toast.value = { show: true, message, type }
  setTimeout(() => { toast.value.show = false }, 3000)
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('ko-KR')
}

onMounted(fetchVideoDetail)
</script>
