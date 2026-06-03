1. 에밋 보내기 (자식 컴포넌트)

```html
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
```

2. 자식에서 프롭 정의

```html
<script setup>
defineProps({
    name: String,
    age: Number,
    balance: Number
})

</script>
```

3. 반복 돌기

```html
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
```

##### 중요! v-for 쓸 때는 반드시 :key 를 써 준다.
```html
<ChildPage
v-for="child in children"
:key="child.name"
:name="child.name"
/>
```

4. 배열을 ref 반응형으로 설정하고 함수의 인자로는 child 객체를 넘겨서 특정 자식의 데이터를 수정할 수 있게 한다.

```html
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
```