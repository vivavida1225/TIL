<script setup>
import { RouterLink, RouterView } from 'vue-router'
import MainPage from '@/views/MainPage.vue';
import OtherView from '@/views/OtherView.vue';
import Navbar from '@/components/Navbar.vue';

</script>

<template>
  <header>
    <div class="wrapper">
        <Navbar />
    </div>
  </header>

  <RouterView />
</template>

<style scoped>

</style>
