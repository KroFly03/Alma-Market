import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
    plugins: [vue()],
    server: {
        proxy: {
            "/api": "http://127.0.0.1:8080",
        },
        host: true,
    },
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
            "tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
        },
    },
});
