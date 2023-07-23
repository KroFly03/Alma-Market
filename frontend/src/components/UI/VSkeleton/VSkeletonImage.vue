<template>
    <div
        class="v-skeleton-image"
        :style="{
            '--max-width': maxWidth,
            '--max-height': maxHeight,
            '--height': height,
            '--width': width,
        }"
    ></div>
</template>

<script setup>
defineProps({
    maxWidth: {
        type: [String],
        default: "none",
    },
    width: {
        type: String,
        default: "150px",
    },
    maxHeight: {
        type: String,
        default: "none",
    },
    height: {
        type: String,
        default: "none",
    },
});
</script>

<style scoped lang="scss">
@import "style";

.v-skeleton-image {
    @apply h-full w-full rounded-md;

    max-width: var(--max-width);
    width: var(--width);
    max-height: var(--max-height);
    height: var(--height);

    @include shining-bg();
}
</style>
