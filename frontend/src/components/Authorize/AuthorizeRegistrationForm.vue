<template>
    <v-form @submit="onRegistration">
        <v-input
            v-model="state.email"
            class="mb-3"
            label="Email"
            :error-message="v$.email.$errors[0]?.$message"
        ></v-input>
        <v-input
            v-model="state.phone"
            class="mb-3"
            label="Телефон"
            :error-message="v$.phone.$errors[0]?.$message"
        ></v-input>
        <v-input
            v-model="state.first_name"
            class="mb-2"
            label="Имя"
            :error-message="v$.first_name.$errors[0]?.$message"
        ></v-input>
        <v-input
            v-model="state.last_name"
            class="mb-3"
            label="Фамилия"
            :error-message="v$.last_name.$errors[0]?.$message"
        ></v-input>
        <v-input
            v-model="state.password"
            type="password"
            class="mb-3"
            label="Пароль"
            :autocomplete="false"
            :error-message="v$.password.$errors[0]?.$message"
        ></v-input>
        <v-input
            v-model="state.repeatPassword"
            type="password"
            label="Подтвердите пароль"
            :autocomplete="false"
            :error-message="v$.repeatPassword.$errors[0]?.$message"
        ></v-input>
        <template #bottom>
            <v-btn class="w-full" :loading="isLoading">Зарегистрироваться</v-btn>
        </template>
    </v-form>
</template>

<script setup>
import { reactive, ref, toRef } from "vue";
import { email, maxLength, required, sameAs } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { api } from "@/api/api.js";
import VInput from "@/components/UI/VInput.vue";
import VBtn from "@/components/UI/VBtn.vue";
import VForm from "@/components/UI/VForm.vue";

const emit = defineEmits(["success"]);

const isLoading = ref(false);
const state = reactive({
    email: "",
    phone: "",
    first_name: "",
    last_name: "",
    password: "",
    repeatPassword: "",
});

const rules = {
    email: { required, email, maxLength: maxLength(254) },
    phone: { required, maxLength: maxLength(254) },
    first_name: { required, maxLength: maxLength(30) },
    last_name: { required, maxLength: maxLength(30) },
    password: { required, maxLength: maxLength(128) },
    repeatPassword: {
        sameAs: sameAs(toRef(state, "password")),
    },
};

const errors = ref({});

const v$ = useVuelidate(rules, state, { $externalResults: errors, $autoDirty: true });

const onRegistration = async () => {
    errors.value = {};

    if (!(await v$.value.$validate())) return;

    isLoading.value = true;
    try {
        await api.auth.register(state);

        Object.keys(state).forEach((key) => {
            state[key] = "";
        });

        v$.value.$reset();
        emit("success");
    } catch (e) {
        errors.value = e.json;
    }
    isLoading.value = false;
};
</script>
