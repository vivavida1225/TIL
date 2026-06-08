### 1. 각 컴포넌트 만들기

```html
<!-- App.vue -->
<template>
    <div>
        <MainPage />
        <nav>
            <RouterLink to="/">Some</RouterLink>
            <span> | </span>
            <RouterLink to="/other">Other</RouterLink>
            <!-- or 
            <RouterLink :to="{ name: 'some' }">Some</RouterLink>
            <span> | </span>
            <RouterLink :to="{ name: 'other' }">Other</RouterLink>   -->
        </nav>
        <RouterView />
    </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import MainPage from '@/components/MainPage.vue';

</script>

<style scoped>

</style>
```

```html
<!-- MainPage.vue -->
<template>
    <div>
        <h2>router 연습하기</h2>
    </div>
</template>

<script setup>

</script>

<style scoped>

</style>
```

```html
<!-- SomeVue.vue -->
<template>
    <div>
        <h4>첫 페이지</h4>
    </div>
</template>

<script setup>

</script>

<style scoped>

</style>
```

### 2. 연결하기
```javascript
// index.js
import { createRouter, createWebHistory } from "vue-router"

import SomeView from "@/views/SomeView.vue"
import OtherView from "@/views/OtherView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'some',
      component: SomeView
    },
    {
      path: '/other',
      name: 'other',
      component: OtherView
    }
  ],
})

export default router
```



```markdown
작성하신 최종 `App.vue` 구조 아주 깔끔하고 좋습니다! 주석 처리해 두신 Named Route(`:to="{ name: 'some' }"`) 문법까지 완벽하게 적어두셨네요.

이 세 가지 태그는 Vue Single Page Application(SPA)의 화면을 구성하는 **'고정 틀'**, **'네비게이션 스위치'**, **'가변 화면 구멍'** 역할을 담당합니다. 각 태그의 작동 원리와 `src/router/index.js` 설계도의 어떤 항목과 통신하는지 매핑해서 명쾌하게 정리해 드릴게요.

---

## 1. `<MainPage />` : 언제나 고정된 "고정 머리판(Layout)"

### 💡 어떻게 작동하나요?

라우터와는 아무런 상관이 없는 **일반 순수 Vue 컴포넌트**입니다. `App.vue` 대문이 열리자마자 상단에서 `import MainPage`로 가져온 객체를 그대로 화면에 박아 넣습니다.

* 아래 설명할 `<RouterView />` **바깥**에 존재하기 때문에, 사용자가 메뉴를 눌러 주소를 아무리 바꿔도 이 녀석은 화면에서 사라지거나 새로고침되지 않고 **그 자리에 항상 고정**되어 출력됩니다.

### 🔗 `index.js`와의 연결고리

* **없음 (0%)**
* 라우터 설정 파일(`index.js`)을 전혀 거치지 않고, `App.vue`가 직접 불러와서 렌더링하는 독립적인 부품입니다.

---

## 2. `<RouterLink to="/">Some</RouterLink>` : 주소창을 바꾸는 "스위치"

### 💡 어떻게 작동하나요?

겉보기에는 HTML의 `<a>` 태그처럼 작동하여 링크를 만들어주지만, 속사정은 완전히 다릅니다. 클릭하는 순간 브라우저의 새로고침(서버 요청)을 영리하게 가로막은 뒤, **브라우저 주소창의 URL만 슬쩍 `/`로 업데이트**하는 스위치 역할을 합니다.

### 🔗 `index.js`와의 연결고리

* **`index.js` 내부 `routes` 배열의 `path` 및 `name` 속성과 연결됩니다.**

```javascript
// index.js 설계도 내부
routes: [
  {
    path: '/',          // 👈 <RouterLink to="/"> 방식이 이 'path'를 찾아옴!
    name: 'some',       // 👈 <RouterLink :to="{ name: 'some' }"> 방식이 이 'name'을 찾아옴!
    component: SomeView
  }
]

```

* 사용자가 링크를 누르면, 라우터는 `index.js`로 달려가 **"야, 주소가 `/`라는데 매핑된 규칙이 뭐냐?"** 하고 이정표를 조회하게 됩니다.

---

## 3. `<RouterView />` : 화면이 갈아끼워지는 "가변 무대(구멍)"

### 💡 어떻게 작동하나요?

쉽게 말해 "주소에 따라 바뀌는 화면들이 들어올 빈 구멍(Placeholder)"입니다. 평소에는 비어있거나 기본 컴포넌트가 채우고 있다가, 주소창의 URL이 변경되면 라우터가 그 주소에 걸맞은 무대(View 컴포넌트)를 낚아채서 이 자리에 쏙 집어넣어 줍니다.

### 🔗 `index.js`와의 연결고리

* **`index.js` 내부 매칭된 라우트 객체의 `component` 속성과 연결됩니다.**

```javascript
// index.js 설계도 내부
{
  path: '/',
  name: 'some',
  component: SomeView  // 👈 <RouterView />는 최종적으로 이 'SomeView' 객체로 변신합니다!
}

```

* 사용자가 `Some` 링크를 눌러 주소가 `/`가 되면 ➡️ 라우터가 `index.js`에서 `SomeView`를 찾아내고 ➡️ `App.vue`에 있는 **`<RouterView />` 태그를 실시간으로 `<SomeView />`로 둔갑**시킵니다.
* 만약 주소가 `/other`로 바뀌면 ➡️ 이 구멍은 순식간에 `<OtherView />`로 교체됩니다.

---

## 🗺️ 세 태그의 협업 메커니즘 한눈에 보기

사용자가 화면에서 **`Other`** 라는 글자를 클릭했을 때 일어나는 전체 인과관계 프로세스입니다.

```
1. 사용자가 <RouterLink to="/other"> 클릭!
   ↓
2. 브라우저 주소창이 새로고침 없이 http://localhost:5173/other 로 변경됨
   ↓
3. 라우터가 [src/router/index.js] 설계도를 펼쳐서 'path: "/other"' 인 녀석을 검색
   ↓
4. 설계도에서 'component: OtherView' 라는 부품 정보를 찾아냄
   ↓
5. [App.vue]로 돌아와, 상단의 <MainPage />는 그대로 놔둔 채
   하단의 <RouterView /> 구멍에만 'OtherView' 컴포넌트를 쏙 끼워 넣어서 화면을 갱신!

```

이 흐름을 완벽히 이해하셨다면 Vue 라우터의 동작 원리 뼈대를 100% 마스터하신 겁니다. 이제 어떤 대형 프로젝트를 만나도 페이지 이동 구조를 자유자재로 설계하실 수 있을 거예요!
```