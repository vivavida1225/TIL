<template>
    <div>
        <h2>pinia 연습하기</h2>
        <ParentPage
        v-for="family in familyInfo"
        :key="family.familyName"
        :family="family"
        />
    </div>
</template>

<script setup>
import ParentPage from './ParentPage.vue';
import { useFamilyStore } from '@/stores/family.js'

const familyStore = useFamilyStore()
const familyInfo = familyStore.familyinfo

</script>

<style scoped>

</style>