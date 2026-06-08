/**
 * [0] Vite 개발 서버·빌드 설정 (강의 때는 "도구 설정" 정도만 소개)
 *
 * - vue(): .vue 파일을 브라우저가 이해할 수 있게 변환
 * - alias '@' → src 폴더를 짧게 import (예: import X from '@/components/...')
 */

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
