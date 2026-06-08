# 틀렸거나 몰랐던 포인트들


### 1. props 변수에 담은 이후 쓰기
```
Vue 3의 <script setup> 규칙상, defineProps로 정의한 데이터는 <template> 영역에서는 balances라는 이름으로 바로 접근할 수 있지만, <script> 영역 내부에서는 그냥 변수처럼 쓸 수 없습니다. 존재하지 않는 변수를 콘솔에 찍으라고 하니 자바스크립트가 실행을 중단해 버린 것입니다.

해결책: defineProps의 반환값을 props라는 변수에 담아두고, 스크립트 안에서는 props.balances로 접근해야 합니다.
```

```html
<template>
  <div>
    <h1>메인 페이지</h1>
    <div v-for="person in balances" :key="person.name">
      <p>{{ person.name }}</p>
    </div>
  </div>
</template>

<script setup>
// 2. defineProps의 리턴값을 'props'라는 변수에 할당합니다
const props = defineProps({
  balances: Array
})

// 3. script 내부에서 호출할 때는 반드시 'props.'을 앞에 붙여야 합니다!
console.log(props.balances)
</script>
```

### 2. cursor: pointer; 추가하기

우리가 아는 '클릭 가능한 손 모양'으로 바꾸는 법.
```css
<style scoped>
.update-button {
    background-color: blue;
    border: 0px;
    border-radius: 5px;
    color: white;

    /* ⭐ 이 한 줄이 마우스 커서를 손 모양(포인터)으로 바꿔주는 치트키입니다 */
    cursor: pointer; 
}
</style>
```

### 3. 버튼을 통해 UpdateView로 이동하는 기능을 구현

크게 두 가지 단계로 나뉩니다. 먼저 라우터 설정에서 해당 경로를 정의하고, 컴포넌트에서 버튼 클릭 시 router.push를 사용하여 프로그래밍 방식으로 이동하는 로직을 작성해야 합니다.

1. router/index.js 설정
이동할 목적지인 UpdateView에 이름을 붙이고, 주소창에 학생 이름이 붙을 수 있도록 :name 파라미터를 설정합니다.


```javascript
{
  path: '/update/:name',
  name: 'update', // 👈 이 이름으로 이동할 겁니다.
  component: () => import('@/views/UpdateView.vue')
}
```

2. `MainPage.vue` 수정 (버튼 클릭 로직)
버튼을 눌렀을 때 `router.push`가 실행되도록 함수를 연결합니다.

```html
<button class="update-button" @click="goToUpdate(person.name)">
  updateBalance
</button>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter() // 리모컨 가져오기

const goToUpdate = (studentName) => {
  // 'update'라는 이름의 경로로 가면서, params에 이름을 실어 보냅니다.
  router.push({ 
    name: 'update', 
    params: { name: studentName } 
  })
}
</script>
```

3. `UpdateView.vue` 작성 (데이터 수신)
```javascript
javascript
<script setup>
import { useRoute } from 'vue-router'

const route = useRoute() // 돋보기 가져오기
const studentName = route.params.name // 주소창에서 이름 낚아채기
</script>
```

### 4. name이 일치하는 객체 정보를 반환하는 기능
#### getters에 인자를 넘겨주는 방식

원래 Vue의 computed나 Pinia의 기본 getters는 인자(Parameter)를 받을 수 없는 구조입니다. 하지만 공식 문서의 설명대로 "게터 내부에서 변수를 인자로 받는 '새로운 함수'를 통째로 리턴"하면 마치 함수를 호출하듯이 인자를 넘겨서 동적 필터링을 할 수 있게 됩니다.

1단계: stores/balance.js에 인자를 받는 Getter 추가하기

```javascript
import { defineStore } from "pinia"
import { computed } from "vue" // 👈 1. computed 임포트를 추가합니다.

export const useBalanceStore = defineStore('balance', () => {
  const balances = [
    {
      name: '김하나',
      balance: 100000,
    },
    {
      name: '김두리',
      balance: 10000,
    },
    {
      name: '김서이',
      balance: 100,
    },
  ]

  // 👈 2. [명세] name이 일치하는 객체 정보를 반환하는 getters 구현
  // 겉껍데기는 computed이지만, 내부에서 (name) => ... 함수를 리턴하는 구조입니다.
  const getPersonByName = computed(() => {
    return (name) => balances.find((person) => person.name === name)
  })

  return { 
    balances,
    getPersonByName // 👈 3. 외부에 노출할 수 있도록 return에 꼭 추가해 줍니다!
  }
})
```
💡 공식 문서 속 핵심 포인트: 이렇게 인자를 받는 게터는 내부에서 매번 새로운 함수를 만들어 반환하기 때문에, Pinia의 장점인 '연산 결과 캐싱(기억하기)'이 작동하지 않는다고 공식 문서에 명시되어 있습니다. 즉, 호출할 때마다 매번 배열 검색 연산이 새로 실행됩니다.

2단계: UpdateView.vue에서 데이터 수신 및 렌더링하기

```html
<template>
  <div class="update-container">
    <h1>데이터 수정 페이지</h1>
    <hr>
    
    <div v-if="person" class="profile-card">
      <p><strong>조회된 이름:</strong> {{ person.name }}</p>
      <p><strong>현재 잔고:</strong> {{ person.balance }}원</p>
    </div>
    <div v-else>
      <p>존재하지 않는 사용자이거나 데이터를 불러올 수 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useBalanceStore } from '@/stores/balance' // 👈 1. 스토어 임포트

const route = useRoute()
const personName = route.params.name

const balanceStore = useBalanceStore() // 👈 2. 스토어 인스턴스 생성

// 👈 3. 게터 함수에 주소창의 이름(personName)을 인자로 넘겨 일치하는 객체를 낚아챕니다.
const person = balanceStore.getPersonByName(personName)

</script>

<style scoped>
</style>
```

```markdown
1. MainPage에서 [updateBalance] 버튼 클릭! (예: '김두리' 클릭)
   ↓
2. 라우터가 주소창을 http://localhost:5173/update/김두리 로 강제 이동
   ↓
3. UpdateView가 켜지며 route.params.name을 통해 '김두리' 문자열 확보
   ↓
4. balanceStore.getPersonByName('김두리') 호출 
   ↓
5. 스토어 게터가 balances 배열에서 .find()를 돌려 { name: '김두리', balance: 10000 } 객체를 반환
   ↓
6. UpdateView의 person 변수에 객체가 저장되면서 템플릿에 "잔고: 10000원"이 깔끔하게 출력!
```

### 5. balance 값들 수정하는 로직
1. 스토어 데이터의 반응성(ref) 확보 및 수정 함수(Action) 등록
- 지난 번에 작성하신 stores/balance.js를 보면 balances 배열이 일반 배열(const balances = [...])로 선언되어 있습니다. 이 상태로는 자바스크립트 상에서 값을 아무리 더해도 화면이 새로 그려지지 않습니다(반응성 유실). 따라서 이를 ref로 감싸주어야 합니다.

- 또한, 스토어의 값을 변경할 때는 스토어 내부에 전용 수정 함수(Action)를 만들어두고 호출하는 것이 Vue 3와 Pinia의 가장 정석적인 패턴입니다.
2. UpdateView.vue에서 버튼에 클릭 이벤트(@click) 연결

```javascript
import { defineStore } from "pinia"
import { ref, computed } from "vue" // 👈 1. ref 임포트를 추가합니다.

export const useBalanceStore = defineStore('balance', () => {
  
  // 👈 2. [중요] 값이 변했을 때 화면이 실시간으로 갱신되도록 ref()로 감싸줍니다!
  const balances = ref([
    {
      name: '김하나',
      balance: 100000,
    },
    {
      name: '김두리',
      balance: 10000,
    },
    {
      name: '김서이',
      balance: 100,
    },
  ])

  // 👈 3. 데이터가 ref로 바뀌었으므로 중간에 .value를 꼭 붙여서 검색해야 합니다.
  const getPersonByName = computed(() => {
    return (name) => balances.value.find((person) => person.name === name)
  })

  // 👈 4. [요구사항] 특정 사용자의 잔고를 1000원 증가시키는 Action 함수 구현
  const increaseBalance = function(name) {
    const person = balances.value.find((p) => p.name === name)
    if (person) {
      person.balance += 1000
    }
  }

  return { 
    balances,
    getPersonByName,
    increaseBalance // 👈 5. 컴포넌트에서 리모컨처럼 호출할 수 있도록 리턴에 포함!
  }
})
```

이후 버튼에 @click 리스너를 달아주고, 자바스크립트 영역에서 스토어의 increaseBalance 함수를 실행시킵니다.

또한 person 객체 자체도 스토어의 변화를 유연하게 추적할 수 있도록 computed로 감싸주는 것이 가장 안전합니다.

```html
<template>
  <div>
    <h1>데이터 수정 페이지</h1>
    
    <div v-if="person">
      <p>이름: {{ person.name }}</p>
      <p>잔고: {{ person.balance }}</p>
      
      <button class="btn-plus" @click="handleIncrease">+</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue' // 👈 1. computed를 임포트합니다.
import { useRoute } from 'vue-router'
import { useBalanceStore } from '@/stores/balance'

const route = useRoute()
const personName = route.params.name

const balanceStore = useBalanceStore()

// 💡 [팁] 스토어의 ref 데이터가 변경되는 것을 실시간으로 추적하기 위해 computed로 감싸둡니다.
const person = computed(() => balanceStore.getPersonByName(personName))

// 2. [요구사항] + 버튼을 누르면 실행될 함수 정의
const handleIncrease = function() {
  // 스토어에 만들어 둔 잔고 증가 함수에 현재 유저 이름을 실어서 보냅니다.
  balanceStore.increaseBalance(personName)
}
</script>

<style scoped>
</style>
```

```markdown
1. UpdateView에서 사용자가 [+] 버튼을 클릭합니다.
   ↓
2. handleIncrease() 함수가 실행되면서 스토어의 balanceStore.increaseBalance('김하나')를 호출합니다.
   ↓
3. 스토어 내부에서 ref로 관리되던 '김하나'의 객체를 찾아 balance 값을 1000원 올립니다.
   ↓
4. 스토어의 데이터(State)가 변하자, 이를 지켜보고 있던 UpdateView의 computed('person')가 번쩍 눈을 뜹니다.
   ↓
5. 템플릿의 {{ person.balance }} 영역이 새로고침 없이 실시간으로 1000원 늘어난 숫자로 슥 바뀝니다!
```