<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink> | 
        <template v-if="!authStore.isAuthenticated">
        <RouterLink :to="{name: 'signup'}">SignUp</RouterLink> | 
        <RouterLink :to="{name: 'signin'}">SignIn</RouterLink> | 
        </template>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
</style>
