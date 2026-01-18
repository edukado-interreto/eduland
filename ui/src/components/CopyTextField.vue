<script setup lang="ts">
const model = defineModel({ type: String })
const { label } = defineProps<{ label?: string }>()
const field = useTemplateRef("field")

function copy_text() {
  const input = field.value?.$el?.querySelector("input")
  if (!input) return
  input.select()
  if (navigator.clipboard) {
    navigator.clipboard.writeText(model.value as string)
  } else {
    document.execCommand("copy")
  }
}
</script>

<template>
  <v-text-field
    ref="field"
    variant="outlined"
    density="compact"
    prepend-inner-icon="mdi-link-variant"
    append-inner-icon="mdi-content-copy"
    @click:append-inner="copy_text"
    :model-value="model"
    :label="label"
    :title="$t('exam.copy')"
    readonly
    hide-details
  />
</template>
