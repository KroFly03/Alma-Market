<template>
    <div class="v-pagination">
        <v-btn
            class="v-pagination__btn v-pagination__prev"
            :disabled="modelValue <= 1"
            @click="onPageClick(modelValue - 1)"
        >
            <v-icon :mdi-icon="mdiChevronLeft"></v-icon>
        </v-btn>

        <v-btn
            v-for="page in availablePages"
            :key="page"
            variant="tonal"
            class="v-pagination__btn"
            :active="modelValue === page"
            :disabled="page === pageBreakSign"
            @click="onPageClick(page)"
        >
            {{ page }}
        </v-btn>

        <v-btn
            class="v-pagination__btn v-pagination__next"
            :disabled="modelValue >= totalPages"
            @click="onPageClick(modelValue + 1)"
        >
            <v-icon :mdi-icon="mdiChevronRight"></v-icon>
        </v-btn>
    </div>
</template>

<script setup>
import VBtn from "@/components/UI/VBtn.vue";
import VIcon from "@/components/UI/VIcon.vue";
import { computed } from "vue";
import { mdiChevronLeft, mdiChevronRight } from "@mdi/js";

const props = defineProps({
    modelValue: {
        type: Number,
        default: 1,
    },
    totalPages: {
        type: Number,
        default: 1,
        validator: (value) => value > 0,
    },
});

const emit = defineEmits(["pageChange", "update:modelValue"]);

const pageBreakSign = "...";

const availablePages = computed(() => {
    const { modelValue, totalPages } = props;

    const pageOffset = 2;
    const breakPageLimit = pageOffset + 2;

    const dynamicPages = [];
    const startDynamicPage = modelValue > breakPageLimit ? modelValue - pageOffset : 2;
    const endDynamicPage =
        totalPages - modelValue >= breakPageLimit ? modelValue + pageOffset : totalPages - 1;

    for (let i = startDynamicPage; i <= endDynamicPage; i++) dynamicPages.push(i);

    const pages = [1];
    if (totalPages <= 1) return pages;

    if (modelValue > breakPageLimit) pages.push(pageBreakSign);
    pages.push(...dynamicPages);

    if (totalPages - modelValue >= breakPageLimit) pages.push(pageBreakSign);
    pages.push(totalPages);

    return pages;
});

const onPageClick = async (newPage) => {
    if (props.modelValue === newPage) return;

    emit("update:modelValue", newPage);
};
</script>

<style scoped lang="scss">
.v-pagination {
    @apply flex;

    &__btn {
        @apply m-0.5 h-[36px] w-full max-w-[28px];
    }

    &__prev {
        @apply mr-1;
    }

    &__next {
        @apply ml-1;
    }
}
</style>
