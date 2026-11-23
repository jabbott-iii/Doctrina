# %% [markdown]
# # Lab 8: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L8.1
#
# Each object keeps its own list and an explicit count, so that `pop` and `size` never depend on
# `#`. Common mistakes: putting `items = {}` in `Stack` as a default, which every stack then
# shares; defining the methods inside `Stack.new`, which stores a copy in every object; and
# `__tostring` with `table.concat(self.items, ", ")`, which fails on a stack that holds `false`.

# %% tags=["answer-L8.1"]
# %%lua
Stack = {}
Stack.__index = Stack

function Stack.new()
  return setmetatable({ items = {}, n = 0 }, Stack)
end

function Stack:push(v)
  self.n = self.n + 1
  self.items[self.n] = v
end

function Stack:pop()
  if self.n == 0 then return nil end
  local v = self.items[self.n]
  self.items[self.n] = nil
  self.n = self.n - 1
  return v
end

function Stack:peek()
  return self.items[self.n]
end

function Stack:size()
  return self.n
end

function Stack.__len(s)
  return s.n
end

function Stack.__tostring(s)
  local parts = {}
  for i = 1, s.n do parts[i] = tostring(s.items[i]) end
  return "Stack(" .. table.concat(parts, ", ") .. ")"
end

# %% [markdown]
# ## Exercise L8.2
#
# The constructor reuses `Stack.new`, the override checks the limit and then calls the parent's
# `push` with an explicit `self`, and the two metamethods are copied because Lua reads them raw.
# Common mistakes: forgetting to copy `__len` and `__tostring`; calling `self:push(v)` inside the
# override, which recurses until the stack overflows; and storing `limit` in `BoundedStack`, which
# gives every bounded stack the same limit.

# %% tags=["answer-L8.2"]
# %%lua
BoundedStack = setmetatable({}, { __index = Stack })
BoundedStack.__index = BoundedStack
BoundedStack.__len = Stack.__len
BoundedStack.__tostring = Stack.__tostring

function BoundedStack.new(limit)
  local s = Stack.new()
  s.limit = limit
  return setmetatable(s, BoundedStack)
end

function BoundedStack:push(v)
  if self:size() >= self.limit then
    error("stack is full", 2)
  end
  Stack.push(self, v)
end

# %% [markdown]
# ## Exercise L8.3
#
# Three forwarding methods and a constructor. A common mistake is making `LimitedStack` inherit
# from `Stack` after all, which gives it `peek` and makes it an instance of `Stack`.

# %% tags=["answer-L8.3"]
# %%lua
LimitedStack = {}
LimitedStack.__index = LimitedStack

function LimitedStack.new(limit)
  return setmetatable({ stack = Stack.new(), limit = limit }, LimitedStack)
end

function LimitedStack:push(v)
  if self.stack:size() >= self.limit then
    error("stack is full", 2)
  end
  self.stack:push(v)
end

function LimitedStack:pop()
  return self.stack:pop()
end

function LimitedStack:size()
  return self.stack:size()
end

# %% [markdown] tags=["answer-L8.3-why"]
# `LimitedStack`, by composition. The history must never be read except from the top, and a
# `BoundedStack` inherits every method of `Stack`, including any that a later change adds, while
# `LimitedStack` offers only the three it forwards, so no code can misuse the history. Accept an
# answer for `BoundedStack` only if it argues that the history must be usable everywhere a `Stack`
# is.

# %% [markdown]
# ## Exercise L8.4
#
# `items` and `n` are locals of `new_private_stack`, reachable only through the three closures. The
# common mistake is `local self = { items = {}, n = 0 }` with methods that use `self.items`, which
# exposes the state the exercise asks to hide.

# %% tags=["answer-L8.4"]
# %%lua
function new_private_stack()
  local items, n = {}, 0
  local self = {}
  function self.push(v)
    n = n + 1
    items[n] = v
  end
  function self.pop()
    if n == 0 then return nil end
    local v = items[n]
    items[n] = nil
    n = n - 1
    return v
  end
  function self.size()
    return n
  end
  return self
end
