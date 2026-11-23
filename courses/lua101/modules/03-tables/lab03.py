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
# # Lab 3: Tables
#
# **Objectives:** LO-3.1, LO-3.2, LO-3.3, LO-3.4\
# **Prerequisites:** the [Module 3 reading](index.md) and
# [Lab 2](../02-control-flow-and-functions/lab02.ipynb)\
# **Time:** about 2 hours
#
# You will watch the length operator as holes appear in a table, predict the borders of ten
# tables, write a sorted report from a record, predict what aliased tables do, finish a deep copy,
# measure the cost of `table.remove(t, 1)` and build a queue that avoids it, and fix a matrix
# whose rows are all one table. As in the earlier labs, each exercise ends with a check cell that
# prints `passed` or fails with a message, and the checks fail until you finish their exercise.

# %% [markdown]
# ## Setup
#
# Nothing in this lab is random. Section 4 measures time, so its numbers depend on your machine.
# The second cell prints the Lua version, which should be `Lua 5.4`.

# %%
# %load_ext lualab
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. The length operator and borders
#
# A border of `t` is an index whose value is present and whose next index is absent, or 0 when
# `t[1]` is absent. The next cell defines `borders(t)`, which finds every border by trying each
# index from 0 to the largest integer key. It is slow on purpose: it shows what `#` is allowed to
# return, not how Lua computes it.

# %% language="lua"
# function borders(t)
#   local largest = 0
#   for k in pairs(t) do
#     if math.type(k) == "integer" and k > largest then largest = k end
#   end
#   local found = {}
#   for b = 0, largest do
#     if (b == 0 or t[b] ~= nil) and t[b + 1] == nil then found[#found + 1] = b end
#   end
#   return found
# end
#
# function show(label, t)
#   print(string.format("%-16s #t = %d   borders: %s", label, #t, table.concat(borders(t), ", ")))
# end

# %% [markdown]
# Run the next cell, which removes items from a sequence of eight. After each step, `#t` is one of
# the borders, but once there is more than one border, nothing says which. Then add a line of your
# own, such as `t[9] = 90; show("t[9] = 90", t)`, predict both columns, and run the cell again.

# %% language="lua"
# local t = { 10, 20, 30, 40, 50, 60, 70, 80 }
# show("start", t)
# t[8] = nil; show("t[8] = nil", t)
# t[4] = nil; show("t[4] = nil", t)
# t[1] = nil; show("t[1] = nil", t)

# %% [markdown]
# The reading built two tables with the same keys and values in two different ways. Here they
# are again, with their borders:

# %% language="lua"
# local a = { 1, nil, 3 }
# local b = {}
# b[1] = 1
# b[3] = 3
# show("constructor", a)
# show("assignments", b)

# %% [markdown]
# ### Exercise L3.1 (LO-3.2, ★★, about 20 minutes)
#
# For each table, predict its borders and replace the `"?"` with them as a list in increasing
# order, such as `{ 3 }` or `{ 1, 3 }`. A table with exactly one border is a sequence. Make all
# ten predictions before you run the check, which also prints `#t` for each table.
#
# <details>
# <summary>Hint</summary>
#
# Write out which of the indices 1, 2, 3, … hold a value. Keys that aren't positive integers,
# such as `"x"` or 0, never affect the borders, and a float key with an integer value is that
# integer.
# </details>

# %% tags=["answer-L3.1"] language="lua"
# border_predictions = {
#   { '{ 10, 20, 30 }',                    "?" },
#   { '{}',                                "?" },
#   { '{ 10, nil, 30 }',                   "?" },
#   { '{ nil, 20 }',                       "?" },
#   { '{ x = 1, y = 2 }',                  "?" },
#   { '{ [0] = "zero", "one", "two" }',    "?" },
#   { '{ 10, 20, nil }',                   "?" },
#   { '{ n = 3, 10, 20, 30 }',             "?" },
#   { '{ [1] = "a", [2] = "b", [4] = "d" }', "?" },
#   { '{ [2.0] = "b", [1] = "a" }',        "?" },
# }

# %% tags=["raises-exception"] language="lua"
# local wrong, unanswered = 0, 0
# for n, row in ipairs(border_predictions) do
#   local constructor, predicted = row[1], row[2]
#   local t = load("return " .. constructor, "=table", "t")()
#   local actual = borders(t)
#   local verdict, shown = "match", "?"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   else
#     shown = "{" .. table.concat(predicted, ",") .. "}"
#     local same = #predicted == #actual
#     for i = 1, #actual do same = same and predicted[i] == actual[i] end
#     if not same then wrong, verdict = wrong + 1, "MISMATCH" end
#   end
#   print(string.format("%2d  %-38s you: %-7s borders: %-7s #t = %d   %s", n, constructor, shown,
#     "{" .. table.concat(actual, ",") .. "}", #t, verdict))
# end
# assert(unanswered == 0, unanswered .. " tables still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# ## 2. Walking a record in order
#
# `pairs` visits a table's keys in no particular order, and the order can change between runs.
# Run the next cell a few times after restarting the kernel (**Kernel**, then **Restart Kernel**,
# then rerun the setup cells) and compare the orders.

# %% language="lua"
# inventory = { pears = 4, apples = 3, figs = 0, kiwis = 12, plums = 7 }
# for name, count in pairs(inventory) do io.write(name, "=", count, " ") end
# print()

# %% [markdown]
# ### Exercise L3.2 (LO-3.1, ★★, about 20 minutes)
#
# Write `report(stock)`, which takes a record like `inventory` and returns one string: a line
# `name: count` for each item whose count isn't 0, in alphabetical order, joined by newlines
# (`"\n"`), with no newline at the end. For `inventory` it returns the five lines below, less the
# figs. It must not change `stock`.
#
# ```text
# apples: 3
# kiwis: 12
# pears: 4
# plums: 7
# ```
#
# <details>
# <summary>Hint</summary>
#
# Collect the names with `pairs`, `table.sort` them, then build a list of lines and join it with
# `table.concat(lines, "\n")`.
# </details>

# %% tags=["answer-L3.2"] language="lua"
# function report(stock)
#   -- your code here
# end
#
# print(report(inventory))

# %% tags=["raises-exception"] language="lua"
# assert(report(inventory) == "apples: 3\nkiwis: 12\npears: 4\nplums: 7",
#   "report(inventory) should list apples, kiwis, pears, and plums, one per line, in that order")
# assert(inventory.figs == 0, "report must not change its argument")
# assert(report({ zucchini = 1, apple = 2 }) == "apple: 2\nzucchini: 1", "sort the names")
# assert(report({}) == "", "an empty record gives an empty string")
# assert(report({ melon = 0 }) == "", "items whose count is 0 are left out")
# print("passed")

# %% [markdown]
# ## 3. References and copies
#
# `aliasing_story` runs a short program and hands back its tables, so that the check can look at
# them afterward. Read it, but don't run anything yet.

# %% language="lua"
# function aliasing_story()
#   local a = { 1, 2, 3 }
#   local b = a
#   local c = { 1, 2, 3 }
#   b[1] = 10
#
#   local nested = { inner = { 5 } }
#   local shallow = {}
#   for k, v in pairs(nested) do shallow[k] = v end
#   shallow.inner[1] = 50
#
#   local function grow(list) list[#list + 1] = 99 end
#   local function replace(list) list = { 0 } end
#   grow(c)
#   replace(c)
#
#   return { a = a, b = b, c = c, nested = nested, shallow = shallow }
# end

# %% [markdown]
# ### Exercise L3.3 (LO-3.3, ★★, about 15 minutes)
#
# Predict the value of each expression at the end of `aliasing_story`: a number, `true`, or
# `false`. Replace each `"?"`, then run the check.

# %% tags=["answer-L3.3"] language="lua"
# alias_predictions = {
#   { "a[1]",                          "?" },
#   { "a == b",                        "?" },
#   { "a == c",                        "?" },
#   { "#c",                            "?" },
#   { "c[1]",                          "?" },
#   { "nested.inner[1]",               "?" },
#   { "shallow == nested",             "?" },
#   { "shallow.inner == nested.inner", "?" },
# }

# %% tags=["raises-exception"] language="lua"
# local story = aliasing_story()
# local wrong, unanswered = 0, 0
# for n, row in ipairs(alias_predictions) do
#   local expression, predicted = row[1], row[2]
#   local actual = load("return " .. expression, "=expression", "t", story)()
#   local verdict = "match"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= actual then
#     wrong, verdict = wrong + 1, "MISMATCH"
#   end
#   print(string.format("%d  %-30s you: %-6s Lua: %-6s %s",
#     n, expression, tostring(predicted), tostring(actual), verdict))
# end
# assert(unanswered == 0, unanswered .. " expressions still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# ### Exercise L3.4 (LO-3.3, ★★★, about 25 minutes)
#
# This `deep_copy` is the reading's first version. It fails on a table that contains itself, and
# it turns one table that appears twice into two. Give it a second parameter, `seen`, that maps
# each original table to its copy, so that both cases work. `deep_copy(t)` must still work when
# called with one argument.
#
# <details>
# <summary>Hint 1</summary>
#
# Create `seen` on the first call with `seen = seen or {}`, and pass it to every recursive call.
# </details>
#
# <details>
# <summary>Hint 2</summary>
#
# Store the new copy in `seen[value]` before the loop that fills it. A table that contains itself
# then finds its own copy in `seen` when the loop reaches it.
# </details>

# %% tags=["answer-L3.4"] language="lua"
# function deep_copy(value)
#   if type(value) ~= "table" then return value end
#   local copy = {}
#   for k, v in pairs(value) do
#     copy[deep_copy(k)] = deep_copy(v)
#   end
#   return copy
# end

# %% tags=["raises-exception"] language="lua"
# local original = { name = "plan", steps = { "draft", "review" }, n = 2 }
# local copy = deep_copy(original)
# assert(copy ~= original and copy.steps ~= original.steps, "the copy's tables must be new tables")
# copy.steps[1] = "outline"
# assert(original.steps[1] == "draft", "changing the copy changed the original")
# assert(copy.name == "plan" and copy.n == 2 and copy.steps[2] == "review",
#   "the copy must hold the same values")
# assert(deep_copy(42) == 42 and deep_copy("x") == "x", "a value that isn't a table is returned as is")
#
# local key = { "key" }
# local copied_key = next(deep_copy({ [key] = "value" }))
# assert(copied_key ~= key and copied_key[1] == "key", "keys that are tables must be copied too")
#
# local shared = { 1 }
# local twice = deep_copy({ first = shared, second = shared })
# assert(twice.first == twice.second, "a table that appears twice must be one table in the copy")
# assert(twice.first ~= shared, "...and a new table, not the original")
#
# local loop = { label = "loop" }
# loop.self = loop
# local ok, result = pcall(deep_copy, loop)
# assert(ok, "deep_copy of a table that contains itself failed: " .. tostring(result))
# assert(result ~= loop and result.self == result, "the copy must contain itself, not the original")
# print("passed")

# %% [markdown]
# ## 4. What a queue costs
#
# The next cell empties lists of 2,500 to 20,000 items with `table.remove(t, 1)`, and prints how
# long each took and how many times longer than the row above. Before you run it, predict that
# ratio: when the list doubles, does the time double, or grow by more? The cell takes about
# 3 seconds.

# %% language="lua"
# local function drain_from_front(n)
#   local t = {}
#   for i = 1, n do t[i] = i end
#   local start = os.clock()
#   while #t > 0 do table.remove(t, 1) end
#   return os.clock() - start
# end
#
# print("     n   seconds   ratio")
# local previous
# for _, n in ipairs({ 2500, 5000, 10000, 20000 }) do
#   local seconds = drain_from_front(n)
#   local ratio = previous and string.format("%.1f", seconds / previous) or ""
#   print(string.format("%6d   %7.4f   %s", n, seconds, ratio))
#   previous = seconds
# end

# %% [markdown]
# Each doubling multiplies the time by about four, because each removal moves every remaining
# item: emptying *n* items moves about $n^2/2$ of them, which is $O(n^2)$.
#
# ### Exercise L3.5 (LO-3.4, ★★, about 20 minutes)
#
# Write a queue whose push and pop are both $O(1)$, as four global functions:
#
# - `queue_new()` returns a new, empty queue;
# - `queue_push(q, value)` adds `value` at the back;
# - `queue_pop(q)` removes and returns the value at the front, or returns `nil` when `q` is empty;
# - `queue_size(q)` returns the number of values in `q`.
#
# Any value except `nil` can be queued, `false` included. The check times 20,000 pushes and pops,
# and fails if they take 0.25 s or more, which a queue that moves its items on every pop does.
#
# <details>
# <summary>Hint</summary>
#
# Keep two indices, `first` and `last`, in the queue's table, next to a table of items. When you
# pop, set the popped slot to `nil` so the queue doesn't keep a reference to it.
# </details>

# %% tags=["answer-L3.5"] language="lua"
# function queue_new()
#   -- your code here
# end
#
# function queue_push(q, value)
#   -- your code here
# end
#
# function queue_pop(q)
#   -- your code here
# end
#
# function queue_size(q)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local q = queue_new()
# assert(queue_size(q) == 0 and queue_pop(q) == nil, "a new queue is empty, and popping it gives nil")
# queue_push(q, "a"); queue_push(q, "b"); queue_push(q, "c")
# assert(queue_size(q) == 3, "three pushes should give three values")
# assert(queue_pop(q) == "a" and queue_pop(q) == "b", "values come out in the order they went in")
# queue_push(q, "d")
# assert(queue_pop(q) == "c" and queue_pop(q) == "d", "...also after more pushes")
# assert(queue_pop(q) == nil and queue_size(q) == 0, "the queue should be empty again")
# queue_push(q, false)
# assert(queue_size(q) == 1 and queue_pop(q) == false, "false is a value like any other")
#
# local n = 20000
# local start = os.clock()
# for i = 1, n do queue_push(q, i) end
# for i = 1, n do assert(queue_pop(q) == i, "value " .. i .. " came out of order") end
# local seconds = os.clock() - start
# print(string.format("%d pushes and pops took %.4f s", n, seconds))
# assert(seconds < 0.25, "20,000 pushes and pops took 0.25 s or more: does a pop move values?")
# print("passed")

# %% [markdown]
# ## 5. A matrix
#
# `new_matrix(rows, cols, fill)` should build a `rows`-by-`cols` matrix filled with `fill`. Run
# the cell, and compare the two numbers it prints with what the code meant to do.

# %% tags=["answer-L3.6"] language="lua"
# function new_matrix(rows, cols, fill)
#   local m, row = {}, {}
#   for j = 1, cols do row[j] = fill end
#   for i = 1, rows do m[i] = row end
#   return m
# end
#
# function transpose(m)
#   -- your code here
# end
#
# local grid = new_matrix(2, 3, 0)
# grid[1][1] = 7
# print(grid[1][1], grid[2][1])

# %% [markdown]
# ### Exercise L3.6 (LO-3.3, LO-3.4, ★★, about 20 minutes)
#
# Fix `new_matrix`, so that each row is a table of its own. Then write `transpose(m)`, which
# returns a new matrix `t` with `t[j][i] == m[i][j]`: a 2-by-3 matrix becomes a 3-by-2 one. Assume
# `m` has at least one row and that all its rows have the same length. `transpose` must not change
# `m`, and must not share any row with it.

# %% tags=["raises-exception"] language="lua"
# local g = new_matrix(2, 3, 0)
# g[1][1] = 7
# assert(g[2][1] == 0, "writing g[1][1] changed g[2][1]: the rows are still one table")
# assert(#g == 2 and #g[1] == 3 and #g[2] == 3, "new_matrix(2, 3, 0) should have 2 rows of 3")
#
# local m = { { 1, 2, 3 }, { 4, 5, 6 } }
# local t = transpose(m)
# assert(#t == 3 and #t[1] == 2 and #t[3] == 2, "the transpose of a 2-by-3 matrix is 3-by-2")
# assert(t[1][2] == 4 and t[3][1] == 3 and t[3][2] == 6, "t[j][i] should be m[i][j]")
# assert(m[1][2] == 2 and #m == 2 and #m[1] == 3, "transpose must not change its argument")
# t[1][1] = 100
# assert(m[1][1] == 1, "changing the transpose changed the original")
# local one = transpose({ { 9 } })
# assert(#one == 1 and #one[1] == 1 and one[1][1] == 9, "the transpose of { { 9 } } is { { 9 } }")
# print("passed")

# %% [markdown]
# ## Summary
#
# - `#t` always returns a border of `t`. A sequence has one border, its length; a table with holes
#   has several, and which one `#` returns depends on how the table was built.
# - `pairs` has no order to rely on; sort the keys to get one.
# - Assigning or passing a table shares it, and `==` compares identity. A deep copy needs a
#   `seen` table to copy shared and self-containing tables correctly.
# - `table.remove(t, 1)` moves every item, so emptying a list that way is $O(n^2)$; a queue with
#   two indices is $O(1)$ for each push and pop.
# - Every row of a matrix must be a table of its own.
#
# Next, do the [Module 3 practice](practice.md).
