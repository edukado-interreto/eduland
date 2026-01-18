<script setup lang="ts">
const { t } = useI18n()
const unit_component = useUnitComponent()
const cefr = useCefr()
const { langs_table, langs_available } = useLangsAvailable()

const props = defineProps<{ exercise: Exercise }>()

const tags_localized = computed(() => {
  return (props.exercise.tags || []).map(tag => t(`tags.${tag}`))
})
</script>

<template>
  <v-row dense class="text-caption text-medium-emphasis d-print-none">
    <v-col cols="auto">
      <v-icon size="small" class="align-start" start>mdi-account</v-icon>
      <span class="username">
        {{ exercise.created_by || $t("exercise.anonymous") }}
      </span>
    </v-col>
    <v-col cols="auto" v-if="exercise.modified">
      <v-icon size="small" start>mdi-clock</v-icon>
      <time :datetime="exercise.modified">
        {{ $d(new Date(exercise.modified), "short") }}
      </time>
    </v-col>

    <v-spacer />

    <v-col cols="auto" v-if="exercise.age_min > 0 || exercise.age_max < 18">
      <v-icon size="small" start>mdi-human-child</v-icon>
      {{ $t("exercise.age") }} {{ exercise.age_min }} -
      {{ exercise.age_max == 18 ? "18+" : exercise.age_max }}
    </v-col>
    <v-col cols="auto" v-if="exercise.lang_learn === true">
      <v-icon size="small" start>mdi-chat</v-icon>
      {{ langs_table[exercise.lang_learn_lang].name }}
      {{
        cefr.display([
          exercise.lang_learn_cefr_level_min,
          exercise.lang_learn_cefr_level_max,
        ])
      }}
    </v-col>
    <v-col cols="auto" v-if="exercise.tags?.length > 0">
      <v-icon size="small" start>mdi-tag</v-icon>
      {{ tags_localized.join(", ") }}
    </v-col>
    <v-col cols="auto">
      <v-icon size="small" start>mdi-heart</v-icon>
      {{ exercise.likes }}
    </v-col>
  </v-row>
</template>

<style scoped>
.v-icon--start {
  margin-inline-end: 0.5ch;
  vertical-align: text-bottom;
}
</style>
