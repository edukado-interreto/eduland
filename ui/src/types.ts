import type { ComponentPublicInstance } from "vue"
import type {
  UnitDefault,
  UnitMultipleChoice,
  UnitOpenAnswer,
  UnitPairing,
} from "#components"
import type { default as TMsgBox } from "@/components/MsgBox.vue"

import type langs from "~/data/langs.js"

type Enumerate<N extends number, Acc extends number[] = []> = Acc["length"] extends N
  ? Acc[number]
  : Enumerate<N, [...Acc, Acc["length"]]>

type Range<F extends number, T extends number> = Exclude<Enumerate<T>, Enumerate<F>>

declare global {
  type MsgBox = typeof TMsgBox

  /* App */

  type VueElement = Element | ComponentPublicInstance | null

  type DRF<T> = {
    previous: string | null
    next: string | null
    count: number
    results: T[]
  }

  type MsgBoxOptions = {
    buttons?: {
      value: boolean
      text: string
    }[]
    color?: string
    icon?: string
    max_width?: number
    modal?: boolean
    text?: string
    title?: string
  }

  type Toast = {
    text: string
    color: string
  }

  type UserReport = {
    user: number
    exercise: string
    nature: "mistake" | "misuse"
    description: string
  }

  /* Auth */

  type User = {
    id: number
    username: string
    email: string
    date_joined: string | Date
    data: { [k: string]: string }
  }

  type LoginCredential = {
    email: string
    password: string
  }

  type LoginResponse = {
    access: string
    refresh: string
    user: User
  }

  type LogoutResponse = {
    detail: string
  }

  type RefreshResponse = {
    access: string
    refresh: string
  }

  /* Models */

  type UnitType = "default" | "open_answer" | "multiple_choice" | "pairing"
  type UnitComponent =
    | typeof UnitDefault
    | typeof UnitMultipleChoice
    | typeof UnitOpenAnswer
    | typeof UnitPairing

  type Cefr = "A1" | "A2" | "B1" | "B2" | "C1" | "C2"
  type CefrValue = 1 | 2 | 3 | 4 | 5 | 6
  type CefrValueStr = "1" | "2" | "3" | "4" | "5" | "6"
  type CefrRange = [CefrValue, CefrValue]
  type MaybeCefrRange = [CefrValue | undefined, CefrValue | undefined]

  type AgeMin = 0
  type AgeMax = 18
  type AgeRange = Range<AgeMin, AgeMax>

  type BuildExercise = {
    age_min: AgeMin
    age_max: AgeMax
    created_by: User["username"]
    description: string
    name: string
    src_lang: string
    searchable: boolean
    lang_learn: boolean
    lang_learn_lang?: Lang["code"]
    lang_learn_cefr_level_min?: CefrValue
    lang_learn_cefr_level_max?: CefrValue
    tags: string[]
    data: {
      sheet: Unit[]
    }
  }
  type Exercise = BuildExercise & {
    lang_learn_lang: Lang["code"]
    lang_learn_cefr_level_min: CefrValue
    lang_learn_cefr_level_max: CefrValue
    _key: string
    id: number
    lid: string
    modified: string
    likes: number
    liked: Liked
    url: string
  }

  // Exercise-like
  type Details = {
    title: string
    src_lang: string
    description: string
    unlisted: boolean
    tags: Tag[]
    age_range: number[]
    lang_learn: {
      lang?: string
      cefr_level_range: [CefrValue?, CefrValue?]
    }
  }

  type Snippet = {
    name: string
    img: string
    unit: {
      type: string
      code: string
      description?: string
      shuffle?: boolean
    }
  }

  type Unit = {
    _key: string
    code: string
    description: string
    shuffle: boolean
    ignore_case: boolean
    solved?: SolvedDrags
    title: string
    type: UnitType
  }

  type Exam = {
    pk: number
    lid: string
    created: Date
    modified: Date
    created_by: string
    name: string
    description: string
    exercise_lid: string
    accept_submission: boolean
    likes: boolean
    liked: Liked
    url: string
  }

  type Submission = {
    pk: number
    created: Date
    exercise_lid: string
    exam_lid: string | null
    exercise: Exercise
    created_by?: string
    guest?: string
    data: object
    score: number
  }

  type NewSubmission = {
    created: Date
    exercise_lid: string
    exam_lid: string | null
    exercise: Exercise
    created_by?: string
    guest?: string
  }

  type Search = {
    limit: number
    offset: number
    name: string
    tags: Tag[]
    created_by: Author["username"]
    src_langs: Lang[]
    lang_learn: {
      langs: Lang[]
      levels: [CefrValue, CefrValue]
    }
    sort: "created" | "likes" | "-created" | "-likes"
  }

  type SearchQuery = {
    limit: number
    offset?: number
    name?: string
    tags?: Tag[]
    created_by?: Author["username"]
    src_lang?: Lang[]
    lang_learn_lang?: Lang[]
    cefr_level_min?: CefrValue
    cefr_level_max?: CefrValue
    ordering: "created" | "likes" | "-created" | "-likes"
  }

  type Option = {
    value?: string
    right?: boolean
    answer?: string
  }

  type GapOption = {
    value: string
    right: boolean
  }

  type Author = {
    id: string
    username: string
    count: number
  }

  type Tag = {
    pk: string
    name: string
    count: number
  }

  type Lang = {
    code: keyof typeof langs.langs
    count: number
  }

  type Solved = {
    parsed: Token[][]
  }

  type SolvedDrags = {
    parsed: [string, string][]
    drags: Drags
  }

  type Token = {
    token?: string
    options?: Option[]
    value?: string
    right?: boolean
    answer?: string
    errorExplanation?: string
  }

  type Drags = ([string, string] | [string, null])[]

  type Liked = number | null
  type LikedResponse = {
    liked: Liked
  }
}

declare module "nuxt/schema" {
  interface PublicRuntimeConfig {
    apiBase: string
  }
}

export {}
