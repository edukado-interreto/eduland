<script setup lang="ts">
// Load a solved, submitted exercise and display it for review
const { submission, silent } = defineProps<{
  submission: Submission
  silent: boolean
}>()
const len = computed(() => submission.exercise.data.sheet.length)
</script>

<template>
  <div v-if="submission">
    <v-sheet
      v-for="(unit, i) in submission.exercise.data.sheet"
      :key="`submitted_${unit._key}`"
    >
      <div class="text-h4 my-4">
        <template v-if="len > 1">{{ i + 1 }}.</template>
        {{ unit.title }}
        <span v-if="unit.title === ''" class="font-italic">Untitled unit</span>
      </div>
      <div v-if="unit.description" class="body-2 mb-4 pre-line">
        <RichContent :text="unit.description" />
      </div>
      <UnitMultipleChoice
        v-if="unit.type == 'multiple_choice'"
        :key="i"
        :solved="unit.solved"
        :readonly="true"
        :silent="silent"
      />
      <UnitPairing
        v-if="unit.type == 'pairing'"
        :key="i"
        :solved="unit.solved"
        :readonly="true"
        :silent="silent"
      />
      <UnitDefault
        v-if="unit.type == 'default'"
        :key="i"
        :solved="unit.solved"
        :readonly="true"
        :silent="silent"
      />
      <UnitOpenAnswer
        v-if="unit.type == 'open_answer'"
        :key="i"
        :solved="unit.solved"
        :readonly="true"
        :ignore_case="unit.ignore_case"
        :silent="silent"
      />
    </v-sheet>
  </div>
</template>
