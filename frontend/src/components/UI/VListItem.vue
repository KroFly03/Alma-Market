<template>
    <component
        :is="to ? 'a' : 'div'"
        class="v-list-item"
        :class="{ 'v-list-item--active': isActive }"
        :href="link?.href.value"
        @click="onClick"
    >
        <div class="v-list-item__overlay"></div>
        <div class="v-list-item__title">{{ title }}</div>
    </component>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { computed } from "vue";

const props = defineProps({
    to: {
        type: [null, String, Object],
        default: null,
    },
    title: {
        type: String,
        default: "",
    },
    active: {
        type: [null, Boolean],
        default: null,
    },
});

const link = props.to ? RouterLink.useLink({ to: props.to }) : null;
const isLink = computed(() => link !== null);

const isActive = computed(() => {
    if (props.active !== null) return props.active;

    if (isLink.value) return link.isActive.value;

    return false;
});

const onClick = (e) => {
    if (isLink.value) link.navigate?.(e);
};
</script>

<style scoped lang="scss">
.v-list-item {
    @apply relative flex cursor-pointer items-center rounded-md px-5 py-2.5;

    &:hover {
        @apply text-primary;
    }

    &--active {
        @apply font-medium text-primary;

        .v-list-item__overlay {
            @apply opacity-10;
        }
    }

    &__overlay {
        @apply pointer-events-none
    absolute left-0 top-0
    h-full w-full
    bg-[currentColor]
    opacity-0 transition-opacity;

        border-radius: inherit;
        border-color: inherit;
    }
}
</style>
