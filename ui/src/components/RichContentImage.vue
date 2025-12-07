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
  <v-img
    v-if="!broken"
    :src="src"
    contain
    max-height="150"
    @error="broken = true"
  />
  <div v-else class="text-grey">
    <v-icon small>mdi-alert-outline</v-icon>
    <i>Invalid image: {{ content }}</i>
  </div>
</template>
