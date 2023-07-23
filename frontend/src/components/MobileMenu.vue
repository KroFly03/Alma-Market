<template>
    <teleport to="body">
        <transition>
            <div
                v-if="isOpen && isMobile"
                class="fixed bottom-0 left-0 right-0 top-0 z-20 flex flex-col bg-white py-2"
            >
                <div class="container">
                    <div class="mb-3">
                        <button class="h-10 w-14" @click="onClose">
                            <v-icon class="m-auto" :mdi-icon="mdiClose"></v-icon>
                        </button>
                    </div>
                    <div>
                        <div v-if="authStore.isLoggedIn" class="flex flex-col">
                            <div class="mobile-menu__btn">
                                <v-icon class="mr-2 text-grey" :mdi-icon="mdiAccount"></v-icon>
                                <span class="text-lg">
                                    {{ authStore.user.name }}
                                </span>
                            </div>

                            <div class="my-3 border-b border-grey border-opacity-30"></div>

                            <template v-if="authStore.isAdmin">
                                <router-link class="text-grey" :to="{ name: 'Admin' }">
                                    Админ панель
                                </router-link>
                                <div class="my-3 border-b border-grey border-opacity-30"></div>
                            </template>

                            <router-link class="py-1 text-grey" :to="{ name: 'AccountOrders' }">
                                Заказы
                            </router-link>
                            <router-link class="py-1 text-grey" :to="{ name: 'AccountSettings' }">
                                Настройки
                            </router-link>
                        </div>

                        <button
                            v-if="!authStore.isLoggedIn"
                            class="mobile-menu__btn hover:underline"
                            @click="onAuthorize"
                        >
                            <v-icon class="mr-1 text-grey" :mdi-icon="mdiAccount"></v-icon>
                            Войти в аккаунт
                        </button>
                        <template v-else>
                            <div class="my-3 border-b border-grey border-opacity-30"></div>
                            <button
                                class="mobile-menu__btn mt-4 text-error"
                                @click="authStore.onLogout"
                            >
                                <v-icon class="mr-1" :mdi-icon="mdiExitToApp"></v-icon>
                                Выход
                            </button>
                        </template>
                        <div class="my-3 border-b border-grey border-opacity-30"></div>
                    </div>
                </div>
            </div>
        </transition>
    </teleport>
</template>

<script setup>
import VIcon from "@/components/UI/VIcon.vue";
import { mdiAccount, mdiClose, mdiExitToApp } from "@mdi/js";
import { useScreen } from "@/composables/useScreen.js";
import { useAuthStore } from "@/stores/authStore.js";
import { useRoute } from "vue-router";
import { watch } from "vue";

const props = defineProps({ isOpen: { type: Boolean, default: false } });
const emit = defineEmits(["update:isOpen", "authorize"]);

const { isMobile } = useScreen();

const onClose = () => {
    emit("update:isOpen", false);
};

const onAuthorize = () => {
    emit("authorize");
};

const authStore = useAuthStore();

const route = useRoute();

watch(
    () => route.path,
    () => {
        onClose();
    }
);
</script>

<style lang="scss" scoped>
.mobile-menu__btn {
    @apply mb-2 flex items-center;
}

.v-enter-active {
    transition: transform 0.4s ease-out;
}
.v-leave-active {
    transition: transform 0.4s ease-in;
}

.v-enter-from,
.v-leave-to {
    transform: translateX(-100%);
}
</style>
