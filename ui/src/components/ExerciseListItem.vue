<script setup lang="ts">
const localePath = useLocalePath()
const { item } = defineProps<{ item: Exercise }>()
</script>

<template>
  <v-card
    :to="localePath({ name: 'exercise-id', params: { id: item.lid } })"
    class="mb-5"
  >
    <v-card-title class="subheading font-weight-bold">
      {{ item.name }}
      <v-tooltip position="bottom" v-if="item.searchable === false">
        <template #activator="{ props }">
          <v-icon v-bind="props" class="ml-2">mdi-link</v-icon>
        </template>
        <span>{{ $t("exercise.unlisted") }}</span>
      </v-tooltip>
    </v-card-title>
    <v-card-subtitle v-if="item.description" v-text="item.description" />
    <v-divider />
    <v-card-text class="pa-2">
      <ExerciseFooterAttributes :exercise="item" />
    </v-card-text>
  </v-card>
</template>
