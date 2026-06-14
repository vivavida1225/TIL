# 1. axios 를 return 하느냐 마느냐의 차이

## 1. return이 없을 때 (현재 코드)
예시 코드:
```javascript
  const createArticle = function ({ title, content}) {

    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/articles/',
      data: {
        title,
        content
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
    .then(res => console.log(res))
  }
```

- 이 코드는 axios 요청을 서버로 멀리 던지기만 하고, 정작 createArticle 함수 자체는 아무것도 반환하지 않고(return undefined) 즉시 종료됩니다.
- 이 함수를 가져다 쓰는 View 컴포넌트에서는 다음과 같은 문제가 발생합니다.

```javascript
// 📄 CreateView.vue (글쓰기 페이지 컴포넌트)에서 호출할 때

const onSubmit = function() {
  // 글 생성 함수를 실행합니다.
  createArticle(payload) 

  // ❌ 에러 발생! createArticle이 리턴한 게 없어서 .then을 붙일 수 없습니다.
  createArticle(payload).then(() => { ... }) 

  // ❌ 의도치 않은 타이밍에 이동! 
  // 서버가 글을 다 저장하기도 전에(비동기니까) 다음 줄이 바로 실행되어 홈으로 튕겨버립니다.
  router.push({ name: 'home' }) 
}
```
### 💡 요약: 함수 내부에서 console.log(res)를 찍는 것 외에, 이 함수를 호출한 바깥 세상(컴포넌트)에서는 글이 다 써졌는지 안 써졌는지 도통 알 방법이 없습니다.

## 2. return을 붙였을 때
- axios 앞에 return을 붙여주면, Axios가 통신 결과물로 만들어내는 Promise 객체(비동기 영수증)를 함수 바깥으로 토스해 줍니다.
```javascript
const createArticle = function ({ title, content }) {
  // ✨ return을 붙여 비동기 약속(Promise)을 바깥으로 돌려줍니다.
  return axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/api/v1/articles/',
    data: { title, content },
    headers: { Authorization: `Token ${authStore.token}` }
  })
  .then(res => {
    console.log(res)
    return res // 필요하다면 결과값도 다음 .then으로 넘겨줍니다.
  })
}
```
- 이렇게 return을 달아두면 컴포넌트 쪽에서 이 함수를 리모컨처럼 쥐고 완벽한 타이밍에 후속 제어를 할 수 있게 됩니다.

```javascript
// 📄 CreateView.vue 에서 호출할 때

const onSubmit = function() {
  // ⭕ 이제 바깥에서도 .then()이나 async/await를 쓸 수 있습니다!
  createArticle(payload)
    .then(() => {
      // 갱신된 글 목록을 보여주기 위해 "서버 응답이 완료된 직후" 홈 화면으로 이동!
      router.push({ name: 'home' })
    })
    .catch((err) => {
      alert('글 작성에 실패했습니다.')
    })
}
```
- 따라서 컴포넌트와 스토어(혹은 외부 통신 함수)를 분리해서 작업할 때는, 바깥쪽에서 타이밍을 잴 수 있도록 return axios... 스타일을 기본 습관으로 삼으시는 것이 훨씬 좋습니다!

### 만약 createArticle에 return이 없다면?
- 글을 다 저장하기도 전에 컴포넌트가 혼자 마음대로 홈 화면으로 튕겨버리는 대참사가 난다고 말씀드렸었죠. 
- 페이지 이동(router.push)은 Vue의 반응성 시스템이 자동으로 해줄 수 있는 영역이 아니라, 우리가 코드로 타이밍을 직접 제어해야 하는 영역이기 때문에 "나 다 끝났어!"라는 영수증(return axios)이 필수였던 것입니다.

## 3. 그럼 그냥 다 리턴을 적어주는 식으로 쓰는 스타일은 어때? 
- 모든 비동기 함수에 return을 기본값으로 깔아두는 스타일이 왜 좋은지, 얻을 수 있는 확실한 이점 3가지를 정리해 드릴게요.
![picture 0](https://cdn.jsdelivr.net/gh/vivavida1225/first_repo@master/images/311196f525e4f1a2fb54fb3c54c18f5bf4a35caa82fdf05580fdf509277ef219.png)  
![picture 1](https://cdn.jsdelivr.net/gh/vivavida1225/first_repo@master/images/e9dc99001e05cd87da92524845c2e3c8d7890ec4d24e1b33dd9a1429f30a6fff.png)  

# 2. `<button type="">` 이 가지는 의미

## HTML의 <button> 태그는 눈에 보이기에는 다 똑같은 버튼처럼 생겼지만, 사실 내부적으로 3가지 명확한 정체성(Type)을 가질 수 있습니다.

- type="submit" (제출 버튼): 클릭했을 때 부모 `<form>`을 가동시켜 데이터를 서버로 전송하거나, 우리가 설정한 @submit 이벤트를 발생시킵니다. (폼 안의 버튼은 이 값이 기본값입니다.)
- type="button" (일반 버튼): 클릭해도 폼을 제출하지 않고 아무 일도 일어나지 않는 순수한 버튼입니다. 오직 자바스크립트의 클릭 이벤트(@click)를 연결해서 커스텀 기능을 실행할 때만 씁니다.
- type="reset" (초기화 버튼): 클릭하면 폼 안에 사용자가 입력한 모든 내용을 한 방에 처음 상태로 싹 리셋해 줍니다. (요즘은 잘 쓰지 않습니다.)

## `<button>create</button>`이라고만 적어도, 최신 브라우저들은 알아서 type="submit"으로 취급한다.
- 그렇다면 왜 굳이 귀찮게 type="submit"을 코드에 직접 명시해 주는 것인가?

### 💡 type="button"과의 충돌을 방지하기 위해
- 맨 밑의 [제출] 버튼 말고도 폼 중간에 다른 버튼들이 들어가야 할 때
```html
<form @submit.prevent="submitData">
  <input type="text" v-model="username">
  
  <button @click="checkDuplicate">중복 확인</button> 

  <button type="submit">회원가입 완료</button>
</form>
```
- 💡 위 코드에서 아이디 중복 확인 버튼에 아무 생각 없이 type을 안 적으면, 유저가 중복 확인을 하려고 버튼을 누르는 순간 아이디 검사만 하는 게 아니라 회원가입 폼 전체가 서버로 제출되어 버리는 대형 버그가 발생!

> 올바른 사용법
```html
<button type="button" @click="checkDuplicate">중복 확인</button>

<button type="submit">회원가입 완료</button>
```

- type="submit"은 이 버튼이 폼 전체를 움직이는 리모컨임을 명시하는 표준 규격입니다.
- 폼 내부의 버튼에 type을 생략하면 자동으로 submit으로 작동하므로, 제출 목적이 아닌 중간 버튼들은 반드시 type="button"을 달아주어야 폼이 멋대로 발사되는 버그를 막을 수 있습니다!
