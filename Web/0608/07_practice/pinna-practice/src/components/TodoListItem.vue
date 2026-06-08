<template>
    <div>
        <input type="checkbox" :id="`todo-text-${todo.id}`" v-model="isDone">
        <label :for="`todo-text-${todo.id}`"> {{ todo.text }} </label>
        <button @click="deleteTodo(todo.id)">삭제</button>
    </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { ref } from 'vue'

const store = useCounterStore()

const prop = defineProps({
                todo: Object,

            })

const deleteTodo = function (selectedId) {
    store.deleteTodo(selectedId)
}

const isDone = ref(prop.todo.isDone)

watch(isDone, () => {
    store.updateTodo(prop.todo.id)
})
</script>


<style scoped>

</style>