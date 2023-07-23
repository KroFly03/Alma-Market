<template>
    <div class="">
        <div
            v-for="idx in lines"
            :key="idx"
            class="v-skeleton-text"
            :style="{
                '--height': lineHeight,
                '--width': width,
            }"
        ></div>
    </div>
</template>

<script setup>
defineProps({
    width: {
        type: String,
        default: "100%",
    },
    lineHeight: {
        type: String,
        default: "15px",
    },
    lines: {
        type: Number,
        default: 1,
    },
});
</script>

<style scoped lang="scss">
@import "style";

.v-skeleton-text {
    @apply mt-1 rounded-md first:mt-0;

    width: var(--width);
    height: var(--height);

    @include shining-bg();

    &:last-child:not(:first-child) {
        @apply max-w-[50%];
    }
}
</style>
