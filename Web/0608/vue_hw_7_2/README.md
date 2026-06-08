# my-forth-front-project


1. family.js 구현

```javascript
import { defineStore } from 'pinia'

export const useFamilyStore = defineStore('family', () => {
    const familyinfo = [
        { 
  familyName: '메디치',
  father: '로도비코 데 메디치', 
  mother: '마리아 살비아티', 
  children: [ 
              {name: '틀레도의 엘 레오노르'}, 
              {name: '코시모 1세'}, 
            ] 
  }, 
  { 
    familyName: '전주 이씨',
    father: '이도', 
    mother: '소헌왕후', 
    children: [ 
                {name: '이향'}, 
                 {name: '이유'}, 
              ] 
  },
    ]
    return {familyinfo}
})
```

2. store 에서 데이터 가져오기

```html
<!-- MainPage.vue -->
<template>
    <div>
        <h2>pinia 연습하기</h2>
        <ParentPage
        v-for="family in familyInfo"
        :key="family.familyName"
        :family="family"
        />
    </div>
</template>

<script setup>
import ParentPage from './ParentPage.vue';
import { useFamilyStore } from '@/stores/family.js'

const familyStore = useFamilyStore()
const familyInfo = familyStore.familyinfo

</script>

<style scoped>

</style>
```

3. 자식 페이지들에서 적절하게 props 선언해서 상위의 데이터 받아주기

```html
<template>
    <div class="parent-container">
        <h3>부모 컴포넌트</h3>
        <p>{{ family.father }}</p>
        <p>{{ family.mother }}</p>
        <ChildPage 
        v-for="child in family.children"
        :key="child.name"
        :child-name="child.name"
        />
    </div>
</template>

<script setup>
import ChildPage from '@/components/ChildPage.vue';

defineProps({
    family: Object
})

</script>
```

##### 4. 잊지 말기! 템플릿은 kebab-case로, JS는 camelCase로.

```html
<template>
    <div class="parent-container">
        <h3>부모 컴포넌트</h3>
        <p>{{ family.father }}</p>
        <p>{{ family.mother }}</p>
        <ChildPage 
        v-for="child in family.children"
        :key="child.name" 
        :child-name="child.name"
        />
    </div>
</template>
<!-- child-name 으로 넘기고 -->
```

```html
<template>
    <div class="child-card">
        <h4>자식 페이지</h4>
        <p>{{ childName }}</p>
    </div>
</template>

<script setup>
defineProps({
    childName: String
})
// childName 으로 받아서 쓴다
</script>
```
