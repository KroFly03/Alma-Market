<template>
    <ContainerWithSidebar :links="links" title="Админ панель">
        <router-view></router-view>
    </ContainerWithSidebar>
</template>

<script setup>
import ContainerWithSidebar from "@/layouts/utils/ContainerWithSidebar.vue";

const links = [
    {
        title: "Товары",
        to: { name: "AdminGoods" },
    },
    {
        title: "Заказы",
        to: { name: "AdminOrders" },
    },
    {
        title: "Пользователи",
        to: { name: "AdminUsers" },
    },
];
</script>

<style scoped lang="scss"></style>
