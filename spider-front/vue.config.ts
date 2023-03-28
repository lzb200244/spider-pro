// eslint-disable-next-line @typescript-eslint/no-var-requires
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  publicPath: './',
  transpileDependencies: true,

  devServer: {
    proxy: {
      '/v1/api': {
        target: 'http://127.0.0.1:8888/v1/api',
        // pathRewrite: { '^/api': '' },
        changeOrigin: true
      }
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
