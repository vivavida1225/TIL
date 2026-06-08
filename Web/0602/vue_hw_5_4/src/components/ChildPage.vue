<template>
    <div>
        <h3>자식 페이지입니다.</h3>
        <p>이름: {{ name }}</p>
        <p>나이: {{ age }}</p>
        <p>잔고: {{ balance }}</p>
        <button @click="$emit('giveMeAllowance')">용돈 주세요!!</button>
        <hr>
    </div>
</template>

<script setup>
defineProps({
    name: String,
    age: Number,
    balance: Number
})

</script>

<style scoped>

</style>