<template>
    <div class="cart-item">
        <div class="mr-6 flex w-8/12 items-center sm:mb-3 sm:mr-0 sm:w-full">
            <router-link
                class="cart-item__img-link"
                :to="{
                    name: 'GoodsItem',
                    params: { id: cartItem.item.id, tab: '' },
                }"
            >
                <img class="cart-item__img" :src="cartItem.item.image" alt="photo" />
            </router-link>
            <router-link
                class="cart-item__title"
                :to="{
                    name: 'GoodsItem',
                    params: { id: cartItem.item.id, tab: '' },
                }"
            >
                {{ cartItem.item.name }}
            </router-link>
        </div>
        <div class="flex w-4/12 items-center justify-between sm:w-full sm:justify-end">
            <div class="cart-item__counter">
                <v-btn
                    bg-color="transparent"
                    text-color="grey"
                    :icon="mdiMinus"
                    :disabled="cartStore.updatingGoodsItemId !== null"
                    @click="decrementQuantity(cartItem)"
                >
                </v-btn>
                <span
                    v-if="cartItem.item.id !== cartStore.updatingGoodsItemId"
                    class="text-body-1 font-weight-medium"
                >
                    {{ cartItem.quantity }}
                </span>
                <v-loader-circlular v-else size="18px"></v-loader-circlular>
                <v-btn
                    bg-color="transparent"
                    text-color="grey"
                    :icon="mdiPlus"
                    :disabled="cartStore.updatingGoodsItemId !== null"
                    @click="incrementQuantity(cartItem)"
                >
                </v-btn>
            </div>
            <div class="ml-3 flex items-center">
                <span class="cart-item__price">
                    {{ formatPrice(cartItem.item.price) }}
                </span>
                <v-btn
                    class="ml-2"
                    bg-color="transparent"
                    text-color="grey"
                    :icon="mdiDelete"
                    @click="removeFromCart(cartItem.item)"
                >
                </v-btn>
            </div>
        </div>
    </div>
</template>

<script setup>
import VBtn from "@/components/UI/VBtn.vue";
import VLoaderCirclular from "@/components/UI/Loaders/VLoaderCirclular.vue";
import { mdiDelete, mdiMinus, mdiPlus } from "@mdi/js";
import { useCartStore } from "@/stores/cartStore.js";
import { formatPrice } from "@/utils/formatPrice.js";
import { toRef } from "vue";

defineProps({
    cartItem: {
        type: Object,
        required: true,
    },
});

const cartStore = useCartStore();
const { removeFromCart, incrementQuantity, decrementQuantity } = cartStore;
</script>

<style lang="scss" scoped>
.cart-item {
    @apply mb-3 
    flex items-center 
    rounded-md 
    bg-white 
    px-6 py-4 
    shadow transition-shadow hover:shadow-md
    sm:flex-col;

    &__img {
        @apply m-auto h-full;

        &-link {
            @apply flex h-[150px] w-full max-w-[150px] md:h-[120px] sm:h-[100px] sm:max-w-[120px] sm:flex-shrink-0;
        }
    }

    &__title {
        @apply ml-6 
        text-xl font-medium 
        transition-colors hover:text-primary 
        md:text-base sm:ml-2 sm:text-sm;
    }

    &__counter {
        @apply flex min-w-[100px] max-w-[140px] items-center justify-between;
    }

    &__price {
        @apply text-2xl md:text-lg;
    }
}
</style>
