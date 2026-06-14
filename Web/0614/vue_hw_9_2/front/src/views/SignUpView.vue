<template>
    <div>
        <h1>회원 가입 페이지</h1>
        <form @submit.prevent="submitSignUp">
            <div>
                <label for="username">username: </label>
                <input type="text" id="username" v-model="username">
            </div>
            <div>
                <label for="password1">password: </label>
                <input type="password" id="password1" v-model="password1">
            </div>
            <div>
                <label for="password2">password confirmation: </label>
                <input type="password" id="password2" v-model="password2">
            </div>

            <button type="submit">submit</button>

        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password1 = ref('')
const password2 = ref('')

const router = useRouter()
const authStore = useAuthStore()

const submitSignUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }

  authStore.signUp(payload)
    .then(() => {
      router.push({ name: 'home' })
    })
    .catch((err) => {
        console.log(err)
    })
}


// const submitSignUp = async function () {
//   const payload = {
//     username: username.value,
//     password1: password1.value,
//     password2: password2.value
//   }

//   try {
//     // 1. 회원가입 요청이 성공하고 토큰이 저장될 때까지 얌전히 기다립니다.
//     await authStore.signUp(payload)
    
//     // 2. 가입 및 로그인 처리가 끝나면 무사히 홈 화면으로 이동합니다.
//     router.push({ name: 'home' })
    
//   } catch (err) {
//     // 3. 비밀번호 불일치, 중복 아이디 등 에러가 나면 이쪽으로 튕겨와 에러를 찍습니다.
//     console.log(err)
//   }
// }

</script>

<style scoped>

</style>