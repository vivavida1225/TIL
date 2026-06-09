<template>
  <div>
    <h2>Detail</h2>
    <div v-if="article">
      <p>글 번호: {{ article.id  }}</p>
      <p>글 제목: {{ article.title  }}</p>
      <p>글 내용: {{ article.content  }}</p>
      <p>작성 시간: {{ article.created_at }}</p>

    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useArticleStore } from '@/stores/articles'
import { useRoute } from 'vue-router'
import axios from 'axios'

const store = useArticleStore()
const route = useRoute()

const article = ref(null)

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`
  })
  .then(res => {
    // console.log(res.data)
    article.value = res.data
  })
  .catch(err => {
    console.log(err)
  })
})

</script>

<style>

</style>
