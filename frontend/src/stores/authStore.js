import { defineStore } from "pinia";
import { computed, onMounted, ref } from "vue";
import { useLocalStorage } from "@/composables/useLocalStorage.js";
import { api } from "@/api/api.js";
import { useRouter } from "vue-router";

export const useAuthStore = defineStore("auth", () => {
    const accessToken = useLocalStorage("accessToken");
    const refreshToken = useLocalStorage("refreshToken");

    const isUserLoading = ref(false);
    const user = ref(null);
    const isLoggedIn = computed(() => Boolean(user.value));

    const loadUser = async () => {
        try {
            const response = await api.auth.current();

            user.value = {
                name: response.first_name,
                email: response.email,
                phone: response.phone,
                role: response.role,
            };
        } catch (e) {
            // empty
        }
    };

    onMounted(async () => {
        isUserLoading.value = true;
        if (accessToken.value) await loadUser();
        isUserLoading.value = false;
    });

    const updateTokens = async () => {
        if (!refreshToken.value) return false;

        try {
            const response = await api.auth.refresh(refreshToken.value);
            refreshToken.value = response.refresh;
            accessToken.value = response.access;

            return true;
        } catch (e) {
            return false;
        }
    };

    const onLogin = async (email, password) => {
        const response = await api.auth.login({ email, password });

        refreshToken.value = response.refresh;
        accessToken.value = response.access;

        await loadUser();
    };

    const router = useRouter();
    const onLogout = async () => {
        if (router.currentRoute.value.meta.requiredAuth) await router.push("/");

        accessToken.value = null;
        refreshToken.value = null;

        user.value = null;
    };

    const isAdmin = computed(() => isLoggedIn.value && user.value.role === "admin");

    return {
        accessToken,
        refreshToken,
        isUserLoading,
        user,
        isLoggedIn,
        loadUser,
        updateTokens,
        onLogin,
        onLogout,
        isAdmin,
    };
});
