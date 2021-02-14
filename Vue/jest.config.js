module.exports = {
  moduleNameMapper: {
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga|css|less|scss|sass)$': '<rootDir>/src/mock/file.mock.js' // 模拟加载静态文件   
  },
  preset: '@vue/cli-plugin-unit-jest',
  collectCoverageFrom: [
    'src/**/*.{js,vue}',
    '!src/main.js',
    '!src/mock/**',
    '!**/node_modules/**',
    '!src/router/**',
    '!src/components/SIdentify.vue'
  ]
}
