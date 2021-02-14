 module.exports = {
    devServer: {
      open: true,
      host: 'localhost',
      port: 8080,
      https: false,
      proxy: {
        '/api': {
          target: 'http://localhost:8000/', // 修改为你的Django服务器地址
          changOrigin: true,
          pathRewrite: {
            '^/api': '' 
          }
        }
      }
    }
  }