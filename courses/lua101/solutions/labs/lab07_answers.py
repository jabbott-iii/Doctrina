# %% [markdown]
# # Lab 7: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L7.1
#
# A binary operator passes its operands in their original order, whichever one has the
# metamethod, so `1 + t` gives `"__add(number, table)"`. `__index` gets the table and the key, and
# `__call` gets the table followed by the call's arguments. Comparisons convert the metamethod's
# string to `true`. `t == t` is `true` without a call, because a table is always equal to itself,
# and `t == 1` is `false` without a call, because `__eq` runs only for two tables. `t ~= u` is
# `not (t == u)`, so `false`.
#
# The common mistakes are `"__add(table, number)"` for `1 + t`, and a string for `t == u`.

# %% tags=["answer-L7.1"]
# %%lua
metamethod_predictions = {
  { [[t + 1]],     "__add(table, number)" },
  { [[1 + t]],     "__add(number, table)" },
  { [[t .. "!"]],  "__concat(table, string)" },
  { [["x" .. t]],  "__concat(string, table)" },
  { [[t.color]],   "__index(table, string)" },
  { [[t[1] ]],     "__index(table, number)" },
  { [[t(1, 2)]],   "__call(table, number, number)" },
  { [[t == u]],    true },
  { [[t == t]],    true },
  { [[t == 1]],    false },
  { [[t ~= u]],    false },
  { [[u < t]],     true },
}

# %% [markdown]
# ## Exercise L7.2
#
# Every metamethod builds its result with `vec`, so results are vectors and operands never change.
# Common mistakes: a `__mul` that handles only `a * 2`, so `2 * a` fails with
# `attempt to index a number value`; and `__eq` written as `a == b`, which calls `__eq` again and
# overflows the stack.

# %% tags=["answer-L7.2"]
# %%lua
vector_mt = {}

function vec(x, y)
  return setmetatable({ x = x, y = y }, vector_mt)
end

function vector_mt.__add(a, b) return vec(a.x + b.x, a.y + b.y) end
function vector_mt.__sub(a, b) return vec(a.x - b.x, a.y - b.y) end

function vector_mt.__mul(a, b)
  if type(a) == "number" then return vec(a * b.x, a * b.y) end
  if type(b) == "number" then return vec(a.x * b, a.y * b) end
  return a.x * b.x + a.y * b.y
end

function vector_mt.__unm(a) return vec(-a.x, -a.y) end
function vector_mt.__eq(a, b) return a.x == b.x and a.y == b.y end
function vector_mt.__tostring(a) return "(" .. a.x .. ", " .. a.y .. ")" end

# %% [markdown]
# ## Exercise L7.3
#
# `setmetatable` returns its table, so the function is one line. Common mistakes:
# `__index = default`, which works only when `default` is a table, and is wrong even then; and an
# `__index` function that stores the default with `rawset`, which the check catches.

# %% tags=["answer-L7.3"]
# %%lua
function with_default(t, default)
  return setmetatable(t, { __index = function() return default end })
end

# %% [markdown]
# ## Exercise L7.4
#
# `views` maps each original table to its view; its weak keys let a forgotten original be
# collected, and because each view refers to its original only through upvalues of its own
# metamethods, the table is an ephemeron and the pair goes together. Common mistakes: making a new
# view on every read, which fails `ro.window == ro.window`; wrapping values in `__index` but not in
# `__pairs`; and `__newindex` raising the error at level 1, which names the lab's cell instead of
# the caller.

# %% tags=["answer-L7.4"]
# %%lua
local views = setmetatable({}, { __mode = "k" })

local function refuse()
  error("attempt to change a read-only table", 2)
end

function deep_read_only(t)
  if type(t) ~= "table" then return t end
  local view = views[t]
  if view then return view end
  view = setmetatable({}, {
    __index = function(_, k) return deep_read_only(t[k]) end,
    __newindex = refuse,
    __len = function() return #t end,
    __pairs = function()
      return function(_, k)
        local key, value = next(t, k)
        if key ~= nil then return key, deep_read_only(value) end
      end, nil, nil
    end,
  })
  views[t] = view
  return view
end

# %% [markdown]
# ## Exercise L7.5
#
# - `by_key` keeps the entry for `kept`, which is still referenced, and the entry under the string
#   key `name`, since strings are never removed and the values of a weak-key table are strong. The
#   entry under the new `{}` key goes: 2 entries.
# - `by_value` loses only `lost`, whose value was referenced nowhere else; the string and the
#   number stay, and `kept` is still referenced.
# - `owners` loses both entries. The second value refers to its own key, but a weak-key table is
#   an ephemeron table, so that reference doesn't keep the key alive: 0 entries.
# - `strong` isn't weak, so its entry stays: 1 entry.
#
# The common mistakes are 1 for `by_key_entries`, as if the string key were collected, and 1 for
# `owners_entries`.

# %% tags=["answer-L7.5"]
# %%lua
weak_predictions = {
  { "by_key_entries",  2 },
  { "by_key_name",     true },
  { "by_value_kept",   true },
  { "by_value_lost",   false },
  { "by_value_text",   true },
  { "by_value_number", true },
  { "owners_entries",  0 },
  { "strong_entries",  1 },
}
