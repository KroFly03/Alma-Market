<template>
    <AppHeader />
    <main class="container my-9 flex flex-grow">
        <router-view></router-view>
    </main>
    <AppFooter />
</template>

<script setup>
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<style scoped lang="scss"></style>
