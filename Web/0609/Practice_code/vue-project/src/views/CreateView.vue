<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <label for="title">제목: </label>
      <input id="title" type="text" v-model.trim="title"> <br>
      <label for="content">내용: </label>
      <textarea id="content" v-model.trim="content"></textarea>
      <input type="submit" value="">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/articles'
import axios from 'axios'

const router = useRouter()
const store = useArticleStore()

const title = ref(null)
const content = ref(null)

const createArticle = function () {
  console.log(title.value, content.value)
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/articles/`,
    data: {
      title: title.value,
      content: content.value,
    },
  })
    .then(() => {
      router.push({ name: 'ArticleView' })
    })
    .catch(err => {
      console.log(err)
    })
}

</script>

<style>

</style>
