# %% [markdown]
# # Lab 12: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L12.1
#
# Collect the times, sort them, and read the minimum and the middle. Common mistakes: calling
# `collectgarbage()` inside the timed region, which adds the collection to the time; and, for an
# even number of runs, taking one of the two middle times instead of their mean.

# %% tags=["answer-L12.1"]
# %%lua
function bench(fn, runs)
  runs = runs or 5
  local times = {}
  for i = 1, runs do
    collectgarbage()
    local start = os.clock()
    fn()
    times[i] = os.clock() - start
  end
  table.sort(times)
  local middle = (runs + 1) // 2
  local median = times[middle]
  if runs % 2 == 0 then
    median = (times[middle] + times[middle + 1]) / 2
  end
  return times[1], median
end

# %% [markdown]
# ## Exercise L12.2
#
# 1. A: `table.insert` is a function call that also computes `#t`.
# 2. B: each `select(i, ...)` copies the remaining arguments, so the loop is quadratic.
# 3. B: every `function … end` allocates a closure.
# 4. B uses more memory: string keys live in the hash part, and each string is an object too.
# 5. B: `..` copies the growing string on every pass.
# 6. B: the set finds each name in one hash lookup; the list is searched from the start.
#
# Races 2, 3, 5, and 6 usually win by ten times or more; race 1 by two to four times. The common
# mistake is A for race 1, from the belief that the library function is the optimized way.

# %% tags=["answer-L12.2"]
# %%lua
race_predictions = { "A", "B", "B", "B", "B", "B" }

# %% [markdown]
# ## Exercise L12.3
#
# Two changes do almost all the work. First, a table that maps each word to its count replaces the
# linear search through `counts`, which made the loop $O(n \cdot k)$ for $k$ distinct words; on the
# test machine that took the best of five runs from 0.27 s to 0.007 s. Second, `table.concat`
# replaces `..`
# in the output loop. Sorting a list of the distinct words, with the counts looked up in the
# comparator, keeps the order identical. Caching `string.lower` in a local made no measurable
# difference, and is left out.

# %% tags=["answer-L12.3"]
# %%lua
function fast_histogram(words)
  local counts, distinct = {}, {}
  for i = 1, #words do
    local w = words[i]:lower()
    local n = counts[w]
    if n == nil then
      distinct[#distinct + 1] = w
      counts[w] = 1
    else
      counts[w] = n + 1
    end
  end
  table.sort(distinct, function(a, b)
    if counts[a] ~= counts[b] then return counts[a] > counts[b] end
    return a < b
  end)
  local lines = {}
  for i, w in ipairs(distinct) do
    lines[i] = w .. " " .. counts[w] .. "\n"
  end
  return table.concat(lines)
end

# %% [markdown] tags=["answer-L12.3-why"]
# 1. A table from each word to its count instead of searching a list: the loop over 20,000 words
#    no longer compares each with up to 2,000 entries. Measured: 0.27 s to 0.007 s.
# 2. `table.concat` for the output instead of `..` in a loop: 0.007 s to 0.0045 s, a smaller gain
#    because the output is only 2,000 lines.
# 3. Caching `string.lower` in a local: no difference beyond the noise, so not kept.
