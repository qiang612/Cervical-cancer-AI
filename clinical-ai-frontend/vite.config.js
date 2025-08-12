import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // 保留您原来的path模块引入

// https://vite.dev/config/
export default defineConfig({
  // 保留您原来的 plugins 配置
  plugins: [vue()],

  // 保留您原来的 resolve.alias 配置
  resolve: {
    alias: {
      // 配置@别名指向src目录
      '@': path.resolve(__dirname, './src')
    }
  },

  // ## ADDED: 添加解决跨域问题的 server.proxy 配置 ##
  server: {
    host: '0.0.0.0', // 允许通过IP地址访问
    // port: 5174, // 您可以根据需要修改前端开发服务器的端口，如果未指定，Vite会使用默认值
    proxy: {
      // 关键配置：当请求地址以 /api 开头时，触发代理规则
      '/api': {
        // 目标是您的后端服务器地址
        target: 'http://localhost:5000',
        
        // changeOrigin: true 对于跨域请求至关重要
        changeOrigin: true,
      },
    }
  }
})