// Plugins
import { fileURLToPath, URL } from "node:url"
import Vue from "@vitejs/plugin-vue"
import Fonts from "unplugin-fonts/vite"
import Components from "unplugin-vue-components/vite"

// Utilities
import { defineConfig } from "vite"
import Vuetify, { transformAssetUrls } from "vite-plugin-vuetify"

const absolute = (path: string) => fileURLToPath(import.meta.resolve(path))

// https://vitejs.dev/config/
export default defineConfig({
  base: "/static/vue/",
  root: "src",
  build: {
    manifest: "assets/manifest.json",
    outDir: absolute("../src/public/static/vue"),
    emptyOutDir: true,
    rollupOptions: {
      input: {
        "eduland-vue": "src/main.ts",
      },
    },
  },
  experimental: {
    renderBuiltUrl(filename, { type }) {
      return type === "asset"
        ? `/static/vue/${filename}`
        : { runtime: `window.__assetsPath(/static/vue/${JSON.stringify(filename)})` }
    },
  },
  plugins: [
    Vue({
      template: { transformAssetUrls },
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/master/packages/vite-plugin#readme
    Vuetify(),
    Components(),
    Fonts({
      fontsource: {
        families: [
          {
            name: "Roboto",
            weights: [100, 300, 400, 500, 700, 900],
            styles: ["normal", "italic"],
          },
        ],
      },
    }),
  ],
  optimizeDeps: {
    exclude: ["vuetify"],
  },
  define: { "process.env": {} },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("src", import.meta.url)),
    },
    extensions: [".js", ".json", ".jsx", ".mjs", ".ts", ".tsx", ".vue"],
  },
  server: {
    port: 5173,
    host: "0.0.0.0",
  },
})
