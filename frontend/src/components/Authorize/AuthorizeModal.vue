<template>
    <v-modal :is-open="model" max-width="420" @update:is-open="onClose">
        <template #body>
            <template v-if="!isForgotPasswordMode">
                <v-tabs v-model="tab" class="mb-2" grow>
                    <v-tab value="login">Вход</v-tab>
                    <v-tab value="registration">Регистрация</v-tab>
                </v-tabs>
                <v-content-views :value="tab">
                    <v-content-view value="login">
                        <p
                            v-if="isSuccessRegistration"
                            class="rounded-md bg-primary bg-opacity-10 p-2 text-sm"
                        >
                            Регистрация прошла успешно. Для входа необходимо подтвердить свой
                            аккаунт на почте.
                        </p>
                        <authorize-login-form
                            @success="onClose"
                            @forgot-password="onForgotPassword"
                        ></authorize-login-form>
                    </v-content-view>
                    <v-content-view value="registration">
                        <authorize-registration-form
                            @success="onSuccessRegistration"
                        ></authorize-registration-form>
                    </v-content-view>
                </v-content-views>
            </template>
            <authorize-forgot-password-form
                v-else
                @close="isForgotPasswordMode = false"
            ></authorize-forgot-password-form>
        </template>
    </v-modal>
</template>

<script setup>
import VModal from "@/components/UI/VModal.vue";
import VTabs from "@/components/UI/VTabs/VTabs.vue";
import VTab from "@/components/UI/VTabs/VTab.vue";
import AuthorizeLoginForm from "@/components/Authorize/AuthorizeLoginForm.vue";
import AuthorizeRegistrationForm from "@/components/Authorize/AuthorizeRegistrationForm.vue";
import AuthorizeForgotPasswordForm from "@/components/Authorize/AuthorizeForgotPasswordForm.vue";
import { computed, ref } from "vue";
import { TabPanel } from "@headlessui/vue";
import VContentViews from "@/components/UI/VContentViews/VContentViews.vue";
import VContentView from "@/components/UI/VContentViews/VContentView.vue";

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue"]);

const model = computed({
    get: () => props.modelValue,
    set: (val) => emit("update:modelValue", val),
});

const tab = ref(null);
const isSuccessRegistration = ref(false);

const onSuccessRegistration = () => {
    isSuccessRegistration.value = true;
    tab.value = "login";
};

const isForgotPasswordMode = ref(false);
const onForgotPassword = () => {
    isForgotPasswordMode.value = true;
};

const onClose = () => {
    isSuccessRegistration.value = false;
    emit("update:modelValue", false);
};
</script>

<style lang="scss"></style>
