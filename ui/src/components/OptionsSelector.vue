<script lang="ts" setup>
import type { SubmitEventPromise } from "vuetify"
import type { VForm } from "vuetify/components"

interface Props {
  label?: string
  autofocus?: boolean
  rules?: Array<(value: any) => boolean | string>
  firstchecked?: boolean
}

const {
  autofocus = false,
  firstchecked = false,
  label = "",
  rules = [],
} = defineProps<Props>()

const model = defineModel<GapOption[]>({ required: true })

const new_option = ref("")

const submit = (e: SubmitEventPromise) => {
  insert(new_option.value)
  new_option.value = ""
}
const insert = (value: string) => {
  const empty = model.value.length === 0
  if (!model.value.map(o => o.value).includes(value)) {
    model.value.push({ value, right: empty })
  }
}
</script>

<template>
  <v-text-field
    v-model="new_option"
    variant="underlined"
    class="ms-4"
    required
    validate-on="blur"
    :placeholder="$t('sheet_editor.add_option_placeholder')"
    :rules="rules"
    @keyup.enter.stop="submit"
  >
    <template #append>
      <v-btn
        @click="submit"
        variant="elevated"
        color="primary"
        icon="mdi-keyboard-return"
        size="small"
        :disabled="!new_option"
      />
      <v-btn
        :disabled="!!new_option || model.map(o => o.value).includes('')"
        icon
        class="mx-4"
        variant="flat"
        size="small"
        @click="insert('')"
        v-tooltip:bottom="$t('editor.option_new_gap_tooltip')"
      >
        <v-icon small icon="mdi-plus" />
        <v-icon small icon="mdi-selection" />
      </v-btn>
    </template>
  </v-text-field>

  <v-list density="compact" width="50%" class="mx-auto">
    <v-list-item
      v-for="(option, index) in model"
      item.title="option.value"
      class="rounded-pill"
      slim
      :class="option.right ? ['bg-green-lighten-5'] : undefined"
    >
      <template #prepend>
        <v-list-item-action
          start
          v-tooltip:bottom="$t('sheet_editor.add_option_is_right_answer')"
        >
          <v-checkbox-btn v-model="option.right" color="green" />
        </v-list-item-action>
      </template>

      <template #title>
        <v-icon small v-if="option.value === ''">mdi-selection</v-icon>
        <span v-else class="font-weight-medium">{{ option.value }}</span>
      </template>

      <template #append>
        <v-list-item-action end>
          <v-hover #="{ isHovering, props }">
            <v-btn
              v-bind="props"
              v-tooltip:bottom="$t('sheet_editor.delete')"
              icon
              variant="flat"
              size="small"
              :class="isHovering ? ['opacity-100'] : ['opacity-10']"
              :color="isHovering ? 'red-lighten-5' : undefined"
              @click="model.splice(index, 1)"
            >
              <v-icon
                :color="isHovering ? 'red' : undefined"
                icon="mdi-close"
                size="x-large"
              ></v-icon>
            </v-btn>
          </v-hover>
        </v-list-item-action>
      </template>
    </v-list-item>
  </v-list>
</template>
