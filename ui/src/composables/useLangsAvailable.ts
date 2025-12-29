import langs from "~/data/langs.js"

export default function () {
  return {
    langs_table: langs.langs, // TODO i18n
    langs_available: Object.entries(langs.langs)
      .map(([code, lang]) => ({
        value: code as Lang["code"],
        title: lang.name, // TODO: localization of languages name
      }))
      .sort((a, b) => a.title.localeCompare(b.title)),
  }
}
