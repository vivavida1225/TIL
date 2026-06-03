### 1. CSS 복습
>기본적인 박스 만들기
```css
.child-card {
    border: 1px solid black;
    margin-bottom: 10px;
}
```

### 2. v-for 과 prop 사용
```html
<template>
    <div class="parant-card">
        <h1>부모 페이지입니다.</h1>
        <ChildPage :my-prop="item" v-for="item in children"/> 
    </div>
</template>
```

### 3. 자식 컴포넌트에서 프롭 받기
```html
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
```

> defineProps 로 받아줘야 사용이 가능하다.