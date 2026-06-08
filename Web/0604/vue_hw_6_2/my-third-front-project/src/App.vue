<template>
    <div>
        <MainPage />
        <nav>
            <RouterLink to="/">Some</RouterLink>
            <span> | </span>
            <RouterLink to="/other">Other</RouterLink>
            <!-- or 
            <RouterLink :to="{ name: 'some' }">Some</RouterLink>
            <span> | </span>
            <RouterLink :to="{ name: 'other' }">Other</RouterLink>   -->
        </nav>
        <RouterView />
    </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import MainPage from '@/components/MainPage.vue';

</script>

<style scoped>

</style>