<template>
    <v-list-item :title="label" :active="value === selectedValue" @click="onClick"></v-list-item>
</template>

<script setup>
import VListItem from "@/components/UI/VListItem.vue";
import { inject, onMounted, reactive } from "vue";

const props = defineProps({
    label: {
        type: String,
        default: "",
    },
    value: {
        type: [String, Number],
        default: "",
    },
    selected: {
        type: Boolean,
        default: false,
    },
});

const option = reactive({
    label: props.label,
    value: props.value,
});

const { onSelectOption, options, selectedValue } = inject("select");

options.value.push(option);

onMounted(() => {
    if (props.selected) onClick();
});

const onClick = () => {
    onSelectOption(option);
};
</script>

<style scoped lang="scss"></style>
