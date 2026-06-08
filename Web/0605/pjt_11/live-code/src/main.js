/**
 * [1-2] Vue 애플리케이션 진입점 (Entry Point)
 *
 *
 * 실행 순서:
 *   1) CSS 불러오기
 *   2) Vue에서 createApp 가져오기
 *   3) App.vue를 루트 컴포넌트로 등록
 *   4) index.html의 #app 요소에 화면 붙이기 (mount)
 */

// 전역 스타일 (모든 페이지 공통 여백 등)
import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";

// App 컴포넌트를 Vue 앱으로 만들고, id가 "app"인 div에 렌더링
createApp(App).mount("#app");
