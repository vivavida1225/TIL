// store/articles.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const accountStore = useAccountStore()

  const API_URL = import.meta.env.VITE_API_URL
  const articles = ref([])

  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        'Authorization': `Token ${accountStore.token}`
        // 'Authorization': `Bearer ${accountStore.token}`
      },
    })
      .then(res => {
        // console.log(res.data)
        articles.value = res.data
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
        //         method: 'get',
        //         url: `${API_URL}/api/v1/articles/`,
        //         headers: {
        //           'Authorization': `Bearer ${accountStore.token}`
        //         },
        //       })
        //         .then(res => {
        //           articles.value = res.data
        //         })
        //       })
        //   }
      })
  }

  return { API_URL, articles, getArticles, }
}, { persist: true })
