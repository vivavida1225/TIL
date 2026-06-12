<template>
  <div class="home-view text-center py-5">
    <div class="hero-icon mb-4">
      <i class="fa-brands fa-youtube" style="font-size: 5rem; color: #dc3545;"></i>
    </div>
    <h1 class="display-5 fw-bold mb-3">관심 종목 영상 검색 서비스</h1>
    <p class="lead text-muted mb-4">
      YouTube에서 관심 있는 주제의 영상을 검색하고,<br>
      나중에 볼 영상과 좋아하는 채널을 저장해 보세요.
    </p>
    <div class="d-flex justify-content-center gap-3 flex-wrap">
      <router-link to="/search" class="btn btn-danger btn-lg px-5">
        <i class="fa-solid fa-magnifying-glass me-2"></i>영상 검색하기
      </router-link>
      <router-link to="/saved" class="btn btn-outline-secondary btn-lg px-4">
        <i class="fa-regular fa-clock me-2"></i>나중에 볼 영상 ({{ savedCount }})
      </router-link>
      <router-link to="/channels" class="btn btn-outline-secondary btn-lg px-4">
        <i class="fa-solid fa-tv me-2"></i>저장된 채널 ({{ channelCount }})
      </router-link>
    </div>

    <div class="features-grid mt-5 row g-4 justify-content-center">
      <div class="col-md-4">
        <div class="card h-100 shadow-sm border-0">
          <div class="card-body p-4">
            <i class="fa-solid fa-magnifying-glass fs-2 text-danger mb-3"></i>
            <h5 class="card-title fw-bold">실시간 영상 검색</h5>
            <p class="card-text text-muted">
              YouTube API를 통해 원하는 키워드의 최신 영상을 실시간으로 검색합니다.
            </p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card h-100 shadow-sm border-0">
          <div class="card-body p-4">
            <i class="fa-regular fa-clock fs-2 text-primary mb-3"></i>
            <h5 class="card-title fw-bold">나중에 볼 영상 저장</h5>
            <p class="card-text text-muted">
              관심 있는 영상을 로컬에 저장해 두고 언제든지 다시 확인할 수 있습니다.
            </p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card h-100 shadow-sm border-0">
          <div class="card-body p-4">
            <i class="fa-solid fa-tv fs-2 text-success mb-3"></i>
            <h5 class="card-title fw-bold">채널 즐겨찾기</h5>
            <p class="card-text text-muted">
              좋아하는 채널을 저장하고 목록으로 한눈에 관리합니다.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const savedCount = computed(() => {
  const saved = localStorage.getItem('mytube_saved_videos')
  return saved ? JSON.parse(saved).length : 0
})

const channelCount = computed(() => {
  const channels = localStorage.getItem('mytube_saved_channels')
  return channels ? JSON.parse(channels).length : 0
})
</script>

<style scoped>
.hero-icon {
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.08); }
}
</style>
