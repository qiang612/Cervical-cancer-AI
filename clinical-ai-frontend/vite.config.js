import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    host: '0.0.0.0',
    proxy: {
      // 规则1：所有以 /api 开头的请求，都转发给后端
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      // ## FINAL FIX: 添加规则2：所有以 /uploads 开头的请求，也转发给后端 ##
      '/uploads': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})