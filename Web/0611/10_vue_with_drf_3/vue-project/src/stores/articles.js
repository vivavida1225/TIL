// store/articles.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const accountStore = useAccountStore()
  // const API_URL = import.meta.env.VITE_API_URL
  
  const API_URL = 'http://127.0.0.1:8000'
  const articles = ref([])

  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        'Authorization': `Token ${accountStore.token}`
      }
    })
      .then(res => {
        console.log(res.data)
        articles.value = res.data
      })
      .catch(err => console.log(err))
  }

  return { API_URL, articles, getArticles, }
}, { persist: true })
