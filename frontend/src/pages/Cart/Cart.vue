<template>
    <div class="w-full">
        <h1>Корзина</h1>
        <template v-if="cartStore.cartItems.length">
            <div class="cart__items">
                <cart-item
                    v-for="cartItem in cartStore.cartItems"
                    :key="cartItem.item.id"
                    :cart-item="cartItem"
                ></cart-item>
            </div>

            <h3 class="mb-2">Самовывоз</h3>

            <yandex-map
                class="yandex-me"
                :settings="settings"
                :zoom="10"
                :coordinates="[59.938955, 30.315644]"
            >
                <yandex-marker
                    marker-id="vfsafv"
                    :coordinates="[59.938955, 30.315644]"
                    marker-type="placemark"
                >
                    <template #component> </template>
                </yandex-marker>
            </yandex-map>

            <div class="mt-6 flex flex-col items-end">
                <button
                    class="mb-2 flex items-center text-sm text-grey hover:underline"
                    @click="onSaveAsPdf"
                >
                    <v-icon :mdi-icon="mdiContentSave"></v-icon>
                    Сохранить в PDF
                </button>
                <div class="flex w-full items-center justify-between sm:flex-col sm:items-stretch">
                    <span class="text-xl sm:mb-3">
                        Итого: <strong>{{ formatPrice(cartStore.cartTotalPrice) }}</strong>
                    </span>
                    <v-btn :disabled="!isLoggedIn" @click="onCheckout"> Оформить заказ </v-btn>
                </div>
            </div>
            <div v-if="!isLoggedIn" class="mt-3 rounded-md bg-grey bg-opacity-20 p-4">
                Для оформления заказа требуется авторизация.
            </div>
        </template>
        <div v-else class="flex flex-col items-center py-4">
            <span class="mb-3 text-xl">В корзине нет товаров</span>
            <v-btn variant="outlined" :to="{ name: 'Home' }"> Вернуться на главную </v-btn>
        </div>
    </div>
</template>

<script setup>
import CartItem from "@/pages/Cart/CartItem.vue";
import VBtn from "@/components/UI/VBtn.vue";
import { useCartStore } from "@/stores/cartStore.js";
import { formatPrice } from "@/utils/formatPrice.js";
import { reactive, toRefs } from "vue";
import { useAuthStore } from "@/stores/authStore.js";
import { api } from "@/api/api.js";
import { useVuelidate } from "@vuelidate/core";
import { helpers, required } from "@vuelidate/validators";
import { RadioGroup, RadioGroupOption } from "@headlessui/vue";
import { mdiCheckCircleOutline, mdiContentSave } from "@mdi/js";
import { YandexMap, YandexMarker } from "vue-yandex-maps";
import VIcon from "@/components/UI/VIcon.vue";

const cartStore = useCartStore();
const { isLoggedIn } = toRefs(useAuthStore());

// let addresses = ref([]);
//
// onMounted(async () => {
//     addresses.value = await api.orders.getAddresses();
// });

const state = reactive({ address: null });
const rules = {
    address: { required: helpers.withMessage("Выберите адрес", required) },
};

const v$ = useVuelidate(rules, state);

const onCheckout = async () => {
    if (!(await v$.value.$validate())) return;

    try {
        const formattedCartItems = cartStore.cartItems.map(({ item, quantity }) => ({
            id: item.id,
            amount: quantity,
        }));

        await api.orders.create(state.address, formattedCartItems);
        cartStore.clearCart();
    } catch (e) {
        console.log("error");
    }
};

const settings = {
    apiKey: "633a73aa-5e99-47fc-bdba-0de30b6dfeca",
    lang: "ru_RU",
    coordorder: "latlong",
    enterprise: false,
    version: "2.1",
};

const onSaveAsPdf = async () => {
    const formattedItems = cartStore.cartItems.map(({ item, quantity }) => ({
        id: item.id,
        name: item.name,
        price: item.price,
        amount: quantity,
    }));

    const blob = await api.basket.getPdf(formattedItems);

    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = "Basket";
    link.click();
};
</script>

<style lang="scss" scoped>
.cart {
    &__address-radio {
        @apply mb-2
        flex
        cursor-pointer
        items-center
        rounded-md
        border border-transparent
        bg-white
        p-4
        shadow-sm
        sm:p-2;

        &--checked {
            @apply border-primary;
        }
    }
}

.yandex-me {
    height: 400px;

    :global(.yandex-balloon) {
        width: 260px;
        height: 120px;
    }
}

.basfb {
    @apply break-all;
}
</style>
