// src/main.js

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// ## ADDED: 1. 导入你的 Vuex store 实例 ##
import store from './store' 
import './style.css' // 引入全局样式文件

// 引入 Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// ## ADDED: 2. 在使用 router 和 Element Plus 之前，先使用 store ##
// 这会将 store 实例注入到所有子组件中
app.use(store) 

app.use(router)
app.use(ElementPlus)

app.mount('#app')