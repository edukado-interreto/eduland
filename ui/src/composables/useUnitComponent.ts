import UnitDefault from "@/components/UnitDefault.vue"
import UnitMultipleChoice from "@/components/UnitMultipleChoice.vue"
import UnitOpenAnswer from "@/components/UnitOpenAnswer.vue"
import UnitPairing from "@/components/UnitPairing.vue"

export default function () {
  return (unit_type) =>
    ({
      default: UnitDefault,
      open_answer: UnitOpenAnswer,
      multiple_choice: UnitMultipleChoice,
      pairing: UnitPairing,
    })[unit_type]
}
