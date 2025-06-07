import { defineConfig } from "vite";
import { resolve } from "path"

export default defineConfig({
    build: {
        outDir: resolve(__dirname, "../src/static"),
        emptyOutDir: false,
        rollupOptions: {
            input: resolve(__dirname, "src/main.js"),
            output: {
                entryFileNames: "main.js"
            }
        }
    }
})