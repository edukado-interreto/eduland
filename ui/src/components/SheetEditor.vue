<script setup lang="ts">
import { nanoid } from "nanoid";
import { useGoTo } from "vuetify";
import { useI18n } from "vue-i18n";
import type { ShallowRef } from "@vue/reactivity";
import type { VForm, VTextarea } from "vuetify/components";

const { t } = useI18n();
const goTo = useGoTo();

// Models
const sheet = defineModel<Unit[]>("sheet", { required: true });

// Emits
const emit = defineEmits(["save"]);

// Types

interface Current {
  index?: number;
  data: Partial<Unit>;
}

// Component references
const unit_component = useUnitComponent();
const unit_description = useTemplateRef<VTextarea>("unit_description");
const add_pair_form = useTemplateRef<VForm>("add_pair_form");
const insert_video_form = useTemplateRef<VForm>("insert_video_form");
const new_gap_form = useTemplateRef<VForm>("new_gap_form");
const unit = useTemplateRef<HTMLElement>("unit");

// State
const new_gap_options = ref<GapOption[]>([]);
const add_gap_dialog = ref(false);

const add_pair_dialog = ref(false);
const add_pair_first_item = ref("");
const add_pair_second_item = ref("");

const insert_video_dialog = ref(false);
const insert_video_url = ref("");

const description_loading = ref(false);

const image_uploading = ref(false);
const audio_uploading = ref(false);

const edit_drawer = ref({
  show: false,
});

const current = ref<Current>({
  index: undefined,
  data: {
    description: "",
    code: "",
  },
});

// Computed properties
const available_types = computed(() => [
  { value: "default", title: t("sheet_editor.types.default") },
  { value: "open_answer", title: t("sheet_editor.types.open_answer") },
  { value: "multiple_choice", title: t("sheet_editor.types.multiple_choice") },
  { value: "pairing", title: t("sheet_editor.types.pairing") },
]);

const snippets: Snippet[] = [
  {
    name: t("sheet_editor.snippets.blank_unit.name"),
    img: "blank.svg",
    unit: {
      type: "default",
      code: "",
    },
  },
  {
    name: t("sheet_editor.snippets.gap_filling_dropdown.name"),
    img: "fill_gap_dropdown.svg",
    unit: {
      type: "default",
      code: t("sheet_editor.snippets.gap_filling_dropdown.code"),
    },
  },
  {
    name: t("sheet_editor.snippets.gap_filling_open_answer.name"),
    img: "fill_gap_open.svg",
    unit: {
      type: "open_answer",
      code: t("sheet_editor.snippets.gap_filling_open_answer.code"),
    },
  },
  {
    name: t("sheet_editor.snippets.multiple_choice.name"),
    img: "choice.svg",
    unit: {
      type: "multiple_choice",
      code: t("sheet_editor.snippets.multiple_choice.code"),
    },
  },
  {
    name: t("sheet_editor.snippets.pairing_text_with_text.name"),
    img: "match_text.svg",
    unit: {
      type: "pairing",
      code: t("sheet_editor.snippets.pairing_text_with_text.code"),
    },
  },
  /*{
    name: t("sheet_editor.snippets.pairing_text_with_pictures.name"),
    img: "match_pic.svg",
    unit: {
      type: "pairing",
      code: t("sheet_editor.snippets.pairing_text_with_pictures.code"),
    },
  },*/
  /*{
    name: t("sheet_editor.snippets.pairing_text_with_sounds.name"),
    img: "match_sound.svg",
    unit: {
      type: "pairing",
      code: t("sheet_editor.snippets.pairing_text_with_sounds.code"),
    },
  },*/
  /*{
    name: t("sheet_editor.snippets.sorting_pictures.name"),
    img: "sort_pic.svg",
    unit: {
      type: "pairing",
      code: t("sheet_editor.snippets.sorting_pictures.code"),
      shuffle: true,
    },
  },*/
  /*{
    name: t("sheet_editor.snippets.pairing_pictures_with_sounds.name"),
    img: "match_pic_sound.svg",
    unit: {
      type: "pairing",
      code: t("sheet_editor.snippets.pairing_pictures_with_sounds.code"),
    },
  },*/
  /*{
    name: t(
      "sheet_editor.snippets.questions_about_a_picture_true_or_false.name",
    ),
    img: "true_false_pic.svg",
    unit: {
      type: "multiple_choice",
      description: t(
        "sheet_editor.snippets.questions_about_a_picture_true_or_false.description",
      ),
      code: t(
        "sheet_editor.snippets.questions_about_a_picture_true_or_false.code",
      ),
    },
  },*/
  {
    name: t(
      "sheet_editor.snippets.questions_about_a_text_multiple_choice.name",
    ),
    img: "choice_paragraph.svg",
    unit: {
      type: "multiple_choice",
      description: t(
        "sheet_editor.snippets.questions_about_a_text_multiple_choice.description",
      ),
      code: t(
        "sheet_editor.snippets.questions_about_a_text_multiple_choice.code",
      ),
    },
  },
  {
    name: t("sheet_editor.snippets.questions_about_a_video_open_answer.name"),
    img: "open_video.svg",
    unit: {
      type: "open_answer",
      description: t(
        "sheet_editor.snippets.questions_about_a_video_open_answer.description",
      ),
      code: t("sheet_editor.snippets.questions_about_a_video_open_answer.code"),
    },
  },
  /*{
    name: t("sheet_editor.snippets.questions_about_a_sound_dropdown.name"),
    img: "dropdown_sound.svg",
    unit: {
      type: "default",
      description: t(
        "sheet_editor.snippets.questions_about_a_sound_dropdown.description",
      ),
      code: t("sheet_editor.snippets.questions_about_a_sound_dropdown.code"),
    },
  },*/
];

// Methods

const get_textarea_input = () =>
  document.querySelector('[name="textarea-input"]') as HTMLTextAreaElement;

const load_snippet_thumb = (snippet: Snippet): string => {
  return `/snippet_thumb/${snippet.img}`;
};

const append_new_sentence = () => {
  const input = get_textarea_input();
  if (!input) return;
  const code = current.value.data.code?.trimEnd() || "";

  if (code !== "") {
    if (current.value.data.code !== undefined) {
      current.value.data.code = code + "\n\n";
    }
  }

  requestAnimationFrame(() => {
    if (!current.value.data.code) return;
    input.selectionStart = current.value.data.code.length;
    input.focus();
  });
};

const doubleRequestAnimationFrame = (fn: () => void) => {
  // force the browser to re-render the DOM before
  // calling the callback function.
  return window.requestAnimationFrame(() => window.requestAnimationFrame(fn));
};

const add_gap_dialog_show = (show: boolean) => {
  add_gap_dialog.value = show;
};

const insert_gap_click = async () => {
  // Using double requestAnimationFrame will ensure that
  // the value of the OptionsSelectors is updated even
  // if the user doesn't press Enter or blurs the input.
  const validation = await new_gap_form.value?.validate();
  if (!validation.valid) return;
  insert_gap();
};

const insert_gap = () => {
  // Ensure ltr string concatenation
  const new_gap =
    "[" +
    new_gap_options.value
      .map((opt) => (opt.right ? "+" + opt.value : opt.value))
      .join("|") +
    "]";

  inject_snippet(new_gap);
  add_gap_dialog.value = false;
  new_gap_options.value = [];
};

const add_pair_insert_click = () => {
  const input = get_textarea_input();
  if (!add_pair_form.value?.validate() || !input) return;

  let code = current.value.data.code?.trimEnd() || "";

  if (code !== "") {
    code += "\n\n";
  }

  code += `${add_pair_first_item.value} == ${add_pair_second_item.value}`;

  if (current.value.data) {
    current.value.data.code = code;
  }

  requestAnimationFrame(() => {
    if (!current.value.data.code) return;
    input.selectionStart = current.value.data.code.length;
    input.focus();
  });

  add_pair_dialog.value = false;
};

const insert_video_insert_click = () => {
  if (!insert_video_form.value?.validate()) return;
  inject_snippet(`{video:${insert_video_url.value}}`);
  insert_video_dialog.value = false;
};

const inject_snippet = (snippet: string) => {
  // insert in the current code a snippet at the
  // current cursor position, move the cursor
  // after the snippet and focus the textarea
  const input = get_textarea_input();
  if (!input) return;
  const start = input.selectionStart;
  const code = current.value.data.code || "";

  current.value.data.code =
    code.slice(0, input.selectionStart) +
    snippet +
    code.slice(input.selectionEnd);

  requestAnimationFrame(() => {
    input.selectionStart = start + snippet.length;
    input.selectionEnd = start + snippet.length;
    input.focus();
  });
};

const keyed = (iterable: Unit[], i: number) => {
  if ("_key" in iterable[i] && iterable[i]._key) {
    return iterable[i]._key;
  }
  iterable[i]._key = nanoid();
  return iterable[i]._key;
};

const move = (offset: number) => {
  if (current.value.index === undefined) return;

  const from = current.value.index;
  const to = from + offset;

  // Swap array elements
  const temp = sheet[from];
  sheet[from] = sheet[to];
  sheet[to] = temp;

  edit(to);
};

const remove = () => {
  if (current.value.index === undefined) return;

  sheet.value.splice(current.value.index, 1);

  if (sheet.value.length === 0) {
    edit_drawer.value.show = false;
    return;
  }

  edit(Math.min(current.value.index, sheet.value.length - 1));
};

const edit = (i: number) => {
  current.value.index = i;
  edit_drawer.value.show = true;
  current.value.data = sheet.value[i];

  nextTick(() => {
    // Scroll to the currently edited section
    const sectionRef = document.querySelector(
      `[data-section-key="${keyed(sheet.value, i)}"]`,
    ) as HTMLElement;
    goTo(sectionRef, { offset: -64 });
  });
};

const add = (unit: Partial<Unit>) => {
  const base_unit = {
    type: "default",
    title: "",
    code: "",
  };

  sheet.value.push({ ...base_unit, ...unit } as Unit);

  edit(sheet.value.length - 1);
};
const close_add_gap_dialog = () => {
  add_gap_dialog_show(false);
  new_gap_options.value = [];
};

// Watch handlers
watch(add_gap_dialog, (val) => {
  if (val) {
    new_gap_options.value = [];
  } else {
    requestAnimationFrame(() => {
      get_textarea_input().focus();
    });
  }
});

watch(add_pair_dialog, (val) => {
  if (val) {
    add_pair_first_item.value = "";
    add_pair_second_item.value = "";
  } else {
    add_pair_form.value?.resetValidation();
    requestAnimationFrame(() => {
      get_textarea_input().focus();
    });
  }
});

watch(insert_video_dialog, (val) => {
  if (val) {
    insert_video_url.value = "";
  } else {
    insert_video_form.value?.resetValidation();
    requestAnimationFrame(() => {
      get_textarea_input().focus();
    });
  }
});

watch(
  () => edit_drawer.value.show,
  (val) => {
    if (val === false) {
      current.value.index = undefined;
    }
  },
);

// Make refs accessible to parent components
defineExpose({
  unit_description,
  add_pair_form,
  insert_video_form,
  new_gap_form,
  unit,
});
</script>

<template>
  <div id="sheet-editor">
    <v-navigation-drawer
      id="editor-drawer"
      :location="$vuetify.display.mobile ? 'bottom' : 'right'"
      permanent
      width="0"
      v-if="sheet && edit_drawer.show"
    >
      <template #prepend>
        <v-toolbar density="compact" flat>
          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                @click="edit((current.index as number) - 1)"
                :disabled="current.index === 0"
                icon="mdi-chevron-up"
              ></v-btn>
            </template>
            <span>{{ t("sheet_editor.edit_previous") }}</span>
          </v-tooltip>

          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                @click="edit((current.index as number) + 1)"
                :disabled="current.index === sheet.length - 1"
                icon="mdi-chevron-down"
              ></v-btn>
            </template>
            <span>{{ t("sheet_editor.edit_next") }}</span>
          </v-tooltip>

          <v-divider vertical class="mx-2"></v-divider>

          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-btn v-bind="props" @click="remove" icon="mdi-delete"></v-btn>
            </template>
            <span>{{ t("sheet_editor.delete") }}</span>
          </v-tooltip>

          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                @click="move(-1)"
                :disabled="current.index === 0"
                icon="mdi-transfer-up"
              ></v-btn>
            </template>
            <span>{{ t("sheet_editor.move_up") }}</span>
          </v-tooltip>

          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                @click="move(+1)"
                :disabled="current.index === sheet.length - 1"
                icon="mdi-transfer-down"
              ></v-btn>
            </template>
            <span>{{ t("sheet_editor.move_down") }}</span>
          </v-tooltip>

          <v-spacer />

          <v-tooltip location="left">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                @click="edit_drawer.show = false"
                icon="mdi-close"
              ></v-btn>
            </template>
            <span>{{ t("sheet_editor.close") }}</span>
          </v-tooltip>
        </v-toolbar>
      </template>

      <v-container class="mt-2">
        <v-select
          variant="outlined"
          density="compact"
          label="Type"
          :items="available_types"
          v-model="current.data.type"
        ></v-select>
        <v-text-field
          v-model="current.data.title"
          :label="t('sheet_editor.title')"
          variant="outlined"
        ></v-text-field>
        <v-textarea
          v-model="current.data.description"
          ref="unit_description"
          id="unit_description"
          rows="1"
          auto-grow
          :label="t('editor.description')"
          variant="outlined"
          :loading="description_loading"
        >
          <template #append>
            <v-menu location="bottom end">
              <template #activator="{ props }">
                <v-icon v-bind="props" :disabled="description_loading">
                  mdi-dots-vertical z
                </v-icon>
              </template>
              <v-list>
                <v-list-item
                  v-if="false"
                  :title="t('sheet_editor.insert_video')"
                  prepend-icon="mdi-movie"
                ></v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-textarea>
        <v-toolbar
          density="compact"
          flat
          color="grey-lighten-4"
          class="rounded-b-0 rounded-t-lg"
        >
          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-btn v-bind="props" icon @click="append_new_sentence">
                <v-icon>mdi-playlist-plus</v-icon>
              </v-btn>
            </template>
            <span>{{ t("sheet_editor.add_sentence") }}</span>
          </v-tooltip>

          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                icon
                @click.stop="add_gap_dialog_show(true)"
                :disabled="current.data.type === 'pairing'"
              >
                <v-icon>mdi-tray-plus</v-icon>
              </v-btn>
            </template>
            <span>{{ t("sheet_editor.insert_gap") }}</span>
          </v-tooltip>

          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                icon
                @click="add_pair_dialog = true"
                :disabled="current.data.type !== 'pairing'"
              >
                <v-icon>mdi-equal</v-icon>
              </v-btn>
            </template>
            <span>{{ t("sheet_editor.add_matching_pair") }}</span>
          </v-tooltip>
          <v-dialog v-model="add_pair_dialog" max-width="750">
            <v-card>
              <v-form
                ref="add_pair_form"
                @submit.prevent="add_pair_insert_click"
              >
                <v-card-title>
                  {{ t("sheet_editor.new_matching_pair") }}
                </v-card-title>
                <v-card-text>
                  <v-text-field
                    v-model="add_pair_first_item"
                    variant="underlined"
                    autofocus
                    :label="t('sheet_editor.first_item')"
                    :rules="[
                      (val: string) => (!val ? 'Please type some text' : true),
                    ]"
                  ></v-text-field>
                  <v-text-field
                    v-model="add_pair_second_item"
                    variant="underlined"
                    :label="t('sheet_editor.second_item')"
                    :rules="[
                      (val: string) => (!val ? 'Please type some text' : true),
                    ]"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer />
                  <v-btn color="primary" type="submit">
                    {{ t("sheet_editor.insert_pair") }}
                  </v-btn>
                  <v-btn variant="text" @click="add_pair_dialog = false">
                    {{ t("main.cancel") }}
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>

          <v-divider vertical inset class="mx-2"></v-divider>

          <v-tooltip location="bottom">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                icon
                @click="insert_video_dialog = true"
                :disabled="current.data.type !== 'pairing'"
              >
                <v-icon>mdi-movie</v-icon>
              </v-btn>
            </template>
            <span>{{ t("sheet_editor.insert_video") }}</span>
          </v-tooltip>

          <v-dialog v-model="insert_video_dialog" max-width="750">
            <v-card>
              <v-form
                @submit.prevent="insert_video_insert_click"
                ref="insert_video_form"
              >
                <v-card-title>
                  {{ t("sheet_editor.insert_video") }}
                </v-card-title>
                <v-card-text>
                  <v-text-field
                    v-model="insert_video_url"
                    autofocus
                    label="Video URL"
                    :rules="[
                      (val: string) =>
                        /^https?:/i.test(val)
                          ? true
                          : t('sheet_editor.valid_url'),
                    ]"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer />
                  <v-btn color="primary" type="submit">
                    {{ t("sheet_editor.insert_video") }}
                  </v-btn>
                  <v-btn variant="text" @click="insert_video_dialog = false">
                    {{ t("main.cancel") }}
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>

          <v-dialog v-model="add_gap_dialog" max-width="750">
            <v-card>
              <v-form
                ref="new_gap_form"
                @submit.prevent="insert_gap_click"
                @keydown.enter.prevent="
                  () => {
                    /*Prevent submiting form on Return in new_option field */
                  }
                "
              >
                <v-card-title>{{ t("sheet_editor.new_gap") }}</v-card-title>
                <v-card-text>
                  <OptionsSelector
                    v-model="new_gap_options"
                    firstchecked
                    :rules="[
                      () =>
                        new_gap_options.length === 0
                          ? $t('sheet_editor.add_option_validation')
                          : true,
                    ]"
                    autofocus
                    @update:model-value="new_gap_form?.resetValidation()"
                  ></OptionsSelector>
                </v-card-text>
                <v-card-actions>
                  <v-spacer />
                  <v-btn variant="text" @click="close_add_gap_dialog">
                    {{ t("main.cancel") }}
                  </v-btn>
                  <v-btn
                    color="primary"
                    variant="elevated"
                    @click.prevent="insert_gap_click"
                  >
                    {{ t("sheet_editor.insert_gap") }}
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>
        </v-toolbar>
        <v-textarea
          :placeholder="t('sheet_editor.start_typing')"
          name="textarea-input"
          ref="textarea"
          v-model="current.data.code"
          auto-grow
          variant="outlined"
          hide-details="auto"
          class="code rounded-t-0 rounded-b-md"
        ></v-textarea>
        <v-switch
          v-model="current.data.shuffle"
          :disabled="current.data.type === 'open_answer'"
          :label="t('sheet_editor.shuffle_options')"
          prepend-icon="mdi-shuffle"
          class="mt-6 mb-0"
        ></v-switch>

        <v-switch
          v-model="current.data.ignore_case"
          :disabled="current.data.type !== 'open_answer'"
          :label="t('sheet_editor.ignore_case')"
          prepend-icon="mdi-case-sensitive-alt"
          class="mt-0"
        ></v-switch>
      </v-container>
    </v-navigation-drawer>
    <v-container
      id="current-sheet"
      :class="edit_drawer.show ? ['edition', 'ms-0'] : undefined"
    >
      <div
        class="mb-5 pa-9"
        v-if="sheet?.length == 0"
        key="no_units"
        style="border: 4px dashed #e7e7e7"
      >
        <div class="text-h6 text-disabled">
          {{ t("sheet_editor.empty_exercise") }}
        </div>
        <span class="text-disabled">
          {{ t("sheet_editor.add_unit_to_begin") }}
        </span>
      </div>

      <v-slide-group direction="vertical">
        <div v-for="(section, i) in sheet" :key="keyed(sheet, i)">
          <!--
          The outer <div> is needed to have both the
          sliding animation when the v-sheets are moved
          and the fading animation of the v-sheet's elevation when
          toggling edit mode.
          -->
          <v-sheet
            :elevation="i == current.index ? 2 : 0"
            :data-section-key="keyed(sheet, i)"
            class="mt-1 mb-4 mx-2 transition-swing"
            rounded
          >
            <v-row no-gutters>
              <v-col class="flex-grow-0">
                <v-btn
                  size="x-small"
                  depressed
                  @click="
                    i != current.index ? edit(i) : (edit_drawer.show = false)
                  "
                  :color="i != current.index ? undefined : 'primary'"
                  class="rounded-te-0 rounded-be-0"
                  style="height: 100%; font-size: 1em"
                >
                  <v-icon>
                    {{ i != current.index ? "mdi-pencil" : "mdi-check-bold" }}
                  </v-icon>
                </v-btn>
              </v-col>
              <v-col class="ms-4">
                <div v-if="section.title" class="text-h4 my-4">
                  <span v-if="sheet.length > 1">{{ i + 1 }}.</span>
                  {{ section.title }}
                  <span class="font-italic">
                    {{ $t("sheet_editor.untitled_unit") }}
                  </span>
                </div>
                <div v-if="section.description" class="body-2 mb-4 pre-line">
                  <RichContent :text="section.description"></RichContent>
                </div>
                <component
                  :is="unit_component(section.type)"
                  :code="section.code"
                  :shuffle="section.shuffle || false"
                  :ignore_case="section.ignore_case"
                  :silent="true"
                  ref="unit"
                />
              </v-col>
            </v-row>
          </v-sheet>
        </div>
      </v-slide-group>

      <v-menu offset-y>
        <template #activator="{ props }">
          <v-btn class="mt-3" variant="tonal" v-bind="props">
            <v-icon class="me-2">mdi-plus</v-icon>
            {{ $t("sheet_editor.add_unit") }}
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(snippet, index) in snippets"
            :key="index"
            @click="add(snippet.unit)"
          >
            <template #prepend>
              <v-img
                width="80"
                height="60"
                contain
                :src="load_snippet_thumb(snippet)"
              >
                <template #placeholder>
                  <v-skeleton-loader type="image" height="60" />
                </template>
              </v-img>
            </template>
            <v-list-item-title>{{ snippet.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-container>
  </div>
</template>

<style scoped>
#sheet-editor {
  container: sheet-editor / inline-size;
}
@container sheet-editor (min-width: 600px) {
  #editor-drawer {
    width: 45cqw;
  }
  #current-sheet.edition {
    width: 55cqw;
  }
}

.pre-line {
  white-space: pre-line;
}

.code {
  font-family: monospace;
}

.v-menu__content {
  max-height: 85vh;
}
</style>
