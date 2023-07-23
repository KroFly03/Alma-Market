<template>
    <paginated-item-list
        :current-page="currentPage"
        :total-pages="totalPages"
        :is-loading="isLoading"
        @update-page="loadOrders"
    >
        <div class="align-self-start">
            <order-item-expansion
                v-for="order in orders"
                :key="order.id"
                :order="order"
            ></order-item-expansion>
        </div>

        <p v-if="!isLoading && !orders.length">У вас еще нет заказов.</p>
    </paginated-item-list>
</template>

<script setup>
import OrderItemExpansion from "@/components/OrderItemExpansion.vue";
import PaginatedItemList from "@/components/PaginatedItemList.vue";
import { usePaginatedDataLoad } from "@/composables/usePaginatedDataLoad.js";
import { onMounted } from "vue";
import { api } from "@/api/api.js";

const {
    isLoading,
    data: orders,
    currentPage,
    totalPages,
    loadPaginatedData,
} = usePaginatedDataLoad();

const loadOrders = async () => {
    await loadPaginatedData(
        async () => await api.orders.getByLoggedUser({ page: currentPage.value })
    );
};

onMounted(async () => {
    await loadOrders();
});
</script>
