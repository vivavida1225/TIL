<template>
  <div>
    <router-link to="/" class="back-btn">
      <i class="fa-solid fa-arrow-left"></i> 뒤로가기
    </router-link>

    <h2 class="fw-bold mb-4">나중에 볼 동영상</h2>

    <!-- Empty State -->
    <div v-if="savedVideos.length === 0" class="text-muted">
      <p>등록된 비디오 없음</p>
    </div>

    <!-- Video Grid -->
    <div v-else class="row g-3">
      <div
        v-for="video in savedVideos"
        :key="video.id"
        class="col-12 col-sm-6 col-md-4 col-lg-3"
      >
        <div class="card h-100 shadow-sm border-0 saved-card">
          <img
            :src="video.thumbnail"
            :alt="video.title"
            class="card-img-top"
            style="aspect-ratio: 16/9; object-fit: cover; cursor: pointer;"
            @click="goToVideo(video.id)"
          />
          <div class="card-body d-flex flex-column">
            <p
              class="card-text fw-semibold mb-2"
              style="font-size: 0.9rem; cursor: pointer; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;"
              @click="goToVideo(video.id)"
            >
              {{ video.title }}
            </p>
            <div class="mt-auto">
              <button @click="removeVideo(video.id)" class="btn btn-sm btn-outline-danger w-100">
                <i class="fa-solid fa-trash me-1"></i>삭제
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const savedVideos = ref([])

function loadSaved() {
  savedVideos.value = JSON.parse(localStorage.getItem('mytube_saved_videos') || '[]')
}

function removeVideo(id) {
  savedVideos.value = savedVideos.value.filter(v => v.id !== id)
  localStorage.setItem('mytube_saved_videos', JSON.stringify(savedVideos.value))
}

function goToVideo(id) {
  router.push({ name: 'video-detail', params: { id } })
}

onMounted(loadSaved)
</script>

<style scoped>
.saved-card {
  transition: transform 0.2s;
}
.saved-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
}
</style>
