const CompressionPlugin = require('compression-webpack-plugin')

module.exports = {
  publicPath: './',
  transpileDependencies: true,

  devServer: {
    proxy: {
      // '/api': 'http://localhost:3000'

      // '/api': {
      //   target: 'http://127.0.0.1:800/v1/api',
      //   pathRewrite: { '^/api': '' }
      // }
    }
  },
  productionSourceMap: false, // 关闭生产环境的source map
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === 'production') {
      // 使用 CompressionPlugin 压缩文件
      config.plugins.push(new CompressionPlugin({
        test: /\.js$|\.css$|\.html$/,
        threshold: 8192,
        deleteOriginalAssets: false
      }))
    }
  },

  css: {
    loaderOptions: {
      css: {
        // 这里的选项会传递给 css-loader
      },
      postcss: {
        // 这里的选项会传递给 postcss-loader
      },
      less: {
        javascriptEnabled: true
      }
    }
  }
}
