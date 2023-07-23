<template>
    <div>
        <slot></slot>
    </div>
</template>

<script setup>
import { provide, toRef } from "vue";

const props = defineProps({
    value: {
        type: [String, Number],
        default: null,
    },
});

provide("v-content-views", { value: toRef(props, "value") });
</script>

<style scoped lang="scss"></style>
