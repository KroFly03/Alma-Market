<template>
    <div class="v-autocomplete" tabindex="0" @focus.capture="isOpen = true">
        <v-input
            v-model="query"
            v-outside-click="onOutsideClick"
            :variant="variant"
            :label="label"
            :error-message="errorMessage"
        >
            <template #appendInner>
                <v-icon :mdi-icon="mdiMenuDown" @click="isOpen = !isOpen"></v-icon>
            </template>
        </v-input>
        <div v-if="isOpen" class="v-autocomplete__items">
            <v-list-item
                v-for="item in filteredItems"
                :key="getItemValue(item)"
                tabindex="0"
                :active="model ? getItemValue(item) === model : false"
                :title="getItemName(item)"
                @click="onItemClick(item)"
                @keydown.enter="onItemClick(item)"
            >
            </v-list-item>
            <div v-if="!filteredItems.length" class="v-autocomplete__item">No results.</div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import VInput from "@/components/UI/VInput.vue";
import VListItem from "@/components/UI/VListItem.vue";
import VOutsideClick from "@/directives/outsideClick.js";
import { mdiMenuDown } from "@mdi/js";
import VIcon from "@/components/UI/VIcon.vue";

const props = defineProps({
    modelValue: {
        type: [null, String, Number],
        required: true,
    },
    variant: {
        type: String,
        default: "underline",
    },
    label: {
        type: String,
        default: "",
    },
    items: {
        type: Array,
        default: () => [],
    },
    itemName: {
        type: String,
        default: "",
    },
    itemValue: {
        type: String,
        default: "",
    },
    filter: {
        type: [null, Function],
        default: null,
    },
    errorMessage: {
        type: String,
        default: "",
    },
});

const emit = defineEmits(["update:modelValue"]);

const isOpen = ref(false);

const model = computed({
    get: () => props.modelValue,
    set: (value) => {
        emit("update:modelValue", value);
    },
});

const query = ref("");

const propFromObjectIfExist = (obj, prop) => (prop ? obj[prop] : obj);
const getItemName = (item) => propFromObjectIfExist(item, props.itemName);
const getItemValue = (item) => propFromObjectIfExist(item, props.itemValue);

const selectedItem = computed(() => props.items.find((x) => getItemValue(x) === model.value));

watch(
    () => selectedItem.value,
    () => {
        query.value = selectedItem.value ? getItemName(selectedItem.value) : "";
    },
    { immediate: true }
);

const defaultFilter = (query, item) =>
    getItemName(item).toLowerCase().includes(query.toLowerCase());

const filteredItems = computed(() => {
    const currentFilter = props.filter || defaultFilter;

    let isQueryEqualToSelectedItem = false;
    if (props.modelValue)
        isQueryEqualToSelectedItem = getItemName(selectedItem.value) === query.value;

    return query.value === "" || isQueryEqualToSelectedItem
        ? props.items
        : props.items.filter((item) => currentFilter(query.value, item));
});

const onOutsideClick = () => {
    const foundItemByQuery = props.items.find((x) => getItemName(x) === query.value);

    if (foundItemByQuery) model.value = getItemValue(foundItemByQuery);
    else query.value = selectedItem.value ? getItemName(selectedItem.value) : "";

    isOpen.value = false;
};

const onItemClick = (item) => {
    model.value = getItemValue(item);
    isOpen.value = false;
};
</script>

<style scoped lang="scss">
.v-autocomplete {
    @apply relative;

    &__items {
        @apply absolute top-[110%] z-10 
        max-h-40 w-full 
        overflow-hidden overflow-y-auto 
        rounded-md 
        bg-white 
        p-1 
        shadow-md;
    }
}
</style>
