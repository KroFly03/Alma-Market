<template>
    <div v-if="isSuccessActivation">
        <h1>Аккаунт активирован!</h1>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
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

const router = useRouter();
const isSuccessActivation = ref(false);

onMounted(async () => {
    try {
        await api.auth.activate(props.uid, props.token);
        isSuccessActivation.value = true;
    } catch (e) {
        await router.push({ name: "NotFound" });
    }
});
</script>
