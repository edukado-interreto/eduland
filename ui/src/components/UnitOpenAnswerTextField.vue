<script setup lang="ts">
const { confetti_shoot } = useConfettiShoot()

const emit = defineEmits(["input", "update:answer"])
const props = defineProps<{
  value: string
  options: Option[]
  shuffle: boolean // Whether shuffle the options
  ignore_case: boolean // Whether to ignore the case
  once: boolean // If true, allow only one try
  errorExplanation?: string // Message to display when picked answer is wrong
  readonly: boolean
  silent: boolean
  success: boolean
}>()

const select = ref<HTMLSelectElement | null>(null)
const answer: Ref<string | undefined> = ref(undefined)

// This will preload the answer on create.
// Note that if the parent component changes the prop 'value' afterwards,
// it will not update the internal 'answer' variable.
answer.value = props.value

const icon = computed(() => {
  if (props.silent) return
  return success.value ? "mdi-check-bold" : "mdi-close-thick"
})

const error_messages = computed(() => {
  if (props.silent || props.success !== false) return
  return props.errorExplanation
})

const choices = computed(() => {
  /**
   * Return the array of the possible answers to choose from.
   + The array contains objects in the form:
   * { "value": <string>, "right": <bool> }
   */

  // shuffle makes no sense in open answers

  //if (props.shuffle) {
  //  return props.shuffle_array(
  //    props.options
  //  )
  //}

  return props.options
})

/**
 * Return the length in character of the longest
 * answer that one can choice (to calculate gap width)
 * @returns {int}
 */
const longest_choice_length = computed(() => {
  return Math.max(...choices.value.map(s => s.length))
})

/**
 * Returns the css value used to set the gap width
 * @returns {str}
 */
const gap_width = computed(() => {
  if (longest_choice_length.value === 0) return "30ch"
  // open answer without options, return a standard size
  // that should fit for a generic answer

  return longest_choice_length.value + 7 + "ch"
  // FIXME
  // heuristic calculation: to display the string "0"
  // into the v-select, a minimum width of 8ch was
  // found to be required. Hence, assuming that any
  // character has roughly the same width of "0", we
  // do the math on the longest answer's length.
  // Note that this assumption is by no mean accurate
  // and changing the styling or the icon slots etc.
  // of the v-select will have an inpact on it.
})

/**
 * @returns: true | false | undefined
 */
const success = computed(() => {
  const adapt_str = (s: string) => s.toLowerCase()
  // s && props.ignore_case ? s.toLowerCase() : s

  const current_option = props.options.find(
    option => adapt_str(option.value) === adapt_str(answer.value),
  )

  if (props.options.every(o => o.right === true)) {
    // the options list contains only one (or more) right option(s),
    // e.g.: "2+2 = [+4]" or "red is a [+color|+colour]".
    // In this case, we consider wrong (success = false) any
    // other answers apart from the empty string (success = undefined).
    if (!answer) return undefined
    return !!current_option
  }

  if (!current_option) return undefined

  return current_option.right
})

const on_change = () => {
  emit("update:answer", answer)

  if (props.silent) return
  if (props.success && select.value) confetti_shoot(select.value)
}

watch(answer, value => {
  emit("input", value)
})
</script>

<template>
  <v-text-field
    ref="select"
    density="compact"
    variant="underlined"
    class="position-relative mx-1 text-center"
    style="display: inline-block; top: 0.4rem"
    :style="`width: ${gap_width}`"
    v-model="answer"
    :color="!silent && !!success ? 'success' : undefined"
    :error="!silent && !success"
    :error-messages="error_messages"
    hide-details
    :hint="error_messages"
    @input="on_change"
    :readonly="readonly || (once && success !== undefined)"
  >
    <template v-if="!silent" #prepend-inner>
      <v-icon :color="!silent && !!success ? 'success' : undefined">
        {{ icon }}
      </v-icon>
    </template>
  </v-text-field>
</template>
