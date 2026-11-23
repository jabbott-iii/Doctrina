# %% [markdown]
# # Lab 9: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L9.1
#
# The first `resume` passes 4 as `first`, and the first `yield` hands out 40. The second passes
# `"hi"` as `got`, and the second `yield` hands out `"hi!"`. The third passes 2 and 3 as `a` and
# `b`, and the function returns 5, so the coroutine is dead. In `co2`, `"stop"` reaches the
# `error`, so `resume` returns `false` and the message, and the coroutine is dead.
#
# The common mistakes are `"true, 4"` for the first `resume`, as if `yield` handed out its
# argument unchanged, and `"suspended"` after the error.

# %% tags=["answer-L9.1"]
# %%lua
echo_predictions = {
  { [[coroutine.status(co)]],        "suspended" },
  { [[coroutine.resume(co, 4)]],     "true, 40" },
  { [[coroutine.resume(co, "hi")]],  "true, hi!" },
  { [[coroutine.status(co)]],        "suspended" },
  { [[coroutine.resume(co, 2, 3)]],  "true, 5" },
  { [[coroutine.status(co)]],        "dead" },
  { [[coroutine.resume(co)]],        "false, cannot resume dead coroutine" },
  { [[coroutine.resume(co2, 1)]],    "true, 10" },
  { [[coroutine.resume(co2, "x")]],  "true, x!" },
  { [[coroutine.resume(co2, "stop")]], "false, stopped" },
  { [[coroutine.status(co2)]],       "dead" },
}

# %% [markdown]
# ## Exercise L9.2
#
# The helper swaps each remaining item into position `k`, recurses, and swaps it back, so `copy`
# is restored after every branch. At the bottom it yields a fresh copy, since the loop may keep
# it while `copy` keeps changing. Common mistakes: yielding `copy` itself, so every kept ordering is
# the same table; swapping in `list` instead of a copy; and stopping at `k == n`, which yields each
# ordering before its last position is settled and gives the right count only by luck.

# %% tags=["answer-L9.2"]
# %%lua
function permutations(list)
  return coroutine.wrap(function()
    local copy = table.move(list, 1, #list, 1, {})
    local n = #copy
    local function place(k)
      if k > n then
        coroutine.yield(table.move(copy, 1, n, 1, {}))
        return
      end
      for i = k, n do
        copy[k], copy[i] = copy[i], copy[k]
        place(k + 1)
        copy[k], copy[i] = copy[i], copy[k]
      end
    end
    place(1)
  end)
end

# %% [markdown]
# ## Exercise L9.3
#
# Each stage is a loop over its source inside `wrap`. `chunked` yields a chunk as soon as it is
# full, and starts a new table, so it never reads ahead. Common mistakes: reusing one table for
# every chunk; forgetting the last, shorter chunk; and yielding an empty table for an empty
# source.

# %% tags=["answer-L9.3"]
# %%lua
function numbered(source)
  return coroutine.wrap(function()
    local n = 0
    for value in source do
      n = n + 1
      coroutine.yield(n .. ": " .. tostring(value))
    end
  end)
end

function chunked(size, source)
  return coroutine.wrap(function()
    local chunk = {}
    for value in source do
      chunk[#chunk + 1] = value
      if #chunk == size then
        coroutine.yield(chunk)
        chunk = {}
      end
    end
    if #chunk > 0 then coroutine.yield(chunk) end
  end)
end

# %% [markdown]
# ## Exercise L9.4
#
# The reading's loop, with the time limit tested before the earliest entry is removed, a counter,
# and a start delay. Common mistakes: removing the entry before testing `until_time`, which loses
# that task; testing with `>=`, which skips tasks due exactly at the limit; and sorting `waiting`
# with `table.sort`, which isn't stable, so tasks due at the same time can run out of order.

# %% tags=["answer-L9.4"]
# %%lua
function spawn(fn, delay)
  waiting[#waiting + 1] = { wake = now + (delay or 0), task = coroutine.create(fn) }
end

function run(until_time)
  local resumes = 0
  while #waiting > 0 do
    local next_index = 1
    for i = 2, #waiting do
      if waiting[i].wake < waiting[next_index].wake then next_index = i end
    end
    if until_time and waiting[next_index].wake > until_time then break end
    local entry = table.remove(waiting, next_index)
    now = entry.wake
    local ok, delay = coroutine.resume(entry.task)
    resumes = resumes + 1
    if not ok then error(delay, 0) end
    if coroutine.status(entry.task) ~= "dead" then
      entry.wake = now + (delay or 0)
      waiting[#waiting + 1] = entry
    end
  end
  return resumes
end

# %% [markdown] tags=["answer-L9.5-why"]
# `busy` was resumed first, at time 0, and kept control until its loop ended, because a coroutine
# gives control back only when it yields; the scheduler couldn't run `quick`, whatever its wake
# time. Calling `sleep(0)` inside the loop every million iterations or so would yield, let the
# scheduler run every task that is due, and then continue `busy`.
