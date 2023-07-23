<template>
    <div class="v-input" :class="[`v-input--${variant}`]">
        <div class="v-input__control">
            <div class="v-input__control-prepend-inner">
                <slot name="prependInner"></slot>
                <v-icon v-if="prependInnerIcon" :mdi-icon="prependInnerIcon"></v-icon>
            </div>
            <input
                v-if="type !== 'textarea'"
                :id="id"
                ref="$el"
                :value="modelValue"
                :type="type"
                class="v-input__field"
                :placeholder="modelValue ? '' : null"
                :readonly="readonly"
                :minlength="minLength"
                :maxlength="maxLength"
                @input="onInput"
                @focus="(e) => $emit('focus', e)"
                @blur="(e) => $emit('blur', e)"
            />
            <textarea
                v-else
                :id="id"
                ref="$el"
                :value="modelValue"
                class="v-input__field"
                :placeholder="modelValue ? '' : null"
                :readonly="readonly"
                :rows="rows"
                :minlength="minLength"
                :maxlength="maxLength"
                @input="onInput"
                @focus="(e) => $emit('focus', e)"
                @blur="(e) => $emit('blur', e)"
            ></textarea>
            <label v-if="label" :for="id" class="v-input__label">{{ label }}</label>
            <div class="v-input__control-append-inner">
                <slot name="appendInner"></slot>
                <v-icon v-if="appendInnerIcon" :mdi-icon="appendInnerIcon"></v-icon>
            </div>
        </div>
        <transition name="slide">
            <div v-if="errorMessage" class="v-input__error-message">
                {{ errorMessage }}
            </div>
        </transition>
    </div>
</template>

<script setup>
import { computed, ref } from "vue";
import VIcon from "@/components/UI/VIcon.vue";

const props = defineProps({
    modelValue: {
        type: [null, String],
        default: null,
    },
    id: {
        type: [null, String],
        default: null,
    },
    type: {
        type: String,
        default: "text",
    },
    label: {
        type: String,
        default: "",
    },
    placeholder: {
        type: String,
        default: "",
    },
    variant: {
        type: String,
        default: "underline",
        validator: (value) => ["underline", "regular"].includes(value),
    },
    prependInnerIcon: {
        type: [null, String],
        default: null,
    },
    appendInnerIcon: {
        type: [null, String],
        default: null,
    },
    readonly: {
        type: [null, Boolean],
        default: null,
    },
    errorMessage: {
        type: String,
        default: "",
    },
    rows: {
        type: String,
        default: "4",
    },
    minLength: {
        type: [null, String, Number],
        default: null,
    },
    maxLength: {
        type: [null, String, Number],
        default: null,
    },
});

const emit = defineEmits(["update:modelValue", "focus", "blur"]);

const $el = ref();
defineExpose({ $el });

const onInput = (e) => {
    emit("update:modelValue", e.target.value);
};
</script>

<style scoped lang="scss">
.v-input {
    @apply relative;

    &__control {
        @apply flex items-center;

        &-append-inner {
            @apply ml-1 flex text-grey;
        }
    }

    &--underline {
        .v-input__field {
            @apply border-b border-grey
      bg-transparent
      hover:border-primary
      focus:border-b-2 focus:border-primary;
        }
    }

    &--regular {
        .v-input__control {
            @apply rounded-md bg-white px-4 py-0 shadow;
        }

        .v-input__error-message {
            @apply mt-1 px-4;
        }

        .v-input__label {
            @apply left-4 top-3;
        }

        .v-input__field {
            @apply mt-2;
        }

        .v-input__field:focus,
        .v-input__field[placeholder] {
            ~ .v-input__label {
                @apply top-0.5;
            }
        }
    }

    &__field {
        @apply mt-3 h-[36px] w-full focus:outline-none;

        &:is(textarea) {
            @apply h-auto;
        }

        &:focus {
            ~ .v-input__label {
                @apply text-primary;
            }
        }

        &:focus,
        &[placeholder] {
            ~ .v-input__label {
                @apply top-0 text-xs;
            }
        }
    }

    &__label {
        @apply pointer-events-none 
        absolute left-0 top-5 
        w-full 
        overflow-hidden
        text-ellipsis
        whitespace-nowrap 
        text-grey 
        transition-all;
    }

    &__error-message {
        @apply mt-2 text-xs text-error;
    }
}

.slide-enter-active,
.slide-leave-active {
    transition: all 0.2s ease-in-out;
}

.slide-enter-from,
.slide-leave-to {
    transform: translateY(-50%);
    opacity: 0;
}
</style>
