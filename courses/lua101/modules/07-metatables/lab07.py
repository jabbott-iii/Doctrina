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
# # Lab 7: Metatables
#
# **Objectives:** LO-7.1, LO-7.2, LO-7.3\
# **Prerequisites:** the [Module 7 reading](index.md) and
# [Lab 6](../06-errors-modules-and-tests/lab06.ipynb)\
# **Time:** about 2 hours
#
# You will predict which metamethod each operation calls and with what arguments, give a vector
# type its operators, give tables default values, build a read-only view that protects nested
# tables too, and predict which entries of weak tables survive a garbage collection. As in the
# earlier labs, each check cell prints `passed` or fails with a message, and the checks fail until
# you finish their exercise.

# %% [markdown]
# ## Setup
#
# Nothing in this lab is random, and section 5's garbage collections happen at moments the code
# chooses. The second cell prints the Lua version, which should be `Lua 5.4`.

# %%
# %load_ext lualab
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. Which metamethod runs?
#
# The next cell makes `tracer`, a metatable whose metamethods each return a string naming
# themselves and the types of the arguments they got, and two tables `t` and `u` that use it. Run
# it, and try `print(t + u)` in a cell of your own.

# %% language="lua"
# local function kinds(...)
#   local names = {}
#   for i = 1, select("#", ...) do names[i] = type((select(i, ...))) end
#   return table.concat(names, ", ")
# end
#
# tracer = {}
# for _, name in ipairs({ "__add", "__concat", "__eq", "__lt", "__index", "__call" }) do
#   tracer[name] = function(...) return name .. "(" .. kinds(...) .. ")" end
# end
#
# t = setmetatable({}, tracer)
# u = setmetatable({}, tracer)

# %% [markdown]
# ### Exercise L7.1 (LO-7.1, ★★, about 15 minutes)
#
# Predict the value of each expression. For most, it is the string the metamethod returns, such as
# `"__add(table, number)"`; for a comparison it is a boolean. Make all twelve predictions before
# you run the check.

# %% tags=["answer-L7.1"] language="lua"
# metamethod_predictions = {
#   { [[t + 1]],     "?" },
#   { [[1 + t]],     "?" },
#   { [[t .. "!"]],  "?" },
#   { [["x" .. t]],  "?" },
#   { [[t.color]],   "?" },
#   { [[t[1] ]],     "?" },
#   { [[t(1, 2)]],   "?" },
#   { [[t == u]],    "?" },
#   { [[t == t]],    "?" },
#   { [[t == 1]],    "?" },
#   { [[t ~= u]],    "?" },
#   { [[u < t]],     "?" },
# }

# %% tags=["raises-exception"] language="lua"
# local wrong, unanswered = 0, 0
# for n, row in ipairs(metamethod_predictions) do
#   local expression, predicted = row[1], row[2]
#   local actual = load("return " .. expression, "=expression", "t")()
#   local verdict = "match"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= actual then
#     wrong, verdict = wrong + 1, "MISMATCH"
#   end
#   print(string.format("%2d  %-10s you: %-30s Lua: %-30s %s", n, expression, tostring(predicted),
#     tostring(actual), verdict))
# end
# assert(unanswered == 0, unanswered .. " expressions still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# ## 2. A vector type
#
# ### Exercise L7.2 (LO-7.1, ★★, about 25 minutes)
#
# `vec(x, y)` makes a two-dimensional vector whose metatable is `vector_mt`. Give `vector_mt`
# these metamethods:
#
# | Expression | Result |
# | :- | :- |
# | `a + b`, `a - b` | A new vector, added or subtracted component by component |
# | `2 * a`, `a * 2` | A new vector, each component multiplied by the number |
# | `a * b` | The dot product, a number: `a.x * b.x + a.y * b.y` |
# | `-a` | A new vector with both components negated |
# | `a == b` | `true` when both components are equal |
# | `tostring(a)` | The string `"(x, y)"`, such as `"(1, 2)"` |
#
# No operation may change its operands.
#
# <details>
# <summary>Hint</summary>
#
# `2 * a` calls `vector_mt.__mul(2, a)`, with the number first. Test `type(a) == "number"` and
# `type(b) == "number"` to tell the three cases of `*` apart.
# </details>

# %% tags=["answer-L7.2"] language="lua"
# vector_mt = {}
#
# function vec(x, y)
#   return setmetatable({ x = x, y = y }, vector_mt)
# end
#
# -- your code here: define vector_mt.__add, __sub, __mul, __unm, __eq, and __tostring

# %% tags=["raises-exception"] language="lua"
# local a, b = vec(1, 2), vec(3, 4)
# assert(tostring(a) == "(1, 2)", "tostring(vec(1, 2)) should be \"(1, 2)\"")
# assert(a + b == vec(4, 6) and b - a == vec(2, 2), "a + b should be (4, 6), and b - a (2, 2)")
# assert(2 * a == vec(2, 4) and a * 2 == vec(2, 4), "a number can multiply on either side")
# assert(a * b == 11, "a * b should be the dot product, 11")
# assert(-a == vec(-1, -2), "-a should be (-1, -2)")
# assert(a == vec(1, 2) and a ~= b and not rawequal(a, vec(1, 2)), "== compares components")
# assert(getmetatable(a + b) == vector_mt and (a + b) * 2 == vec(8, 12), "results are vectors too")
# assert(a.x == 1 and a.y == 2 and b.x == 3 and b.y == 4, "no operation may change its operands")
# assert(tostring(vec(0.5, -3)) == "(0.5, -3)", "tostring of other components")
# print("passed")

# %% [markdown]
# ## 3. Default values
#
# ### Exercise L7.3 (LO-7.2, ★, about 15 minutes)
#
# Write `with_default(t, default)`, which gives `t` a metatable so that every key `t` doesn't have
# reads as `default`, and returns `t`. Reading a missing key must store nothing. Make it work when
# `default` is `false`.
#
# <details>
# <summary>Hint</summary>
#
# `__index` can be a function of the table and the key. A table as `__index` won't do here:
# `default` is a single value, not a table of keys.
# </details>

# %% tags=["answer-L7.3"] language="lua"
# function with_default(t, default)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local counts = with_default({ apples = 2 }, 0)
# assert(type(counts) == "table" and counts.apples == 2, "with_default returns t, with its own keys")
# assert(counts.pears == 0 and counts[42] == 0, "missing keys read as the default")
# counts.pears = counts.pears + 1
# assert(counts.pears == 1, "a missing key can be read, then assigned")
# assert(rawget(counts, "plums") == nil and counts.plums == 0 and rawget(counts, "plums") == nil,
#   "reading a missing key must store nothing")
# local flags = with_default({}, false)
# assert(flags.anything == false, "a default of false works")
# local a, b = with_default({}, "a"), with_default({}, "b")
# assert(a.x == "a" and b.x == "b", "each table keeps its own default")
# print("passed")

# %% [markdown]
# ## 4. A read-only view, all the way down
#
# The reading's `read_only` protects the top level of a table only: `ro.window.title = "x"` still
# changes the nested table, because `ro.window` is the real one.
#
# ### Exercise L7.4 (LO-7.2, LO-7.3, ★★★, about 35 minutes)
#
# Write `deep_read_only(t)`, which returns a read-only view of `t` at every depth:
#
# - Reading a value that isn't a table returns it. Reading a table value returns a read-only view
#   of that table, and the same view every time: `ro.window == ro.window`.
# - Any assignment through a view, at any depth and to any key, raises the error
#   `"attempt to change a read-only table"` at level 2.
# - `#` and `pairs` work on every view, and `pairs` gives views for table values. The view shows
#   later changes made to the original.
#
# <details>
# <summary>Hint 1</summary>
#
# Keep a table that maps each original table to its view, and look there before making a new
# view. Give it weak keys, so that the cache doesn't keep tables alive that the program has
# forgotten.
# </details>
#
# <details>
# <summary>Hint 2</summary>
#
# Make `__index` a function that reads `t[k]` and passes the result through `deep_read_only`,
# which returns non-tables unchanged. `__pairs` returns an iterator built on `next(t, k)` that does
# the same for each value.
# </details>

# %% tags=["answer-L7.4"] language="lua"
# function deep_read_only(t)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local data = { name = "config", sizes = { 1, 2, 3 }, window = { title = "Main", pos = { x = 1 } } }
# ro = deep_read_only(data)
# assert(ro.name == "config" and ro.sizes[2] == 2 and ro.window.pos.x == 1, "reads reach every depth")
# assert(#ro.sizes == 3, "# works on a view")
# assert(ro.window == ro.window and ro.window.pos == ro.window.pos, "one table, one view")
# assert(ro.window ~= data.window, "reading a table value gives a view, not the original")
# for _, write in ipairs({ "ro.name = 'x'", "ro.new = 1", "ro.sizes[1] = 9", "ro.window.title = 'x'",
#                          "ro.window.pos.x = 2" }) do
#   local ok, err = pcall(load(write, "=caller", "t"))
#   assert(not ok and err == "caller:1: attempt to change a read-only table",
#     write .. " should raise 'attempt to change a read-only table' at level 2; got " .. tostring(err))
# end
# assert(data.name == "config" and data.sizes[1] == 1 and data.window.pos.x == 1,
#   "the original must be unchanged")
# local keys = 0
# for k, v in pairs(ro) do
#   keys = keys + 1
#   if k == "window" then
#     assert(not pcall(function() v.title = "x" end), "pairs must give views for table values")
#   end
# end
# assert(keys == 3, "pairs should visit the original's three keys")
# local total = 0
# for _, v in ipairs(ro.sizes) do total = total + v end
# assert(total == 6, "ipairs should work on a view")
# data.name = "changed"
# assert(ro.name == "changed", "a view shows later changes to the original")
# print("passed")

# %% [markdown]
# ## 5. Weak tables
#
# `weak_story` builds four tables, three of them weak, fills them, forces a full garbage collection
# with `collectgarbage()`, and reports what survived. Read it before the exercise, but don't run
# anything yet.

# %% language="lua"
# function weak_story()
#   local kept = {}
#
#   local by_key = setmetatable({}, { __mode = "k" })
#   by_key[kept] = "kept key"
#   by_key[{}] = "new key"
#   by_key.name = {}
#
#   local by_value = setmetatable({}, { __mode = "v" })
#   by_value.kept = kept
#   by_value.lost = {}
#   by_value.text = "a string"
#   by_value.number = 42
#
#   local owners = setmetatable({}, { __mode = "k" })
#   owners[{}] = { note = "refers to nothing" }
#   local cyclic = {}
#   owners[cyclic] = { owner = cyclic }
#   cyclic = nil
#
#   local strong = {}
#   strong[{}] = true
#
#   collectgarbage()
#
#   local function count(t)
#     local n = 0
#     for _ in pairs(t) do n = n + 1 end
#     return n
#   end
#   return {
#     by_key_entries = count(by_key),
#     by_key_name = by_key.name ~= nil,
#     by_value_kept = by_value.kept ~= nil,
#     by_value_lost = by_value.lost ~= nil,
#     by_value_text = by_value.text ~= nil,
#     by_value_number = by_value.number ~= nil,
#     owners_entries = count(owners),
#     strong_entries = count(strong),
#   }
# end

# %% [markdown]
# ### Exercise L7.5 (LO-7.3, ★★, about 15 minutes)
#
# Predict each value `weak_story` reports: a number of entries, or `true` if the entry survived
# and `false` if it was removed. Then run the check.

# %% tags=["answer-L7.5"] language="lua"
# weak_predictions = {
#   { "by_key_entries",  "?" },
#   { "by_key_name",     "?" },
#   { "by_value_kept",   "?" },
#   { "by_value_lost",   "?" },
#   { "by_value_text",   "?" },
#   { "by_value_number", "?" },
#   { "owners_entries",  "?" },
#   { "strong_entries",  "?" },
# }

# %% tags=["raises-exception"] language="lua"
# local story = weak_story()
# local wrong, unanswered = 0, 0
# for n, row in ipairs(weak_predictions) do
#   local name, predicted = row[1], row[2]
#   local actual = story[name]
#   local verdict = "match"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= actual then
#     wrong, verdict = wrong + 1, "MISMATCH"
#   end
#   print(string.format("%d  %-16s you: %-6s Lua: %-6s %s", n, name, tostring(predicted),
#     tostring(actual), verdict))
# end
# assert(unanswered == 0, unanswered .. " values still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# Last, watch a weak cache empty. The cell caches an area for each of 1,000 shapes, drops every
# shape but one, and counts the cache's entries before and after a collection. The collector also
# runs on its own whenever the program has allocated enough memory, so the cell stops it first,
# with `collectgarbage("stop")`; otherwise it might empty the cache before the first count. Try
# removing that line and running the cell a few times.

# %% language="lua"
# collectgarbage("stop")
# local area_cache = setmetatable({}, { __mode = "k" })
# local function area(shape)
#   local result = area_cache[shape]
#   if result == nil then
#     result = shape.width * shape.height
#     area_cache[shape] = result
#   end
#   return result
# end
#
# local function entries(t)
#   local n = 0
#   for _ in pairs(t) do n = n + 1 end
#   return n
# end
#
# local shapes = {}
# for i = 1, 1000 do shapes[i] = { width = i, height = 2 } end
# for _, shape in ipairs(shapes) do area(shape) end
# local keep = shapes[1]
# shapes = nil
# print("entries before collecting:", entries(area_cache))
# collectgarbage()             -- a full collection runs even while the collector is stopped
# print("entries after collecting: ", entries(area_cache), "kept:", area_cache[keep])
# collectgarbage("restart")

# %% [markdown]
# ## Summary
#
# - A binary operator's metamethod gets both operands in their original order, from whichever
#   operand has it; `==` calls `__eq` only for two different tables.
# - Metamethods for arithmetic, `==`, and `tostring` make a table behave like a value type, as long
#   as every operation returns a new table.
# - A function in `__index` supplies defaults without storing them.
# - An empty proxy sees every read and write; a weak-keyed cache of proxies gives one view per
#   table without keeping the tables alive.
# - Weak tables drop entries whose weak part is an unreachable object, at the next collection;
#   strings, numbers, and the entries of ordinary tables stay.
#
# Next, do the [Module 7 practice](practice.md), then review for the midterm exam.
