const CompressionPlugin = require('compression-webpack-plugin')
const TerserPlugin = require('terser-webpack-plugin');

// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const path = require('path')
const {defineConfig} = require('@vue/cli-service')
const external = {
  'vue': 'Vue',
  'vue-router': 'VueRouter',
  'vuex': 'Vuex',
  'xlsx': 'XLSX'
}
module.exports = defineConfig({
    //打包读取缓存历史加快构建
    // chainWebpack: config => {
    //
    //   // 对js文件启用 cache-loader
    //   config.module
    //     .rule('js')
    //     .test(/\.js$/)
    //     .use('cache-loader')
    //     .loader('cache-loader')
    //     .end()
    // },
    //打包路径前缀
    publicPath: process.env.NODE_ENV === 'production'
      ? '/' // 修改为你的CDN地址
      : './',
    //打包输出文件夹
    outputDir: 'dist',
    //使用babel编译
    transpileDependencies: true,
    configureWebpack: {
      //加快打包速度和使用多线程打包
      optimization: {
        minimize: true,
        minimizer: [
          new TerserPlugin({
            terserOptions: {
              compress: {
                drop_console: true,
                drop_debugger: true,
              },
              format: {
                comments: false,
              }
            },
            extractComments: false,
          }),
        ],
      },
      resolve: {
        alias: {
          '@': path.resolve(__dirname, 'src')
        }
      },

      //不打包的组件，用于cdn
      externals: process.env.NODE_ENV === 'production' ? external : {},
      plugins: [
        //支持gzip打包
        new CompressionPlugin({
          algorithm: 'gzip', // 压缩算法
          test: new RegExp('\\.(js|css)$'), // 匹配文件类型
          threshold: 10240, // 阈值，当文件超过该尺寸时才会压缩
          minRatio: 0.8, // 压缩比例，即压缩后文件大小与原文件大小的比值
          deleteOriginalAssets: false // 不删除原文件
        }),

        //   //打包分析工具
        // new BundleAnalyzerPlugin({
        //   analyzerMode: 'static', // 生成静态HTML报告
        //   openAnalyzer: false, // 不自动打开报告页面
        //   reportFilename: 'bundle-report.html' // 将报告输出到 dist/bundle-report.html 文件
        // }),


      ]
    },

    devServer: {
      https: process.env.NODE_ENV === 'production', // 使用https协议
      proxy: {
        '/api': {
          target: process.env.VUE_APP_BASE_API,
          pathRewrite: { // 用于重写请求路径
            '^/api': '/v1/api'
          },
          changeOrigin: true,
          secure: false // 关闭SSL证书验证

        }
      }
    },
    productionSourceMap: false, // 关闭生产环境的source map

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
)
