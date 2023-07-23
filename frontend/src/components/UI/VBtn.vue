<template>
    <component
        :is="isLink ? 'a' : 'button'"
        :href="link?.href.value"
        class="v-btn"
        :class="{
            [`${colorClasses}`]: true,
            'v-btn--outlined': variant === 'outlined',
            'v-btn--active': isActive,
            'v-btn--icon': icon,
            'v-btn--loading': loading,
            'v-btn--small': size === 'small',
            'v-btn--large': size === 'large',
        }"
        :disabled="isLink ? disabled : disabled || loading"
        @click="onClick"
    >
        <span class="v-btn__overlay"></span>
        <v-icon v-if="prependIcon" :mdi-icon="prependIcon" class="v-btn__prepend-icon"></v-icon>
        <span class="v-btn__content" :class="loading ? 'invisible' : ''">
            <slot v-if="!icon"></slot>
            <v-icon v-else :mdi-icon="icon"></v-icon>
        </span>
        <v-loader-circlular v-if="loading" class="absolute" color="white"></v-loader-circlular>
    </component>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { computed } from "vue";
import VIcon from "@/components/UI/VIcon.vue";
import VLoaderCirclular from "@/components/UI/Loaders/VLoaderCirclular.vue";

const props = defineProps({
    bgColor: {
        type: String,
        default: "primary",
    },
    textColor: {
        type: String,
        default: "white",
    },
    variant: {
        type: String,
        default: "default",
        validator: (value) => ["default", "outlined", "tonal"].includes(value),
    },
    to: {
        type: [null, String, Object],
        default: null,
    },
    disabled: {
        type: [null, Boolean],
        default: null,
    },
    active: {
        type: [null, Boolean],
        default: null,
    },
    prependIcon: {
        type: [null, String],
        default: null,
    },
    icon: {
        type: [null, String],
        default: null,
    },
    loading: {
        type: Boolean,
        default: false,
    },
    size: {
        type: String,
        default: "default",
        validator: (val) => ["small", "default", "large"].includes(val),
    },
});

const colorClasses = computed(() => {
    if (props.variant === "default") return `bg-${props.bgColor} text-${props.textColor}`;
    // if (props.variant === "tonal") return `text-${props.textColor}`;

    return `border-${props.bgColor} text-${props.bgColor}`;
});

const link = props.to ? RouterLink.useLink({ to: props.to }) : null;
const isLink = computed(() => link !== null);

const isActive = computed(() => {
    if (props.active !== null) return props.active;

    if (isLink.value) return link.isExactActive.value;

    return false;
});

const onClick = (e) => {
    if (props.loading) {
        e.preventDefault();
        return;
    }

    if (isLink.value) link.navigate?.(e);
};
</script>

<style scoped lang="scss">
$base-height: 44px;
$base-padding-x: 14px;

$size-multiplier: 0.2;

.v-btn {
    @apply relative
  inline-flex items-center
  justify-center
  whitespace-nowrap
  rounded-md
  border-primary px-4
  font-medium
  tracking-wide
  transition-colors
  focus:outline-none;

    height: $base-height;
    padding: 0 $base-padding-x;

    &:active {
        .v-btn__overlay {
            @apply bg-black;
        }
    }

    &:hover:not(&--active):not([disabled]),
    &:focus:not(&--active) {
        .v-btn__overlay {
            @apply opacity-5;
        }
    }

    &--small {
        height: calc($base-height * (1 - $size-multiplier));
        padding: 0 calc($base-padding-x * (1 - $size-multiplier));
    }

    &--large {
        height: calc($base-height * (1 + $size-multiplier));
        padding: 0 calc($base-padding-x * (1 + $size-multiplier));
    }

    &--active {
        .v-btn__overlay {
            @apply opacity-10;
        }
    }

    &--loading {
        cursor: pointer;
        pointer-events: all;
    }

    &[disabled]:not(&--loading) {
        pointer-events: none;
        opacity: 0.3;

        .v-btn__overlay {
            //@apply opacity-10;
        }
    }

    &--outlined {
        @apply border bg-transparent;
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

    &__content {
        @apply flex items-center;
    }

    &__prepend-icon {
        @apply mr-1;
    }

    &--icon {
        @apply h-auto rounded-full p-0.5;
    }
}
</style>
