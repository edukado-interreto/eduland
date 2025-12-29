import {
  UnitDefault,
  UnitMultipleChoice,
  UnitOpenAnswer,
  UnitPairing,
} from "@/components"

export default function () {
  return (unit_type: UnitType): UnitComponent =>
    ({
      default: UnitDefault,
      open_answer: UnitOpenAnswer,
      multiple_choice: UnitMultipleChoice,
      pairing: UnitPairing,
    })[unit_type]
}
