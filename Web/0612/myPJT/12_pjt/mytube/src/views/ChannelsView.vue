<template>
  <div>
    <router-link to="/" class="back-btn">
      <i class="fa-solid fa-arrow-left"></i> 뒤로가기
    </router-link>

    <h2 class="fw-bold mb-4">좋아하는 채널</h2>

    <!-- Empty State -->
    <div v-if="channels.length === 0" class="text-muted">
      <p>등록된 채널 없음</p>
    </div>

    <!-- Channel List -->
    <div v-else class="row g-3">
      <div
        v-for="channel in channels"
        :key="channel.id"
        class="col-12 col-sm-6 col-md-4"
      >
        <div class="card shadow-sm border-0 channel-card">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="channel-avatar bg-danger text-white d-flex align-items-center justify-content-center rounded-circle flex-shrink-0">
              {{ channel.title.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-grow-1 overflow-hidden">
              <p class="fw-semibold mb-0 text-truncate">{{ channel.title }}</p>
              <small class="text-muted">{{ channel.id }}</small>
            </div>
            <button @click="removeChannel(channel.id)" class="btn btn-sm btn-outline-danger flex-shrink-0">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const channels = ref([])

function loadChannels() {
  channels.value = JSON.parse(localStorage.getItem('mytube_saved_channels') || '[]')
}

function removeChannel(id) {
  channels.value = channels.value.filter(c => c.id !== id)
  localStorage.setItem('mytube_saved_channels', JSON.stringify(channels.value))
}

onMounted(loadChannels)
</script>

<style scoped>
.channel-avatar {
  width: 48px;
  height: 48px;
  font-size: 1.2rem;
  font-weight: 700;
}
.channel-card {
  transition: transform 0.2s;
}
.channel-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.1) !important;
}
</style>
