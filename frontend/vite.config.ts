import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@src': fileURLToPath(new URL('./src', import.meta.url)),
      '@theme': fileURLToPath(new URL('./src/shared/theme', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 백엔드 주소
        changeOrigin: true,
        secure: false,
      },
    },
  }
})
