<template>
    <router-link class="flex flex-col text-white" :style="{ width: 'fit-content' }" to="/">
        <span class="text-2xl font-bold sm:text-lg sm:leading-none">Alma Market</span>
        <span v-if="!isShort" class="text-md sm:text-sm">Alma Media System</span>
    </router-link>
</template>

<script setup>
defineProps({
    isShort: {
        type: Boolean,
        default: false,
    },
});
</script>

<style lang="scss"></style>
