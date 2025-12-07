<script setup lang="ts">
import { computed, ref } from "vue";
import useTokenize from "@/composables/useTokenize";
import UnitOpenAnswerTextField from "@/components/UnitOpenAnswerTextField.vue";

const tokenize = useTokenize();
type Props = {
  code?: string;
  shuffle?: boolean;
  solved?: Solved;
  readonly?: boolean;
  silent?: boolean;
  parsed?: [string, string][];
  ignore_case?: boolean;
};
const {
  code = "",
  shuffle = false,
  solved,
  readonly = false,
  silent = false,
  parsed,
  ignore_case = false,
} = defineProps<Props>();

const score_awarded = ref(0);

const gaps: Ref<Element[]> = ref([]);

const on_answer = (answer, i, j) => {
  // We use this event to update the amount of
  // right answers. We access the computed
  // 'success' prop of each child component
  // to get the amount of successful answers.
  score_awarded.value = gaps.value.filter((c) => !!c.success).length;
};
const get_solved = () => {
  // inject the answers into "parsed"
  // and return the whole object
  let i = 0;
  const parsed_filled = parsed_local.value.map((phrase) =>
    phrase.map((token) => {
      if (token.token != "gap") return token;
      token.answer = gaps.value[i].answer;
      i++;
      return token;
    }),
  );
  return {
    parsed: parsed_filled,
  };
};
const score_available = computed(() => {
  return parsed_local.value.flatMap((line) =>
    line.filter((t) => t.token === "gap"),
  ).length;
});
const parsed_local: ComputedRef<Token[][]> = computed(() => {
  if (solved !== undefined) return solved.parsed;
  // if the parent component provided a 'solved' prop,
  // bypass 'code' and load the 'solved' object which
  // contains the already parsed 'code' with answers
  // included.

  return tokenize(code);
});

defineExpose({ get_solved });
</script>

<template>
  <div class="editor">
    <div class="gap_demo">
      <ol
        class="ms-4"
        :class="parsed_local.length === 1 ? ['just-one'] : undefined"
      >
        <li v-for="(phrase, i) in parsed_local" :key="i" class="pre-line">
          <template v-for="(token, j) in phrase">
            <UnitOpenAnswerTextField
              :key="j"
              v-if="token.token === 'gap'"
              :options="token.options || []"
              :value="token.answer || ''"
              :shuffle="shuffle"
              :ignore_case="ignore_case"
              :once="false"
              :error-explanation="token.errorExplanation"
              :readonly="readonly"
              :ref="(el) => gaps.push(el)"
              :silent="silent"
              :success="token.right || false"
              @answer="on_answer($event, i, j)"
            />
            <span :key="j" v-if="token.token === 'text'" v-text="token.value" />
          </template>
        </li>
      </ol>
    </div>
  </div>
</template>

<style scoped>
ol.just-one {
  list-style: none;
}
li {
  margin-bottom: 1.25em;
  line-height: 2.25em;
}

.pre-line {
  white-space: pre-line;
}
</style>
