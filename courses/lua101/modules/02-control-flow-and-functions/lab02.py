# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: tags,-all
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
# # Lab 2: Control flow and functions
#
# **Objectives:** LO-2.1, LO-2.2, LO-2.3, LO-2.4\
# **Prerequisites:** the [Module 2 reading](index.md) and [Lab 1](../01-first-steps/lab01.ipynb)\
# **Time:** about 2 hours
#
# You will predict how many times loops run, predict how many values calls give, write a
# variadic function, find the stack's limit by experiment and then step around it with a tail
# call, and fix a function whose defaults don't work. As in Lab 1, each exercise ends with a check
# cell that prints `passed` or fails with a message, and the checks fail until you finish their
# exercise.

# %% [markdown]
# ## Setup
#
# Nothing in this lab is random. The second cell prints the Lua version, which should be
# `Lua 5.4`.

# %%
# %load_ext lualab
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. How many times does a loop run?
#
# Each row below is the header of a numeric `for`, written as the part after `for i =`. Predict how
# many passes each loop makes, and replace its `"?"` with the number. Make all ten predictions
# before you run anything. The rules you need are the four in the reading's section on the
# numeric `for`.

# %% tags=["answer-L2.1"] language="lua"
# loop_predictions = {
#   { "1, 10, 3",    "?" },
#   { "10, 1",       "?" },
#   { "1, 3.5",      "?" },
#   { "5, 1, -2",    "?" },
#   { "0, 1, 0.25",  "?" },
#   { "0, 0.3, 0.1", "?" },
#   { "1, 1",        "?" },
#   { "-3, 3, 3",    "?" },
#   { "1, 0, -1",    "?" },
#   { "2, 8, 2.5",   "?" },
# }

# %% [markdown]
# ### Exercise L2.1 (LO-2.1, ★★, about 15 minutes)
#
# Run the check. It runs each loop, prints the values the control variable took, and compares the
# count with your prediction. For each mismatch, work out which rule you missed, correct the
# prediction, and run both cells again.

# %% tags=["raises-exception"] language="lua"
# local wrong, unanswered = 0, 0
# for n, row in ipairs(loop_predictions) do
#   local header, predicted = row[1], row[2]
#   local run = load("local seen = {} for i = " .. header .. " do seen[#seen + 1] = i end return seen",
#     "=loop", "t")
#   local seen = run()
#   local shown = {}
#   for k, v in ipairs(seen) do shown[k] = tostring(v) end
#   local verdict = "match"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= #seen then
#     wrong, verdict = wrong + 1, "MISMATCH"
#   end
#   print(string.format("%2d  for i = %-12s you: %-4s Lua: %-3d  i = %s   %s",
#     n, header, tostring(predicted), #seen, table.concat(shown, ", "), verdict))
# end
# assert(unanswered == 0, unanswered .. " loops still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# Look at row 6. Its last `i` prints as `0.2`, but the loop stopped before a fourth pass because
# the next value would have been 0.30000000000000004, just over the bound. Change the bound in
# the next cell to `0.30000000000000004` and run it: the fourth pass appears.

# %% language="lua"
# for i = 0, 0.3, 0.1 do
#   print(string.format("%.17g", i))
# end

# %% [markdown]
# ## 2. How many values does a call give?
#
# With the two functions in the next cell, predict the value of each expression in the cell after
# it: `select("#", ...)` counts its arguments, and `#` counts a table's items. Replace each
# `"?"`, then run the check.

# %% language="lua"
# function two() return 1, 2 end
# function none() end

# %% tags=["answer-L2.2"] language="lua"
# count_predictions = {
#   { 'select("#", two())',         "?" },
#   { 'select("#", two(), two())',  "?" },
#   { 'select("#", (two()))',       "?" },
#   { 'select("#", none())',        "?" },
#   { 'select("#", none(), none())', "?" },
#   { '#{ two(), two() }',          "?" },
#   { 'select("#", nil, nil)',      "?" },
#   { 'select("#", two(), nil)',    "?" },
# }

# %% [markdown]
# ### Exercise L2.2 (LO-2.2, ★★, about 15 minutes)
#
# Run the check, and correct each mismatch by applying the adjustment rule: a call gives all its
# results only when it is the last item in a list.

# %% tags=["raises-exception"] language="lua"
# local wrong, unanswered = 0, 0
# for n, row in ipairs(count_predictions) do
#   local expression, predicted = row[1], row[2]
#   local actual = load("return " .. expression, "=expression", "t")()
#   local verdict = "match"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= actual then
#     wrong, verdict = wrong + 1, "MISMATCH"
#   end
#   print(string.format("%d  %-30s you: %-4s Lua: %d   %s",
#     n, expression, tostring(predicted), actual, verdict))
# end
# assert(unanswered == 0, unanswered .. " expressions still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# ### Exercise L2.3 (LO-2.2, ★★, about 20 minutes)
#
# Write a global function `stats(...)` that takes any number of numbers and returns four values:
# how many there are, the smallest, the largest, and their mean. Called with no arguments, it
# returns the single value `0`. Use `select("#", ...)` to count, so that the function would
# notice a `nil` among its arguments instead of stopping early.
#
# <details>
# <summary>Hint</summary>
#
# Start `smallest` and `largest` at the first argument, `(select(1, ...))`, then loop from 2. The
# mean of integers should be a float, which `/` gives you.
# </details>

# %% tags=["answer-L2.3"] language="lua"
# function stats(...)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local n, lo, hi, mean = stats(3, 1, 2)
# assert(n == 3 and lo == 1 and hi == 3, "stats(3, 1, 2) should give 3, 1, 3, ...")
# assert(mean == 2.0 and math.type(mean) == "float", "the mean of 3, 1, 2 should be the float 2.0")
# assert(select("#", stats(7)) == 4, "stats(7) should return four values")
# assert(select(4, stats(7)) == 7.0, "the mean of one number is that number, as a float")
# assert(select("#", stats()) == 1 and stats() == 0, "stats() should return the single value 0")
# local _, lo2, hi2 = stats(-5, 10, 2.5, -7)
# assert(lo2 == -7 and hi2 == 10, "stats(-5, 10, 2.5, -7) should find -7 and 10")
# print("passed")

# %% [markdown]
# ## 3. The stack's limit, and the way around it
#
# `depth(n)` recurses `n` levels deep without a tail call. The next cell finds the largest `n`
# for which it succeeds, by binary search with `pcall`, which calls a function and returns
# `false` instead of stopping when it raises an error (module 6 covers it). It takes about a
# second. Predict the order of magnitude before you run it: a thousand, a million, or more?

# %% language="lua"
# local function depth(n)
#   if n == 0 then return 0 end
#   return 1 + depth(n - 1)
# end
#
# local lo, hi = 1, 10000000
# while lo < hi do
#   local mid = (lo + hi + 1) // 2
#   if pcall(depth, mid) then lo = mid else hi = mid - 1 end
# end
# print("deepest depth(n) that worked:", lo)
# print("one more level:", select(2, pcall(depth, lo + 1)))

# %% [markdown]
# Now change `depth` to use more stack per call: add the line
# `local a, b, c, d, e, f = n, n, n, n, n, n` before its `if`, and run the cell again. Each frame
# is bigger, so the same million slots hold fewer frames. Then remove the line again.
#
# ### Exercise L2.4 (LO-2.3, ★★, about 20 minutes)
#
# `sum_to(n)` adds the integers from 1 to `n`, but it recurses without a tail call, so
# `sum_to(1000000)` overflows the stack. Rewrite it as a proper tail call with an accumulator
# parameter, so that `sum_to(n)` still works when called with one argument. Keep it recursive:
# the check calls it a million levels deep.
#
# <details>
# <summary>Hint</summary>
#
# Give it a second parameter, `acc`, that defaults to 0, and make the recursive call the whole
# of a `return` statement.
# </details>

# %% tags=["answer-L2.4"] language="lua"
# function sum_to(n)
#   if n == 0 then return 0 end
#   return n + sum_to(n - 1)
# end

# %% tags=["raises-exception"] language="lua"
# assert(sum_to(0) == 0, "sum_to(0) should be 0")
# assert(sum_to(10) == 55, "sum_to(10) should be 55")
# local ok, result = pcall(sum_to, 1000000)
# assert(ok, "sum_to(1000000) failed: " .. tostring(result))
# assert(result == 500000500000, "sum_to(1000000) should be 500000500000")
# print("passed")

# %% [markdown]
# ## 4. Options with defaults
#
# `make_label` builds a label from a table of options: `text` (default `""`), `upper`, which
# capitalizes the text (default `false`), and `border`, which wraps it in brackets (default
# `true`). Run the cell, and compare the third line with what its call asked for.

# %% tags=["answer-L2.5"] language="lua"
# function make_label(opts)
#   opts = opts or {}
#   local text = opts.text or ""
#   local upper = opts.upper or false
#   local border = opts.border or true
#   if upper then text = text:upper() end
#   if border then text = "[" .. text .. "]" end
#   return text
# end
#
# print(make_label{ text = "total" })
# print(make_label{ text = "total", upper = true })
# print(make_label{ text = "total", border = false })

# %% [markdown]
# ### Exercise L2.5 (LO-2.4, ★★, about 15 minutes)
#
# Fix `make_label` so that every option's default works, including `border = false`. Change only
# the defaults that are wrong. Then, in the Markdown cell after the check, say in one sentence
# why `opts.upper or false` was harmless while `opts.border or true` was not.

# %% tags=["raises-exception"] language="lua"
# assert(make_label{ text = "total" } == "[total]", "the default border is on")
# assert(make_label{ text = "total", border = false } == "total", "border = false turns it off")
# assert(make_label{ text = "total", upper = true } == "[TOTAL]", "upper = true capitalizes")
# assert(make_label() == "[]", "make_label() uses every default")
# print("passed")

# %% [markdown] tags=["answer-L2.5-why"]
# *Your sentence here: why was `opts.upper or false` harmless?*

# %% [markdown]
# ## Summary
#
# - The numeric `for` fixes its count before the first pass; a float step can stop one pass
#   short, or not, depending on rounding.
# - A call gives all its results only as the last item in a list, and `select("#", ...)` counts
#   values, `nil` included.
# - Recursion without a tail call ran out of stack just under 500,000 levels for a small function,
#   and sooner for larger frames; a proper tail call has no limit.
# - `x or default` is wrong for options whose valid values include `false`; test for `nil`.
#
# Next, do the [Module 2 practice](practice.md), then start PA1.
