<script>
export default {
  props: ["src", "content"],
  data: () => ({
    broken: false,
  }),
  watch: {
    src() {
      this.broken = false
    },
  },
}
</script>

<template>
  <audio
    v-if="!broken"
    controls
    style="max-height: 150px; max-width: 100%"
    :key="src"
  >
    <source :src="src" @error="broken = true" />
  </audio>
  <div v-else class="text-grey">
    <v-icon small>mdi-alert-outline</v-icon>
    <i>Invalid sound: {{ content }}</i>
  </div>
</template>
