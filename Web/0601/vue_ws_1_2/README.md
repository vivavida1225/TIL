# Vue 기초 구조 학습

1. CDN 링크 넣기
```javascript
<script src="https://unpkg.com/vue@3/dist/vue.global.js"><script>
```

2. 쓸 함수 불러오기
```javascript
const {createApp, ref} = Vue
```

3. createApp 속 정의
```javascript
const app = createApp({
    setup() {
      const hello = ref('Hello, Vue!')

      return{
        hello,
      }
    }
   })
```

4. mount 하기
```javascript
firstApp.mount('#firstApp')
```
