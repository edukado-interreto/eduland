<script setup lang="ts">
const textarea: HTMLTextAreaElement = document.getElementById("id_data");
const exercise =  textarea.value === "{}" ? { sheet: [] } : JSON.parse(textarea.value);
const sheet = ref(exercise.sheet);

watchEffect(() => {
  const new_exercise = exercise;
  new_exercise.sheet = sheet.value;
  textarea.value = JSON.stringify(new_exercise);
});
</script>

<template>
  <div id="exercise-editor">
    <v-app>
      <SheetEditor
        v-model:sheet="sheet"
        ref="sheet_editor"
        class="mt-8"
        @save="save"
      />
    </v-app>
  </div>
</template>
