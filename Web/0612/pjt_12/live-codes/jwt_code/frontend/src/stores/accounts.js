import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = import.meta.env.VITE_API_URL
  const token = ref(null)
  // const refresh = ref(null)
  // const user = ref(null)

  const router = useRouter()

  const signUp = function ({ username, password1, password2, age }) {

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, age
      }
    })
      .then(res => {
        console.log('회원 가입이 완료되었습니다.')
        logIn({ username, password: password1 })
      })
      .catch(err => console.log(err))
  }

  const logIn = function ({ username, password }) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      },
    })
      .then(res => {
        console.log('로그인이 완료되었습니다.')
        console.log(res.data)
        token.value = res.data.key
        // token.value = res.data.access   // token 저장
        // user.value = res.data.user      // 같이 전달되는 로그인 user 정보 저장
        // refresh.value = res.data.refresh
        router.push({ name: 'ArticleView' }) 
      })
      .catch(err => console.log(err))
  }

  const isLogin = computed(() => {
    return token.value ? true : false
  })


  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`
    })
      .then(res => {
        token.value = null
        user.value = null
        refresh.value = null
        router.push({ name: 'LogInView' })
      })
      .catch(err => console.log(err))
  }

  // const refreshAccessToken = function () {
  //   return axios({
  //     method: 'post',
  //     url: `${API_URL}/accounts/token/refresh/`,
  //     data: {
  //       refresh: refresh.value,
  //     }
  //   })
  //     .then(res => {
  //       // console.log(res)
  //       token.value = res.data.access
  //       return true
  //     })
  //     .catch(err => {
  //       console.log(err)
  //       return false
  //     })
  // }

  return {
    token,
    // user,
    // refresh,
    isLogin,
    signUp,
    logIn,
    logOut,
    // refreshAccessToken,
  }
}, { persist: true })