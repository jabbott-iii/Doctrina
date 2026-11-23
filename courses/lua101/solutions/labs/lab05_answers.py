# %% [markdown]
# # Lab 5: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L5.1
#
# 1. 1: `a` and `b` come from two calls, so they have two counts.
# 2. 2: `d` is the same closure as `c`, so they share one count.
# 3. 20: the closure captured the variable `x`, which changed before the call.
# 4. 20: each pass of the numeric `for` has its own `i`, so `fs[2]` sees 2.
# 5. 4: the `while` loop's `i` is one variable, which is 4 when the loop ends.
# 6. 7: `get` and `set` share a value; `get2` comes from another call and holds 0.
# 7. 6: `adder(3)(1)` is 4, and `adder(2)(4)` is 6.
# 8. `"ab"`: each pass of the generic `for` has its own `w`.
#
# The common mistakes are 1 for snippet 5, as if each closure kept the value of its own pass, and
# 3 for snippet 4.

# %% tags=["answer-L5.1"]
# %%lua
closure_predictions = {
  { [[local a, b = new_counter(), new_counter(); a(); a(); return b()]], 1 },
  { [[local c = new_counter(); local d = c; c(); return d()]], 2 },
  { [[local x = 10; local f = function() return x end; x = 20; return f()]], 20 },
  { [[local fs = {}; for i = 1, 3 do fs[i] = function() return i * 10 end end; return fs[2]()]], 20 },
  { [[local fs, i = {}, 1; while i <= 3 do fs[i] = function() return i end; i = i + 1 end; return fs[1]()]], 4 },
  { [[local get, set = make_box(0); set(7); local get2 = make_box(0); return get() + get2()]], 7 },
  { [[local function adder(n) return function(x) return x + n end end; return adder(2)(adder(3)(1))]], 6 },
  { [[local fs = {}; for _, w in ipairs({ "a", "b" }) do fs[#fs + 1] = function() return w end end; return fs[1]() .. fs[2]()]], "ab" },
}

# %% [markdown]
# ## Exercise L5.2
#
# `reduce` chooses its starting point once, then runs one loop. `compose` packs its functions, and
# packs the values between steps, so a `nil` in the middle survives `table.unpack`. Common
# mistakes: `if not initial`, which treats an `initial` of `false` as missing; `{...}` with `#`,
# which loses trailing `nil`s; and applying the functions left to right.

# %% tags=["answer-L5.2"]
# %%lua
function reduce(list, fn, initial)
  local acc, start = initial, 1
  if acc == nil then
    acc, start = list[1], 2
  end
  for i = start, #list do
    acc = fn(acc, list[i])
  end
  return acc
end

function compose(...)
  local fns = table.pack(...)
  return function(...)
    local values = table.pack(...)
    for i = fns.n, 1, -1 do
      values = table.pack(fns[i](table.unpack(values, 1, values.n)))
    end
    return table.unpack(values, 1, values.n)
  end
end

# %% [markdown]
# ## Exercise L5.3
#
# `NIL` is a table made once, so it equals nothing else and can stand for `nil` in the cache.
# `memo_fib` calls itself through the global, which by then holds the memoized function, so
# each `n` is computed once: 31 calls for `n` from 0 to 30. Common mistakes: storing `nil`
# directly, which passes the Fibonacci checks but not the `nil` one; memoizing `slow_fib`, whose
# recursive calls bypass the cache; and one cache shared by every memoized function, declared
# outside `memoize`.

# %% tags=["answer-L5.3"]
# %%lua
function memoize(fn)
  local NIL = {}
  local cache = {}
  return function(x)
    local result = cache[x]
    if result == nil then
      result = fn(x)
      if result == nil then result = NIL end
      cache[x] = result
    end
    if result == NIL then return nil end
    return result
  end
end

memo_fib = memoize(function(n)
  fib_calls = fib_calls + 1
  if n < 2 then return n end
  return memo_fib(n - 1) + memo_fib(n - 2)
end)

# %% [markdown]
# ## Exercise L5.4
#
# `value` holds the next value to return, and the closure moves it on by `step` after each one.
# The sign of `step` decides which way to compare with `to`. Common mistakes: comparing with `<=`
# even for a negative step, which visits nothing for `range(5, 1, -2)`; and forgetting the default
# step.

# %% tags=["answer-L5.4"]
# %%lua
function range(from, to, step)
  step = step or 1
  if step == 0 then error("range: step is 0") end
  local value = from
  return function()
    if (step > 0 and value > to) or (step < 0 and value < to) then return nil end
    local current = value
    value = value + step
    return current
  end
end

# %% [markdown]
# ## Exercise L5.5
#
# The step function is a local defined once, so every call of `reverse_ipairs` returns the same
# function. Common mistakes: defining the step function inside `reverse_ipairs`, which works in a
# loop but makes a new closure each time; and starting the control value at `#list`, which skips
# the last item.

# %% tags=["answer-L5.5"]
# %%lua
local function reverse_step(list, i)
  i = i - 1
  if i >= 1 then return i, list[i] end
end

function reverse_ipairs(list)
  return reverse_step, list, #list + 1
end

# %% [markdown] tags=["answer-L5.5-why"]
# `reverse_step` receives everything it needs, the list and the last index, as arguments on every
# call, so it keeps nothing between calls and one function serves any number of loops. `range`'s
# iterator keeps its next value in an upvalue that each call changes, so each loop needs a closure
# with a variable of its own.
