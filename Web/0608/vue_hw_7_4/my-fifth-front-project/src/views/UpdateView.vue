<template>
    <div>
        <h1>데이터 수정 페이지</h1>
        <p>이름: {{ person.name }}</p>
        <p>잔고: {{ person.balance }}</p>
        <button @click="handleIncrease">+</button>

    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useBalanceStore } from '@/stores/balance'

const route = useRoute()
const personName = route.params.name

const balanceStore = useBalanceStore()

const person = computed(() => balanceStore.getPersonByName(personName))

const handleIncrease = function() {
    balanceStore.increaseBalance(personName)
}
</script>

<style scoped>

</style>