<template>
    <div class="child-card">
        <h3>자식 페이지입니다.</h3>
        <p> 이름: {{ myProp.name }} </p>
        <p> 나이: {{ myProp.age }} </p>
    </div>
</template>

<script setup>
    defineProps({
        myProp: Object
    })
</script>

<style scoped>
.child-card {
    border: 1px solid black;
    margin-bottom: 10px;
}

</style>