<template>
    <div class="header__top-bar sm:hidden">
        <div class="container flex h-full items-center justify-end">
            <a class="telegram-link" href="https://t.me/alma_market_bot" target="_blank">
                Связаться в Telegram
            </a>
        </div>
    </div>
    <header class="header__bottom">
        <div class="header__bottom-content container flex h-full items-center">
            <div class="header__logo flex items-center">
                <v-btn class="header__burger" size="small" @click="isMobileMenuOpen = true">
                    <v-icon :mdi-icon="mdiMenu"></v-icon>
                </v-btn>
                <app-logo class="mr-10 sm:mr-0"></app-logo>
            </div>
            <div class="header__search flex">
                <v-input
                    v-model="search"
                    class="grow"
                    label="Поиск"
                    variant="regular"
                    placeholder="Поиск..."
                    @keydown.enter="onSearch"
                >
                    <template #appendInner>
                        <v-btn
                            :icon="mdiMagnify"
                            bg-color="transparent"
                            text-color="grey"
                            @click="onSearch"
                        ></v-btn>
                    </template>
                </v-input>
            </div>
            <div class="header__actions ml-2 flex justify-end">
                <div class="sm:hidden">
                    <v-btn
                        v-if="!isLoggedIn"
                        :prepend-icon="mdiAccount"
                        @click="isAuthorizeModalOpen = true"
                    >
                        Войти
                    </v-btn>
                    <v-dropdown v-else>
                        <template #target>
                            <v-btn :prepend-icon="mdiAccount">{{ user.name }}</v-btn>
                        </template>

                        <v-dropdown-item
                            v-if="isAdmin"
                            title="Админ панель"
                            :to="{ name: 'Admin' }"
                        ></v-dropdown-item>
                        <v-dropdown-item
                            title="Заказы"
                            :to="{ name: 'AccountOrders' }"
                        ></v-dropdown-item>
                        <v-dropdown-item
                            title="Настройки"
                            :to="{ name: 'AccountSettings' }"
                        ></v-dropdown-item>
                        <v-dropdown-item title="Выход" @click="onLogout"></v-dropdown-item>
                    </v-dropdown>
                </div>
                <div class="relative">
                    <v-btn
                        :prepend-icon="isMobile ? null : mdiCart"
                        :size="isMobile ? 'small' : null"
                        :to="{ name: 'Cart' }"
                    >
                        <template v-if="!isMobile"> Корзина </template>
                        <v-icon v-else :mdi-icon="mdiCart"></v-icon>
                    </v-btn>
                    <span class="cart__badge">
                        {{ cartItems.length }}
                    </span>
                    <transition name="scale">
                        <div v-if="lastAddedItem && !isMobile" class="cart__notification">
                            <span class="cart__notification-title"> Товар добавлен в корзину </span>
                            <div class="cart__notification-content">
                                <img
                                    class="cart__notification-image"
                                    :src="lastAddedItem.image"
                                    alt="Goods item image"
                                />
                                <p class="cart__notification-text">{{ lastAddedItem.name }}</p>
                            </div>
                        </div>
                    </transition>
                </div>
            </div>
        </div>
        <authorize-dialog v-model="isAuthorizeModalOpen"></authorize-dialog>
        <mobile-menu
            v-model:is-open="isMobileMenuOpen"
            @authorize="isAuthorizeModalOpen = true"
        ></mobile-menu>
    </header>
</template>

<script setup>
import VBtn from "@/components/UI/VBtn.vue";
import AppLogo from "@/components/AppLogo.vue";
import AuthorizeDialog from "@/components/Authorize/AuthorizeModal.vue";
import VDropdown from "@/components/UI/VDropdown/VDropdown.vue";
import VDropdownItem from "@/components/UI/VDropdown/VDropdownItem.vue";
import VInput from "@/components/UI/VInput.vue";
import { mdiAccount, mdiCart, mdiMagnify, mdiMenu } from "@mdi/js";
import { useCartStore } from "@/stores/cartStore.js";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/authStore.js";
import { storeToRefs } from "pinia";
import { useScreen } from "@/composables/useScreen.js";
import VIcon from "@/components/UI/VIcon.vue";
import MobileMenu from "@/components/MobileMenu.vue";

const search = ref("");
const isAuthorizeModalOpen = ref(false);

const cartStore = useCartStore();
const { cartItems, lastAddedItem } = storeToRefs(cartStore);

const router = useRouter();

const onSearch = () => {
    router.push({ name: "Home", query: { search: search.value } });
    document.activeElement.blur();
    search.value = "";
};

const authStore = useAuthStore();
const { user, isLoggedIn, isAdmin } = storeToRefs(authStore);
const { onLogout } = authStore;

const { isMobile } = useScreen();

const isMobileMenuOpen = ref(false);
</script>

<style lang="scss" scoped>
.header {
    @apply flex flex-col;

    &__content {
        @apply absolute w-full bg-primary;
    }

    &__top-bar {
        @apply h-11 bg-primary brightness-90 sm:hidden;
    }

    &__bottom {
        @apply sticky top-0 z-20 h-[80px] w-full bg-primary sm:h-[105px];

        :global(*) {
            @apply scroll-mt-[80px] sm:scroll-mt-[105px];
        }

        &-content {
            display: grid;
            grid-template-areas: "logo search actions";

            @screen sm {
                grid-template-rows: 50px 50px;
                grid-template-areas:
                    "logo actions"
                    "search search";
            }
        }
    }

    &__logo {
        grid-area: logo;
    }

    &__search {
        grid-area: search;
    }

    &__actions {
        grid-area: actions;
    }

    &__burger {
        @apply mr-2 hidden sm:block;
    }
}

.cart {
    &__badge {
        @apply absolute -top-1 left-[85%]
        flex h-[20px]
        w-auto min-w-[20px] 
        items-center justify-center 
        rounded-full 
        bg-white 
        p-0.5
        text-sm font-medium leading-none
        sm:-top-0.5 sm:left-[80%]
        sm:h-[16px] sm:min-w-[16px];
    }

    &__notification {
        @apply absolute -bottom-5 right-0 top-[120%]
        h-fit w-96
        origin-top-right
        rounded
        bg-white
        p-4
        shadow-md;

        &-title {
            @apply mb-1 block text-lg font-medium;
        }

        &-content {
            @apply flex w-full items-center;
        }

        &-image {
            @apply mr-2 w-24;
        }

        &-text {
            @apply line-clamp-2;
        }
    }
}

.telegram-link {
    @apply font-medium text-white hover:underline;
}

.scale-enter-active,
.scale-leave-active {
    @apply transition-all;
}

.scale-enter-from,
.scale-leave-to {
    @apply scale-[0.2] opacity-0;
}
</style>
