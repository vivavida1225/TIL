<template>
    <div>
        <MainPage 
        :balances="balanceStore.balances"
        />
    </div>
</template>

<script setup>
import MainPage from '@/components/MainPage.vue';
import { useBalanceStore } from '@/stores/balance'


const balanceStore = useBalanceStore()

</script>

<style scoped>

</style>