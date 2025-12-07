/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from "@/plugins"

// Components
import Exercise from "@/Exercise.vue"

// Composables
import { createApp } from "vue"

// Styles
// import "unfonts.css"

// Fonts
// import "@fontsource/roboto/100.css"
// import "@fontsource/roboto/300.css"
// import "@fontsource/roboto/400.css"
// import "@fontsource/roboto/500.css"
// import "@fontsource/roboto/700.css"
// import "@fontsource/roboto/900.css"

// /* Optional italic styles */
// import "@fontsource/roboto/100-italic.css"
// import "@fontsource/roboto/300-italic.css"
// import "@fontsource/roboto/400-italic.css"
// import "@fontsource/roboto/500-italic.css"
// import "@fontsource/roboto/700-italic.css"
// import "@fontsource/roboto/900-italic.css"

/* Django-Vite */
import "vite/modulepreload-polyfill"

const app = createApp(Exercise)

registerPlugins(app)

app.mount("#app")
