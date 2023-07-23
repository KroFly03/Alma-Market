<template>
    <div v-if="goodsItem" class="goods-item">
        <h1 class="mb-6">
            {{ goodsItem.name }}
        </h1>
        <div class="mb-6 flex rounded-md bg-white p-8 shadow-md sm:flex-col sm:p-4">
            <div class="flex w-4/12 justify-center sm:mb-3 sm:w-full">
                <img
                    class="goods-item__preview-photo"
                    :src="goodsItem.image"
                    alt="Photo"
                    @click="isFullscreenPhotoOpen = true"
                />
            </div>
            <div class="w-5/12 px-6 sm:w-full sm:px-0">
                <h4>Характеристики:</h4>
                <ul class="mb-3">
                    <li
                        v-for="(characteristic, idx) in previewCharacteristics"
                        :key="idx"
                        class="py-1"
                    >
                        <span class="font-medium"> {{ characteristic.name }}: </span>
                        {{ characteristic.value }}
                    </li>
                </ul>
                <router-link
                    v-if="goodsItem.characteristic.length > previewCharacteristics.length"
                    class="goods-item__more-characteristic"
                    :to="{ params: { tab: 'characteristics' } }"
                    @click="scrollToTabs"
                >
                    Показать все характеристики
                </router-link>
            </div>
            <div class="w-3/12 sm:mt-4 sm:w-full">
                <p class="mb-4 text-4xl font-bold">
                    {{ formatPrice(goodsItem.price) }}
                </p>
                <v-btn
                    v-if="!inCart(goodsItem)"
                    :prepend-icon="mdiCartPlus"
                    @click="addToCart(goodsItem)"
                >
                    В корзину
                </v-btn>
                <v-btn v-else variant="outlined" :to="{ name: 'Cart' }"> Перейти в корзину </v-btn>
            </div>
        </div>

        <v-modal
            :is-open="isFullscreenPhotoOpen"
            fullscreen
            :title="goodsItem.name"
            @update:is-open="isFullscreenPhotoOpen = false"
        >
            <template #body>
                <img class="m-auto h-full p-4" :src="goodsItem.image" alt="Photo" />
            </template>
        </v-modal>

        <div class="mb-6 rounded-md bg-white p-4 shadow-md">
<!--          ref on div because chrome not scroll (with scroll margin) to element with overflow auto -->
          <div ref="tabsRef">
            <v-tabs  class="mb-3">
                <v-tab
                    v-for="tabItem in tabs"
                    :key="tabItem.value"
                    :to="{ params: { tab: tabItem.value } }"
                >
                    {{ tabItem.name }}
                </v-tab>
            </v-tabs>
          </div>
            <v-content-views :value="tab">
                <v-content-view value="">
                    {{ goodsItem.description ?? "Описание отсутствует." }}
                </v-content-view>
                <v-content-view value="characteristics">
                    <div>
                        <ul class="goods-item__characteristics-list">
                            <li
                                v-for="(characteristic, idx) in goodsItem.characteristic"
                                :key="idx"
                                class="w-100 goods-item__characteristics-item p-2"
                            >
                                <span class="goods-item__characteristics-item-name text-grey">
                                    {{ characteristic.name }}:
                                </span>
                                <span class="ml-3">
                                    {{ characteristic.value }}
                                </span>
                            </li>
                        </ul>
                    </div>
                </v-content-view>
            </v-content-views>
        </div>
    </div>
</template>

<script setup>
import VBtn from "@/components/UI/VBtn.vue";
import VTabs from "@/components/UI/VTabs/VTabs.vue";
import VTab from "@/components/UI/VTabs/VTab.vue";
import VModal from "@/components/UI/VModal.vue";
import VContentViews from "@/components/UI/VContentViews/VContentViews.vue";
import VContentView from "@/components/UI/VContentViews/VContentView.vue";
import { mdiCartPlus } from "@mdi/js";
import { computed, onMounted, ref } from "vue";
import { formatPrice } from "@/utils/formatPrice.js";
import { useCartStore } from "@/stores/cartStore.js";
import { api } from "@/api/api.js";

const props = defineProps({
    id: {
        type: [Number, String],
        required: true,
    },
    tab: {
        type: String,
        default: "",
    },
});

const goodsItem = ref(null);
const isFullscreenPhotoOpen = ref(false);

onMounted(async () => {
    goodsItem.value = await api.goods.getById(props.id);
});

const previewCharacteristics = computed(() => {
    return goodsItem.value.characteristic.slice(0, 6);
});

const { addToCart, inCart } = useCartStore();

const tabs = [
    {
        name: "Описание товара",
        value: "",
    },
    {
        name: "Характеристики",
        value: "characteristics",
    },
];

const tabsRef = ref(null);
const scrollToTabs = () => {
  console.log(tabsRef.value.$el);
    setTimeout(() => {
        tabsRef.value.scrollIntoView({ behavior: "smooth" });
    });
};
</script>

<style lang="scss">
.goods-item {
    @apply w-full;

    &__characteristics {
        &-list {
            width: 100%;
            max-width: 800px;
        }

        &-item {
            display: grid;
            grid-template-columns: repeat(2, 1fr);

            &:hover {
                background-color: rgba(var(--v-theme-primary), 0.2);
            }
        }
    }

    &__more-characteristic {
        @apply text-primary;
    }

    &__preview-photo {
        cursor: pointer;
    }
}
</style>
