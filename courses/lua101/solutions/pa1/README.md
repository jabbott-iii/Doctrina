# PA1 answer key and grading notes

`pa1.py`, paired with `pa1.ipynb`, is the source of PA1: the model solutions, the visible tests,
and the hidden tests. Students receive `assignments/pa1/pa1.ipynb`, which
`tools/student_version.py` makes from it. Change the source, never the student version, and
then make the student version again.

The autograder awards each test cell's points when every test in it passes. Problem 5, Part B,
is graded by hand, half a point for each function, against the model answer in the source.

## Reasoning and common mistakes

### Problem 1: Exact division

`a % b == 0` tests divisibility, and `a // b` then gives an integer quotient. The common mistake
is returning `a / b` in both cases, which gives the float `2.0` for `exact_division(6, 3)`; the
visible test on `math.type` catches it. A second mistake tests `a / b == a // b`, which works
here but compares a float with an integer, and the reading recommends `%`.

### Problem 2: Collatz sequences

Halving with `/` instead of `//` turns `n` into a float after the first even step. The step
counts stay right, so `collatz_steps` passes, but `collatz_peak` then returns floats such as
`16.0`, and the subtype tests fail. Students who start `peak` at 0 instead of `n` still pass,
because every sequence's peak is at least `n`; that is worth a comment in feedback, not a
deduction.

### Problem 3: Counting by type

The hidden tests put `nil` before and after other arguments. A loop over `{...}` with `ipairs`
stops at the first `nil`, and `#{...}` can miss the trailing ones; only `select("#", ...)`
counts them all. Writing `type(select(i, ...))` without the extra parentheses passes every
argument from `i` on to `type`, which ignores all but the first, so it happens to work; the
model answer keeps the parentheses to say what it means.

### Problem 4: Digit sums

The base case `n < 10` returns the digit itself, which also covers 0. A solution that uses
`n / 10` and `math.floor` returns floats for large `n`, and `math.maxinteger` loses precision as a
float, so the digit sum comes out wrong; the hidden tests catch both.

### Problem 5: Applying a function many times

Part A needs a proper tail call, `return apply_n(f, f(x), n - 1)`. The version
`return f(apply_n(f, x, n - 1))` gives the same results for small `n` but overflows the stack at
1,000,000, which the hidden test checks. A loop passes the tests but not the statement, which asks
for recursion; the autograder can't tell, so check by reading the code, and deduct the part's
points if it loops.

### Problem 6: Prices with options

The trap is `opts.cents or true`, which makes `cents = false` impossible; the hidden tests check
it. `opts.symbol or "$"` is correct even for `symbol = ""`, because the empty string is truthy:
students who "fix" that line with an `== nil` test aren't wrong, only longer. Rounding halves up
is `(cents + 50) // 100`; `math.floor(cents / 100 + 0.5)` also works.

### Problem 7: A bug report

The message is `cell:3: attempt to perform arithmetic on a nil value (global 'ratoi')`, so
`error_line` is 3 and `error_variable` is `"ratoi"`. Students sometimes give 5, the line that
called the function, or `"ratio"`, the name the code meant; the hidden tests check the exact
values from the message.
