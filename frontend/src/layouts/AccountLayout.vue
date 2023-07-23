<template>
    <container-with-sidebar :links="links" title="Личный кабинет">
        <router-view></router-view>
    </container-with-sidebar>
</template>

<script setup>
import ContainerWithSidebar from "@/layouts/utils/ContainerWithSidebar.vue";

const links = [
    {
        title: "Заказы",
        to: { name: "AccountOrders" },
    },
    {
        title: "Настройки",
        to: { name: "AccountSettings" },
    },
];
</script>

<style scoped lang="scss"></style>
