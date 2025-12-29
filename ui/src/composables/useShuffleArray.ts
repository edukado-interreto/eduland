const shuffle_array = (in_array: unknown[]) => {
  /**
   * Shuffle an array using the Fisher-Yates algorithm,
   * O(n), un-biased.
   */

  const out_array = in_array.slice()
  // clone the input array

  let currentIndex = out_array.length
  let randomIndex: typeof currentIndex

  // While there remain elements to shuffle...
  while (currentIndex !== 0) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex--
    // And swap it with the current element.
    ;[out_array[currentIndex], out_array[randomIndex]] = [
      out_array[randomIndex],
      out_array[currentIndex],
    ]
  }

  return out_array
}

export default function () {
  return shuffle_array
}
