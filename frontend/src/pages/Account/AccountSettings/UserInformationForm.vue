<template>
    <v-form class="rounded-md bg-white p-6 shadow">
        <div class="flex items-center">
            <h4>Личная информация</h4>
            <div class="ml-auto flex">
                <v-loader-circlular v-if="isLoading"></v-loader-circlular>
                <v-fade-transition>
                    <span v-if="isSaved" class="text-sm text-primary"> Сохранено! </span>
                </v-fade-transition>
            </div>
        </div>
        <div class="flex justify-between sm:flex-col sm:justify-start">
            <v-input
                v-model="state.first_name"
                class="user-information__input"
                label="Имя"
                :error-message="v$.first_name.$errors[0]?.$message"
                :readonly="isLoading"
            ></v-input>
            <v-input
                v-model="state.last_name"
                class="user-information__input mx-6 sm:mx-0"
                label="Фамилия"
                :error-message="v$.last_name.$errors[0]?.$message"
                :readonly="isLoading"
            ></v-input>
            <v-input
                v-model="state.phone"
                class="user-information__input"
                label="Телефон"
                :error-message="v$.phone.$errors[0]?.$message"
                :readonly="isLoading"
            ></v-input>
        </div>
    </v-form>
</template>

<script setup>
import VLoaderCirclular from "@/components/UI/Loaders/VLoaderCirclular.vue";
import VFadeTransition from "@/components/UI/Transitions/VFadeTransition.vue";
import VInput from "@/components/UI/VInput.vue";
import { onMounted, reactive, ref } from "vue";
import { maxLength, required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { useWatchDebounce } from "@/composables/useWatchDebounce.js";
import { api } from "@/api/api.js";
import VForm from "@/components/UI/VForm.vue";

const state = reactive({ first_name: "", last_name: "", phone: "" });
const errors = ref(null);

const isLoading = ref(false);
const isSaved = ref(false);

const rules = {
    first_name: { required, maxLength: maxLength(100) },
    last_name: { required, maxLength: maxLength(100) },
    phone: { required },
};

const v$ = useVuelidate(rules, state, { $externalResults: errors });

onMounted(async () => {
    isLoading.value = true;
    const response = await api.auth.current();
    isLoading.value = false;

    Object.keys(state).forEach((key) => {
        state[key] = response[key];
    });

    useWatchDebounce(
        state,
        async () => {
            errors.value = null;
            if (!(await v$.value.$validate())) return;

            isLoading.value = true;
            try {
                await api.auth.update(state);

                isSaved.value = true;
                setTimeout(() => {
                    isSaved.value = false;
                }, 2000);
            } catch (e) {
                if (e.response.status === 400) errors.value = e.json;
            }
            isLoading.value = false;
        },
        { delayMs: 1500 }
    );
});
</script>

<style lang="scss" scoped>
.user-information {
    &__input {
        @apply w-4/12 sm:mb-4 sm:w-full;
    }
}
</style>
