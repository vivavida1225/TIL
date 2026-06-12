<template>
  <div class="card h-100 shadow-sm border-0 video-card" @click="$emit('click')">
    <div class="thumbnail-wrap">
      <img
        :src="video.snippet.thumbnails.medium?.url || video.snippet.thumbnails.default?.url"
        :alt="video.snippet.title"
        class="card-img-top"
        style="aspect-ratio: 16/9; object-fit: cover;"
      />
      <div class="play-overlay">
        <i class="fa-solid fa-circle-play"></i>
      </div>
    </div>
    <div class="card-body p-2">
      <p
        class="card-title fw-semibold mb-1"
        style="font-size: 0.88rem; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;"
      >
        {{ video.snippet.title }}
      </p>
      <p class="card-text text-muted mb-0" style="font-size: 0.78rem;">
        <i class="fa-solid fa-user me-1"></i>{{ video.snippet.channelTitle }}
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  video: {
    type: Object,
    required: true,
  },
})
defineEmits(['click'])
</script>

<style scoped>
.video-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
}
.thumbnail-wrap {
  position: relative;
  overflow: hidden;
}
.play-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  opacity: 0;
  transition: opacity 0.2s;
  font-size: 3rem;
  color: rgba(255, 255, 255, 0.9);
}
.video-card:hover .play-overlay {
  opacity: 1;
}
</style>
