<script setup lang="ts">
type Value = {
  value: string
  right: boolean
}
type Props = {
  value: Value
  options: any[]
  shuffle: boolean
  once?: boolean
  errorExplanation?: string
  readonly?: boolean
  silent: boolean
}

const props = defineProps<Props>()

const emit = defineEmits(["update:answer", "input"])

const select: Ref<HTMLElement | null> = ref(null)

const answer = ref(props.value)

const { confetti_shoot } = useConfettiShoot()

// Computed properties
const icon = computed(() => {
  if (props.silent) return undefined
  if (success.value === undefined) return undefined
  return success.value ? "mdi-check-bold" : "mdi-close-thick"
})

const error_messages = computed(() => {
  if (props.silent) return undefined
  if (success.value !== false) return undefined
  return props.errorExplanation
})

const choices = computed(() => {
  if (props.shuffle) return shuffle_array(props.options)
  return props.options
})

const longest_choice_length = computed(() =>
  Math.max(...choices.value.map((s: any) => s.value.length)),
)

const gap_width = computed(() => `calc(${longest_choice_length.value + 7}ch + 4em)`)

const success = computed(() => {
  if ("right" in (answer.value || {})) {
    return answer.value.right
  }
  return undefined
})

// Methods
function shuffle_array(array: any[]) {
  const clonedArray = array.slice()
  let currentIndex = clonedArray.length,
    randomIndex

  while (currentIndex !== 0) {
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex--
    ;[clonedArray[currentIndex], clonedArray[randomIndex]] = [
      clonedArray[randomIndex],
      clonedArray[currentIndex],
    ]
  }

  return clonedArray
}

function onChange() {
  emit("update:answer", answer.value)

  if (props.silent) return
  if (typeof window === "undefined") return
  if (success.value === true && select?.value) {
    confetti_shoot(select.value)
  }
}

// Watcher
watch(answer, newValue => {
  emit("input", newValue)
})
defineExpose({ answer, choices })
</script>

<template>
  <span class="print">
    <span
      class="choice"
      v-for="choice in choices.map(c => c.value)"
      :key="choice"
      v-text="choice"
    />
  </span>
  <v-select
    ref="select"
    v-model="answer"
    :items="choices"
    class="gap-select"
    item-title="value"
    return-object
    :success="!props.silent && success === true"
    :error-messages="error_messages"
    :error="!props.silent && success === false"
    @change="onChange"
    :readonly="props.readonly || (props.once && success !== undefined)"
    :width="gap_width"
    hide-details="auto"
    density="compact"
    variant="underlined"
  >
    <template v-if="!silent" #prepend-inner>
      <v-icon size="x-small" :color="!silent && !!success ? 'success' : undefined">
        {{ icon }}
      </v-icon>
    </template>
  </v-select>
</template>

<style scoped lang="scss">
.gap-select {
  position: relative;
  bottom: 0.3rem;
  padding: 0 0.2em;
  display: inline-block;
  @media print {
    display: none;
  }
  .v-field {
    font-size: 20px;
    .v-select__selection-text{
      font-size: calc(15px + 0.4vw) !important;
    }

    &--appended {
      padding-inline-end: initial;
    }
    &__append-inner {
      @media print {
        display: none;
      }
    }
  }
}

.print {
  display: none;

  @media print {
    display: initial;
  }
  .choice {
    color: dimgrey;
    padding: 0.5ch;
    border: solid 1px silver;
    border-radius: 1ch;
    margin: 0 1pt;
  }
}
</style>
