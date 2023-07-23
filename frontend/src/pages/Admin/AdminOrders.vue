<template>
    <paginated-item-list
        :current-page="currentPage"
        :total-pages="totalPages"
        :is-loading="isLoading"
        @update-page="loadOrders"
    >
        <template #top>
            <search-row v-model="search"></search-row>
        </template>

        <p v-if="!orders.length && !isLoading">По вашему запросу ничего не найдено.</p>
        <div>
            <OrderItemExpansion
                v-for="(order, idx) in orders"
                :key="order.id"
                v-model:order="orders[idx]"
                for-admin
                @update="onUpdateOrder"
            ></OrderItemExpansion>
        </div>
    </paginated-item-list>
</template>

<script setup>
import OrderItemExpansion from "@/components/OrderItemExpansion.vue";
import PaginatedItemList from "@/components/PaginatedItemList.vue";
import { usePaginatedDataLoad } from "@/composables/usePaginatedDataLoad.js";
import { onMounted, ref, watch } from "vue";
import { api } from "@/api/api.js";
import SearchRow from "@/components/SearchRow.vue";
import { useWatchDebounce } from "@/composables/useWatchDebounce.js";
import { useRouteQuery } from "@/composables/useRouteQuery.js";

const { isLoading, data: orders, totalPages, loadPaginatedData } = usePaginatedDataLoad();

const page = useRouteQuery("page", 1, (val) => parseInt(val));

const loadOrders = async () => {
    await loadPaginatedData(
        async () => await api.orders.get({ page: page.value, search: search.value })
    );
};

onMounted(async () => {
    await loadOrders();
});

const search = ref("");
useWatchDebounce(
    search,
    async () => {
        page.value = 1;

        await loadOrders();
    },
    { delayMs: 1000 }
);

watch(page, loadOrders);

const onUpdateOrder = (order) => {
    console.log(order);
};
</script>
