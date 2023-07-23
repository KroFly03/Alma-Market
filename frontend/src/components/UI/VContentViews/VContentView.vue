<template>
    <div v-show="parent.value.value === value">
        <slot></slot>
    </div>
</template>

<script setup>
import { inject } from "vue";

const props = defineProps({
    value: {
        type: [Number, String],
        default: "",
    },
});

const parent = inject("v-content-views");
</script>

<style scoped lang="scss"></style>
