# 1. front\src\stores\auth.js 코드

```javascript
import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

// 'auth'라는 이름의 전역 인증 관리 창고(Store)를 정의합니다.
export const useAuthStore = defineStore('auth', () => {
  
  // 📌 1. 새로고침 대응 (영속성 유지)
  // 브라우저의 로컬 스토리지에 'auth'라는 이름으로 저장된 세션 데이터를 읽어옵니다.
  // 로컬 스토리지는 문자열만 저장하므로 JSON.parse를 통해 다시 자바스크립트 객체로 변환합니다.
  const savedAuth = JSON.parse(localStorage.getItem('auth'))

  // 📌 2. 인증 상태 정의 (State)
  // 로컬 스토리지에 기존 토큰이 존재하면 그 값을 초기값으로 쓰고, 없으면 null(비로그인 상태)로 설정합니다.
  // 컴포넌트들이 이 token 변수를 지켜보며 로그인 여부를 판단합니다.
  const token = ref(savedAuth?.token || null)

  // 📌 3. 실시간 로그인 여부 계산 (Getter)
  // 토큰의 존재 여부를 boolean(true/false) 값으로 실시간 변환하여 반환합니다.
  // 토큰이 null이 아니면 true(인증됨), null이면 false(인증 안 됨)가 됩니다.
  const isAuthenticated = computed(() => {
    return token.value !== null
  })

  // 📌 4. 토큰 저장 및 동기화 함수 (Action)
  // 로그인이나 회원가입 성공 시 서버로부터 받은 토큰을 메모리(State)와 로컬 스토리지에 동시 저장합니다.
  const saveToken = function (newToken) {
    token.value = newToken // Pinia 상태 업데이트 (화면 실시간 반영용)

    // 브라우저를 껐다 켜도 로그인이 유지되도록 로컬 스토리지에 반영구 저장합니다.
    // 객체를 통째로 저장하기 위해 문자열(JSON.stringify)로 변환합니다.
    localStorage.setItem('auth', JSON.stringify({
      token: newToken,
      isAuthenticated: true
    }))
  }

  // 📌 5. 회원가입 비동기 요청 함수 (Action)
  const signUp = function ({ username, password1, password2 }) {
    // DRF의 회원가입 엔드포인트로 사용자가 입력한 정보를 POST 요청 보냅니다.
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/accounts/signup/',
      data: {
        username,
        password1,
        password2
      }
    })
    // 서버가 회원가입을 승인하고 토큰을 담아 응답(res)을 주면, 이를 가로채 저장합니다.
    .then((res) => {
      saveToken(res.data.key) // DRF(dj-rest-auth)는 보통 토큰 값을 'key'라는 필드에 담아줍니다.
    })
  }

  // 📌 6. 로그인 비동기 요청 함수 (Action)
  const signIn = function ({ username, password }) {
    // DRF의 로그인 엔드포인트로 인증 정보(ID/PW)를 전송합니다.
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/accounts/login/',
      data: {
        username,
        password
      }
    })
    // 로그인 성공 시 백엔드가 발급해 준 고유 인증 토큰(key)을 받아와 내 창고에 저장합니다.
    .then((res) => {
      saveToken(res.data.key)
    })
  }

  // 외부에 노출하여 모든 컴포넌트가 공유할 자산들을 반환합니다.
  return {
    token,
    isAuthenticated,
    signUp,
    signIn
  }
})
```


# 2. 회원가입 함수 async / await 로 구현하면

```javascript
const submitSignUp = async function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }

  try {
    // 1. 회원가입 요청이 성공하고 토큰이 저장될 때까지 얌전히 기다립니다.
    await authStore.signUp(payload)
    
    // 2. 가입 및 로그인 처리가 끝나면 무사히 홈 화면으로 이동합니다.
    router.push({ name: 'home' })
    
  } catch (err) {
    // 3. 비밀번호 불일치, 중복 아이디 등 에러가 나면 이쪽으로 튕겨와 에러를 찍습니다.
    console.log(err)
  }
}
```
