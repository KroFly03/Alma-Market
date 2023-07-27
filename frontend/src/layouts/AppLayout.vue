<template>
  <div class="wrapper">
    <AppHeader />
    <main class="container my-9 overflow-auto">
        <router-view></router-view>
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<style lang="scss" scoped>
.wrapper {
  display: grid;
  grid-template-rows: auto auto 1fr auto;
  min-height: 100vh;
}
</style>
