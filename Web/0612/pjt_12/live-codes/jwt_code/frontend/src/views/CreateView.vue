<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <label for="title">제목: </label>
      <input type="text" id="title" v-model.trim="title">
      <br/>
      <label for="content">내용: </label>
      <textarea type="text" id="content" v-model.trim="content"></textarea>
      <br/>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useArticleStore } from '@/stores/articles'
  import { useAccountStore } from '@/stores/accounts'
  import { useRouter } from 'vue-router'

  const store = useArticleStore()
  const accountStore = useAccountStore()
  const router = useRouter()

  const title = ref(null)
  const content = ref(null)

  const createArticle = function () {
    axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/articles/`,
      data: {
        title: title.value,
        content: content.value
      },
      headers: {
        'Authorization': `Token ${accountStore.token}`
        // 'Authorization': `Bearer ${accountStore.token}`
      },
    })        
      .then(res => {
        router.push({ name: 'ArticleView' })
      })
      .catch(err =>{
        console.log(err)

        // if (err.response?.status === 401) {
        //   console.log('Access Token 재발급 진행!')
          
        //   // access token 재발급은 비동기 요청
        //   accountStore.refreshAccessToken()
        //     .then(ok => {
        //       // 재발급에 실패한 경우 종료
        //       if (!ok) {
        //         window.alert('다시 로그인이 필요합니다.')
        //         accountStore.logOut()   // 기존에 저장된 token을 제거하기 위함
        //         router.push({ name: 'LogInView' })
        //         return 
        //       }
        //       // 재발급에 성공한 경우 재요청 진행
        //       axios({
        //         method: 'post',
        //         url: `${API_URL}/api/v1/articles/`,
        //         headers: {
        //           'Authorization': `Bearer ${accountStore.token}`
        //         },
        //         data: {
        //           title: title.value,
        //           content: content.value
        //         },
        //       })
        //         .then(res => {
        //           router.push({ name: 'ArticleView' })
        //         })
        //       })
        //   }
      })
  }

  
</script>

<style>

</style>
