module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000'
      },
      '/app_info': {
        target: 'http://localhost:5000'
      }
    }
  },
  runtimeCompiler: true
}
