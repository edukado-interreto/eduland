<script setup lang="ts">
import { computed, onBeforeMount, ref, watch, watchEffect } from "vue";
import type { ComponentPublicInstance, ComputedRef, Ref } from "vue";

// const { confetti_shoot } = useConfettiShoot()
const props = defineProps([
  "value",
  "options",
  "shuffle", // bool: whether shuffle the options
  "once", // bool: if true, allow only one try
  "error-explanation", // string: message to display when picked answer is wrong
  "readonly",
  "silent",
]);
const emit = defineEmits(["update:answer", "input"]);

const checkbox: Ref<(Element | ComponentPublicInstance)[]> = ref([]);
const answer = ref([]);

onBeforeMount(() => {
  // This will preload the answer on create.
  // Note that if the parent component changes
  // the prop 'value' afterwards, it will not
  // update the internal 'answer' variable.
  answer.value = props.value || [];
});

const choices: ComputedRef<Token[]> = computed(() => {
  /**
   * Return the array of the possible answers to choose from.
   + The array contains objects in the form:
   * { "value": <string>, "right": <bool> }
   */

  if (props.shuffle) {
    return shuffle_array(props.options);
  }

  return props.options;
});

const success = computed(() => {
  /**
   * The correctness status of each checkbox
   * @returns: [ true | false ]
   */
  return choices.value.map((c) => {
    const checked = answer.value.includes(c.value);
    if (checked && c.right === true) return true;
    if (!checked && c.right === false) return true;
    return false;
  });
});

const correct_answers = computed(() => {
  return choices.value.map((c) => c.right);
});

const show_success_feedback = computed(() => {
  /**
   * Whether provide success feedback for each checkbox.
   * It is true if the option is correctly checked and all
   * other right options are checked as well. False otherwise.
   * @returns: [ true | false ]
   */
  return choices.value.map(
    (c, i) => success.value[i] && c.right && success.value.every(Boolean),
  );
});

const is_correct_answer = (i) => {
  if (props.silent === true) return false;
  return correct_answers.value[i];
};

const is_checked = (i) => {
  return answer.value.includes(choices.value[i]);
};

const is_error = (i) => {
  if (props.silent) return false;
  return success[i] === false;
};

const on_change = (i) => {
  emit("update:answer", answer.value);

  if (props.silent) return;
  if (process.server) return;
  if (show_success_feedback.value[i] === true) {
    // confetti_shoot(checkbox.value[i].$el.querySelector("input"))
  }
};

const shuffle_array = (in_array) => {
  /**
   * Shuffle an array using the Fisher-Yates algorithm,
   * O(n), un-biased.
   */

  const out_array = in_array.slice();
  // clone the input array

  let currentIndex = out_array.length,
    randomIndex;

  // While there remain elements to shuffle...
  while (currentIndex != 0) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;
    // And swap it with the current element.
    [out_array[currentIndex], out_array[randomIndex]] = [
      out_array[randomIndex],
      out_array[currentIndex],
    ];
  }

  return out_array;
};

watch(answer, (v) => {
  emit("input", v);
});

watchEffect(() => {
  props.silent &&
    answer.value.map((v) =>
      on_change(choices.value.findIndex((c) => c.value === v)),
    );
});

defineExpose({ success, answer, choices });
</script>

<template>
  <v-checkbox
    density="compact"
    v-for="(choice, i) in choices"
    v-model="answer"
    :value="choice.value"
    :hide-details="true"
    @change="on_change(i)"
    :ref="
      (el) => {
        checkbox.push(el);
      }
    "
    :key="choice.value"
    :readonly="readonly"
    :color="silent ? 'primary' : is_correct_answer(i) ? 'green' : 'grey'"
  >
    <template v-slot:label>
      <span
        v-text.trim="choice.value"
        class="text-black"
        :class="{
          'text-decoration-line-through': is_checked(i) && is_error(i),
          'font-weight-bold': is_correct_answer(i),
          'text-success': is_correct_answer(i),
        }"
      />
      <template v-if="!silent">
        <v-icon v-if="show_success_feedback[i]" class="mx-1" color="success">
          mdi-check-bold
        </v-icon>
        <v-icon v-if="is_checked(i) && is_error(i)" class="mx-1" color="error">
          mdi-close-thick
        </v-icon>
      </template>
    </template>
  </v-checkbox>
</template>
