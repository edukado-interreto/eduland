/**
 * plugins/i18n.ts
 *
 * Framework documentation: https://vue-i18n.intlify.dev/guide/essentials/started.html
 */

// Composables
import { createI18n } from "vue-i18n"

import * as en from "@/locales/en.json"
import * as eo from "@/locales/eo.json"
import * as fr from "@/locales/fr.json"
import * as sk from "@/locales/sk.json"

const lang = document?.querySelector("html")?.getAttribute("lang")

// https://vue-i18n.intlify.dev/api/general.html#createi18n
export default createI18n({
  locale: lang || "en",
  fallbackLocale: "en",
  messages: { en, eo, fr, sk },
})
