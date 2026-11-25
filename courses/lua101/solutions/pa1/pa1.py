# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # PA1: Numbers and functions
#
# **Objectives:** LO-1.1, LO-1.2, LO-1.4, LO-2.1, LO-2.2, LO-2.3, LO-2.4\
# **When:** after Module 2, as the [suggested pace](../../README.md#suggested-pace) places it\
# **Points:** 22, for scoring yourself; the course has no grades\
# **Time:** about 3 hours
#
# Write each answer in the cell marked `-- YOUR CODE HERE`, replacing the line
# `error("not implemented")`. Each problem's test cell checks your answer with visible tests,
# which you can run as often as you like. An instructor or a mentor who reviews your work can
# also run hidden tests, which check the cases the problem statement describes but the
# visible tests don't, so read each statement closely and test those cases yourself.
#
# - Don't change or delete the test cells.
# - Define each function as a global, as each problem's starter code does, so the test cells can
#   call it.
# - Before you submit, restart the kernel and run every cell from the top (**Kernel** > **Restart
#   Kernel and Run All Cells**), and check that every test cell prints `passed`.
# - The course policies apply. In particular, generative AI tools may not write any part of this
#   assignment; say in the last cell which tools you used, and how, or write "none".

# %%
# %load_ext lualab
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% [markdown]
# ## Problem 1: Exact division (LO-1.2, 3 points)
#
# Write `exact_division(a, b)` for integers `a` and `b`. When `b` divides `a` exactly, it returns
# the quotient as an **integer**. Otherwise it returns the quotient as a float. When `b` is 0, it
# returns `nil`. For example, `exact_division(6, 3)` is the integer `2`, `exact_division(7, 2)` is
# `3.5`, and `exact_division(7, 0)` is `nil`.

# %% nbgrader={"grade": false, "grade_id": "exact-division", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function exact_division(a, b)
#   -- BEGIN SOLUTION
#   if b == 0 then
#     return nil
#   end
#   if a % b == 0 then
#     return a // b
#   end
#   return a / b
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "exact-division-tests", "locked": true, "points": 3, "schema_version": 3, "solution": false, "task": false} language="lua"
# assert(exact_division(6, 3) == 2, "exact_division(6, 3) should be 2")
# assert(math.type(exact_division(6, 3)) == "integer", "an exact quotient should be an integer")
# assert(exact_division(7, 2) == 3.5, "exact_division(7, 2) should be 3.5")
# assert(exact_division(7, 0) == nil, "division by 0 should give nil")
# -- BEGIN HIDDEN TESTS
# assert(exact_division(-7, 7) == -1 and math.type(exact_division(-7, 7)) == "integer",
#   "exact_division(-7, 7) should be the integer -1")
# assert(exact_division(0, 5) == 0 and math.type(exact_division(0, 5)) == "integer",
#   "exact_division(0, 5) should be the integer 0")
# assert(exact_division(-9, 4) == -2.25, "exact_division(-9, 4) should be -2.25")
# assert(exact_division(-9, -3) == 3 and math.type(exact_division(-9, -3)) == "integer",
#   "exact_division(-9, -3) should be the integer 3")
# assert(math.type(exact_division(1, 3)) == "float", "exact_division(1, 3) should be a float")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 2: Collatz sequences (LO-2.1, LO-1.2, 4 points)
#
# Start from a positive integer `n`. If `n` is even, halve it; if it is odd, replace it with
# `3 * n + 1`. Repeat until `n` is 1. For example, 6 becomes 3, 10, 5, 16, 8, 4, 2, 1: eight
# steps, and the largest value on the way is 16.
#
# Write two functions, each with a loop:
#
# - `collatz_steps(n)` returns the number of steps to reach 1. `collatz_steps(1)` is 0.
# - `collatz_peak(n)` returns the largest value the sequence reaches, `n` itself included. It must
#   return an **integer**, never a float.

# %% nbgrader={"grade": false, "grade_id": "collatz", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function collatz_steps(n)
#   -- BEGIN SOLUTION
#   local steps = 0
#   while n ~= 1 do
#     if n % 2 == 0 then
#       n = n // 2
#     else
#       n = 3 * n + 1
#     end
#     steps = steps + 1
#   end
#   return steps
#   -- END SOLUTION
# end
#
# function collatz_peak(n)
#   -- BEGIN SOLUTION
#   local peak = n
#   while n ~= 1 do
#     if n % 2 == 0 then
#       n = n // 2
#     else
#       n = 3 * n + 1
#     end
#     if n > peak then
#       peak = n
#     end
#   end
#   return peak
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "collatz-tests", "locked": true, "points": 4, "schema_version": 3, "solution": false, "task": false} language="lua"
# assert(collatz_steps(6) == 8, "collatz_steps(6) should be 8")
# assert(collatz_steps(1) == 0, "collatz_steps(1) should be 0")
# assert(collatz_peak(6) == 16, "collatz_peak(6) should be 16")
# assert(math.type(collatz_peak(6)) == "integer", "collatz_peak should return an integer")
# -- BEGIN HIDDEN TESTS
# assert(collatz_steps(27) == 111, "collatz_steps(27) should be 111")
# assert(collatz_steps(837799) == 524, "collatz_steps(837799) should be 524")
# assert(collatz_peak(1) == 1, "collatz_peak(1) should be 1")
# assert(collatz_peak(27) == 9232 and math.type(collatz_peak(27)) == "integer",
#   "collatz_peak(27) should be the integer 9232")
# assert(collatz_peak(837799) == 2974984576, "collatz_peak(837799) should be 2974984576")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 3: Counting by type (LO-2.2, 3 points)
#
# Write `count_type(name, ...)`, which returns how many of the arguments after `name` have the
# type `name`, as `type` reports it. For example, `count_type("number", 1, "a", 2)` is 2. It must
# count `nil` arguments too: `count_type("nil", 1, nil, nil)` is 2.

# %% nbgrader={"grade": false, "grade_id": "count-type", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function count_type(name, ...)
#   -- BEGIN SOLUTION
#   local count = 0
#   for i = 1, select("#", ...) do
#     if type((select(i, ...))) == name then
#       count = count + 1
#     end
#   end
#   return count
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "count-type-tests", "locked": true, "points": 3, "schema_version": 3, "solution": false, "task": false} language="lua"
# assert(count_type("number", 1, "a", 2) == 2, 'count_type("number", 1, "a", 2) should be 2')
# assert(count_type("string") == 0, "with no arguments to count, the count is 0")
# assert(count_type("nil", 1, nil, nil) == 2, 'count_type("nil", 1, nil, nil) should be 2')
# -- BEGIN HIDDEN TESTS
# assert(count_type("nil", nil) == 1, 'count_type("nil", nil) should be 1')
# assert(count_type("nil", nil, nil, nil, 4) == 3, "the nils before the last argument count")
# assert(count_type("boolean", false, true, 0, "") == 2, "false and true are both booleans")
# assert(count_type("function", print, type, 1) == 2, "functions are values too")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 4: Digit sums (LO-2.3, LO-1.2, 2 points)
#
# Write `digit_sum(n)`, which returns the sum of the decimal digits of a non-negative integer
# `n`, as an integer. It must be **recursive**: no loops. For example, `digit_sum(1234)` is 10.

# %% nbgrader={"grade": false, "grade_id": "digit-sum", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function digit_sum(n)
#   -- BEGIN SOLUTION
#   if n < 10 then
#     return n
#   end
#   return n % 10 + digit_sum(n // 10)
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "digit-sum-tests", "locked": true, "points": 2, "schema_version": 3, "solution": false, "task": false} language="lua"
# assert(digit_sum(1234) == 10, "digit_sum(1234) should be 10")
# assert(digit_sum(0) == 0, "digit_sum(0) should be 0")
# -- BEGIN HIDDEN TESTS
# assert(digit_sum(7) == 7, "digit_sum(7) should be 7")
# assert(digit_sum(1000000) == 1, "digit_sum(1000000) should be 1")
# assert(digit_sum(math.maxinteger) == 88, "digit_sum(math.maxinteger) should be 88")
# assert(math.type(digit_sum(9999999999)) == "integer", "digit_sum should return an integer")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 5: Applying a function many times (LO-2.3, 5 points)
#
# **Part A (3 points).** Write `apply_n(f, x, n)`, which applies the function `f` to `x`, `n`
# times, and returns the result: `apply_n(f, x, 3)` is `f(f(f(x)))`, and `apply_n(f, x, 0)` is
# `x`. It must be recursive, and it must work for `n` as large as 1,000,000.

# %% nbgrader={"grade": false, "grade_id": "apply-n", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function apply_n(f, x, n)
#   -- BEGIN SOLUTION
#   if n == 0 then
#     return x
#   end
#   return apply_n(f, f(x), n - 1)
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "apply-n-tests", "locked": true, "points": 3, "schema_version": 3, "solution": false, "task": false} language="lua"
# local function double(v) return v * 2 end
# assert(apply_n(double, 1, 10) == 1024, "doubling 1 ten times gives 1024")
# assert(apply_n(double, 5, 0) == 5, "applying f zero times returns x")
# -- BEGIN HIDDEN TESTS
# local function inc(v) return v + 1 end
# local ok, result = pcall(apply_n, inc, 0, 1000000)
# assert(ok, "apply_n(inc, 0, 1000000) failed: " .. tostring(result))
# assert(result == 1000000, "apply_n(inc, 0, 1000000) should be 1000000")
# assert(apply_n(function(s) return s .. "!" end, "hi", 3) == "hi!!!", "apply_n works on strings")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# **Part B (2 points).** For each of these four functions, say whether its recursive call is a
# proper tail call, and give the reason in a sentence. Write your answer in the cell below.
#
# ```lua
# local function a(n) if n == 0 then return 0 end return a(n - 1) end
# local function b(n) if n == 0 then return 0 end return 1 + b(n - 1) end
# local function c(n) if n == 0 then return 0 end return (c(n - 1)) end
# local function d(n, acc) if n == 0 then return acc end return d(n - 1, acc * 2) end
# ```

# %% [markdown] nbgrader={"grade": true, "grade_id": "tail-calls-written", "locked": false, "points": 2, "schema_version": 3, "solution": true, "task": false}
# BEGIN SOLUTION
#
# - `a`: a proper tail call. `return a(n - 1)` is `return` followed by one call, so the caller has
#   nothing left to do.
# - `b`: not a tail call. The caller adds 1 after `b(n - 1)` returns.
# - `c`: not a tail call. The parentheses keep only the first result, which the caller does after
#   `c(n - 1)` returns.
# - `d`: a proper tail call. The multiplication happens before the call, as part of computing its
#   argument, and the call itself is the whole return.
#
# Half a point each; a classification without a correct reason earns nothing.
#
# END SOLUTION

# %% [markdown]
# ## Problem 6: Prices with options (LO-2.4, LO-1.4, 3 points)
#
# Write `format_price(cents, opts)`, which formats a non-negative whole number of cents as a
# price. `opts` is an optional table of options:
#
# | Option | Meaning | Default |
# | :- | :- | :- |
# | `symbol` | the currency symbol in front of the amount, which may be `""` | `"$"` |
# | `cents` | show the cents; if `false`, round to the nearest whole unit, and round halves up | `true` |
# | `space` | put a space between the symbol and the amount | `false` |
#
# For example, `format_price(123456)` is `"$1234.56"`, `format_price(150, { cents = false })` is
# `"$2"`, and `format_price(99, { symbol = "€", space = true })` is `"€ 0.99"`.
#
# `string.format("%d.%02d", 12, 5)` gives `"12.05"`: `%02d` writes an integer with at least two
# digits, padding with a zero. Module 4 explains `string.format` in full.

# %% nbgrader={"grade": false, "grade_id": "format-price", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# function format_price(cents, opts)
#   -- BEGIN SOLUTION
#   opts = opts or {}
#   local symbol = opts.symbol or "$"
#   local show_cents = opts.cents
#   if show_cents == nil then
#     show_cents = true
#   end
#   local gap = ""
#   if opts.space then
#     gap = " "
#   end
#   if show_cents then
#     return symbol .. gap .. string.format("%d.%02d", cents // 100, cents % 100)
#   end
#   return symbol .. gap .. string.format("%d", (cents + 50) // 100)
#   -- END SOLUTION
# end

# %% nbgrader={"grade": true, "grade_id": "format-price-tests", "locked": true, "points": 3, "schema_version": 3, "solution": false, "task": false} language="lua"
# assert(format_price(123456) == "$1234.56", 'format_price(123456) should be "$1234.56"')
# assert(format_price(5) == "$0.05", 'format_price(5) should be "$0.05"')
# assert(format_price(99, { symbol = "€", space = true }) == "€ 0.99",
#   'format_price(99, { symbol = "€", space = true }) should be "€ 0.99"')
# -- BEGIN HIDDEN TESTS
# assert(format_price(150, { cents = false }) == "$2", "150 cents rounds up to $2")
# assert(format_price(149, { cents = false }) == "$1", "149 cents rounds down to $1")
# assert(format_price(1000, { symbol = "" }) == "10.00", "an empty symbol is allowed")
# assert(format_price(0) == "$0.00", 'format_price(0) should be "$0.00"')
# assert(format_price(250, { cents = true }) == "$2.50", "cents = true shows the cents")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Problem 7: A bug report (LO-1.1, 2 points)
#
# `percent_draft(part, whole)` should return `part` as a percentage of `whole`, rounded to the
# nearest whole number, as an integer: `percent_draft(1, 3)` should be 33. Run the next cell. It
# raises an error, on purpose; don't change it.

# %% nbgrader={"grade": false, "grade_id": "percent-draft", "locked": true, "schema_version": 3, "solution": false, "task": false} tags=["raises-exception"] language="lua"
# function percent_draft(part, whole)
#   local ratio = part / whole
#   return math.floor(ratoi * 100 + 0.5)
# end
# print(percent_draft(1, 3))

# %% [markdown]
# In the cell below, do two things:
#
# 1. Set the global `error_line` to the line number the error message names, as an integer, and
#    `error_variable` to the name of the variable it names, as a string.
# 2. Define `percent(part, whole)`: a corrected copy of `percent_draft`.

# %% nbgrader={"grade": false, "grade_id": "percent", "locked": false, "schema_version": 3, "solution": true, "task": false} language="lua"
# -- BEGIN SOLUTION
# error_line = 3
# error_variable = "ratoi"
#
# function percent(part, whole)
#   local ratio = part / whole
#   return math.floor(ratio * 100 + 0.5)
# end
# -- END SOLUTION

# %% nbgrader={"grade": true, "grade_id": "percent-tests", "locked": true, "points": 2, "schema_version": 3, "solution": false, "task": false} language="lua"
# assert(math.type(error_line) == "integer", "error_line should be an integer")
# assert(type(error_variable) == "string", "error_variable should be a string")
# assert(percent(1, 3) == 33, "percent(1, 3) should be 33")
# assert(math.type(percent(1, 3)) == "integer", "percent should return an integer")
# -- BEGIN HIDDEN TESTS
# assert(error_line == 3, "the message names line 3 of the cell")
# assert(error_variable == "ratoi", "the message names the global 'ratoi'")
# assert(percent(2, 3) == 67, "percent(2, 3) should be 67")
# assert(percent(1, 8) == 13, "12.5 rounds up to 13")
# assert(percent(5, 5) == 100, "percent(5, 5) should be 100")
# -- END HIDDEN TESTS
# print("passed")

# %% [markdown]
# ## Tools you used
#
# Say which tools, if any, you used for this assignment and how, or write "none".
#
# *Your answer here.*
