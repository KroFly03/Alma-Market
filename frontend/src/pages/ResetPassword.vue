<template>
    <v-modal
        v-model:is-open="isModalOpen"
        :close-on-click-backdrop="false"
        max-width="460"
        title="Восстановление пароля"
        @update:is-open="onClose"
    >
        <template #body>
            <template v-if="!isSuccess">
                <v-input
                    v-model="state.new_password"
                    type="password"
                    label="Новый пароль"
                    class="mb-3"
                    :error-message="v$.new_password.$errors[0]?.$message"
                ></v-input>
                <v-input
                    v-model="state.confirmNewPassword"
                    type="password"
                    label="Новый пароль еще раз"
                    :error-message="v$.confirmNewPassword.$errors[0]?.$message"
                ></v-input>
                <p v-if="isFetchFailed" class="mt-3 text-sm text-error">
                    Произошла ошибка, возможно, ссылка уже не действительна
                </p>
                <v-btn class="mt-6 w-full" :loading="isLoading" @click="onChange">Изменить</v-btn>
            </template>
            <template v-else>
                <p class="mb-4 text-sm">Пароль изменен!</p>
                <v-btn class="w-full" @click="onClose">Закрыть</v-btn>
            </template>
        </template>
    </v-modal>
</template>

<script setup>
import VModal from "@/components/UI/VModal.vue";
import VInput from "@/components/UI/VInput.vue";
import VBtn from "@/components/UI/VBtn.vue";
import { reactive, ref, toRef } from "vue";
import { required, sameAs } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { useRouter } from "vue-router";
import { api } from "@/api/api.js";

const props = defineProps({
    uid: {
        type: String,
        required: true,
    },
    token: {
        type: String,
        required: true,
    },
});

const isModalOpen = ref(true);

const state = reactive({
    new_password: "",
    confirmNewPassword: "",
});
const isLoading = ref(false);
const errors = ref(null);

const isFetchFailed = ref(false);
const isSuccess = ref(false);

const rules = {
    new_password: { required },
    confirmNewPassword: {
        required,
        sameAs: sameAs(toRef(state, "new_password")),
    },
};

const v$ = useVuelidate(rules, state, { $externalResults: errors, $autoDirty: true });

const onChange = async () => {
    errors.value = null;
    if (!(await v$.value.$validate())) return;

    isLoading.value = true;
    try {
        await api.auth.setNewPassword({
            uid: props.uid,
            token: props.token,
            newPassword: state.new_password,
        });
        isSuccess.value = true;
    } catch (e) {
        const response = e.json;

        if ("new_password" in response) errors.value = response;
        else {
            isFetchFailed.value = true;
        }
    }
    isLoading.value = false;
};

const router = useRouter();
const onClose = async () => {
    await router.replace({ name: "Home" });
};
</script>
