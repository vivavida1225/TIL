### v-if 사용하기

```html
    <ul v-if="isLogin">
      <li>유저네임 : {{user.userName}} </li>
      <li>관리자여부 : {{user.isAdmin}} </li>
      <li>비밀번호 : {{user.passWord}} </li>
    </ul>
```

### 로그인 함수 정의하기

```javascript
const isLogin = ref(false)

const login = () => {
    isLogin.value = !isLogin.value
    console.log(`Value of isLogin has been changed to ${isLogin.value}`)
}
```