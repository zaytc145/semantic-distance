import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
    plugins: [vue()],
    build: {
        manifest: true,
        outDir: "./static",
        assetsDir: "./js",
        rollupOptions: {
            input: "./resources/js/app.js",
        }
    }
});
