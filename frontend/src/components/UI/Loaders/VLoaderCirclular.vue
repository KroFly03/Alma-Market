<template>
    <div
        class="v-loader-circular"
        :class="[`border-${color}`]"
        :style="{ width: parseInt(size) + 'px', height: parseInt(size) + 'px' }"
    ></div>
</template>

<script setup>
defineProps({
    size: {
        type: String,
        default: "24px",
    },
    color: {
        type: String,
        default: "primary",
    },
});
</script>

<style scoped lang="scss">
.v-loader-circular {
    @apply rounded-[50%] border-4 border-b-transparent;
    animation: rotation 1s linear infinite;
}

@keyframes rotation {
    0% {
        rotate: 0deg;
    }

    0% {
        rotate: 360deg;
    }
}
</style>
