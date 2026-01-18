<script setup lang="ts">
const unit_component = useUnitComponent();
const all_silent = ref(true);
const all_readonly = ref(false);
const submitted = ref(false);
const units: Ref<{ [key: `unit-${string}`]: UnitComponent }> = ref({});
const append_unit = (el: unknown, unit: Unit) => {
  if (el) units.value[`unit-${unit._key}`] = el;
};
let data = document.getElementById("exercise-data")?.innerText;
let exercise = data && JSON.parse(data);
const submit = () => {
  // show the results of the quiz

  submitted.value = true;
  window.scrollTo({ top: 220, behavior: "smooth" });

  all_silent.value = false;
  all_readonly.value = true;
};
</script>

<template>
  <v-container v-if="!exercise" class="d-flex">
    <v-spacer />
    <v-progress-circular indeterminate color="primary" size="70" width="3" />
    <v-spacer />
  </v-container>
  <v-container v-if="exercise">
    <v-sheet v-for="(unit, i) in exercise.sheet" :key="unit._key">
      <div class="text-h4 my-4">
        <span v-if="exercise.sheet.length > 1">{{ i + 1 }}.</span>
        <span class="font-weight-medium">{{ unit.title }}</span>
        <span v-if="unit.title === ''" class="font-italic">
          {{ $t("sheet_editor.untitled_unit") }}
        </span>
      </div>
      <div v-if="unit.description" class="body-2 mb-4 pre-line">
        <RichContent :text="unit.description" />
      </div>
      <component
        :is="unit_component(unit.type)"
        :code="unit.code"
        :shuffle="unit.shuffle"
        :ignore_case="unit.ignore_case"
        :silent="all_silent"
        :readonly="all_readonly"
        :ref="(el) => append_unit(el, unit)"
      />
    </v-sheet>

    <v-btn
      @click="submit"
      type="submit"
      class="d-flex mt-9 d-print-none"
      :color="submitted ? 'grey' : 'primary'"
      :disabled="submitted"
      v-text="$t('exercise.check')"
    />
  </v-container>
</template>
