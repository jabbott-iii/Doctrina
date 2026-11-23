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
# # Lab 12: Performance and memory
#
# **Objectives:** LO-12.1, LO-12.2, LO-12.3\
# **Prerequisites:** the [Module 12 reading](index.md) and
# [Lab 11](../11-packages-and-tooling/lab11.ipynb)\
# **Time:** about 2 hours
#
# You will write a benchmark helper, predict the winner of six races between two ways of doing the
# same thing and check your predictions, read the garbage collector's statistics, and speed up a
# slow word counter at least fivefold, justifying each change with a measurement. Every number here
# depends on your machine and how busy it is, so the checks compare ratios, never times.

# %% [markdown]
# ## Setup
#
# The second cell prints the Lua version, which should be `Lua 5.4`. Close other heavy programs
# before you measure: they make every timing slower and noisier.

# %%
# %load_ext lualab
import os
import platform
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)
print("machine:", platform.processor() or platform.machine(), "| system:", platform.system(),
      "| load average:", os.getloadavg()[0] if hasattr(os, "getloadavg") else "unknown")

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. A benchmark helper
#
# ### Exercise L12.1 (LO-12.1, ★★, about 20 minutes)
#
# Write `bench(fn, runs)`, which calls `fn` `runs` times, 5 by default, after a full garbage
# collection before each call, times each call with `os.clock`, and returns two numbers: the
# minimum time and the median time. The median of an even number of times is the mean of the two
# in the middle.

# %% tags=["answer-L12.1"] language="lua"
# function bench(fn, runs)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local calls = 0
# local fastest, median = bench(function() calls = calls + 1 end)
# assert(calls == 5, "bench should call fn 5 times by default, not " .. calls)
# assert(math.type(fastest) == "float" and math.type(median) == "float", "return two floats")
# assert(fastest <= median, "the minimum can't be larger than the median")
# calls = 0
# bench(function() calls = calls + 1 end, 4)
# assert(calls == 4, "bench should call fn runs times")
# local times = { 0.03, 0.01, 0.04, 0.02 }
# local index = 0
# local real_clock = os.clock
# local clock_calls = 0
# os.clock = function() clock_calls = clock_calls + 1; return clock_calls % 2 == 0 and times[clock_calls // 2] or 0 end
# local ok, low, mid = pcall(bench, function() end, 4)
# os.clock = real_clock
# assert(ok, "bench failed: " .. tostring(low))
# assert(math.abs(low - 0.01) < 1e-12 and math.abs(mid - 0.025) < 1e-12,
#   "with times 0.03, 0.01, 0.04, 0.02, bench should return 0.01 and 0.025; got " .. low .. " and " .. mid)
# print("passed")

# %% [markdown]
# ## 2. Six races
#
# Each race compares two ways, A and B, of doing the same work. For races 1 to 3, 5, and 6, the
# question is which is faster; for race 4, which uses more memory. The next cell defines the races.
# Read them, but don't run the comparison yet.

# %% language="lua"
# local N = 200000
# local args = {}
# for i = 1, 200 do args[i] = i end
# local function sum_select(...)
#   local s = 0
#   for i = 1, select("#", ...) do s = s + (select(i, ...)) end
#   return s
# end
# local function sum_pack(...)
#   local t = table.pack(...)
#   local s = 0
#   for i = 1, t.n do s = s + t[i] end
#   return s
# end
# local list, set = {}, {}
# for i = 1, 2000 do list[i] = "item" .. i; set["item" .. i] = true end
#
# races = {
#   { "append with a counter vs table.insert",
#     function() local t, n = {}, 0 for i = 1, N do n = n + 1; t[n] = i end end,
#     function() local t = {} for i = 1, N do table.insert(t, i) end end },
#   { "200 arguments with select vs table.pack",
#     function() for _ = 1, 500 do sum_select(table.unpack(args)) end end,
#     function() for _ = 1, 500 do sum_pack(table.unpack(args)) end end },
#   { "a closure created on every pass vs none",
#     function() local s = 0 for i = 1, N do local f = function() return i end; s = s + f() end end,
#     function() local s = 0 for i = 1, N do s = s + i end end },
#   { "memory: integer keys from 1 vs string keys", "memory",
#     function() local t = {} for i = 1, N do t[i] = i end return t end,
#     function() local t = {} for i = 1, N do t["k" .. i] = i end return t end },
#   { "building text with .. vs table.concat",
#     function() local s = "" for i = 1, 5000 do s = s .. "line " .. i .. "\n" end end,
#     function() local p = {} for i = 1, 5000 do p[i] = "line " .. i .. "\n" end return table.concat(p) end },
#   { "finding 2,000 names in a list vs in a set",
#     function() for i = 1, 2000 do local want = "item" .. i
#       for _, v in ipairs(list) do if v == want then break end end end end,
#     function() for i = 1, 2000 do local _ = set["item" .. i] end end },
# }

# %% [markdown]
# ### Exercise L12.2 (LO-12.2, ★★, about 20 minutes)
#
# For each race, predict the winner, `"A"` or `"B"`: the faster one, or for race 4 the one that uses
# more memory. Write down why, from the reading. Then run the check, which measures both sides with
# your `bench` and prints the ratio. It takes about ten seconds.

# %% tags=["answer-L12.2"] language="lua"
# race_predictions = { "?", "?", "?", "?", "?", "?" }

# %% tags=["raises-exception"] language="lua"
# local function memory_of(build)
#   collectgarbage()
#   local before = collectgarbage("count")
#   local keep = build()
#   collectgarbage()
#   local used = collectgarbage("count") - before
#   keep = nil
#   return used
# end
# local wrong, unanswered = 0, 0
# for n, race in ipairs(races) do
#   local a, b, winner, ratio
#   if race[2] == "memory" then
#     a, b = memory_of(race[3]), memory_of(race[4])
#     winner, ratio = a > b and "A" or "B", math.max(a, b) / math.min(a, b)
#   else
#     a, b = bench(race[2], 3), bench(race[3], 3)
#     winner, ratio = a < b and "A" or "B", math.max(a, b) / math.min(a, b)
#   end
#   local predicted = race_predictions[n]
#   local verdict = "match"
#   if predicted == "?" then unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= winner then wrong, verdict = wrong + 1, "MISMATCH" end
#   print(string.format("%d  %-46s you: %-2s winner: %s by %.1f times   %s", n, race[1], predicted,
#     winner, ratio, verdict))
# end
# assert(unanswered == 0, unanswered .. " races still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; work out why, then correct them")
# print("passed")

# %% [markdown]
# ## 3. The garbage collector's statistics
#
# Run the next cell. It builds and drops a hundred thousand small tables, and prints the memory in
# use, from `collectgarbage("count")`, before, after, and after a full collection. It also prints
# the collector's mode, which `collectgarbage("incremental")` and `collectgarbage("generational")`
# set and return. The notebooks' Lua starts in incremental mode; the standalone `lua` starts in
# generational mode.

# %% language="lua"
# local mode = collectgarbage("incremental")
# collectgarbage("incremental")
# collectgarbage()
# local start = collectgarbage("count")
# for i = 1, 100000 do local _ = { i, i, i } end
# local after = collectgarbage("count")
# collectgarbage()
# print(string.format("mode: %s | KB at start %.0f, after the loop %.0f, after collecting %.0f",
#   mode, start, after, collectgarbage("count")))

# %% [markdown]
# The memory after the loop is above the start, but far below the 100,000 tables' total size: the
# incremental collector ran several cycles while the loop allocated. Try it in generational mode by
# changing the second line.
#
# ## 4. Speeding up a hot path
#
# `slow_histogram(words)` counts the words of a list, ignoring case, and returns one line per word,
# `word count`, most frequent first, ties in alphabetical order. The next cell defines it, and a
# word list of 20,000 words from a vocabulary of 2,000, and times it.

# %% language="lua"
# function make_words(n, vocabulary)
#   local words, state = {}, 12345
#   for i = 1, n do
#     state = (state * 1103515245 + 12345) % 2147483648
#     words[i] = (state % 2 == 0 and "W" or "w") .. (state // 2 % vocabulary)
#   end
#   return words
# end
#
# function slow_histogram(words)
#   local counts = {}
#   for i = 1, #words do
#     local w = string.lower(words[i])
#     local found = false
#     for j = 1, #counts do
#       if counts[j].word == w then
#         counts[j].n = counts[j].n + 1
#         found = true
#         break
#       end
#     end
#     if not found then table.insert(counts, { word = w, n = 1 }) end
#   end
#   table.sort(counts, function(a, b)
#     if a.n ~= b.n then return a.n > b.n end
#     return a.word < b.word
#   end)
#   local result = ""
#   for i = 1, #counts do
#     result = result .. counts[i].word .. " " .. counts[i].n .. "\n"
#   end
#   return result
# end
#
# WORDS = make_words(20000, 2000)
# local start = os.clock()
# local text = slow_histogram(WORDS)
# print(string.format("slow_histogram: %.3f s, %d bytes of output", os.clock() - start, #text))

# %% [markdown]
# ### Exercise L12.3 (LO-12.3, ★★★, about 40 minutes)
#
# Write `fast_histogram(words)`, which returns exactly what `slow_histogram` returns, at least five
# times faster. Work by the reading's method: time `slow_histogram`'s parts to find where the time
# goes, change one thing at a time, and measure after each change with your `bench`. In the Markdown
# cell after the check, list each change you kept, why it helps, and the time it gave.
#
# <details>
# <summary>Hint</summary>
#
# Look for the loop inside a loop, and for the string that grows with `..`.
# </details>

# %% tags=["answer-L12.3"] language="lua"
# function fast_histogram(words)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# assert(fast_histogram(WORDS) == slow_histogram(WORDS), "fast_histogram must return exactly what slow_histogram does")
# assert(fast_histogram({}) == slow_histogram({}), "...for an empty list too")
# local few = { "b", "A", "a", "B", "c" }
# assert(fast_histogram(few) == "a 2\nb 2\nc 1\n", "ties go in alphabetical order")
# local slow = bench(function() slow_histogram(WORDS) end, 3)
# local fast = bench(function() fast_histogram(WORDS) end, 3)
# print(string.format("slow %.4f s, fast %.4f s: %.1f times faster", slow, fast, slow / fast))
# assert(slow / fast >= 5, "fast_histogram should be at least 5 times faster")
# print("passed")

# %% [markdown] tags=["answer-L12.3-why"]
# *Your answer here: each change you kept, why it helps, and the time `bench` measured after it.*

# %% [markdown]
# ## Summary
#
# - A benchmark repeats, collects garbage first, and reports the minimum, with the median for the
#   spread.
# - The races' winners followed from how Lua works: allocation in loops, copying arguments, a
#   linear search against a table lookup, and string keys against the array part.
# - The collector reclaims temporary tables while a loop runs; its mode depends on the build.
# - The word counter's speedup came from two algorithmic changes, not from local tricks.
#
# Next, do the [Module 12 practice](practice.md).
