const CEFR = { A1: 1, A2: 2, B1: 3, B2: 4, C1: 5, C2: 6 } as const
const LABELS = { 1: "A1", 2: "A2", 3: "B1", 4: "B2", 5: "C1", 6: "C2" } as const
const [MIN, MAX] = [CEFR.A1, CEFR.C2]

const is_default = (range: MaybeCefrRange) => range[0] === MIN && range[1] === MAX

/**
 * Return a human readable text describing a cefr level range.
 * @example
 *   const cefr = useCefr()
 *   cefr.dispay([1, 2]) => "A1 - A2"
 *   cefr.dispay([2, 2]) => "A2"
 *   cefr.dispay([1, 6]) => "" (any level: empty string)
 */
const display = (range: MaybeCefrRange) => {
  if (is_default(range)) return ""

  const [min, max] = [range[0] || MIN, range[1] || MAX]
  if (min === max) return LABELS[min]
  return `${LABELS[min]} - ${LABELS[max]}`
}

export default () => ({
  CEFR,
  LABELS,
  MAX,
  MIN,
  display,
  is_default,
})
