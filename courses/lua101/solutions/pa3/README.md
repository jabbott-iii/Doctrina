# PA3 answer key and grading notes

Students receive `assignments/pa3/`: the handout, the starter `iter.lua`, and two example tests.
This folder holds what they don't see:

| File | What it is |
| :- | :- |
| `iter.lua` | The model solution |
| `hidden_spec.lua` | The hidden tests: 47 tests in nine blocks, worth 70 points |
| `spec/iter_spec.lua` | A model student test suite, which earns full marks on the Tests criterion |
| `grading.json` | The settings for `tools/grade_project.py`: the module's name and the 10 broken versions |

## Grading a submission

1. Put the submission's `iter.lua` and `spec/` folder in a folder of their own.
2. From the repository's root, with the notebook environment active, run:

   ```bash
   python courses/lua101/tools/grade_project.py courses/lua101/solutions/pa3 path/to/submission
   ```

   It prints the hidden-test points by function, each failed hidden test, how many of the
   student's tests pass on the model solution, and which broken versions the student's tests
   caught. It runs the hidden tests one function's block at a time. Each busted run stops after
   60 seconds, which only an endless loop reaches; that block then earns no points, and the
   others are unaffected.
3. Score the rubric. **Tests** follows from the script's output and the handout's levels.
   **Design** and **Style** need a read of `iter.lua`, against the notes below.
4. Check the second and third lines of `iter.lua`: the tools used and the people the student
   talked with. A missing line is a policy matter, not a deduction in the rubric.

Before grading a term's submissions, run the self-test, which grades the model with the model
tests. It should print 70.00 of 70 points and catch all 10 broken versions; if a broken version no
longer applies to the model, the script stops and says which:

```bash
python courses/lua101/tools/grade_project.py courses/lua101/solutions/pa3 --self-test
```

On the test machine, an Intel Core i7-11800H with Lua 5.4.8 and busted 2.3.0, the whole
self-test, with 20 busted runs, took 0.9 s. A submission with an endless loop takes a minute
longer for each block that loops.

## The broken versions

Each is the model with one change. They test whether the student's tests check what the handout
promises, not whether they are long:

| Broken version | Caught by a test that… |
| :- | :- |
| `from_list` stops at `false` | collects a list with `false` in it |
| `count` ignores `step` | uses a step other than 1 |
| `map` ends quietly when `fn` returns `nil` | expects the error `map: fn returned nil` |
| `filter` keeps only results equal to `true` | uses a predicate that returns a truthy non-boolean |
| `take` calls the source once more than it needs | counts the source's calls after `take(n, …)` |
| `take` accepts a negative `n` | expects the error for `n = -1` |
| `zip` calls `b` after `a` has ended | counts `b`'s calls when `a` is shorter |
| `split` treats `sep` as a pattern | splits on `.` or `%` |
| `split` drops an empty last field | splits a string that ends with the separator, or `""` |
| `memoize` doesn't cache `nil` | counts calls of a function that returns `nil` |

The starter tests catch one, `take` accepting a negative `n`. In a trial, a suite with one test
of each function's normal results, and nothing else, caught none: every broken version needs a
test of an edge, of laziness, or of an error, which is what LO-6.3 asks for.

## Design and Style: what to look for

Full-marks design looks like the model:

- One local helper raises every argument error, at the right level. The model's `fail` raises at
  level 3, because the error passes through it as well as the public function; a student who
  calls `error(…, 2)` directly in each function is equally correct, and loses nothing.
- Each iterator's state, such as `taken` and `done` in `take`, lives in locals of the call that
  created it, so two iterators never share state. A solution that keeps a position in the module
  table, such as `iter.position`, works for one iterator at a time, and fails the hidden zip test
  that zips two lists.
- Nothing is computed before it is asked for. A `map` that calls `to_list` on its source loops
  forever on `count`: in a trial, its block timed out and the other blocks scored, for 62 of 70
  points. Deduct for the design too, since the handout asks for laziness.

For Style, read for the things the handout names. A comment that explains why, such as the
model's on the `NIL` placeholder, is the standard; a comment on every line is not.

## Reasoning and common mistakes

### `from_list` and `to_list`

`return list[i]` already returns `nil` at the end, so `from_list` needs no test. The common
mistake is `if list[i] then`, which ends at a `false` value; the same mistake in `to_list`, as
`if not value then break end`, drops everything after a `false`.

### `count`

Computing each value as `start + (k - 1) * step` keeps it exact for integers and avoids drift for
floats. Students who add `step` each time pass every hidden test, which use integers only.

### `map` and `filter`

Both must check for `nil` from the source before calling `fn` or `pred`. In `map`, testing
`if not result` instead of `if result == nil` raises an error for a result of `false`, which the
handout says is a value. In `filter`, `if pred(value) == true` is the broken version above.

### `take`

The order of the checks is the point: test the count before calling the source, and remember
that the source ended, so that it is never called again. Accept any check of `n` that rejects -1,
1.5, and `"3"`; a solution that also accepts `2.0` is fine, because the handout doesn't test it.

### `zip`

`zip` must call `a`, test it, and only then call `b`. Calling both first and testing afterward is
the broken version above. Returning `nil` for the ended side, instead of ending, never stops when
one iterator is endless.

### `split`

`s:find(sep, position, true)` with the fourth argument is the whole trick: it searches for plain
text from a position. Solutions with `gmatch("[^,]+")` drop empty fields and assume a one-character
separator; solutions with `gmatch("(.-)" .. sep)` treat `sep` as a pattern and miss the last
field.

### `memoize`

This is Lab 5's exercise with argument checks added. The common mistakes are the lab's: storing
`nil` in the cache, and one cache shared by every memoized function. `x ~= x` is the test for NaN,
because NaN is the only value not equal to itself.
