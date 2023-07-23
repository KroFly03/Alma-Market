<template>
    <Popover v-model="show" class="relative">
        <PopoverButton ref="target">
            <slot name="target"></slot>
        </PopoverButton>

        <PopoverPanel class="absolute z-10" :static="visible">
            <slot></slot>
        </PopoverPanel>
    </Popover>
</template>

<script setup>
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import { ref, watch } from "vue";

const target = ref(null);

const props = defineProps({
    visible: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:visible"]);

watch(
    () => props.visible,
    async () => {
        target.value.$el.click();
    }
);
</script>

<style scoped lang="scss"></style>
