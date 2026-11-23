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
# # Lab 8: Objects and classes
#
# **Objectives:** LO-8.1, LO-8.2, LO-8.3\
# **Prerequisites:** the [Module 8 reading](index.md) and [Lab 7](../07-metatables/lab07.ipynb)\
# **Time:** about 2 hours
#
# You will write a stack class, a subclass that limits its size, the same limited stack by
# composition, and a stack whose state hides in closures, and then measure what each kind of
# object costs. As in the earlier labs, each check cell prints `passed` or fails with a message,
# and the checks fail until you finish their exercise.

# %% [markdown]
# ## Setup
#
# Section 5 measures time and memory, so its numbers depend on your machine. The second cell
# prints the Lua version, which should be `Lua 5.4`, and defines `is_instance` from the reading.

# %%
# %load_ext lualab
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% language="lua"
# print(_VERSION)
#
# function is_instance(object, class)
#   local mt = getmetatable(object)
#   while mt do
#     if mt == class then return true end
#     local parent = getmetatable(mt)
#     mt = parent and parent.__index
#   end
#   return false
# end

# %% [markdown]
# ## 1. A class
#
# ### Exercise L8.1 (LO-8.1, ★★, about 25 minutes)
#
# Write the class `Stack`. Its objects hold any values except `nil`:
#
# - `Stack.new()` returns a new, empty stack.
# - `s:push(v)` adds `v` on top; `s:pop()` removes and returns the top value, or returns `nil` when
#   `s` is empty; `s:peek()` returns the top value without removing it; and `s:size()` returns the
#   number of values.
# - `#s` is the same as `s:size()`, and `tostring(s)` lists the values from the bottom up, as in
#   `Stack(1, 2, 3)`; an empty stack is `Stack()`.
#
# Keep the methods in `Stack`, not in each object.
#
# <details>
# <summary>Hint</summary>
#
# Give each object its own list and count in `Stack.new`: `{ items = {}, n = 0 }`. `__len` and
# `__tostring` go in `Stack` too, since `Stack` is every stack's metatable.
# </details>

# %% tags=["answer-L8.1"] language="lua"
# Stack = {}
# Stack.__index = Stack
#
# function Stack.new()
#   -- your code here
# end
#
# -- your code here: push, pop, peek, size, __len, and __tostring

# %% tags=["raises-exception"] language="lua"
# local s = Stack.new()
# assert(getmetatable(s) == Stack, "Stack.new() should return an object whose metatable is Stack")
# assert(s:size() == 0 and #s == 0 and s:pop() == nil and s:peek() == nil, "a new stack is empty")
# s:push(1); s:push(2); s:push(3)
# assert(s:size() == 3 and #s == 3 and s:peek() == 3, "three pushes: size 3, 3 on top")
# assert(tostring(s) == "Stack(1, 2, 3)", "tostring lists the values from the bottom up")
# assert(s:pop() == 3 and s:pop() == 2 and s:size() == 1, "pop removes from the top")
# assert(tostring(Stack.new()) == "Stack()", "an empty stack is Stack()")
# local t = Stack.new()
# t:push("x")
# assert(s:size() == 1 and s:peek() == 1 and t:size() == 1 and t:peek() == "x",
#   "two stacks must not share state")
# for _, name in ipairs({ "push", "pop", "peek", "size" }) do
#   assert(rawget(s, name) == nil and type(Stack[name]) == "function",
#     name .. " should live in Stack, not in each object")
# end
# s:push(false)
# assert(s:peek() == false and s:size() == 2, "false is a value like any other")
# assert(tostring(s) == "Stack(1, false)", "tostring must handle false too")
# print("passed")

# %% [markdown]
# ## 2. A subclass
#
# ### Exercise L8.2 (LO-8.2, ★★, about 25 minutes)
#
# Write `BoundedStack`, a subclass of `Stack` whose objects hold at most `limit` values.
# `BoundedStack.new(limit)` returns a new, empty bounded stack. Its `push` raises the error
# `"stack is full"` at level 2 when the stack already holds `limit` values; every other method,
# `#`, and `tostring` work as for `Stack`. Don't change `Stack`.
#
# <details>
# <summary>Hint</summary>
#
# Follow the reading's `Savings`. Build the object with `Stack.new()`, then give it the metatable
# `BoundedStack`. Remember which two metamethods a subclass must copy.
# </details>

# %% tags=["answer-L8.2"] language="lua"
# BoundedStack = setmetatable({}, { __index = Stack })
# BoundedStack.__index = BoundedStack
#
# -- your code here

# %% tags=["raises-exception"] language="lua"
# local b = BoundedStack.new(2)
# assert(getmetatable(b) == BoundedStack, "BoundedStack.new should return a BoundedStack")
# assert(is_instance(b, BoundedStack) and is_instance(b, Stack), "a bounded stack is a Stack")
# b:push("a"); b:push("b")
# local ok, err = pcall(load("bounded:push('c')", "=caller", "t", { bounded = b }))
# assert(not ok and err == "caller:1: stack is full",
#   "pushing onto a full stack should raise 'stack is full' at level 2; got " .. tostring(err))
# assert(b:size() == 2 and b:peek() == "b", "the failed push must change nothing")
# assert(#b == 2 and tostring(b) == "Stack(a, b)", "# and tostring must work as for Stack")
# assert(b:pop() == "b", "pop is inherited")
# b:push("c")
# assert(b:peek() == "c", "after a pop there is room again")
# local plain = Stack.new()
# for i = 1, 10 do plain:push(i) end
# assert(plain:size() == 10 and rawget(Stack, "limit") == nil, "Stack itself must stay unlimited")
# local roomy = BoundedStack.new(5)
# for i = 1, 5 do roomy:push(i) end
# assert(roomy:size() == 5 and b:size() == 2, "each bounded stack must keep its own limit")
# print("passed")

# %% [markdown]
# ## 3. The same design by composition
#
# ### Exercise L8.3 (LO-8.2, ★★, about 25 minutes)
#
# Write `LimitedStack`, which does the job of `BoundedStack` by composition: each object holds a
# `Stack` in its field `stack`, and offers only `push`, `pop`, and `size`, forwarding each to the
# stack. `LimitedStack.new(limit)` returns a new, empty limited stack, and `push` raises
# `"stack is full"` at level 2 like `BoundedStack`'s. Then answer the question in the Markdown
# cell after the check.

# %% tags=["answer-L8.3"] language="lua"
# LimitedStack = {}
# LimitedStack.__index = LimitedStack
#
# -- your code here

# %% tags=["raises-exception"] language="lua"
# local l = LimitedStack.new(2)
# assert(getmetatable(l.stack) == Stack, "each limited stack should hold a Stack in its field stack")
# l:push(1); l:push(2)
# local ok, err = pcall(load("limited:push(3)", "=caller", "t", { limited = l }))
# assert(not ok and err == "caller:1: stack is full", "a full stack should raise 'stack is full' at level 2")
# assert(l:size() == 2 and l:pop() == 2 and l:size() == 1, "push, pop, and size work")
# assert(l.peek == nil, "LimitedStack offers only push, pop, and size")
# assert(not is_instance(l, Stack), "a limited stack has a Stack; it isn't one")
# assert(LimitedStack.new(1).stack ~= l.stack, "each limited stack needs a Stack of its own")
# print("passed")

# %% [markdown] tags=["answer-L8.3-why"]
# *Your answer here: an editor keeps an undo history that must never hold more than 100 changes,
# and must never be read except from the top. Would you build it from `BoundedStack` or from
# `LimitedStack`? Defend your choice in two or three sentences.*

# %% [markdown]
# ## 4. Private state
#
# ### Exercise L8.4 (LO-8.3, ★★, about 20 minutes)
#
# Write `new_private_stack()`, which returns a stack whose items and count live in closures, not in
# any table that the caller can reach. The object is a table of three functions, called with a dot:
# `s.push(v)`, `s.pop()`, which returns `nil` when the stack is empty, and `s.size()`.

# %% tags=["answer-L8.4"] language="lua"
# function new_private_stack()
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local s = new_private_stack()
# assert(s.size() == 0 and s.pop() == nil, "a new stack is empty")
# s.push("a"); s.push("b")
# assert(s.size() == 2 and s.pop() == "b" and s.pop() == "a" and s.size() == 0, "push, pop, size")
# local t = new_private_stack()
# s.push(1)
# assert(t.size() == 0, "two stacks must not share state")
# for name, value in pairs(s) do
#   assert(type(value) == "function", "the field '" .. tostring(name) .. "' exposes the state")
# end
# assert(getmetatable(s) == nil, "a closure-based object needs no metatable")
# print("passed")

# %% [markdown]
# ## 5. What each kind of object costs
#
# The next cell builds 10,000 counters of each kind, both with four methods, and measures the
# memory each takes and the time 5 million calls take. Before you run it, predict: which kind takes
# more memory per object, and about how many times more? Which call is faster? The cell takes about
# a second.

# %% language="lua"
# local Counter = {}
# Counter.__index = Counter
# function Counter.new() return setmetatable({ count = 0 }, Counter) end
# function Counter:increment() self.count = self.count + 1 end
# function Counter:decrement() self.count = self.count - 1 end
# function Counter:reset() self.count = 0 end
# function Counter:get() return self.count end
#
# local function new_closure_counter()
#   local count = 0
#   return {
#     increment = function() count = count + 1 end,
#     decrement = function() count = count - 1 end,
#     reset = function() count = 0 end,
#     get = function() return count end,
#   }
# end
#
# local function bytes_per_object(make, n)
#   collectgarbage(); collectgarbage()
#   local before = collectgarbage("count")     -- kilobytes in use
#   local keep = {}
#   for i = 1, n do keep[i] = make() end
#   collectgarbage(); collectgarbage()
#   return (collectgarbage("count") - before) * 1024 / n, keep
# end
#
# local n = 10000
# print(string.format("bytes per counter: metatable %.0f, closures %.0f",
#   bytes_per_object(Counter.new, n), bytes_per_object(new_closure_counter, n)))
#
# local a, b = Counter.new(), new_closure_counter()
# local start = os.clock()
# for _ = 1, 5000000 do a:increment() end
# local middle = os.clock()
# for _ = 1, 5000000 do b.increment() end
# print(string.format("5 million calls: metatable %.3f s, closures %.3f s",
#   middle - start, os.clock() - middle))

# %% [markdown]
# Both memory figures include the slot each counter takes in the list `keep`. Change `n`, or add a
# fifth method to both kinds, and run the cell again: the closure-based counter grows with every
# method, and the metatable-based one doesn't.
#
# ## Summary
#
# - A class is a table of methods that serves as its objects' metatable; each object holds only
#   its own data, and methods take the object as `self`.
# - A subclass falls back on its parent through `__index`, overrides by redefining, and must copy
#   the metamethods it keeps, such as `__len` and `__tostring`.
# - Composition holds a part and forwards only the methods it chooses, so the object isn't an
#   instance of the part's class, and exposes nothing else.
# - Closure-based objects hide their state completely, and their calls are faster, but every object
#   pays for its own closures.
#
# Next, do the [Module 8 practice](practice.md).
