# 사용한 것 정리

### 1. 컴포넌트 임포트하고 템플릿에 넣기

```html
<script setup>
import ColorChanger from '@/components/ColorChanger.vue';
</script>
```

```html
<template>
  <div>
   <ColorChanger/>
  </div>
</template>
```

### 2. 자식 컴포넌트 정의하기

2.1 인풋 받아서 v-model 로 변수에 넘기기

```html
<input v-model="inputColor">
```

2.2 ref 임포트하고 변수 정의하기
```html
<script setup>
    import { ref } from 'vue'
    const inputColor = ref('')
</script>
```

2.3 v-bind 로 클래스에 추가해 주기
```html
<p :class="inputColor">입력창에 올바른 색상명을 입력하면 글자색이 바뀌어요.</p>
```
2.4 CSS 클래스 정의

```css
<style scoped>
  .red {
    color: red;
  }
  .blue {
    color: blue;
  }
  .green {
    color: green;
  }
</style>
```