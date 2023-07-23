export default (api) => ({
    get: async ({ page = 1, search }) => {
        const searchParams = new URLSearchParams({ page });
        if (search) searchParams.append("code", search);

        return await api.get("orders/", { searchParams }).json();
    },

    getAddresses: async () => {
        return await api.get("orders/address/").json();
    },

    getByLoggedUser: async () => {
        return await api.get("orders/user/").json();
    },

    create: async (address, cartItems) => {
        return await api.post("orders/create/", { json: { address, goods: cartItems } }).json();
    },

    updateStatus: async (orderId, status) => {
        return await api.patch(`orders/${orderId}/update/`, { json: { status } }).json();
    },
});
