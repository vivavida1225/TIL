import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

let id = 0
export const useCounterStore = defineStore('counter', () => {
const todos = ref([
  {id : id++, text: '할일 1', isDone: false},
  {id : id++, text: '할일 2', isDone: false},

])

const addTodo = function (todoText) {
  todos.value.push({
    id: id++,
    text: todoText, // user input
    isDone: false,
  })
}

const deleteTodo = function(selectedId) {
  // 방법 1
  // const index = todos.value.findIndex(todo => todo.id === selectedId)
  // todos.value.splice(index, 1)

  // 선택된 id 와 일치하지 않는 애들만 새로운 배열로 만들어 저장
  todos.value = todos.value.filter(todo => todo.id !== selectedId)
}

const updateTodo = function (updateId) {
  todos.value.forEach(todo => {
    if (todo.id === updateId) {
      todo.isDone = !todo.isDone
    }
  })
}

  return { 
    todos, 
    addTodo,
    deleteTodo,
  }
})

