<template>
    <div class="v-tabs" :class="{ 'flex-grow': grow }">
        <slot></slot>
    </div>
</template>

<script setup>
import { computed, onMounted, provide, readonly } from "vue";

const props = defineProps({
    modelValue: {
        type: [Number, String],
        default: 0,
    },
    grow: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue"]);

const model = computed({
    get: () => props.modelValue,
    set: (val) => emit("update:modelValue", val),
});

const tabs = [];

const onSelect = (value) => {
    model.value = value;
};

provide("v-tabs", { onSelect, tabs, selected: readonly(model) });

onMounted(() => {
    if (!model.value) model.value = tabs[0];
});
</script>

<style scoped lang="scss">
.v-tabs {
    @apply flex space-x-1 overflow-auto;
}
</style>
