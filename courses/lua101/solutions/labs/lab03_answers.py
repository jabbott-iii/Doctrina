# %% [markdown]
# # Lab 3: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L3.1
#
# - Rows 1, 2, 5, 6, 7, 8, and 10 are sequences. `{}` and `{ x = 1, y = 2 }` have the single
#   border 0, because `t[1]` is absent; the field `n`, the key 0, and the string keys don't count.
# - `{ 10, 20, nil }` is a sequence of length 2: a trailing `nil` leaves no value after it, so it
#   makes no hole.
# - `{ 10, nil, 30 }` has the borders 1 and 3; `{ nil, 20 }` has 0 and 2; and
#   `{ [1] = "a", [2] = "b", [4] = "d" }` has 2 and 4.
# - `{ [2.0] = "b", [1] = "a" }` is the sequence `{ "a", "b" }`, because the key 2.0 becomes the
#   integer 2.
#
# The common mistakes are counting the values (3 for `{ 10, nil, 30 }` only) instead of finding
# the borders, and counting the field `n` or the key 0.

# %% tags=["answer-L3.1"]
# %%lua
border_predictions = {
  { '{ 10, 20, 30 }',                    { 3 } },
  { '{}',                                { 0 } },
  { '{ 10, nil, 30 }',                   { 1, 3 } },
  { '{ nil, 20 }',                       { 0, 2 } },
  { '{ x = 1, y = 2 }',                  { 0 } },
  { '{ [0] = "zero", "one", "two" }',    { 2 } },
  { '{ 10, 20, nil }',                   { 2 } },
  { '{ n = 3, 10, 20, 30 }',             { 3 } },
  { '{ [1] = "a", [2] = "b", [4] = "d" }', { 2, 4 } },
  { '{ [2.0] = "b", [1] = "a" }',        { 2 } },
}

# %% [markdown]
# ## Exercise L3.2
#
# Collect the names that pass the filter, sort them, then build the lines. Reading `stock[name]`
# after sorting is fine, because sorting `names` doesn't change `stock`. Common mistakes: joining
# with `..` in the loop and leaving a newline at the end, and printing inside `report` instead of
# returning the string.

# %% tags=["answer-L3.2"]
# %%lua
function report(stock)
  local names = {}
  for name, count in pairs(stock) do
    if count ~= 0 then names[#names + 1] = name end
  end
  table.sort(names)
  local lines = {}
  for i, name in ipairs(names) do
    lines[i] = name .. ": " .. stock[name]
  end
  return table.concat(lines, "\n")
end

print(report(inventory))

# %% [markdown]
# ## Exercise L3.3
#
# `b` is `a`, so `b[1] = 10` changes `a[1]`, and `a == b`. `c` is a separate table, so `a == c`
# is `false` even though they started with the same contents. `grow` appends through the shared
# reference, so `#c` is 4, but `replace` only points its parameter at a new table, so `c[1]` is
# still 1. The shallow copy is a new table (`shallow == nested` is `false`) whose `inner` is the
# original's `inner`, so writing through it changed `nested.inner[1]` to 50.
#
# The common mistake is predicting `#c == 1` and `c[1] == 0`, as if `replace` changed the
# caller's variable.

# %% tags=["answer-L3.3"]
# %%lua
alias_predictions = {
  { "a[1]",                          10 },
  { "a == b",                        true },
  { "a == c",                        false },
  { "#c",                            4 },
  { "c[1]",                          1 },
  { "nested.inner[1]",               50 },
  { "shallow == nested",             false },
  { "shallow.inner == nested.inner", true },
}

# %% [markdown]
# ## Exercise L3.4
#
# The order of the two new lines matters: `seen[value] = copy` must come before the loop, so that
# a table that contains itself finds its copy when the loop reaches it. Common mistakes: storing
# the copy in `seen` only after the loop, which still overflows the stack; creating a new `seen`
# in every call by not passing it on; and passing `seen` for values but not for keys.

# %% tags=["answer-L3.4"]
# %%lua
function deep_copy(value, seen)
  if type(value) ~= "table" then return value end
  seen = seen or {}
  if seen[value] then return seen[value] end
  local copy = {}
  seen[value] = copy
  for k, v in pairs(value) do
    copy[deep_copy(k, seen)] = deep_copy(v, seen)
  end
  return copy
end

# %% [markdown]
# ## Exercise L3.5
#
# The queue is the reading's, with a size. `last - first + 1` is the count, which is 0 when the
# queue is empty because `first` is then `last + 1`. Common mistakes: testing emptiness with
# `if not q.items[q.first]`, which treats a queued `false` as empty; and `table.remove(q.items, 1)`,
# which passes the order tests but took 1.9 s for the timed part on an Intel Core i7-11800H.

# %% tags=["answer-L3.5"]
# %%lua
function queue_new()
  return { first = 1, last = 0, items = {} }
end

function queue_push(q, value)
  q.last = q.last + 1
  q.items[q.last] = value
end

function queue_pop(q)
  if q.first > q.last then return nil end
  local value = q.items[q.first]
  q.items[q.first] = nil
  q.first = q.first + 1
  return value
end

function queue_size(q)
  return q.last - q.first + 1
end

# %% [markdown]
# ## Exercise L3.6
#
# The original stored one `row` table in every `m[i]`, so `grid[2][1]` printed 7. Creating the row
# inside the outer loop gives each row its own table. `transpose` builds each new row from one
# column of `m`. A common mistake is `t[j][i] = m[i][j]` before `t[j]` exists, which stops with
# `attempt to index a nil value (field '?')`.

# %% tags=["answer-L3.6"]
# %%lua
function new_matrix(rows, cols, fill)
  local m = {}
  for i = 1, rows do
    local row = {}
    for j = 1, cols do row[j] = fill end
    m[i] = row
  end
  return m
end

function transpose(m)
  local t = {}
  for j = 1, #m[1] do
    local row = {}
    for i = 1, #m do row[i] = m[i][j] end
    t[j] = row
  end
  return t
end

local grid = new_matrix(2, 3, 0)
grid[1][1] = 7
print(grid[1][1], grid[2][1])
