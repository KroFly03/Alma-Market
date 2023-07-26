export default (api) => ({
    login: async ({ email, password }) => {
        return await api
            .post("auth/login", {
                json: { email, password },
            })
            .json();
    },

    refresh: async (refreshToken) => {
        return await api.post("auth/refresh/", { json: { refresh: refreshToken } }).json();
    },

    register: async ({ phone, email, first_name, last_name, password }) => {
        return await api
            .post("users", {
                json: {
                    email,
                    phone,
                    first_name,
                    last_name,
                    password,
                },
            })
            .json();
    },

    activate: async (uid, token) => {
        return await api.post("users/activation/", { json: { uid, token } });
    },

    current: async () => {
        return await api.get("users/me").json();
    },

    update: async ({ first_name, last_name, phone }) => {
        return await api
            .patch("users/me", {
                json: { first_name, last_name, phone },
            })
            .json();
    },

    changePassword: async ({ currentPassword, newPassword }) => {
        return await api
            .patch("users/set_password/", {
                json: { current_password: currentPassword, new_password: newPassword },
            })
            .json();
    },

    forgotPassword: async ({ email }) => {
        return await api.post("users/reset_password/", { json: { email } }).json();
    },

    setNewPassword: async ({ uid, token, newPassword }) => {
        return await api
            .post("users/reset_password_confirm/", {
                json: { uid, token, new_password: newPassword },
            })
            .json();
    },
});
