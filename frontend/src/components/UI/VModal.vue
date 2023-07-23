<template>
    <teleport to="body">
        <transition :name="isMobile ? 'mobile' : 'desktop'" duration="400">
            <div
                v-if="isOpen"
                class="v-modal"
                :class="[{ 'v-modal--fullscreen': fullscreen || isMobile }]"
            >
                <div class="v-modal__backdrop" />

                <div class="fixed inset-0">
                    <div class="v-modal__layout" @click.self="onClose">
                        <div
                            class="v-modal__content"
                            :style="{ maxWidth: `${parseInt(maxWidth)}px` }"
                        >
                            <h3 v-if="title" class="v-modal__title">
                                {{ title }}
                            </h3>
                            <button class="v-modal__close" @click="onClose">
                                <v-icon class="v-modal__close-icon" :mdi-icon="mdiClose"></v-icon>
                            </button>
                            <div class="v-modal__content-body">
                                <slot name="body"></slot>
                            </div>
                            <div v-if="$slots.footer" class="mt-4">
                                <slot name="footer"></slot>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </teleport>
</template>
<script setup>
import VIcon from "@/components/UI/VIcon.vue";
import { mdiClose } from "@mdi/js";
import { useScreen } from "@/composables/useScreen.js";

const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false,
    },
    title: {
        type: String,
        default: "",
    },
    maxWidth: {
        type: String,
        default: "300",
    },
    fullscreen: {
        type: Boolean,
        default: false,
    },
    closeOnClickBackdrop: {
        type: Boolean,
        default: true,
    },
});

const emit = defineEmits(["update:isOpen"]);

const onClose = () => {
    console.log("fsa");
    if (!props.closeOnClickBackdrop) return;

    onCloseByButton();
};

const onCloseByButton = () => {
    emit("update:isOpen", false);
};

const { isMobile } = useScreen();
</script>

<style lang="scss" scoped>
.v-modal {
    @apply relative z-50;

    &--fullscreen {
        .v-modal__layout {
            @apply items-stretch p-0 sm:h-full sm:items-end;
        }

        .v-modal__content {
            @apply max-w-full #{!important};
            @apply h-full  rounded-none sm:bottom-0 sm:h-[90%] sm:rounded-t-xl sm:px-4;
        }

        .v-modal__content-body {
            @apply overflow-y-auto;
        }

        .v-modal__close {
            @apply right-2 top-1;

            &-icon {
                @apply h-8 w-8;
            }
        }
    }

    &__backdrop {
        @apply fixed inset-0 bg-black bg-opacity-50;
    }

    &__layout {
        @apply flex min-h-full w-full items-center justify-center;
    }

    &__content {
        @apply absolute
        flex
        w-full
        flex-col 
        overflow-hidden 
        rounded-xl 
        bg-white 
        p-10 pb-0
        shadow-xl
        transition-all;
        //text-left align-middle

        &-body {
            @apply min-h-full pb-5;
        }
    }

    &__header {
        @apply mb-2 flex items-center;
    }

    &__close {
        @apply absolute right-4 
        top-4 
        cursor-pointer text-grey
        outline-none 
        transition-transform hover:scale-110;
    }

    &__title {
        @apply mb-2 text-lg font-medium leading-6;
    }
}

.desktop-enter-active .v-modal__backdrop,
.desktop-leave-active .v-modal__backdrop,
.mobile-enter-active .v-modal__backdrop,
.mobile-leave-active .v-modal__backdrop {
    transition: opacity 0.3s ease-in-out;
}

.desktop-enter-from .v-modal__backdrop,
.desktop-leave-to .v-modal__backdrop,
.mobile-enter-from .v-modal__backdrop,
.mobile-leave-to .v-modal__backdrop {
    opacity: 0;
}

.desktop-enter-active .v-modal__content,
.desktop-leave-active .v-modal__content {
    transition: all 0.2s ease-in-out;
}

.desktop-enter-from .v-modal__content,
.desktop-leave-to .v-modal__content {
    opacity: 0;
    transform: scale(0.95);
}

.mobile-enter-active .v-modal__content,
.mobile-leave-active .v-modal__content {
    transition: all 0.4s ease-in-out;
}

.mobile-enter-from .v-modal__content,
.mobile-leave-to .v-modal__content {
    transform: translateY(100%);
    opacity: 0.5;
}
</style>
