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
# # Lab 1: First steps
#
# **Objectives:** LO-1.1, LO-1.2, LO-1.3, LO-1.4\
# **Prerequisites:** the [Module 1 reading](index.md)\
# **Time:** about 2 hours
#
# In this lab you run Lua in notebook cells and from a script file, read the errors Lua reports,
# predict the values of 20 expressions before Lua shows you, and fix the two bugs that a missing
# `local` causes. Each exercise ends with a check cell. Run it after your answer: it prints
# `passed` or fails with a message that says what is wrong.
#
# Run the cells in order, from the top. If you change an earlier cell, run it again before the
# cells after it. Some cells fail on purpose until you finish their exercise: the cell that runs
# the buggy script, and each check.

# %% [markdown]
# ## Setup
#
# The first cell loads `lualab`, which adds the `%%lua` cell magic, and prints the versions this
# lab was written for. Nothing in this lab is random, so it sets no random seed. The second cell
# is your first Lua: it prints the version of Lua the cells run, which should be `Lua 5.4`.

# %%
# %load_ext lualab
import contextlib
import io
import os
import sys

import lualab
import lupa

os.makedirs("scratch", exist_ok=True)  # the lab writes its script files here
print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. Running Lua and reading its errors
#
# Every `%%lua` cell is one chunk, like a line typed at the interactive interpreter. Global
# variables last from cell to cell; local variables end with their cell. Run the next two cells.
# Before you run the second, predict what it prints.

# %% language="lua"
# local secret = "only in this cell"
# shared = "in every later cell"
# print(secret, shared)

# %% language="lua"
# print(secret, shared)

# %% [markdown]
# `secret` was local to the first cell, so in the second it is an undeclared global, which reads
# as `nil`.
#
# ### A script with a bug
#
# The next cell writes `average.lua`, the script from the reading, into the lab's `scratch`
# folder. The cell after it runs the script with `dofile`, which runs a file as a chunk, exactly
# as `lua scratch/average.lua` would in a terminal. Run both, and read the error.

# %% tags=["answer-L1.1"]
# %%writefile scratch/average.lua
-- average.lua: prints the average of three scores.
local total = 0
local count = 0

local function add(score)
  total = total + score
  count = count + 1
end

add(90)
add(72)
add(81)
print("average:", totl / count)

# %% tags=["raises-exception"] language="lua"
# dofile("scratch/average.lua")

# %% [markdown]
# ### Exercise L1.1 (LO-1.1, ★, about 10 minutes)
#
# Use the error message to find the bug. Fix it in the `%%writefile` cell above, then run that
# cell, the `dofile` cell, and the check below. The script should print `average:` followed by
# `81.0`.
#
# Then try the other two ways of running Lua, in a terminal from the repository's root, after
# `source .venv/lua/bin/activate` (see [setting up](../../setup.md)):
#
# 1. Run `lua courses/lua101/modules/01-first-steps/scratch/average.lua`, and compare its output
#    with the cell's.
# 2. Run `lua -i`, type `7 // 2` and then `7 / 2`, and press Ctrl+D to leave.
#
# <details>
# <summary>Hint</summary>
#
# The message names the line and the variable. Which name on that line was never assigned?
# </details>

# %% tags=["raises-exception"]
output = io.StringIO()
with contextlib.redirect_stdout(output):
    lualab.run('dofile("scratch/average.lua")')
assert output.getvalue() == "average:\t81.0\n", (
    f"the script printed {output.getvalue()!r}; expected 'average:', a tab, and '81.0'"
)
print("passed")

# %% [markdown]
# ## 2. Predict, then run
#
# This section is the lab's center. Each line of the table below holds an expression from the
# reading's rules, as a string, and your prediction of its value. Replace each `"?"` with the
# value you predict, written as Lua: `3`, `3.0`, `"105"`, `true`, `nil`, or `math.huge`. Write
# `"error"` if you predict that the expression raises an error.
#
# Write all 20 predictions before you run the cell, without running any of the expressions.
# Then run the cell and the check after it, which compares each prediction with what Lua does.
# The subtype counts: `3` and `3.0` are different predictions.

# %% tags=["answer-L1.2"] language="lua"
# predictions = {
#   { "7 // 2",                            "?" },
#   { "7 / 2",                             "?" },
#   { "6 / 2",                             "?" },
#   { "-7 // 2",                           "?" },
#   { "-7 % 3",                            "?" },
#   { "7 % -3",                            "?" },
#   { "2 ^ 3",                             "?" },
#   { "3 + 4.0",                           "?" },
#   { "\"10\" + 5",                        "?" },
#   { "\"10\" .. 5",                       "?" },
#   { "\"10\" == 10",                      "?" },
#   { "#\"hello\"",                        "?" },
#   { "10 // 0",                           "?" },
#   { "10 / 0",                            "?" },
#   { "math.maxinteger + 1 == math.mininteger", "?" },
#   { "nil or \"default\"",                "?" },
#   { "0 and \"zero\"",                    "?" },
#   { "false and nil",                     "?" },
#   { "not nil",                           "?" },
#   { "1 == 1.0",                          "?" },
# }

# %% [markdown]
# ### Exercise L1.2 (LO-1.2, LO-1.4, ★★, about 25 minutes)
#
# Run the check. It prints one line for each expression: what you predicted, what Lua gives, and
# whether they match. For each mismatch, find the rule in the reading that explains Lua's answer,
# then correct your prediction above and run both cells again. The check passes when all 20
# match.

# %% tags=["raises-exception"] language="lua"
# local function describe(v)
#   if type(v) == "number" then
#     return string.format("%s (%s)", tostring(v), math.type(v))
#   elseif type(v) == "string" then
#     return string.format("%q", v)
#   end
#   return tostring(v)
# end
#
# local function same(a, b)
#   if type(a) ~= type(b) then return false end
#   if type(a) == "number" and math.type(a) ~= math.type(b) then return false end
#   return a == b
# end
#
# local wrong, unanswered = 0, 0
# for i, row in ipairs(predictions) do
#   local expression, predicted = row[1], row[2]
#   local ok, actual = pcall(load("return " .. expression, "=expression", "t"))
#   if not ok then actual = "error" end
#   local verdict
#   if predicted == "?" then
#     unanswered = unanswered + 1
#     verdict = "no prediction yet"
#   elseif same(predicted, actual) then
#     verdict = "match"
#   else
#     wrong = wrong + 1
#     verdict = "MISMATCH"
#   end
#   print(string.format("%2d  %-40s you: %-16s Lua: %-16s %s",
#     i, expression, describe(predicted), describe(actual), verdict))
# end
# assert(unanswered == 0, unanswered .. " expressions still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# ### Floor division, shown as a table
#
# Floor division rounds down, toward minus infinity. Many other languages truncate toward zero
# instead. The next cell prints both for `x // 3`, with `x % 3`, for `x` from -6 to 6. Read down
# the columns: where do `floor` and `truncate` differ, and what does `x % 3` do at the same rows?
# Change `divisor` to `-3` and run the cell again.

# %% language="lua"
# local divisor = 3
#
# local function truncate(a, b)  -- integer division that rounds toward zero, as in C
#   local q = a // b
#   if q < 0 and q * b ~= a then q = q + 1 end
#   return q
# end
#
# print(string.format("%4s  %8s  %8s  %6s", "x", "floor", "truncate", "x % d"))
# for x = -6, 6 do
#   local marker = (x // divisor ~= truncate(x, divisor)) and "  <- differ" or ""
#   print(string.format("%4d  %8d  %8d  %6d%s",
#     x, x // divisor, truncate(x, divisor), x % divisor, marker))
# end

# %% [markdown]
# The two divisions differ only when the exact quotient is negative and not a whole number. On
# exactly those rows, `x % divisor` is not zero and has the divisor's sign, so that
# `x == (x // divisor) * divisor + x % divisor` holds on every row.
#
# ### Floats that print the same but aren't equal
#
# Run the cell. Then change `b` to `0.25` and run it again: why are those two sums equal when the
# first two weren't? (0.25 is a sum of powers of two, which a float stores exactly.)

# %% language="lua"
# local a = 0.1 + 0.2
# local b = 0.3
# print("print shows:", a, b)
# print("all digits: ", string.format("%.17g  %.17g", a, b))
# print("a == b:     ", a == b)
# print("close:      ", math.abs(a - b) < 1e-9)

# %% [markdown]
# ## 3. The bug a missing `local` causes
#
# This is the reading's `count_words`, with the bug. The program keeps a count of its own in
# the global `n`, which should still be 100 after `count_words` runs. Here `count_words` is
# itself global, unlike in the reading, so that the check cell, a separate chunk, can call it.
# Run the cell.

# %% tags=["answer-L1.3"] language="lua"
# function count_words(text)
#   n = 0
#   for _ in text:gmatch("%S+") do
#     n = n + 1
#   end
#   return n
# end
#
# n = 100
# print("words:", count_words("one two three"))
# print("n:", n)

# %% [markdown]
# ### Exercise L1.3 (LO-1.3, ★, about 10 minutes)
#
# Fix `count_words` so that it no longer changes the global `n`, and run the cell again. Then run
# the check, which resets `n` to 100 first. In one sentence, say in the Markdown cell below the
# check why the function's own result was right even with the bug.

# %% tags=["raises-exception"] language="lua"
# n = 100
# assert(count_words("one two three") == 3, "count_words should return 3 for three words")
# assert(count_words("") == 0, "count_words should return 0 for an empty string")
# assert(n == 100, "count_words still changes the global n (now " .. tostring(n) .. ")")
# print("passed")

# %% [markdown] tags=["answer-L1.3-why"]
# *Your sentence here: why was `count_words`'s result right even with the bug?*

# %% [markdown]
# ## 4. Truthiness and the `and`–`or` trap
#
# `cond and a or b` reads like C's `cond ? a : b`, but returns `b` whenever `a` is falsy. Predict
# the three lines this cell prints, then run it.

# %% language="lua"
# print(true and "yes" or "no")
# print(false and "yes" or "no")
# print(true and false or "no")

# %% [markdown]
# The third line prints `no`, although the condition is `true`: `true and false` is `false`, so
# the `or` picks its right-hand side.
#
# ### Exercise L1.4 (LO-1.4, ★★, about 15 minutes)
#
# Write a global function `choose(cond, a, b)` that returns `a` when `cond` is truthy and `b`
# otherwise, and that is right even when `a` is `false` or `nil`. Use an `if` statement. The
# check tries the cases where the `and`–`or` idiom fails.

# %% tags=["answer-L1.4"] language="lua"
# function choose(cond, a, b)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# assert(choose(true, "a", "b") == "a", "choose(true, 'a', 'b') should be 'a'")
# assert(choose(nil, "a", "b") == "b", "choose(nil, 'a', 'b') should be 'b'")
# assert(choose(0, "zero", "none") == "zero", "0 is truthy, so choose(0, ...) picks a")
# assert(choose("", 1, 2) == 1, "'' is truthy, so choose('', 1, 2) picks 1")
# assert(choose(true, false, "b") == false, "choose(true, false, 'b') should be false, not 'b'")
# assert(choose(true, nil, "b") == nil, "choose(true, nil, 'b') should be nil, not 'b'")
# print("passed")

# %% [markdown]
# ## Summary
#
# - A `%%lua` cell, a line at the `lua -i` prompt, and a file run by `lua` or `dofile` are each a
#   chunk. Globals outlive the chunk; locals don't.
# - An error message names the chunk, the line, and what went wrong; for a `nil`, it names the
#   variable that held it.
# - `/` and `^` give floats, `//` rounds down, `%` takes the divisor's sign, and the two always
#   satisfy `a == (a // b) * b + a % b`.
# - `print` rounds floats to 14 significant digits, so compare floats with a tolerance.
# - Only `nil` and `false` are falsy, and `cond and a or b` fails when `a` is falsy.
# - A missing `local` passes the function's own tests and breaks code elsewhere.
#
# Next, do the [Module 1 practice](practice.md). PA1 starts in week 2, after Module 2.
