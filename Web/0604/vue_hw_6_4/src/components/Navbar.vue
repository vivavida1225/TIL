<template>
    <div>
        <h1>router 연습하기</h1>
        <nav>
            <RouterLink :to="{name: 'mainpage'}">Main</RouterLink>
            <span> | </span>
            <RouterLink :to="{name: 'other'}">Other</RouterLink>
            <span> | </span>
            <RouterLink :to="{name: 'students'}">students</RouterLink>
        </nav>
    </div>
</template>

<script setup>

</script>

<style scoped>

</style>