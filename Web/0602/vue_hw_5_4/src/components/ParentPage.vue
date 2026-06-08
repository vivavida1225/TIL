<template>
    <div>
        <h2>부모 페이지입니다.</h2>
        <hr>
        <ChildPage
        @giveMeAllowance="updateBalance(child)"
        v-for="child in children"
        :key="child.name"
        :name="child.name"
        :age="child.age"
        :balance="child.balance" 
        />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import ChildPage from '@/components/ChildPage.vue';

const children = ref([
    {name: '김하나', age: 30, balance: 100000},
    {name: '김두리', age: 20, balance: 10000},
    {name: '김서이', age: 10, balance: 1000}
])

const updateBalance = function(child) {
    child.balance += 1000
    console.log('잔고 증가!!')
}

</script>

<style scoped>

</style>