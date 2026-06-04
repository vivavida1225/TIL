## 핵심 코드

```html
<!-- StudentViews.vue -->
<template>
    <div>
        <h3>학생들 상세 정보 목록입니다.</h3>
        <p v-for="student in students" :key="student.name">
            <!-- 방법 1. 선언식으로 작성
            <RouterLink :to="{name: 'studentDetail', params: {name: student.name}}">
                {{ student.name }} 학생 정보 보기
            </RouterLink> -->
            <!-- 방법 2. 프로그래밍식 작성 -->
             <span class="link-style" @click="goToDetail(student.name)">
                {{ student.name }} 학생 정보 보기
             </span>
        </p>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

    const students = [
        {name: '김하나'},
        {name: '김두리'},
        {name: '김서이'},
    ]

// 프로그래밍식을 위해: router 인스턴스 & 이동 위한 함수 정의
const router = useRouter()
const goToDetail = function(studentName) {
    router.push({
        name: 'studentDetail',
        params: {name: studentName}
        // or
        //router.push(`/students/${studentName}`)
    })
}
</script>

<style scoped>
.link-style {
  /* color: blue;
  text-decoration: underline; */
  cursor: pointer; /* 마우스를 올렸을 때 손가락 모양으로 변하게 */
}
</style>
```

## Q. 선언식이 코드가 더 짧고 작성도 쉬운 것 같은데 왜 프로그래밍식 작성법을 알아야 하는가?

## Answer:

```markdown
두 방식을 모두 직접 짜보시면서 장단점을 체감하셨다니 정말 훌륭합니다!

정확하게 보셨습니다. 단순히 "이 글자를 누르면 이 주소로 가라" 같은 **단순 링킹 구조에서는 선언식(`<RouterLink>`)이 가독성이나 코드 압축률 면에서 압도적으로 유리**합니다.

그렇다면 굳이 자바스크립트 코드를 더 써가며 프로그래밍식(`router.push`)을 써야 하는 이유는 무엇일까요? 핵심은 "내 통제 하에 비즈니스 로직(조건과 연산)을 끼워 넣을 수 있는가?"에 있습니다.

프로그래밍식 방식이 실무에서 무조건 쓰일 수밖에 없는 결정적인 이점들을 정리해 드릴게요.

---

## 1. 조건부 이동 (가장 중요)

선언식은 클릭하는 순간 무조건 주소가 바뀝니다. 중간에 멈추거나 검사할 기회가 없죠. 반면 프로그래밍식은 "자바스크립트 조건문(`if`)을 통과해야만 이동"하게 만들 수 있습니다.

```javascript
const goToDetail = function(studentName) {
  // 예시: 권한 체크 로직 검사
  if (currentUser.role !== 'ADMIN') {
    alert('학생 상세 정보는 관리자만 볼 수 있습니다!')
    return // 👈 이동하지 않고 여기서 함수를 끝내버림!
  }

  // 조건을 통과한 타당한 유저만 이동시킴
  router.push({ name: 'studentDetail', params: { name: studentName } })
}

```

---

## 2. 비동기 처리(API 통신) 후 이동

실무에서는 버튼을 눌렀을 때 바로 페이지가 바뀌면 안 되고, **서버에 데이터를 보내 승인이 떨어진 후에** 페이지를 넘겨야 하는 경우가 대다수입니다.

* **로그인 화면:** ID/PW 입력 ➡️ 로그인 버튼 클릭 ➡️ 서버에 검증 요청 (비동기) ➡️ **"성공했다"는 응답이 오면** 메인 페이지로 이동 (`router.push('/home')`)
* **결제 화면:** 결제 버튼 클릭 ➡️ PG사 결제 모달 완료 ➡️ **결제가 성공적으로 끝나면** 완료 페이지로 이동 (`router.push('/success')`)

이처럼 서버와의 통신 타이밍을 자바스크립트로 완벽하게 제어해야 할 때는 `router.push`가 필수입니다.

---

## 3. 이동하기 직전에 '사전 작업' 처리

페이지를 넘기기 전에 데이터를 로컬 스토리지에 저장하거나, 전역 상태(Pinia 등)를 변경하거나, 로그 분석 데이터(Analytics)를 서버로 전송하는 등 컴포넌트 이동 직전에 해야 할 행동(Side Effect)이 있을 때 유용합니다.

```javascript
const goToDetail = function(studentName) {
  // 1. 최근 본 학생 명단에 이름 추가 (로컬 작업)
  recentViews.value.push(studentName)
  
  // 2. 구글 애널리틱스에 로그 전송
  analytics.logEvent('view_student_detail', { name: studentName })

  // 3. 이제 목적지로 출발!
  router.push(`/students/${studentName}`)
}

```

---

## 4. 유저의 클릭 없이 '자동으로' 이동시키기 (이벤트 바인딩의 유연성)

`<RouterLink>`는 오직 사용자가 마우스로 '클릭'했을 때만 동작합니다. 하지만 웹서비스를 만들다 보면 **클릭 외의 다양한 상황에서 주소를 바꿔야 할 때**가 많습니다.

* **세션 만료:** 은행 사이트에서 10분 동안 아무 작업도 안 했을 때 자바스크립트 타이머가 끝나면 **알아서 로그인 페이지로 튕겨내기**
* **키보드 이벤트:** 검색창에 글자를 치고 `Enter` 키를 쳤을 때 검색 결과 페이지로 강제 이동시키기
* **에러 핸들링:** 데이터를 불러오다가 500 에러가 나면 자바스크립트 catch 문에서 즉시 에러 페이지로 리다이렉트 시키기

---

## 📌 결론 및 실무 가이드

두 방식은 우열을 가리는 게 아니라 **상황에 맞춰 적절히 섞어 쓰는 콤비**입니다.

1. **선언식 (`RouterLink`) 가이드:**
* 상단 네비게이션 바, 단순 메뉴판, "뒤로 가기" 버튼 등 **클릭 시 아무런 조건 없이 100% 이동이 보장되는 단순 주소 이동**에 사용합니다.


2. **프로그래밍식 (`router.push`) 가이드:**
* 로그인/회원가입, 폼 제출, 검색, 권한 제한 확인, 자동 리다이렉트 등 **이동 전에 생각(로직 연산, API 호출, 조건문 검사)이 필요한 모든 상황**에 사용합니다.



지금 연습하시는 학생 목록 과제는 단순 이동이라 선언식이 훨씬 간결해 보이는 게 정상이지만, 조금만 깊어져도 `router.push` 리모컨을 쥐게 될 일이 훨씬 많아질 거예요!
```