import { defineStore } from "pinia"
import { ref, computed } from "vue"

export const useBalanceStore = defineStore ('balance', () => {
    const balances = ref([
            {
    name: '김하나',
    balance: 100000
    },
    {
    name: '김두리',
    balance: 10000
    },
    {
    name: '김서이',
    balance: 100
    },
    ])

    const getPersonByName = computed(() => {
        return (name) => balances.value.find((person) => person.name == name)
    }) 

    const increaseBalance = function(name) {
        const person = balances.value.find((temp) => temp.name === name)
        if (person) {
            person.balance += 1000
        }
    }

    return {
        balances,
        getPersonByName,
        increaseBalance,
    }
})