import { registerPlugins } from "@/plugins"

// Components
import Editor from "@/Editor.vue"

// Composables
import { createApp } from "vue"

/* Django-Vite */
import "vite/modulepreload-polyfill"

const app = createApp(Editor)

registerPlugins(app)

app.mount("#mount-editor")
