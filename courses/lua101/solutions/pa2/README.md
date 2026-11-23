# PA2 answer key and grading notes

`pa2.py`, paired with `pa2.ipynb`, is the source of PA2: the model solutions, the visible tests,
and the hidden tests. Students receive `assignments/pa2/pa2.ipynb`, which
`tools/student_version.py` makes from it. Change the source, never the student version, and
then make the student version again.

The autograder awards each test cell's points when every test in it passes. Problem 6, Part B,
is graded by hand against the model answer in the source: a point for the reason and an example
together, half a point for either alone.

Three hidden tests time a function on a large input, with limits set from measurements on an
Intel Core i7-11800H with lupa 2.8 (Lua 5.4.8). Each limit is at least 11 times what the model
solution took there, and at most a third of what the slow solution took:

| Test | Model solution | Slow solution | Limit |
| :- | :- | :- | :- |
| 2,000 calls of `set_size` on 10,000 members | 0.04 ms | 0.3 s, counting with `pairs` | 0.1 s |
| `rle_encode` on 200,000 runs | 0.04 s | 3.8 s, with `..` in the loop | 0.5 s |
| `utf8_reverse` on 60,000 characters | 0.006 s | 9.9 s, with `table.insert(t, 1, c)` | 0.25 s |

If the grading machine is much slower, rerun the model solution there before trusting a timing
failure.

## Reasoning and common mistakes

### Problem 1: Word frequencies

`text:lower():gmatch("%a+")` finds the words and folds their case in one pass, and
`(counts[word] or 0) + 1` counts them; `or` is safe here, because a count is never `false`.
`top_words` copies the table into a list, sorts it with a two-key comparator, and cuts the list to
`k` items. Common mistakes: `%w+`, which counts digits as words; a comparator without the
alphabetical tie-break, which the visible tests already catch; and `table.remove` in a loop to cut
the list, which works but costs more.

### Problem 2: A set type

The model keeps the members as keys of `items`, and the count in `size`, which makes `set_size`
constant time. The traps are in the statement:

- `set_new` must count its arguments with `select("#", ...)`. A loop over `{...}` with `ipairs`
  stops at the first `nil`, so `set_new(nil, 1, nil, 2, nil)` comes out empty.
- `false` must be a possible member. A representation that stores each member as its own value,
  `items[v] = v`, makes `false` look absent; storing `true` avoids that.
- `set_has` must return `false`, not `nil`, for a non-member.
- Adding a member twice must not change the count, so `set_add` tests for membership before it
  increments.

`set_intersection` is fastest when it walks the smaller set, as the model does; a solution that
walks either set is correct and loses no points.

### Problem 3: Run-length encoding

The encoder finds each run with an inner loop; `s:find("^" .. c .. "*", i)` also works, if the
student escapes punctuation characters with `%`. The decoder needs a validity check, and Lua
patterns can't say "only runs" with a repeated group. The model removes every run with `gsub`
and checks that nothing is left. Another correct check walks the code with `find` and an `init`
position. Common mistakes: no validity check, so `"3a2"` decodes to `"aaa"`; `(%d+)(.)`, which
accepts a digit as the character; and returning `code:gsub(...)` from a helper without
parentheses, which returns the count too.

### Problem 4: Reversing UTF-8 text

`utf8.len` validates the text and counts its characters at once, so the model can fill the result
from the back. `gmatch(utf8.charpattern)` and `utf8.codes` with `utf8.char` both work for the
walk. Common mistakes: `s:reverse()`, and `table.insert(t, 1, c)`, which is $O(n^2)$ and fails the
timed test.

### Problem 5: Merging settings

The model deep-copies `defaults`, then copies each override in, merging where both sides hold a
table. Common mistakes: a shallow copy, which passes the visible tests but shares the tables that
come from `overrides`; `result[k] = v or result[k]`, which makes an override of `false`
impossible; and merging a table override into a non-table default, which stops with an error.

### Problem 6: Lists with holes

Part A loops to `n`, not to `#list`, and tests `list[i] ~= nil` rather than `list[i]`, so `false`
is kept. Part B's model answer is in the source. Accept any table whose `#` provably misses a
value in Lua 5.4.8, such as the one built by assignment in the model; `{ 1, nil, 3 }` built with a
constructor doesn't qualify, because there `#` returns 3. An answer that only says "`#` is
unreliable", without saying that it returns a border, earns half a point.
