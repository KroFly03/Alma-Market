<template>
    <div class="goods-item">
        <h2 class="mb-5">
            {{ isEdit ? "Редактирование товара" : "Добавление товара" }}
        </h2>
        <v-loader-circlular v-if="isLoading"></v-loader-circlular>
        <template v-else>
            <div class="goods-item__main">
                <div class="w-6/12 sm:mb-3 sm:w-full">
                    <div class="h-60">
                        <img
                            v-if="state.imageUrl"
                            class="goods-item__img"
                            :src="state.imageUrl"
                            alt="Goods item"
                        />
                        <v-icon
                            v-else
                            class="goods-item__img"
                            :mdi-icon="mdiImage"
                            color="grey"
                        ></v-icon>
                    </div>
                    <div>
                        <input
                            ref="inputFileRef"
                            type="file"
                            accept="image/png, image/jpeg"
                            @change="onUploadImage"
                        />
                        <p v-if="v$.imageFile.$errors.length" class="mt-1 text-xs text-error">
                            {{ v$.imageFile.$errors[0]?.$message }}
                        </p>
                    </div>
                </div>
                <div class="w-6/12 sm:w-full">
                    <v-input
                        v-model="state.name"
                        class="mb-4"
                        label="Название"
                        variant="regular"
                        :error-message="v$.name.$errors[0]?.$message"
                    ></v-input>
                    <v-input
                        v-model="state.price"
                        class="mb-4"
                        label="Цена"
                        variant="regular"
                        :error-message="v$.price.$errors[0]?.$message"
                    >
                        <template #appendInner> ₽</template>
                    </v-input>
                    <v-input
                        v-model="state.amount"
                        class="mb-4"
                        label="Количество"
                        variant="regular"
                        :error-message="v$.amount.$errors[0]?.$message"
                    ></v-input>
                </div>
            </div>
            <div class="mb-4 flex sm:flex-col">
                <v-autocomplete
                    v-model="state.category"
                    class="mr-3 grow sm:mb-2 sm:mr-0"
                    variant="regular"
                    label="Категория"
                    item-value="id"
                    item-name="name"
                    :items="categories"
                    :error-message="v$.category.$errors[0]?.$message"
                ></v-autocomplete>
                <v-autocomplete
                    v-model="state.manufacturer"
                    class="grow"
                    variant="regular"
                    label="Производитель"
                    item-value="id"
                    item-name="name"
                    :items="manufacturers"
                    :error-message="v$.manufacturer.$errors[0]?.$message"
                ></v-autocomplete>
            </div>
            <v-input
                v-model="state.description"
                class="mb-5"
                label="Описание"
                type="textarea"
                variant="regular"
                rows="10"
            ></v-input>
            <h3 class="mb-4">Характеристики</h3>
            <div class="goods-item__characteristic">
                <v-autocomplete
                    v-model="characteristicToAdd.characteristic"
                    class="goods-item__characteristic-name"
                    :items="allCharacteristics"
                    variant="regular"
                    item-value="id"
                    item-name="name"
                    label="Характеристика"
                ></v-autocomplete>
                <v-input
                    v-model="characteristicToAdd.value"
                    class="goods-item__characteristic-value"
                    variant="regular"
                    label="Значение"
                ></v-input>
                <v-btn
                    class="goods-item__characteristic-btn"
                    variant="tonal"
                    @click="onAddCharacteristic"
                >
                    <v-icon :mdi-icon="mdiPlus"></v-icon>
                </v-btn>
            </div>
            <div
                v-for="(characteristic, idx) in state.characteristics"
                :key="idx"
                class="goods-item__characteristic"
            >
                <v-autocomplete
                    v-model="characteristic.characteristic"
                    class="goods-item__characteristic-name"
                    :items="allCharacteristics"
                    variant="regular"
                    item-value="id"
                    item-name="name"
                    label="Характеристика"
                    :error-message="
                        v$.characteristics.$each.$response.$errors[idx].characteristic[0]?.$message
                    "
                ></v-autocomplete>
                <v-input
                    v-model="characteristic.value"
                    class="goods-item__characteristic-value"
                    variant="regular"
                    label="Значение"
                    :error-message="
                        v$.characteristics.$each.$response.$errors[idx].value[0]?.$message
                    "
                ></v-input>
                <v-btn
                    class="goods-item__characteristic-btn"
                    bg-color="error"
                    variant="tonal"
                    @click="onRemoveCharacteristic(idx)"
                >
                    <v-icon :mdi-icon="mdiMinus"></v-icon>
                </v-btn>
            </div>
            <div class="mt-8 flex justify-end">
                <v-btn size="x-large" @click="onSave">
                    {{ isEdit ? "Сохранить" : "Добавить товар" }}
                </v-btn>
            </div>
        </template>
    </div>
</template>

<script setup>
import VLoaderCirclular from "@/components/UI/Loaders/VLoaderCirclular.vue";
import VInput from "@/components/UI/VInput.vue";
import VBtn from "@/components/UI/VBtn.vue";
import VIcon from "@/components/UI/VIcon.vue";
import VAutocomplete from "@/components/UI/VAutocomplete.vue";
import { onMounted, reactive, ref, toRaw } from "vue";
import { mdiImage, mdiMinus, mdiPlus } from "@mdi/js";
import { helpers, maxLength, numeric, required, requiredIf } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { useDataLoad } from "@/composables/useDataLoad.js";
import { api } from "@/api/api.js";
import { useRouter } from "vue-router";
import { notification } from "@/main.js";

const props = defineProps({
    isEdit: {
        type: Boolean,
        default: false,
    },
    id: {
        type: [Number, String],
        default: 0,
    },
});

const allCharacteristics = ref([]);
const categories = ref([]);
const manufacturers = ref([]);

onMounted(async () => {
    allCharacteristics.value = await api.goods.getAllCharacteristics();
    categories.value = await api.goods.getCategories();
    manufacturers.value = await api.goods.getManufacturers();
});

const state = reactive({
    imageUrl: "",
    imageFile: null,
    name: "",
    price: "",
    amount: "",
    description: "",
    category: null,
    manufacturer: null,
    characteristics: [],
});

const rules = {
    imageFile: { required: requiredIf(!props.isEdit) },
    name: { required, maxLength: maxLength(100) },
    description: { required, maxLength: maxLength(1000) },
    price: { required, numeric },
    amount: { required, numeric },
    category: { required },
    manufacturer: { required },
    characteristics: {
        $each: helpers.forEach({
            characteristic: {
                required,
                isUnique: helpers.withMessage("Характеристика повторяется", (characteristic) => {
                    const characteristicCount = state.characteristics.filter(
                        (item) => item.characteristic === characteristic
                    ).length;

                    return characteristicCount === 1;
                }),
            },
            value: { required },
        }),
    },
};

const { isLoading, loadData } = useDataLoad();

onMounted(async () => {
    if (!props.isEdit) return;

    await loadData(async () => {
        try {
            const goodsItem = await api.goods.getById(props.id);

            state.imageUrl = goodsItem.image;
            state.name = goodsItem.name;
            state.price = goodsItem.price;
            state.amount = goodsItem.amount;
            state.description = goodsItem.description;
            state.category = goodsItem.category.id;
            state.manufacturer = goodsItem.manufacturer.id;
            state.characteristics = goodsItem.characteristics.map((elem) => ({
                characteristic: elem.id,
                value: elem.value,
            }));
        } catch (e) {
            console.log("error");
        }
    });
});

const characteristicToAdd = reactive({ characteristic: null, value: null });
const onAddCharacteristic = () => {
    state.characteristics.unshift({ ...characteristicToAdd });

    characteristicToAdd.characteristic = null;
    characteristicToAdd.value = null;
};
const onRemoveCharacteristic = (removeIdx) => {
    state.characteristics.splice(removeIdx, 1);
};

const inputFileRef = ref();
const onUploadImage = () => {
    if (inputFileRef.value.files.length) {
        state.imageUrl = URL.createObjectURL(inputFileRef.value.files[0]);
        state.imageFile = inputFileRef.value.files[0];
    } else state.imageUrl = "";
};

const v$ = useVuelidate(rules, state);
const router = useRouter();
const onSave = async () => {
    if (!(await v$.value.$validate())) return;

    const goodsItem = toRaw(state);
    if (props.isEdit) goodsItem.id = props.id;

    try {
        const response = props.isEdit
            ? await api.goods.edit(goodsItem)
            : await api.goods.add(goodsItem);

        const message = props.isEdit ? "Товар изменен" : "Товар добавлен";
        notification.show("success", message);
    } catch (e) {
        if (!e.response.ok) {
            notification.show("error", "Произошла ошибка");
        }
    }
};
</script>

<style lang="scss" scoped>
.goods-item {
    &__main {
        @apply mb-4 flex rounded-md bg-white p-8 shadow-md sm:flex-col sm:items-center sm:p-4;
    }

    &__characteristic {
        @apply mb-2 grid gap-3 sm:mb-5 sm:gap-1;

        grid-template-areas:
            "name name value value btn"
            "name name value value btn";

        @screen sm {
            grid-template-areas:
                "name name name btn"
                "value value value btn";
        }

        &-name {
            grid-area: name;
        }

        &-value {
            grid-area: value;
        }

        &-btn {
            @apply grow sm:h-full;

            grid-area: btn;
        }
    }

    &__img {
        @apply h-full w-full p-5;
    }

    &__footer {
        @apply ml-3 flex w-2/12 justify-center;
    }
}
</style>
