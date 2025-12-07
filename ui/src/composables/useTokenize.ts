/**
 * Regular expression to match any sequence of characters enclosed in square brackets.
 *
 * Breakup of the regexp:
 *
 *  /
 *    \[      a literal [
 *    (       followed by this group (capturing):
 *      [     any of these characters
 *        ^   shall not be found:
 *        \]  a literal ].
 *      ]     Just that.
 *      *     Repeating zero or more times.
 *    )       End of the group.
 *    \]      Followed by a literal ]
 *  /
 *
 * @constant {RexExp}
 */
const REGEX = /\[([^\]]*)\]/

// TODO: this regex should contain a negative lookbehind
// to provide an escape mechanism for the exercise creators
// e.g. 'In JavaScript, \[1,2,3\] is an [+array|object]'.
// At the moment of writing, this is still unsupported in
// Safari (23% of users worldwide), so we should use a
// workaround, or a finite state automaton (FSA).
// See: https://caniuse.com/?search=lookbehind

const parse_line = (line: string): Token[] =>
  line
    .split(REGEX)
    .map((value, i) => {
      // The split will return an array having text at
      // odd positions and gaps at even positions, e.g.:
      //
      // "The [+cat|mouse] eats the [cat|+mouse].".split(…)
      // >> ['The ', '+cat|mouse', ' eats the ', 'cat|+mouse', '.']
      //
      // "[+Cats|Mice] eat [cats|+mices]".split(…)
      // >> ['', '+Cats|Mice', ' eat ', 'cats|+mices', '']
      //
      // This happens because we are splitting on a regexp,
      // but we have a capture group. So instead of getting
      // only the non-gaps portions, we also get the content
      // of the capture group(s) spliced into the returning array.
      //
      // Then we use .map() to process the tokens accordingly.
      //
      if (i % 2 === 0) return { token: "text", value } // is text

      // is a match of the capture group, i.e. the content
      // of a gap without the enclosing [ … ] brakets.
      //if (!value) return { value: "" }
      const ret = { token: "gap", options: [] }

      value.split("|").forEach((v, i, a) => {
        // a prepending '+' in an option marks
        // a right answer: set ret.right accordingly
        // and remove the leading '+' from the option
        let right = false
        if (v[0] === "+") {
          right = true
          v = v.slice(1)
        }

        // a '~' in the last option introduces a
        // message to show when a wrong answer is given,
        // e.g. [cat|+fish|dog~It can swim!]
        // remove that message from the option and use
        // it as ret.errorExplanation
        if (i === a.length - 1) {
          ;[v, ret.errorExplanation] = v.split("~")
        }

        ret.options.push({ value: v, right })
      })
      return ret
    })
    .filter((t) => t.value !== "")

const tokenize = (code: string): Token[][] => code.split("\n\n").map(parse_line)

export default function () {
  return tokenize
}
