<template>
    <svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
        <path :d="mdiIcon"></path>
    </svg>
</template>

<script setup>
defineProps({
    mdiIcon: {
        type: String,
        required: true,
    },
});
</script>

<style scoped lang="scss"></style>
