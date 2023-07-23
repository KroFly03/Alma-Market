export default (api) => ({
    get: async () => {
        return await api.get("basket/").json();
    },

    add: async ({ goodsItemId, amount }) => {
        return await api
            .post("basket/add/", {
                json: { item: goodsItemId, amount },
            })
            .json();
    },

    update: async ({ goodsItemId, amount }) => {
        return await api
            .patch(`basket/${goodsItemId}/update/`, {
                json: { amount },
            })
            .json();
    },

    remove: async ({ goodsItemId }) => {
        return await api.delete(`basket/${goodsItemId}/delete/`).json();
    },
});
