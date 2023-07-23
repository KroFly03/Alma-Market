<template>
    <div class="v-select">
        <v-input
            v-outside-click="() => (isOpen = false)"
            class="v-select__input"
            variant="regular"
            readonly
            :model-value="selectedOption?.label"
            :label="label"
            :append-inner-icon="mdiMenuDown"
            @click="isOpen = !isOpen"
        ></v-input>
        <div v-show="isOpen" class="v-select__options">
            <slot></slot>
        </div>
    </div>
</template>

<script setup>
import VInput from "@/components/UI/VInput.vue";
import { mdiMenuDown } from "@mdi/js";
import { computed, provide, ref } from "vue";
import VOutsideClick from "@/directives/outsideClick.js";

const props = defineProps({
    modelValue: {
        type: [String, Number],
        default: "",
    },
    placeholder: {
        type: String,
        default: "",
    },
    label: {
        type: String,
        default: "",
    },
});

const emit = defineEmits(["update:modelValue"]);

const model = computed({
    get: () => props.modelValue,
    set: (val) => {
        emit("update:modelValue", val);
    },
});

const isOpen = ref(false);

const options = ref([]);
const selectedOption = computed(() => options.value.find(({ value }) => value === model.value));

const onSelectOption = (option) => {
    isOpen.value = false;
    model.value = option.value;
};

provide("select", { onSelectOption, options, selectedValue: model });
</script>

<style scoped lang="scss">
.v-select {
    @apply relative;

    &__input {
        cursor: pointer;

        &:deep(input) {
            pointer-events: none;
        }
    }

    &__options {
        @apply absolute top-[110%] z-10
    max-h-40 w-full
    overflow-hidden overflow-y-auto
    rounded-md
    bg-white p-1
    shadow-md;
    }
}
</style>
