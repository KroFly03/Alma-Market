<template>
    <paginated-item-list :current-page="page" :total-pages="totalPages" :is-loading="isLoading">
        <template #top>
            <search-row v-model="search"></search-row>
        </template>

        <!--      TODO: Таблицу вынести в компонент-->
        <div class="v-table rounded-md bg-white shadow-md">
            <table class="w-full">
                <thead>
                    <tr>
                        <th class="v-table__cell text-left">Email пользователя</th>
                        <th class="v-table__cell text-left">Имя</th>
                        <th class="v-table__cell text-left">Фамилия</th>
                        <th class="v-table__cell text-left">Телефон</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in users" :key="user.id" class="v-table__row">
                        <td class="v-table__cell">{{ user.email }}</td>
                        <td class="v-table__cell">{{ user.first_name }}</td>
                        <td class="v-table__cell">{{ user.last_name }}</td>
                        <td class="v-table__cell">{{ user.phone }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </paginated-item-list>
</template>

<script setup>
import PaginatedItemList from "@/components/PaginatedItemList.vue";
import SearchRow from "@/components/SearchRow.vue";
import { onMounted, ref, watch } from "vue";
import { usePaginatedDataLoad } from "@/composables/usePaginatedDataLoad.js";
import { api } from "@/api/api.js";
import { useWatchDebounce } from "@/composables/useWatchDebounce.js";
import { useRouteQuery } from "@/composables/useRouteQuery.js";

const { isLoading, data: users, totalPages, loadPaginatedData } = usePaginatedDataLoad();

const page = useRouteQuery("page", 1);

const loadUsers = async () => {
    await loadPaginatedData(
        async () => await api.users.get({ page: page.value, search: search.value })
    );
};

onMounted(async () => {
    await loadUsers();
});

const search = ref("");
useWatchDebounce(
    search,
    async () => {
        page.value = 1;
        await loadUsers();
    },
    { delayMs: 1000 }
);

watch(page, loadUsers);
</script>

<style lang="scss">
.v-table {
    @apply overflow-x-auto;

    &__row {
        &:hover {
            .v-table__cell {
                @apply bg-black bg-opacity-10 transition-colors;
            }
        }
    }

    &__cell {
        @apply border-b border-b-grey border-opacity-20 px-4 py-2;
    }
}
</style>
