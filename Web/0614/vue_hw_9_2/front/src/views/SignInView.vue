<template>
  <div>
    <h1>로그인 페이지</h1>

    <form @submit.prevent="submitSignIn">
      <div>
        <label for="username">username : </label>
        <input type="text" id="username" v-model="username">
      </div>

      <div>
        <label for="password">password : </label>
        <input type="password" id="password" v-model="password">
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
const password = ref('')

const router = useRouter()
const authStore = useAuthStore()

const submitSignIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }

  authStore.signIn(payload)
    .then(() => {
      router.push({ name: 'home' })
    })
}
</script>

<style scoped>

</style>