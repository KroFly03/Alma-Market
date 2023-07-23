module.exports = {
    extends: [
        "eslint:recommended",
        "plugin:vue/vue3-essential",
        "plugin:vue/vue3-strongly-recommended",
        "plugin:vue/vue3-recommended",
        "plugin:prettier/recommended",
    ],
    rules: {
        "prettier/prettier": ["error", {}, { usePrettierrc: true }],
        "no-unused-vars": 1,
    },
    plugins: ["prettier"],
};
