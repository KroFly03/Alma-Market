export default (api) => ({
    get: async ({ page = 1, search }) => {
        const searchParams = new URLSearchParams({ page });
        if (search) searchParams.append("email", search);

        return await api.get("users/", { searchParams }).json();
    },
});
