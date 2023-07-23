<template>
    <div class="flex w-full justify-between sm:flex-col">
        <div class="mr-4 xl:w-3/12 lg:w-4/12 sm:mb-4 sm:mr-0 sm:w-full">
            <div class="rounded-md bg-white p-3 shadow-md">
                <v-select v-model="selectedCategory" class="mb-3" label="Категория">
                    <v-option :value="null" label="Все"></v-option>
                    <v-option
                        v-for="filterCategory in categories"
                        :key="filterCategory.id"
                        :label="filterCategory.name"
                        :value="filterCategory.id"
                    ></v-option>
                </v-select>
                <v-select v-model="selectedManufacturer" class="mb-3" label="Производитель">
                    <v-option :value="null" label="Все"></v-option>
                    <v-option
                        v-for="filterManufacturer in manufacturers"
                        :key="filterManufacturer.id"
                        :label="filterManufacturer.name"
                        :value="filterManufacturer.id"
                    ></v-option>
                </v-select>
                <div>
                    <h5 class="mb-1 ml-1">Цена</h5>
                    <div class="flex items-center">
                        <v-input
                            v-model="priceMin"
                            variant="regular"
                            label="Мин."
                            max-length="6"
                        ></v-input>
                        <span class="mx-2">—</span>
                        <v-input
                            v-model="priceMax"
                            variant="regular"
                            label="Макс."
                            max-length="6"
                        ></v-input>
                    </div>
                </div>
                <div class="mt-4 flex">
                    <v-btn class="mr-3 flex-grow" variant="outlined" @click="onResetFilter">
                        Сбросить
                    </v-btn>
                    <v-btn class="flex-grow" @click="onFilter">Применить</v-btn>
                </div>
            </div>
        </div>
        <paginated-item-list
            v-model:current-page="page"
            class="xl:w-9/12 lg:w-8/12 sm:w-full"
            :total-pages="totalPages"
        >
            <template #top>
                <h3 v-if="search" class="mb-4">Результаты поиска: «{{ search }}»</h3>
            </template>

            <p v-if="!goods.length && !isLoading">По вашему запросу ничего не найдено.</p>

            <div class="grid grid-cols-3 gap-6 lg:grid-cols-2 md:grid-cols-1 sm:grid-cols-1">
                <template v-if="isLoading">
                    <goods-item-card-skeleton
                        v-for="idx in 6"
                        :key="idx"
                    ></goods-item-card-skeleton>
                </template>
                <template v-else>
                    <goods-item-card
                        v-for="goodsItem in goods"
                        :key="goodsItem.id"
                        :goods-item="goodsItem"
                    ></goods-item-card>
                </template>
            </div>
        </paginated-item-list>

        <!--      router-view for modals on page-->
        <router-view v-show="false"></router-view>
    </div>
</template>

<script setup>
import GoodsItemCard from "@/components/GoodsItemCard/GoodsItemCard.vue";
import GoodsItemCardSkeleton from "@/components/GoodsItemCard/GoodsItemCardSkeleton.vue";
import PaginatedItemList from "@/components/PaginatedItemList.vue";
import VSelect from "@/components/UI/VSelect/VSelect.vue";
import VOption from "@/components/UI/VSelect/VOption.vue";
import VBtn from "@/components/UI/VBtn.vue";
import VInput from "@/components/UI/VInput.vue";
import { onMounted, ref, watch } from "vue";
import { usePaginatedDataLoad } from "@/composables/usePaginatedDataLoad.js";
import { api } from "@/api/api.js";
import { useRouter } from "vue-router";
import { useRouteQuery } from "@/composables/useRouteQuery.js";

const props = defineProps({
    search: {
        type: String,
        default: "",
    },
    category: {
        type: [null, Number],
        default: null,
    },
    manufacturer: {
        type: [null, Number],
        default: null,
    },
    priceMin: {
        type: [null, Number],
        default: null,
    },
    priceMax: {
        type: [null, Number],
        default: null,
    },
});

const page = useRouteQuery("page", 1, (val) => parseInt(val));

const { isLoading, data: goods, totalPages, loadPaginatedData } = usePaginatedDataLoad();

const categories = ref([]);
const manufacturers = ref([]);

const loadGoods = async () => {
    await loadPaginatedData(() =>
        api.goods.get({
            search: props.search,
            page: page.value,
            category: props.category,
            manufacturer: props.manufacturer,
            priceMin: props.priceMin,
            priceMax: props.priceMax,
        })
    );
};

onMounted(async () => {
    const [_, loadedCategories, loadedManufacturers] = await Promise.allSettled([
        loadGoods(),
        api.goods.getCategories(),
        api.goods.getManufacturers(),
    ]);

    categories.value = loadedCategories.value;
    manufacturers.value = loadedManufacturers.value;
});

const selectedCategory = ref(props.category);
const selectedManufacturer = ref(props.manufacturer);
const priceMin = ref(props.priceMin);
const priceMax = ref(props.priceMax);

const router = useRouter();
const onFilter = () => {
    const filterQuery = {};

    filterQuery.search = props.search || undefined;
    filterQuery.category = selectedCategory.value || undefined;
    filterQuery.manufacturer = selectedManufacturer.value || undefined;
    filterQuery.priceMin = priceMin.value || undefined;
    filterQuery.priceMax = priceMax.value || undefined;

    router.push({
        query: filterQuery,
    });
};

const onResetFilter = () => {
    selectedCategory.value = null;
    selectedManufacturer.value = null;
    priceMin.value = "";
    priceMax.value = "";
};

watch(
    () => [props.search, props.category, props.manufacturer, props.priceMin, props.priceMax],
    async () => {
        page.value = 1;

        selectedCategory.value = props.category;
        selectedManufacturer.value = props.manufacturer;
        priceMin.value = props.priceMin;
        priceMax.value = props.priceMax;

        await loadGoods();
    }
);

watch(page, async () => await loadGoods());
</script>

<style lang="scss" scoped></style>
