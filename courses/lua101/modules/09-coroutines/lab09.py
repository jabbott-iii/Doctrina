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
# # Lab 9: Coroutines
#
# **Objectives:** LO-9.1, LO-9.2, LO-9.3\
# **Prerequisites:** the [Module 9 reading](index.md) and
# [Lab 8](../08-objects-and-classes/lab08.ipynb)\
# **Time:** about 2 hours
#
# You will trace values through `resume` and `yield`, write a recursive generator of permutations,
# add two stages to a pipeline, extend the reading's scheduler with start delays and a time limit,
# and watch one task that never yields hold up all the others. As in the earlier labs, each check
# cell prints `passed` or fails with a message, and the checks fail until you finish their
# exercise.

# %% [markdown]
# ## Setup
#
# Section 5 measures real time, so its numbers depend on your machine; everything else is the same
# on every run. The second cell prints the Lua version, which should be `Lua 5.4`.

# %%
# %load_ext lualab
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. Values in and out
#
# `make_echo` makes a coroutine that multiplies, decorates, and adds what it is given. Read it, and
# don't run anything yet.

# %% language="lua"
# function make_echo()
#   return coroutine.create(function(first)
#     local got = coroutine.yield(first * 10)
#     local a, b = coroutine.yield(got .. "!")
#     if a == "stop" then error("stopped", 0) end
#     return a + b
#   end)
# end

# %% [markdown]
# ### Exercise L9.1 (LO-9.1, ★★, about 15 minutes)
#
# The check makes two echo coroutines, `co` and `co2`, and evaluates the expressions below in
# order. Predict what each one gives, as all its values in order, separated by a comma and a space:
# for example `"true, 40"` or `"suspended"`. Make all eleven predictions before you run the check.

# %% tags=["answer-L9.1"] language="lua"
# echo_predictions = {
#   { [[coroutine.status(co)]],        "?" },
#   { [[coroutine.resume(co, 4)]],     "?" },
#   { [[coroutine.resume(co, "hi")]],  "?" },
#   { [[coroutine.status(co)]],        "?" },
#   { [[coroutine.resume(co, 2, 3)]],  "?" },
#   { [[coroutine.status(co)]],        "?" },
#   { [[coroutine.resume(co)]],        "?" },
#   { [[coroutine.resume(co2, 1)]],    "?" },
#   { [[coroutine.resume(co2, "x")]],  "?" },
#   { [[coroutine.resume(co2, "stop")]], "?" },
#   { [[coroutine.status(co2)]],       "?" },
# }

# %% tags=["raises-exception"] language="lua"
# co, co2 = make_echo(), make_echo()
# local wrong, unanswered = 0, 0
# for n, row in ipairs(echo_predictions) do
#   local expression, predicted = row[1], row[2]
#   local results = table.pack(load("return " .. expression, "=step", "t")())
#   local shown = {}
#   for i = 1, results.n do shown[i] = tostring(results[i]) end
#   local actual = table.concat(shown, ", ")
#   local verdict = "match"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= actual then
#     wrong, verdict = wrong + 1, "MISMATCH"
#   end
#   print(string.format("%2d  %-30s you: %-34s Lua: %-34s %s", n, expression, predicted, actual,
#     verdict))
# end
# assert(unanswered == 0, unanswered .. " expressions still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# ## 2. A recursive generator
#
# ### Exercise L9.2 (LO-9.2, ★★★, about 25 minutes)
#
# Write `permutations(list)`, which returns a generator, for the generic `for`, of every ordering of
# the items of `list`. Each ordering it gives is a new table, so the loop may keep it, and `list`
# itself is unchanged when the loop ends. The orderings may come in any order.
#
# <details>
# <summary>Hint 1</summary>
#
# Write a recursive helper `place(k)` that fills position `k` with each item not yet placed in
# turn, and calls `place(k + 1)`; at `k = #list + 1` an ordering is complete, so yield a copy of
# it.
# </details>
#
# <details>
# <summary>Hint 2</summary>
#
# A neat way to try each item at position `k` is to swap it into place, recurse, and swap it back:
# work on a copy of `list`, and swap `copy[k]` with `copy[i]` for each `i` from `k` to the end.
# </details>

# %% tags=["answer-L9.2"] language="lua"
# function permutations(list)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local seen, count = {}, 0
# local original = { "a", "b", "c" }
# for p in permutations(original) do
#   count = count + 1
#   assert(#p == 3, "each ordering should have all three items")
#   seen[table.concat(p)] = true
# end
# assert(count == 6, "three items have 6 orderings, not " .. count)
# for _, word in ipairs({ "abc", "acb", "bac", "bca", "cab", "cba" }) do
#   assert(seen[word], "the ordering " .. word .. " is missing")
# end
# assert(table.concat(original) == "abc", "the list itself must be unchanged")
# local kept = {}
# for p in permutations({ 1, 2 }) do kept[#kept + 1] = p end
# assert(#kept == 2 and kept[1] ~= kept[2] and table.concat(kept[1]) ~= table.concat(kept[2]),
#   "each ordering must be a new table")
# local n = 0
# for _ in permutations({ 1, 2, 3, 4, 5 }) do n = n + 1 end
# assert(n == 120, "five items have 120 orderings")
# local empty = 0
# for p in permutations({}) do empty = empty + 1; assert(#p == 0) end
# assert(empty == 1, "the empty list has exactly one ordering: the empty one")
# print("passed")

# %% [markdown]
# ## 3. A pipeline
#
# The next cell defines the reading's producer, `lines_of`, and a source that counts how many times
# it has been asked for a value.

# %% language="lua"
# function lines_of(text)
#   return coroutine.wrap(function()
#     for line in text:gmatch("[^\n]+") do coroutine.yield(line) end
#   end)
# end
#
# function counting_source(values)
#   local source = { calls = 0 }
#   function source.next()
#     source.calls = source.calls + 1
#     return values[source.calls]
#   end
#   return source
# end

# %% [markdown]
# ### Exercise L9.3 (LO-9.2, ★★, about 20 minutes)
#
# Write two pipeline stages with `coroutine.wrap`, each taking a source, a function that returns
# the next value or `nil`:
#
# - `numbered(source)` gives each value as the string `"n: value"`, counting from 1.
# - `chunked(size, source)` gives the values in tables of `size` consecutive values; the last table
#   may be shorter, and an empty source gives nothing. It must ask its source for no more values
#   than the chunk it is building needs.

# %% tags=["answer-L9.3"] language="lua"
# function numbered(source)
#   -- your code here
# end
#
# function chunked(size, source)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local out = {}
# for line in numbered(lines_of("alpha\nbeta\ngamma")) do out[#out + 1] = line end
# assert(table.concat(out, "|") == "1: alpha|2: beta|3: gamma", "numbered should give 1: alpha, ...")
# local sizes = {}
# for chunk in chunked(2, lines_of("a\nb\nc\nd\ne")) do sizes[#sizes + 1] = table.concat(chunk) end
# assert(table.concat(sizes, ",") == "ab,cd,e", "chunks of 2 from a..e: ab, cd, e")
# assert(chunked(3, lines_of(""))() == nil, "an empty source gives no chunks")
# local kept = {}
# for chunk in chunked(2, lines_of("a\nb\nc")) do kept[#kept + 1] = chunk end
# assert(#kept == 2 and kept[1] ~= kept[2] and kept[1][1] == "a" and kept[2][1] == "c",
#   "each chunk must be a new table, which the loop may keep")
# local source = counting_source({ 1, 2, 3, 4, 5 })
# local chunks = chunked(2, source.next)
# local first = chunks()
# assert(first[1] == 1 and first[2] == 2 and source.calls == 2,
#   "the first chunk should ask the source for exactly 2 values, not " .. source.calls)
# local labels = {}
# for line in numbered(chunked(2, lines_of("p\nq\nr"))) do labels[#labels + 1] = line end
# assert(#labels == 2 and labels[1]:sub(1, 3) == "1: ", "stages compose: numbered over chunked")
# print("passed")

# %% [markdown]
# ## 4. A scheduler with start delays and a time limit
#
# The next cell holds the reading's scheduler state and `sleep`, and a `log` that tasks write to.

# %% language="lua"
# now = 0
# waiting = {}
# log = {}
#
# function sleep(seconds)
#   coroutine.yield(seconds)
# end
#
# function note(text)
#   log[#log + 1] = now .. " " .. text
# end
#
# function reset_scheduler()
#   now, waiting, log = 0, {}, {}
# end

# %% [markdown]
# ### Exercise L9.4 (LO-9.3, ★★★, about 30 minutes)
#
# Write two global functions:
#
# - `spawn(fn, delay)` schedules a new task, a coroutine running `fn`, to start at `now + delay`;
#   `delay` defaults to 0.
# - `run(until_time)` repeatedly takes the waiting task with the earliest wake time, sets `now` to
#   that time, and resumes it. A task that yields is put back with the wake time `now` plus the
#   delay it yielded; a task that finishes is dropped; a task that raises an error stops `run`
#   with that error. Among tasks with the same wake time, the one that was put in `waiting` first
#   runs first. `run` stops when no task is waiting, or when the earliest wake time is later than
#   `until_time`; with no `until_time`, it runs until no task is waiting. It returns the number of
#   resumes it made.
#
# <details>
# <summary>Hint</summary>
#
# Start from the reading's `run`. Before removing the earliest entry, compare its wake time with
# `until_time`, and stop without removing it if it is later.
# </details>

# %% tags=["answer-L9.4"] language="lua"
# function spawn(fn, delay)
#   -- your code here
# end
#
# function run(until_time)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# reset_scheduler()
# spawn(function() for i = 1, 3 do note("tick " .. i); sleep(2) end end)
# spawn(function() note("tock"); sleep(3); note("tock again") end)
# spawn(function() note("late start") end, 5)
# local resumes = run()
# local expected = "0 tick 1, 0 tock, 2 tick 2, 3 tock again, 4 tick 3, 5 late start"
# assert(table.concat(log, ", ") == expected,
#   "the log should read " .. expected .. "; it reads " .. table.concat(log, ", "))
# assert(resumes == 7, "that takes 7 resumes, not " .. tostring(resumes))
# assert(#waiting == 0 and now == 6, "finished tasks are dropped, and the clock ends at 6")
#
# reset_scheduler()
# for _, name in ipairs({ "a", "b", "c" }) do
#   spawn(function() note(name); sleep(1); note(name) end)
# end
# run()
# assert(table.concat(log, ",") == "0 a,0 b,0 c,1 a,1 b,1 c",
#   "tasks due at the same time run in the order they were put in waiting")
#
# reset_scheduler()
# spawn(function() while true do note("beat"); sleep(1) end end)
# assert(run(3.5) == 4 and now == 3 and #waiting == 1, "run(3.5) should resume at 0, 1, 2, and 3")
# assert(run(5) == 2 and now == 5, "a second run continues where the first stopped")
#
# reset_scheduler()
# spawn(function() sleep(1); error("broken", 0) end)
# local ok, err = pcall(run)
# assert(not ok and err == "broken", "an error in a task should stop run with that error")
# print("passed")

# %% [markdown]
# ## 5. A task that never yields
#
# The next cell runs three tasks on your scheduler, and records the real time, from `os.clock`, at
# which each line is logged. The task `busy` computes for about half a second without calling
# `sleep`. Before you run it, predict: when does `quick`, which is due at simulated time 1, write
# its line, in real time?

# %% tags=["raises-exception"] language="lua"
# reset_scheduler()
# local start = os.clock()
# local function stamp(text) note(string.format("%s (real %.2f s)", text, os.clock() - start)) end
# spawn(function() stamp("busy starts"); local x = 0; for i = 1, 1e8 do x = x + i end; stamp("busy ends") end)
# spawn(function() stamp("quick runs") end, 1)
# spawn(function() sleep(2); stamp("slow runs") end)
# run()
# for _, line in ipairs(log) do print(line) end

# %% [markdown] tags=["answer-L9.5-why"]
# *Your answer here: `quick` was due at simulated time 1. Why did it run only after `busy`
# finished, and what change to `busy` would let `quick` run on time?*

# %% [markdown]
# ## Summary
#
# - `resume`'s arguments arrive as the function's parameters, then as `yield`'s results; `yield`'s
#   arguments and the function's returns come back from `resume`, after `true`, or after `false`
#   and the message when the coroutine fails.
# - A recursive generator keeps its paused calls on the coroutine's stack, so it needs no explicit
#   stack of its own.
# - Pipeline stages built with `wrap` take a source and are one; the consumer pulls each value
#   through, and no stage reads ahead of what it needs.
# - A scheduler resumes the earliest task, moves its clock, and reschedules what yields; it works
#   only as long as every task yields often.
#
# Next, do the [Module 9 practice](practice.md), then start PA4.
