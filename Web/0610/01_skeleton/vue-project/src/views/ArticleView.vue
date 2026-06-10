<template>
  <div>
    <h1>Article Page</h1>
    <RouterLink :to="{ name:'CreateView'}">
      [CREATE]
    </RouterLink>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { RouterLink } from 'vue-router'


</script>

<style>

</style>
