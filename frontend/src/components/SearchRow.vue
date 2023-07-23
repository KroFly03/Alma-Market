<template>
    <div class="w-100 mb-6 flex items-center justify-between sm:flex-col">
        <div class="w-6/12 sm:mb-4 sm:w-full">
            <v-input v-model="modelValue" label="Поиск">
                <!--                <template #append-inner>-->
                <!--                    <v-icon :icon="mdiMagnify" @click="$emit('search', modelValue.value)"></v-icon>-->
                <!--                </template>-->
            </v-input>
        </div>
        <div v-if="$slots.actions" class="flex w-6/12 justify-end sm:w-full">
            <slot name="actions"></slot>
        </div>
    </div>
</template>

<script setup>
import { mdiMagnify } from "@mdi/js";
import { computed } from "vue";
import VInput from "@/components/UI/VInput.vue";

const props = defineProps({
    modelValue: {
        type: String,
        required: true,
    },
});

const emit = defineEmits(["update:modelValue", "search"]);

const modelValue = computed({
    get: () => props.modelValue,
    set: (newValue) => emit("update:modelValue", newValue),
});
</script>
