<script setup lang="ts">
import { enableDragDropTouch } from "@dragdroptouch/drag-drop-touch"; // @ts-ignore
import useConfettiShoot from "@/composables/useConfettiShoot";
import useShuffleArray from "@/composables/useShuffleArray";
import type { VCol } from "vuetify/components";

const instance = getCurrentInstance();
const { confetti_shoot } = useConfettiShoot();
const shuffle_array = useShuffleArray();

enableDragDropTouch();

type Props = {
  code?: string;
  shuffle?: boolean;
  solved?: SolvedDrags;
  readonly?: boolean;
  silent?: boolean;
  parsed?: [string, string][];
};
const {
  code = "",
  shuffle = false,
  solved,
  readonly = false,
  silent = false,
  parsed,
} = defineProps<Props>();

const uid = computed(() => instance?.uid || 0);
const score_awarded = ref(0);
const drags = ref<Drags | []>([]);
const movable = ref<[boolean, boolean][] | []>([]);
const hovered = ref<[boolean, boolean][] | []>([]);

const guess_col = useTemplateRef<VCol[]>("guess_col");

const update_dragging = () => {
  drags.value = parsed_local.value
    .map((p) => p[0])
    .sort((a, b) => a.localeCompare(b))
    .map((e) => [e, null]);

  if (shuffle) {
    drags.value = shuffle_array(drags.value) as Drags;
  }

  movable.value = parsed_local.value.map((p) => [false, false]);
  hovered.value = parsed_local.value.map((p) => [false, false]);
};

const load_drags_from_solved = () => {
  if (!solved || !solved.drags) return;
  nextTick(() => {
    drags.value = [...solved.drags];
  });
};

const on_dragstart = (e: DragEvent, src_row: number, src_col: number) => {
  if (readonly || e.dataTransfer === null) return;
  e.dataTransfer.setData(
    "text/plain",
    JSON.stringify({ uid: uid.value, row: src_row, col: src_col }),
  );
};

const on_dragleave = (e: DragEvent, dst_row: number, dst_col: number) => {
  if (readonly) return;
  hovered.value[dst_row][dst_col] = false;
};

const on_dragover = (e: DragEvent, dst_row: number, dst_col: number) => {
  if (readonly) return;
  if (drags.value[dst_row][dst_col] !== null) return;
  e.preventDefault();
};

const on_dragenter = (e: DragEvent, dst_row: number, dst_col: number) => {
  if (readonly) return;
  if (drags.value[dst_row][dst_col] !== null) return;
  e.preventDefault();
  hovered.value[dst_row][dst_col] = true;
};

const on_drop = (e: DragEvent, dst_row: number, dst_col: number) => {
  if (readonly || e.dataTransfer === null) return;
  let src;
  try {
    src = JSON.parse(e.dataTransfer.getData("text"));
    if (src.uid !== uid.value) throw "Cross-component drop";
  } catch (e) {
    hovered.value[dst_row][dst_col] = false;
    return;
  }
  e.preventDefault();
  drags.value[dst_row][dst_col] = drags.value[src.row][src.col];
  drags.value[src.row][src.col] = null;
  hovered.value[dst_row][dst_col] = false;

  if (dst_col === 1 && success.value[dst_row]) {
    if (!silent) {
      const element = guess_col.value?.[dst_row].$el;
      if (element) confetti_shoot(element);
    }
  }
};

const get_solved = (): SolvedDrags => ({
  parsed: parsed_local.value,
  drags: drags.value,
});

const parsed_local = computed(() => {
  if (solved) return solved.parsed || [];
  return code
    .split("\n\n")
    .map((s, i) => {
      let [src, dst] = s.split(/==(.*)/s).map((s) => s.trim());
      if (!dst) {
        dst = `${i + 1}`;
      }
      return [src, dst] as [string, string];
    })
    .filter(([src, dst]) => !!src);
});

const success = computed(() => {
  return drags.value.map((pair, i) => {
    if (pair[1] === null) return undefined;
    return pair[1] === parsed_local.value[i][0];
  });
});

const score_available = computed(() => 0); // TODO

load_drags_from_solved();

watch(() => solved, load_drags_from_solved);
watch(() => shuffle, update_dragging);
watch(parsed_local, update_dragging);

onMounted(update_dragging);

defineExpose({ get_solved });
</script>

<template>
  <v-container class="mb-5" fluid>
    <v-row
      v-for="(pair, i) in drags"
      :key="parsed_local[i][1]"
      class="d-flex"
      style="align-items: stretch"
    >
      <!-- 1st column: options -->
      <v-col md="4" class="grow-2 fill-height">
        <v-sheet
          v-if="pair[0] !== null"
          :draggable="!readonly && movable[i][0]"
          @dragstart="on_dragstart($event, i, 0)"
          rounded
          elevation="2"
          class="draggable-sheet align-center fill-height"
          dense
        >
          <span
            class="ms-2"
            :class="{ 'cursor-grab': !readonly }"
            @mouseenter="movable[i][0] = true"
            @touchstart="movable[i][0] = true"
            @mouseleave="movable[i][0] = false"
            @touchend="movable[i][0] = false"
          >
            <v-icon color="grey" :disabled="readonly">mdi-drag</v-icon>
          </span>
          <span class="ps-1 ps-lg-2">
            <RichContent :text="pair[0]" />
          </span>
          <span></span>
        </v-sheet>
        <v-sheet
          v-else
          rounded
          :color="hovered[i][0] ? 'grey-lighten-2' : 'grey-lighten-5'"
          class="drop-zone ma-n1 pa-2 text-grey border-t border-s text-center fill-height"
          @drop="on_drop($event, i, 0)"
          @dragenter="on_dragenter($event, i, 0)"
          @dragleave="on_dragleave($event, i, 0)"
          @dragover="on_dragover($event, i, 0)"
        >
          &nbsp;
        </v-sheet>
      </v-col>

      <!-- 2nd column: drop zones -->
      <v-col md="4" class="grow-2 fill-height" ref="guess_col">
        <v-sheet
          v-if="pair[1] !== null"
          :draggable="!readonly && movable[i][1]"
          @dragstart="on_dragstart($event, i, 1)"
          rounded
          elevation="2"
          class="draggable-sheet align-center fill-height"
        >
          <span
            class="ms-2"
            :class="{ 'cursor-grab': !readonly }"
            @mouseenter="movable[i][1] = true"
            @touchstart="movable[i][1] = true"
            @mouseleave="movable[i][1] = false"
            @touchend="movable[i][1] = false"
          >
            <v-icon color="grey" :disabled="readonly">mdi-drag</v-icon>
          </span>
          <span class="ps-2 ps-lg-4">
            <RichContent :text="pair[1]" />
          </span>
          <span></span>
        </v-sheet>
        <v-sheet
          v-else
          rounded
          class="drop-zone border-t border-s ma-n1 pa-2 text-grey d-flex justify-center align-center fill-height"
          :color="hovered[i][1] ? 'grey-lighten-2' : 'grey-lighten-4'"
          @drop="on_drop($event, i, 1)"
          @dragenter="on_dragenter($event, i, 1)"
          @dragleave="on_dragleave($event, i, 1)"
          @dragover="on_dragover($event, i, 1)"
        >
          <div class="drop-zone-text">
            {{ $t("exercise.drop_here") }}
          </div>
        </v-sheet>
      </v-col>

      <!-- 3rd column: answers -->
      <TransitionGroup name="result">
        <v-col md="4" class="grow-1 fill-height">
          <v-sheet
            rounded
            elevation="2"
            class="draggable-sheet align-center fill-height"
            key="answer"
          >
            <span></span>
            <span class="ps-2 ps-lg-4">
              <RichContent :text="parsed_local[i][1]" />
            </span>
            <span
              v-show="!silent && success !== undefined"
              key="feedback"
              class="px-2"
            >
              <v-icon v-if="success[i]" color="success">
                mdi-check-bold
              </v-icon>
              <v-icon v-if="!success[i]" color="error">
                mdi-close-thick
              </v-icon>
            </span>
          </v-sheet>
        </v-col>
      </TransitionGroup>
    </v-row>
  </v-container>
</template>

<style scoped>
.draggable-sheet {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  flex-direction: column-reverse;
}
.v-sheet {
  min-height: 3rem;
}
.v-locale--is-ltr {
  .first {
    order: 1;
  }
  .second {
    order: 2;
  }
}
.v-locale--is-rtl {
  .first {
    order: 2;
  }
  .second {
    order: 1;
  }
}
.grow-1 {
  flex-grow: 1;
}
.grow-2 {
  flex-grow: 2;
}
li {
  margin-bottom: 1.25em;
  line-height: 2.25em;
}
.pre-line {
  white-space: pre-line;
}
.drop-zone {
  transition: background-color 300ms ease-out;

  .drop-zone-text {
    pointer-events: none;
    touch-action: none;
    text-shadow: 0 1px white;
  }
}
.result {
  &-move,
  &-enter-active,
  &-leave-active {
    transition: all 300ms ease;
  }

  &-enter-from,
  &-leave-to {
    opacity: 0;
    transform: translateX(3rem);
  }

  /* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
  &-leave-active {
    position: absolute;
  }
}
</style>
