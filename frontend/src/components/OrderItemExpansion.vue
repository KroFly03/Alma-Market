<template>
    <Disclosure v-slot="{ open }" as="div" class="order-item">
        <DisclosureButton v-slot="{ open }" class="w-full py-2">
            <div class="flex w-full items-center sm:items-start">
                <v-icon
                    :mdi-icon="mdiChevronDown"
                    class="mr-4 sm:mr-2"
                    :class="{ 'rotate-180': open }"
                ></v-icon>
                <div class="flex items-center sm:flex-col sm:items-start">
                    <div class="flex flex-col items-start">
                        <span class="mr-3 text-sm leading-none">
                            от {{ formatDate(order.created) }}
                        </span>
                        <span class="mr-3 text-lg font-medium sm:text-base">
                            Заказ {{ order.code }}
                        </span>
                    </div>
                    <span
                        class="order-item__status"
                        :class="`order-item__status--${statusesMap.get(order.status)}`"
                    >
                        {{ order.status }}
                    </span>
                </div>
                <div class="ml-auto flex flex-col items-start">
                    <span class="text-sm leading-none">Итого:</span>
                    <span class="text-lg font-medium sm:text-base">{{
                        formatPrice(totalPrice)
                    }}</span>
                </div>
            </div>
        </DisclosureButton>
        <div class="relative min-h-[80px] overflow-hidden">
            <transition name="preview">
                <div v-if="!open" class="absolute mt-2 flex items-center">
                    <img
                        v-for="previewImage in previewImages"
                        :key="previewImage"
                        :src="previewImage"
                        class="order-item__preview-image"
                        alt="photo"
                    />
                    <div
                        v-if="order.goods.length > previewImages.length"
                        class="order-item__preview-left order-item__preview-image"
                    >
                        <span> + {{ order.goods.length - previewImages.length }} </span>
                    </div>
                </div>
            </transition>

            <transition name="content">
                <DisclosurePanel as="div">
                    <div v-if="forAdmin" class="mb-4">
                        <div class="flex sm:flex-col">
                            <span class="mr-2 font-medium">Имя клиента:</span>
                            <span>{{ order.user.first_name }}</span>
                        </div>
                        <div class="flex sm:flex-col">
                            <span class="mr-2 font-medium">Телефон клиента:</span>
                            <span>{{ order.user.phone }}</span>
                        </div>
                        <div class="mt-2 flex">
                            <v-select v-model="selectedNewStatus" variant="regular" label="Статус">
                                <v-option
                                    v-for="[key, value] in statusesMap"
                                    :key="value"
                                    :value="value"
                                    :label="key"
                                >
                                </v-option>
                            </v-select>
                            <v-btn class="ml-2" @click="updateStatus">Изменить</v-btn>
                        </div>
                    </div>
                    <div class="mb-5">
                        <div class="flex sm:flex-col">
                            <span class="mr-2 font-medium">Способ получения:</span>
                            <span>
                                {{ order.address }}
                            </span>
                        </div>
                        <div class="flex sm:flex-col">
                            <span class="mr-2 font-medium">Дата доставки:</span>
                            <span>
                                {{ formatDate(order.receive) }}
                            </span>
                        </div>
                    </div>
                    <div
                        v-for="goodsItem in order.goods"
                        :key="goodsItem.id"
                        class="flex items-center sm:mb-3 sm:flex-wrap"
                    >
                        <router-link
                            class="mr-4 flex-shrink-0"
                            :to="{
                                name: 'GoodsItem',
                                params: { id: goodsItem.id, tab: '' },
                            }"
                        >
                            <img :src="goodsItem.image" class="h-24 w-24" alt="photo" />
                        </router-link>
                        <router-link
                            v-bind="props"
                            class="mr-3 font-medium transition-colors hover:text-primary sm:order-1 sm:mr-0 sm:mt-2 sm:w-full sm:text-sm"
                            :to="{
                                name: 'GoodsItem',
                                params: { id: goodsItem.id, tab: '' },
                            }"
                        >
                            {{ goodsItem.name }}
                        </router-link>
                        <div class="ml-auto flex items-center whitespace-nowrap sm:w-auto">
                            <span class="mr-1 text-sm leading-normal"
                                >{{ goodsItem.amount }} шт. x
                            </span>
                            <span class="font-medium">
                                {{ formatPrice(goodsItem.price) }}
                            </span>
                        </div>
                    </div>
                </DisclosurePanel>
            </transition>
        </div>
    </Disclosure>
</template>

<script setup>
import { computed, ref } from "vue";
import { formatPrice } from "@/utils/formatPrice.js";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import { mdiChevronDown } from "@mdi/js";
import VIcon from "@/components/UI/VIcon.vue";
import VBtn from "@/components/UI/VBtn.vue";
import VSelect from "@/components/UI/VSelect/VSelect.vue";
import VOption from "@/components/UI/VSelect/VOption.vue";
import { api } from "@/api/api.js";

const props = defineProps({
    order: {
        type: Object,
        required: true,
    },
    forAdmin: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:order"]);

const previewImages = computed(() =>
    props.order.goods.slice(0, 5).map((goodsItem) => goodsItem.image)
);

const totalPrice = computed(() =>
    props.order.goods.reduce((accum, goodsItem) => accum + goodsItem.price, 0)
);

const statusesMap = new Map([
    ["Сформирован", "formed"],
    ["Выполнен", "completed"],
    ["Отменен", "canceled"],
]);

const selectedNewStatus = ref(statusesMap.get(props.order.status));

const updateStatus = async () => {
    const response = await api.orders.updateStatus(props.order.id, selectedNewStatus.value);

    emit("update:order", {
        ...props.order,
        status: [...statusesMap].find((keyValue) => keyValue[1] === response.status)[0],
    });
};

const formatDate = (date) => {
    return new Date(date).toLocaleDateString("ru");
};
</script>

<style lang="scss" scoped>
.order-item {
    @apply mb-3 rounded-md bg-white p-4 shadow-md;

    &__status {
        @apply ml-2 rounded-full px-3 py-1 text-sm text-white sm:ml-0 sm:px-2 sm:py-0.5;

        &--formed {
            @apply bg-primary;
        }
        &--completed {
            @apply bg-[green];
        }
        &--canceled {
            @apply bg-error;
        }
    }

    &__preview-image {
        @apply mr-2 h-16 w-16;
    }

    &__preview-left {
        @apply flex
    items-center justify-center
    text-lg font-medium text-primary;
    }
}

.preview-enter-active,
.preview-leave-active {
    transition: all 0.1s ease-in-out;
}

.preview-enter-from,
.preview-leave-to {
    opacity: 0;
    transform: translateY(-40%);
}

.content-enter-active,
.content-leave-active {
    transition: all 0.2s ease-out;
}

.content-enter-from,
.content-leave-to {
    opacity: 0;
}
</style>
