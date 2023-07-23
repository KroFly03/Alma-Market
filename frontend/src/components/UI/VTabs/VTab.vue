<template>
    <v-btn
        class="v-tab"
        :class="{ 'v-tab--selected': isSelected }"
        :active="isSelected"
        bg-color="white"
        :text-color="isSelected ? 'primary' : 'gray'"
        :to="to"
        @click="to ? () => {} : parent.onSelect(value)"
    >
        <slot />
    </v-btn>
</template>

<script setup>
import VBtn from "@/components/UI/VBtn.vue";
import { computed, inject } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
    to: {
        type: [null, String, Object],
        default: null,
    },
    value: {
        type: [String, Number],
        default: "",
    },
});

const parent = inject("v-tabs");

if (!props.to) parent.tabs.push(props.value);

const link = props.to ? RouterLink.useLink({ to: props.to }) : null;

const isSelected = computed(() => {
    return link ? link.isExactActive.value : parent?.selected.value === props.value;
});
</script>

<style scoped lang="scss">
.v-tab {
    @apply grow-[inherit] rounded-none rounded-t-md focus:ring-0;

    &--selected {
        @apply border-b-2 border-[currentColor];
    }
}
</style>
