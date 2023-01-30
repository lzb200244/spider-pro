<template>
  <div>
    <a-layout>
      <a-layout-header :style="{background:'#fff'}" style="padding: 0 ">
        <Header/>
      </a-layout-header>
      <a-layout-content :style="{background:'#fff'}">
        <router-view></router-view>
      </a-layout-content>
      <a-layout-footer :style="{background:'#fff'}">
        <Footer/>
      </a-layout-footer>
    </a-layout>
  </div>

</template>

<script >
import Footer from '@/components/layout/Footer.vue'
import Header from '@/components/layout/Header.vue'

export default {
  components: {
    Header, Footer
  },
  setup() {

  }
}

</script>

<style>

</style>
