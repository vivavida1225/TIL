<template>
    <div>
        <h2>User View</h2>
        <h3>{{ $route.params }} User 페이지</h3>
        <h3>{{ $route.params.id }}번 User 페이지</h3>
        <h3>{{ userId }}번 User 페이지</h3>
        <hr>
        <RouterLink :to="{name: 'userProfile'}">Profile</RouterLink>
        <RouterLink :to="{name: 'userPosts'}">Posts</RouterLink>
        <hr>
        <RouterView/>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, RouterLink, RouterView } from 'vue-router'

const route = useRoute()
const userId = ref(route.params.id)


</script>

<style scoped>

</style>