import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vue 앱 인스턴스 생성
const app = createApp(App)

app.use(router)

app.mount('#app')
