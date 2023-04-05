// eslint-disable-next-line @typescript-eslint/no-var-requires
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
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
  configureWebpack: {
    resolve: {
      extensions: ['.js', '.vue', '.json', '.ts'], // 后缀名省略配置
      alias: {
        components: '@/components'
      }
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

})
