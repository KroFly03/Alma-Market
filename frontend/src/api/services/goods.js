export default (api) => ({
    get: async ({ search, page = 1, category, manufacturer, priceMin, priceMax }) => {
        const searchParams = new URLSearchParams({ page });

        if (search) searchParams.append("name", search);
        if (category) searchParams.append("category", category);
        if (manufacturer) searchParams.append("manufacturer", manufacturer);
        if (priceMin) searchParams.append("price_min", priceMin);
        if (priceMax) searchParams.append("price_max", priceMax);

        return await api.get("goods/", { searchParams }).json();
    },

    getById: async (id) => {
        return await api.get(`goods/${id}/`).json();
    },

    getCategories: async () => {
        return await api.get(`goods/cat/`).json();
    },

    getManufacturers: async () => {
        return await api.get(`goods/manufact/`).json();
    },

    add: async ({
        imageFile,
        name,
        price,
        amount,
        description,
        characteristics,
        category,
        manufacturer,
    }) => {
        const formData = new FormData();

        formData.append("image", imageFile);
        formData.append(
            "json",
            JSON.stringify({
                name,
                price,
                amount,
                description,
                characteristics,
                category,
                manufacturer,
            })
        );

        return await api.post("goods/create/", { body: formData }).json();
    },

    edit: async ({
        id,
        imageFile,
        name,
        price,
        amount,
        description,
        characteristics,
        category,
        manufacturer,
    }) => {
        const formData = new FormData();

        if (imageFile) formData.append("image", imageFile);

        formData.append(
            "json",
            JSON.stringify({
                name,
                price,
                amount,
                description,
                characteristics,
                category,
                manufacturer,
            })
        );

        return await api.patch(`goods/${id}/update/`, { body: formData }).json();
    },

    getAllCharacteristics: async () => {
        return await api.get("goods/chars/").json();
    },
});
