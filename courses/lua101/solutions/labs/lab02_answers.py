# %% [markdown]
# # Lab 2: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L2.1
#
# - `1, 10, 3` runs 4 times (1, 4, 7, 10): the bound is reached exactly.
# - `10, 1` runs 0 times: the default step is +1, and 10 is already past 1.
# - `1, 3.5` runs 3 times (1, 2, 3): the integer start and step make an integer loop, and 4 > 3.5.
# - `5, 1, -2` runs 3 times (5, 3, 1).
# - `0, 1, 0.25` runs 5 times: 0.25 is exact in binary, so the last pass is exactly 1.0.
# - `0, 0.3, 0.1` runs 3 times, not 4: the fourth value would be 0.30000000000000004 > 0.3.
# - `1, 1` runs once; `-3, 3, 3` runs 3 times (-3, 0, 3); `1, 0, -1` runs twice (1, 0).
# - `2, 8, 2.5` runs 3 times (2.0, 4.5, 7.0): the float step makes it a float loop.
#
# The common mistake is predicting 4 for row 6 by counting 0, 0.1, 0.2, 0.3 on paper.

# %% tags=["answer-L2.1"]
# %%lua
loop_predictions = {
  { "1, 10, 3",    4 },
  { "10, 1",       0 },
  { "1, 3.5",      3 },
  { "5, 1, -2",    3 },
  { "0, 1, 0.25",  5 },
  { "0, 0.3, 0.1", 3 },
  { "1, 1",        1 },
  { "-3, 3, 3",    3 },
  { "1, 0, -1",    2 },
  { "2, 8, 2.5",   3 },
}

# %% [markdown]
# ## Exercise L2.2
#
# `two(), two()` gives 1 + 2 = 3 values; `(two())` gives 1; `none()` as the last item gives 0,
# but `none(), none()` gives 1, because the first call isn't last and is adjusted to one `nil`.
# `{ two(), two() }` is `{ 1, 1, 2 }`. `nil, nil` is 2 values, and `two(), nil` is 2.

# %% tags=["answer-L2.2"]
# %%lua
count_predictions = {
  { 'select("#", two())',         2 },
  { 'select("#", two(), two())',  3 },
  { 'select("#", (two()))',       1 },
  { 'select("#", none())',        0 },
  { 'select("#", none(), none())', 1 },
  { '#{ two(), two() }',          3 },
  { 'select("#", nil, nil)',      2 },
  { 'select("#", two(), nil)',    2 },
}

# %% [markdown]
# ## Exercise L2.3
#
# The early `return 0` handles the empty case, so the loop can assume at least one argument.
# Common mistakes: returning `0, nil, nil, nil` for no arguments (four values, not one), and
# computing the mean with `//`, which gives an integer.

# %% tags=["answer-L2.3"]
# %%lua
function stats(...)
  local n = select("#", ...)
  if n == 0 then
    return 0
  end
  local smallest = (select(1, ...))
  local largest = smallest
  local total = smallest
  for i = 2, n do
    local v = (select(i, ...))
    if v < smallest then smallest = v end
    if v > largest then largest = v end
    total = total + v
  end
  return n, smallest, largest, total / n
end

# %% [markdown]
# ## Exercise L2.4
#
# `acc = acc or 0` is safe here, because `false` is never a valid total. The recursive call is
# the whole `return` expression, so it is a proper tail call. A common mistake is
# `return sum_to(n - 1, acc) + n`, which is still not a tail call.

# %% tags=["answer-L2.4"]
# %%lua
function sum_to(n, acc)
  acc = acc or 0
  if n == 0 then return acc end
  return sum_to(n - 1, acc + n)
end

# %% [markdown]
# ## Exercise L2.5
#
# Only `border` needed a change: its default is `true`, so `or` overrode `false`.

# %% tags=["answer-L2.5"]
# %%lua
function make_label(opts)
  opts = opts or {}
  local text = opts.text or ""
  local upper = opts.upper or false
  local border = opts.border
  if border == nil then border = true end
  if upper then text = text:upper() end
  if border then text = "[" .. text .. "]" end
  return text
end

print(make_label{ text = "total" })
print(make_label{ text = "total", upper = true })
print(make_label{ text = "total", border = false })

# %% [markdown] tags=["answer-L2.5-why"]
# `opts.upper or false` turns a falsy `upper` into `false`, which is already the default, so it
# can't change the result; `opts.border or true` turns `false` into `true`, the opposite of what
# the caller asked for.
