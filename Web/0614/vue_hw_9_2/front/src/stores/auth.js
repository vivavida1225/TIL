import axios from "axios"
import { ref, computed } from 'vue'
import { defineStore } from "pinia"

export const useAuthStore = defineStore('auth', () => {
    const savedAuth = JSON.parse(localStorage.getItem('auth'))

    const token = ref(savedAuth?.token || null)

    const isAuthenticated = computed(() => {
        return token.value !== null
    })

    const saveToken = function (newToken) {
    token.value = newToken

    localStorage.setItem('auth', JSON.stringify({
      token: newToken,
      isAuthenticated: true
    }))
  }

  const signUp = function ({ username, password1, password2 }) {
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/signup/',
      data: {
        username,
        password1,
        password2
      }
    })
    .then((res) => {
      saveToken(res.data.key)
    }).catch((err) => {console.log(err.response.data)})
  }

  const signIn = function ({ username, password }) {
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/login/',
      data: {
        username,
        password
      }
    })
    .then((res) => {
      saveToken(res.data.key)
    })
  }

  return {
    token,
    isAuthenticated,
    signUp,
    signIn
  }
})