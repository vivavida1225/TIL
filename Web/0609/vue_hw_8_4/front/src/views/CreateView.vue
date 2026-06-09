<template>
  <div>
    <h1>게시글 생성 페이지</h1>
    <form @submit.prevent="createArticle">
      <label for="title">제목: </label>
      <input type="text" id="title" v-model.trim="title">
      <br>
      <label for="content">내용: </label>
      <textarea id="content" v-model.trim="content"></textarea>
      <br>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ArticleList from '../components/ArticleList.vue'
import axios from 'axios'
import { useArticleStore } from '@/stores/articles'
import { useRouter } from 'vue-router'

const title = ref(null)
const content = ref(null)

const store = useArticleStore()
const router = useRouter()

const createArticle = function () {
  axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/api/v1/articles/',
    data: {
      title: title.value,
      content: content.value
    }
  })
  .then(() => {
    router.push({name: 'home'})
  })
  .catch(err => console.log(err))
}
</script>

<style lang="scss" scoped>

</style>