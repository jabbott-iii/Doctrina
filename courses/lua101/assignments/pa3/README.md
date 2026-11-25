# PA3: An iterator library

**Objectives:** LO-5.2, LO-5.3, LO-6.1, LO-6.2, LO-6.3, and, revisited, LO-3.1 and LO-4.2\
**When:** after Module 6, as the [suggested pace](../../README.md#suggested-pace) places it\
**Checking your work:** the example tests, your own tests, and the rubric below\
**Time:** about 6 hours, spread over modules 5 and 6

You will write `iter`, a module of **lazy iterators**: functions that produce values one at a
time, and that combine into pipelines such as "the first five even squares" without building a
list in between. You will also write the busted tests that show it works. This is your first Lua
project outside a notebook: two files you run with the standalone `lua` and `busted`.

## What to hand in

Submit these two files through the learning management system:

- `iter.lua`, the module, with its second line saying which tools you used, and how, or "none",
  and its third line naming everyone you discussed the assignment with, or "no one";
- `spec/iter_spec.lua`, your tests. You may split them across more files in `spec/` whose names
  end in `_spec.lua`.

## Getting started

1. Copy this folder, `assignments/pa3/`, to a folder of your own. It holds the starter module,
   [`iter.lua`](iter.lua), whose functions all raise `not implemented`, and the starter tests,
   [`spec/iter_spec.lua`](spec/iter_spec.lua), with two examples.
2. In a terminal, put Lua and busted on your `PATH`, as [setting up](../../setup.md) describes:
   `source .venv/lua/bin/activate` from the repository's root.
3. From your copy of the folder, run `busted`. It finds `spec/` and the module on its own. Both
   example tests fail until you write `from_list`, `count`, and `take`.

Use the notebooks from modules 5 and 6 for trying out ideas, but write the module and the tests in
these files: the grader runs them with `busted`, not in a notebook.

## The library

In this assignment, an **iterator** is a function that returns the next value each time it is
called, and `nil` once it has no more, as the stateful iterators of module 5 do. So each one can
go straight into a generic `for`: `for v in iter.from_list({ 1, 2 }) do … end`. An iterator never
produces `nil` as a value, but it can produce `false`.

| Function | Returns |
| :- | :- |
| `iter.from_list(list)` | An iterator over the values of the sequence `list`, in order, `false` included |
| `iter.count(start, step)` | An endless iterator over `start`, `start + step`, `start + 2 * step`, …; both default to 1 |
| `iter.map(fn, it)` | An iterator over `fn(v)` for each value `v` of `it` |
| `iter.filter(pred, it)` | An iterator over the values `v` of `it` for which `pred(v)` is truthy |
| `iter.take(n, it)` | An iterator over the first `n` values of `it`, or all of them if there are fewer |
| `iter.zip(a, b)` | An iterator whose calls each return two values, the next of `a` and the next of `b`; it ends when either ends |
| `iter.split(s, sep)` | An iterator over the fields of the string `s` between occurrences of `sep`, which is plain text, not a pattern |
| `iter.to_list(it)` | A new sequence of every value of `it` |
| `iter.memoize(fn)` | A function that returns `fn(x)`'s first result, calling `fn` at most once for each argument `x` |

The details that the tests check:

- **Laziness.** Creating an iterator with `map`, `filter`, `take`, or `zip` calls nothing. Each
  call of the new iterator calls its source only as often as it must: `take(n, it)` calls `it` at
  most `n` times, and never again after `it` has returned `nil`; `zip` calls `a` first, calls `b`
  only when `a` gave a value, and calls neither once one of them has ended.
- **`count`** gives exactly `start + (k - 1) * step` as its `k`-th value, so that floats don't
  drift. It never ends, so pass it through `take` before `to_list`, or `to_list` never returns.
- **`map`** treats a result of `false` as a value. A result of `nil` would end the iterator early
  without saying so, so `map` raises an error instead (see below).
- **`split`** keeps empty fields, at the ends too: `"a,,b"` gives `"a"`, `""`, and `"b"`;
  `",a,"` gives `""`, `"a"`, and `""`; and the empty string gives one empty field. A separator
  may be longer than one character, and characters such as `.` and `%` in it match themselves.
- **`memoize`** caches results of `nil` and `false` too, gives each memoized function a cache of
  its own, and works for any argument except `nil` and NaN, including `false` and tables.

### Errors

Each function checks its arguments when it is called, and raises an error for a wrong one, **at
level 2**, so that the message names the caller's line. Each message starts with the function's
name:

| Function | Raises | When |
| :- | :- | :- |
| `from_list` | `from_list: list must be a table` | `list` isn't a table |
| `count` | `count: start and step must be numbers` | either one, when given, isn't a number |
| `count` | `count: step must not be 0` | `step` is 0 |
| `map` | `map: fn must be a function`, `map: it must be a function` | the argument named isn't a function |
| `map` | `map: fn returned nil` | while iterating, `fn` returns `nil` |
| `filter` | `filter: pred must be a function`, `filter: it must be a function` | the argument named isn't a function |
| `take` | `take: n must be a non-negative integer` | `n` isn't an integer of 0 or more, such as -1, 1.5, or `"3"` |
| `take` | `take: it must be a function` | `it` isn't a function |
| `zip` | `zip: a and b must be functions` | either one isn't a function |
| `split` | `split: s must be a string` | `s` isn't a string |
| `split` | `split: sep must be a non-empty string` | `sep` isn't a string, or is `""` |
| `to_list` | `to_list: it must be a function` | `it` isn't a function |
| `memoize` | `memoize: fn must be a function` | `fn` isn't a function |
| `memoize` | `memoize: the argument must not be nil or NaN` | the memoized function is called with `nil` or NaN |

Two errors come later, while the result is in use. The function `memoize` returns checks its
argument on each call, and raises its error at level 2 too, naming the line that called it.
`map: fn returned nil` happens inside the iterator, during the loop; the tests check its message
but not its position.

## Your tests

Write tests for every promise in this handout: each function's normal results, its edges (an
empty list, `false` values, `n = 0`, an absent separator), its laziness, and each error and its
message. Test laziness with a source that counts its calls, such as:

```lua
local calls = 0
local function source()
  calls = calls + 1
  return calls
end
```

The grader judges your tests the way Lab 6 did: it runs them against a correct `iter` library,
where they must all pass, and against 10 versions of it that each break one promise in this
handout, where each version should make at least one of your tests fail. It doesn't publish the
broken versions; work out from the handout what a careless implementation would get wrong.

## How it is graded

The course has no grades. This section describes the full check that an instructor or a
mentor who reviews your work can run. The hidden tests aren't published, so when you work
alone, test every promise in this handout yourself, and score your work with the rubric.

### Hidden tests: 70 points

The hidden tests check the promises above, function by function. Each function's tests earn its
points in proportion to how many of them pass:

| Function | Points | Function | Points |
| :- | :- | :- | :- |
| `from_list` | 5 | `zip` | 8 |
| `count` | 5 | `split` | 10 |
| `map` | 8 | `to_list` | 4 |
| `filter` | 8 | `memoize` | 12 |
| `take` | 10 | **Total** | **70** |

### Rubric: 30 points

| Criterion | Full marks | Partial | Little or none |
| :- | :- | :- | :- |
| **Tests** (10) | Every test passes on a correct library, and the tests catch at least 9 of the 10 broken versions: 10 points | 7–8 caught: 7 points; 4–6: 4 points; 1–3: 1 point | No tests, or none that catch a broken version: 0 points. Each test that fails on a correct library, because it checks something this handout doesn't promise, costs 2 points |
| **Design** (10) | Each function does one job. The argument checks share one local helper or one pattern. Every helper is local, the module creates no globals, and each iterator keeps its state in its own closure | The code works, but repeats itself where a helper would do, or puts helpers or state in the module table: 6 points | Globals, state shared between iterators, or work done before it is asked for: 3 points or fewer |
| **Style** (10) | Consistent two-space indentation, descriptive local names, a comment wherever the reason for the code isn't obvious (such as a placeholder for `nil`), no dead or commented-out code, and lines of 100 characters or fewer | Readable, with a few lapses: 6 points | Hard to follow: 3 points or fewer |

## Policies

The course's [policies](../../README.md#policies) apply. Discuss ideas with anyone, but write your
own code and tests, and name everyone you discussed the assignment with on the third line of
`iter.lua`. Generative AI tools may explain concepts and error messages to you, but may not write
any part of the module or its tests; say on the second line of `iter.lua` which tools you used, and
how, or write "none".
