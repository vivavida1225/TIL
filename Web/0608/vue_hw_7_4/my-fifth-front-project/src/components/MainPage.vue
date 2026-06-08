<template>
    <div>
        <h1>메인 페이지</h1>
        <div
        v-for="person in balances"
        :key="person.name"
        >
        <p>이름: {{ person.name }}</p>
        <p>잔고: {{ person.balance }}</p>
        <button 
        class="update-button"
        @click=goToUpdate(person.name)>
        updateBalance</button>
        <hr>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const props = defineProps({
    balances: Array
})

const goToUpdate = function (personName) {
    router.push({
        name: 'update',
        params: { name: personName }
    })
}
</script>

<style scoped>
.update-button {
    background-color: blue;
    border: 0px;
    border-radius: 5px;
    color: white;
    cursor: pointer;
}

</style>