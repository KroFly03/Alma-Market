import ky from "ky";
import auth from "@/api/services/auth.js";
import goods from "@/api/services/goods.js";
import orders from "@/api/services/orders.js";
import users from "@/api/services/users.js";
import basket from "@/api/services/basket.js";
import { useAuthStore } from "@/stores/authStore.js";

const apiInstance = ky.extend({
    prefixUrl: "/api",
    retry: {
        limit: 10,
        statusCodes: [401],
        methods: ["GET"],
    },
    hooks: {
        beforeRequest: [
            (request) => {
                const { accessToken } = useAuthStore();

                if (accessToken) request.headers.set("Authorization", `Bearer ${accessToken}`);
            },
        ],
        beforeError: [
            async (error) => {
                error.json = await error.response.json();

                // TODO: СДЕЛАТЬ ОБНОВЛЕНИЕ ТОКЕНА
                // if (error.response.status === 401) {
                //     const authStore = useAuthStore();
                //
                //     const isTokensUpdated = await authStore.updateTokens();
                //
                //     if (authStore.accessToken && isTokensUpdated) await authStore.loadUser();
                //     else if (!isTokensUpdated) await auth.onLogout();
                // }

                return error;
            },
        ],
        beforeRetry: [
            async (error) => {
                console.log("meeee");
            },
        ],
    },
});

export const api = {
    auth: auth(apiInstance),
    goods: goods(apiInstance),
    orders: orders(apiInstance),
    basket: basket(apiInstance),
    users: users(apiInstance),
};
