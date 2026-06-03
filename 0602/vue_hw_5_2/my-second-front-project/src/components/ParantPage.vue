<template>
    <div class="parant-card">
        <h1>부모 페이지입니다.</h1>
        <ChildPage :my-prop="item" v-for="item in children"/> 
    </div>
</template>

<script setup>
import ChildPage from '@/components/ChildPage.vue';

const children = [
    {name: '김하나', age: 30},
    {name: '김두리', age: 20},
    {name: '김서이', age: 10},
]

</script>

<style scoped>
.parant-card{
    border: 1px solid black;
    padding: 10px;
}

</style>