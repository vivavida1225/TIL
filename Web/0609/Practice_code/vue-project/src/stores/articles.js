// store/articles.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`, // 후행 슬래쉬 빼먹지 말기!!
    })
      .then(res => {
        // console.log(res)
        // console.log(res.data)    
        articles.value = res.data    
      })
      .catch(err => {
        console.log(err)
      })
  }

  return { 
    articles,
    API_URL,
    
    getArticles,
  }
}, { persist: true })
