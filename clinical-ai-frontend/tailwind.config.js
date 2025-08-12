/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // 扫描所有 templates 文件夹下的 html 文件
    './static/js/**/*.js'      // 也可以扫描 JS 文件（如果需要）
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}