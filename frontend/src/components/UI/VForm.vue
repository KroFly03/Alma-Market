<template>
    <form @submit.prevent>
        <slot></slot>
        <p v-if="errors" class="my-2 text-sm text-error">{{ errors }}</p>
        <div class="mt-3">
            <slot name="bottom"></slot>
        </div>
    </form>
</template>

<script setup>
const props = defineProps({
    errors: {
        type: String,
        default: "",
    },
});
</script>

<style scoped lang="scss"></style>
