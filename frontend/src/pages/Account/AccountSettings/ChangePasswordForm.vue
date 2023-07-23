<template>
    <v-form class="rounded-md bg-white p-6 shadow">
        <div class="flex items-center">
            <h4 class="mb-0">Пароль</h4>
            <v-btn class="ml-auto" type="button" variant="tonal" @click="isOpen = true">
                Изменить
            </v-btn>
        </div>
        <div v-if="isOpen" class="mt-1">
            <div class="mb-4 flex justify-between sm:flex-col sm:justify-start">
                <v-input
                    v-model="state.first_name"
                    class="change-password__input"
                    type="password"
                    label="Текущий пароль"
                    :error-message="v$.oldPassword.$errors[0]?.$message"
                    :readonly="isLoading"
                ></v-input>
                <v-input
                    v-model="state.last_name"
                    class="change-password__input mx-6 sm:mx-0"
                    type="password"
                    label="Новый пароль"
                    :error-message="v$.newPassword.$errors[0]?.$message"
                    :readonly="isLoading"
                ></v-input>
                <v-input
                    v-model="state.phone"
                    class="change-password__input"
                    type="password"
                    label="Новый пароль еще раз"
                    :error-message="v$.confirmNewPassword.$errors[0]?.$message"
                    :readonly="isLoading"
                ></v-input>
            </div>
            <div class="flex justify-end">
                <v-btn @click="onSave">Сохранить</v-btn>
            </div>
        </div>
    </v-form>
</template>

<script setup>
import VInput from "@/components/UI/VInput.vue";
import VBtn from "@/components/UI/VBtn.vue";
import { reactive, ref } from "vue";
import { required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { api } from "@/api/api.js";
import VForm from "@/components/UI/VForm.vue";

const isOpen = ref(false);

const state = reactive({ currentPassword: "", newPassword: "", confirmNewPassword: "" });
const isLoading = ref(false);

const rules = {
    oldPassword: { required },
    newPassword: { required },
    confirmNewPassword: { required },
};

const v$ = useVuelidate(rules, state);

// const onSave = () => {
//     try {
//         api.auth.changePassword(state);
//     } catch (e) {}
// };
</script>

<style scoped lang="scss">
.change-password {
    &__input {
        @apply w-4/12 sm:mb-4 sm:w-full;
    }
}
</style>
