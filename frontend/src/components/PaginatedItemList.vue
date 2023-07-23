<template>
    <div ref="elem" class="flex h-full flex-col">
        <slot name="top"></slot>

        <slot></slot>

        <div class="mt-auto flex w-full justify-center">
            <v-pagination
                v-model="page"
                class="mt-4"
                :total-pages="totalPages"
                @page-change="$emit('pageChange')"
            ></v-pagination>
        </div>
    </div>
</template>

<script setup>
import { computed, ref } from "vue";
import VPagination from "@/components/UI/VPagination.vue";

const props = defineProps({
    isLoading: {
        type: Boolean,
        default: false,
    },
    currentPage: {
        type: Number,
        default: 1,
    },
    totalPages: {
        type: Number,
        default: 1,
    },
});

const emit = defineEmits(["update:currentPage", "pageChange"]);

const elem = ref();

const page = computed({
    get: () => props.currentPage,
    set: (newValue) => {
        emit("update:currentPage", newValue);
        elem.value.scrollIntoView({ behavior: "smooth" });
    },
});
</script>
