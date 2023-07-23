<template>
    <div class="goods-item-card">
        <router-link
            class="goods-item-card__img-link"
            :title="goodsItem.name"
            :to="{ name: 'GoodsItem', params: { id: goodsItem.id, tab: '' } }"
        >
            <img :src="goodsItem.image" alt="photo" />
        </router-link>

        <div class="goods-item-card__content">
            <router-link
                class="goods-item-card__title"
                :title="goodsItem.name"
                :to="{ name: 'GoodsItem', params: { id: goodsItem.id, tab: '' } }"
            >
                {{ goodsItem.name }}
            </router-link>
            <div class="goods-item-card__actions">
                <span class="goods-item-card__price">
                    {{ formatPrice(goodsItem.price) }}
                </span>
                <v-btn
                    v-if="isEditable"
                    variant="outlined"
                    :to="{ name: 'AdminGoodsItem', params: { id: goodsItem.id } }"
                    >Изменить
                </v-btn>
                <template v-else>
                    <v-btn
                        v-if="!inCart(goodsItem)"
                        :loading="isAddToCartLoading"
                        @click="onAddToCart(goodsItem)"
                    >
                        В корзину
                    </v-btn>
                    <v-btn v-else variant="outlined" :to="{ name: 'Cart' }"> В корзине</v-btn>
                </template>
            </div>
        </div>
    </div>
</template>

<script setup>
import VBtn from "@/components/UI/VBtn.vue";
import { formatPrice } from "@/utils/formatPrice.js";
import { useCartStore } from "@/stores/cartStore.js";
import { ref } from "vue";

defineProps({
    goodsItem: {
        type: [null, Object],
        default: null,
    },
    isEditable: {
        type: Boolean,
        default: false,
    },
});

const { inCart, addToCart } = useCartStore();

const isAddToCartLoading = ref(false);
const onAddToCart = async (goodsItem) => {
    isAddToCartLoading.value = true;
    await addToCart(goodsItem);
    isAddToCartLoading.value = false;
};
</script>

<style lang="scss" scoped>
.goods-item-card {
    @apply flex flex-col rounded-md bg-white p-6 shadow-md sm:flex-row;

    &__title {
        @apply my-3 
        line-clamp-4 
        h-14
        text-lg font-medium 
        transition-colors hover:text-primary 
        sm:my-0 sm:mb-1 sm:line-clamp-4 sm:h-24 sm:text-base;
    }

    &__img-link {
        @apply m-auto flex 
        h-[250px] w-full max-w-[250px] 
        items-center justify-center 
        p-3 
        sm:m-0 sm:mr-4 sm:h-[140px] sm:max-w-[100px] sm:items-start sm:p-0;
    }

    &__content {
        @apply mt-auto 
        flex flex-col justify-end 
        sm:mt-0 sm:w-full sm:justify-between;
    }

    &__actions {
        @apply flex items-center justify-end sm:flex-col sm:items-end;
    }

    &__price {
        @apply mr-3 text-lg font-bold sm:mb-1 sm:mr-0;
    }
}
</style>
