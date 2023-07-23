<template>
    <v-form :errors="error" @submit="onLogin">
        <v-input
            id="email"
            v-model="state.email"
            class="mb-4"
            label="Email"
            :error-messages="v$.email.$errors[0]?.$message"
        ></v-input>
        <v-input
            id="password"
            v-model="state.password"
            label="Пароль"
            type="password"
            :autocomplete="false"
            :error-messages="v$.password.$errors[0]?.$message"
        ></v-input>
        <template #bottom>
            <button
                class="mb-2 text-sm hover:text-primary"
                type="button"
                @click="emit('forgotPassword')"
            >
                Забыли пароль?
            </button>
            <v-btn class="mb-2 w-full" :loading="isLoading"> Войти </v-btn>
        </template>
    </v-form>
</template>

<script setup>
import { reactive, ref } from "vue";
import { required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { useAuthStore } from "@/stores/authStore.js";
import VInput from "@/components/UI/VInput.vue";
import VBtn from "@/components/UI/VBtn.vue";
import VForm from "@/components/UI/VForm.vue";

const emit = defineEmits(["success", "forgotPassword"]);

const isLoading = ref(false);
const state = reactive({
    email: "",
    password: "",
});
const error = ref("");

const rules = {
    email: { required },
    password: { required },
};

const v$ = useVuelidate(rules, state);

const authStore = useAuthStore();

const onLogin = async () => {
    if (!(await v$.value.$validate())) return;

    error.value = "";
    isLoading.value = true;
    try {
        await authStore.onLogin(state.email, state.password);
        emit("success");
    } catch (e) {
        if (e.response.status === 401) {
            error.value = "Неверное имя пользователя или пароль.";
        }
    }
    isLoading.value = false;
};
</script>
