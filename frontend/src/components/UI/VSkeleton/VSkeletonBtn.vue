<template>
    <div class="v-skeleton-btn"></div>
</template>

<script setup></script>

<style scoped lang="scss">
@import "style";

.v-skeleton-btn {
    @apply h-[40px] w-[96px] rounded-md;
    @include shining-bg();
}
</style>
