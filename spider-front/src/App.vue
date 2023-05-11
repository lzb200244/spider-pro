<script setup lang="ts">
import Footer from '@/components/layout/Footer.vue'
import Header from '@/components/layout/Header.vue'

</script>

<template>
  <div>
    <a-layout :style="{background:'#fff'}">
      <a-layout-header v-if="$route.path!=='/account'" style="padding: 0 ">
        <Header/>
      </a-layout-header>
      <a-layout-content :style="{minHeight:'100vh'}">
        <router-view/>
      </a-layout-content>
      <a-layout-footer :style="{background:'#fff',width:'100%'}" v-if="$route.path!=='/account'">
        <Footer/>
      </a-layout-footer>
    </a-layout>
  </div>
</template>
