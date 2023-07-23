<template>
    <div>
        <div class="mb-4 flex items-center">
            <button @click="emit('close')">
                <v-icon class="text-grey" :mdi-icon="mdiArrowLeft"></v-icon>
            </button>
            <h3 class="mb-0 ml-3">Восстановление пароля</h3>
        </div>
        <v-form v-if="!isEmailSent" @submit="onSend">
            <p class="text-sm">
                Укажите адрес электронной почты, который вы использовали при регистрации. Мы вышлем
                вам инструкцию по восстановлению пароля
            </p>
            <v-input
                v-model="state.email"
                class="mb-4"
                label="Email"
                :error-message="v$.email.$errors[0]?.$message"
            ></v-input>
            <v-btn class="w-full" :loading="isLoading">Восстановить</v-btn>
        </v-form>
        <p v-else class="text-sm">Письмо отправлено. Следуйте инструкции в нем</p>
    </div>
</template>

<script setup>
import VInput from "@/components/UI/VInput.vue";
import VBtn from "@/components/UI/VBtn.vue";
import VIcon from "@/components/UI/VIcon.vue";
import { reactive, ref } from "vue";
import { email, required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { api } from "@/api/api.js";
import { mdiArrowLeft } from "@mdi/js";
import VForm from "@/components/UI/VForm.vue";

const emit = defineEmits(["close"]);

const state = reactive({ email: "" });
const isLoading = ref(false);
const rules = { email: { required, email } };

const v$ = useVuelidate(rules, state);

const isEmailSent = ref(false);

const onSend = async () => {
    if (!(await v$.value.$validate())) return;

    isLoading.value = true;
    try {
        await api.auth.forgotPassword(state);
        isEmailSent.value = true;
    } catch (e) {
        console.log("error");
    }
    isLoading.value = false;
};
</script>

<style scoped lang="scss"></style>
