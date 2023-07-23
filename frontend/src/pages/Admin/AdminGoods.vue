<template>
    <paginated-item-list
        v-model:current-page="page"
        :total-pages="totalPages"
        :is-loading="isLoading"
    >
        <template #top>
            <search-row v-model="search">
                <template #actions>
                    <v-btn :to="{ name: 'AdminGoodsItemNew' }"> Добавить товар </v-btn>
                </template>
            </search-row>
        </template>

        <p v-if="!goods.length && !isLoading">По вашему запросу ничего не найдено.</p>
        <div class="grid grid-cols-3 gap-6 lg:grid-cols-2 sm:grid-cols-1">
            <template v-if="isLoading">
                <goods-item-card-skeleton v-for="idx in 6" :key="idx"></goods-item-card-skeleton>
            </template>
            <template v-else>
                <goods-item-card
                    v-for="goodsItem in goods"
                    :key="goodsItem.id"
                    :goods-item="goodsItem"
                    is-editable
                ></goods-item-card>
            </template>
        </div>
    </paginated-item-list>
</template>

<script setup>
import GoodsItemCard from "@/components/GoodsItemCard/GoodsItemCard.vue";
import PaginatedItemList from "@/components/PaginatedItemList.vue";
import SearchRow from "@/components/SearchRow.vue";
import VBtn from "@/components/UI/VBtn.vue";
import { onMounted, ref, watch } from "vue";
import { usePaginatedDataLoad } from "@/composables/usePaginatedDataLoad.js";
import { api } from "@/api/api.js";
import { useWatchDebounce } from "@/composables/useWatchDebounce.js";
import { useRouteQuery } from "@/composables/useRouteQuery.js";
import GoodsItemCardSkeleton from "@/components/GoodsItemCard/GoodsItemCardSkeleton.vue";

const { isLoading, data: goods, totalPages, loadPaginatedData } = usePaginatedDataLoad();

const page = useRouteQuery("page", 1, (val) => parseInt(val));

const loadGoods = async () => {
    await loadPaginatedData(
        async () => await api.goods.get({ page: page.value, search: search.value })
    );
};

onMounted(async () => {
    await loadGoods();
});

const search = ref("");
useWatchDebounce(
    search,
    async () => {
        page.value = 1;
        await loadGoods();
    },
    { delayMs: 1000 }
);

watch(page, loadGoods);
</script>
