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
            <RadioGroup v-model="state.address">
                <RadioGroupOption
                    v-for="address in addresses"
                    :key="address.id"
                    v-slot="{ checked }"
                    as="template"
                    :value="address.id"
                >
                    <div
                        class="cart__address-radio"
                        :class="checked ? 'cart__address-radio--checked' : ''"
                    >
                        <div class="w-[40px]">
                            <v-icon
                                v-if="checked"
                                class="mr-2 text-primary"
                                :mdi-icon="mdiCheckCircleOutline"
                            ></v-icon>
                        </div>
                        <span>{{ address.name }}</span>
                    </div>
                </RadioGroupOption>
            </RadioGroup>
            <p v-if="v$.address.$errors.length" class="text-error">
                {{ v$.address.$errors[0]?.$message }}
            </p>

            <div class="mt-6 flex items-center justify-between sm:flex-col sm:items-stretch">
                <span class="text-xl sm:mb-3">
                    Итого: <strong>{{ formatPrice(cartStore.cartTotalPrice) }}</strong>
                </span>
                <v-btn :disabled="!isLoggedIn" @click="onCheckout"> Оформить заказ </v-btn>
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
import VIcon from "@/components/UI/VIcon.vue";
import { useCartStore } from "@/stores/cartStore.js";
import { formatPrice } from "@/utils/formatPrice.js";
import { onMounted, reactive, ref, toRefs } from "vue";
import { useAuthStore } from "@/stores/authStore.js";
import { api } from "@/api/api.js";
import { useVuelidate } from "@vuelidate/core";
import { helpers, required } from "@vuelidate/validators";
import { RadioGroup, RadioGroupOption } from "@headlessui/vue";
import { mdiCheckCircleOutline } from "@mdi/js";

const cartStore = useCartStore();
const { isLoggedIn } = toRefs(useAuthStore());

let addresses = ref([]);

onMounted(async () => {
    addresses.value = await api.orders.getAddresses();
});

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
</style>
