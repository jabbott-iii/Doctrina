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
# # Lab 5: Closures and iterators
#
# **Objectives:** LO-5.1, LO-5.2, LO-5.3\
# **Prerequisites:** the [Module 5 reading](index.md) and
# [Lab 4](../04-strings-and-patterns/lab04.ipynb)\
# **Time:** about 2 hours
#
# You will predict what closures return, write `reduce` and a `compose` that takes any number of
# functions, count the calls a recursive function makes before and after memoizing it, and write
# a stateful and a stateless iterator. As in the earlier labs, each exercise ends with a check cell
# that prints `passed` or fails with a message, and the checks fail until you finish their
# exercise.

# %% [markdown]
# ## Setup
#
# Nothing in this lab is random. Section 3 measures time, so its numbers depend on your machine.
# The second cell prints the Lua version, which should be `Lua 5.4`.

# %%
# %load_ext lualab
import sys

import lupa

print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. What a closure sees
#
# The next cell defines two factories from the reading as globals, so the snippets below can use
# them. Run it, then try a few calls of your own, such as
# `local c = new_counter(); print(c(), c())`.

# %% language="lua"
# function new_counter()
#   local count = 0
#   return function()
#     count = count + 1
#     return count
#   end
# end
#
# function make_box(value)
#   local function get() return value end
#   local function set(new) value = new end
#   return get, set
# end

# %% [markdown]
# ### Exercise L5.1 (LO-5.1, ★★, about 15 minutes)
#
# Each snippet is a short program that ends by returning one value. Predict that value and replace
# its `"?"` with it: a number, or a string in quotes. Make all eight predictions before you run the
# check.

# %% tags=["answer-L5.1"] language="lua"
# closure_predictions = {
#   { [[local a, b = new_counter(), new_counter(); a(); a(); return b()]], "?" },
#   { [[local c = new_counter(); local d = c; c(); return d()]], "?" },
#   { [[local x = 10; local f = function() return x end; x = 20; return f()]], "?" },
#   { [[local fs = {}; for i = 1, 3 do fs[i] = function() return i * 10 end end; return fs[2]()]], "?" },
#   { [[local fs, i = {}, 1; while i <= 3 do fs[i] = function() return i end; i = i + 1 end; return fs[1]()]], "?" },
#   { [[local get, set = make_box(0); set(7); local get2 = make_box(0); return get() + get2()]], "?" },
#   { [[local function adder(n) return function(x) return x + n end end; return adder(2)(adder(3)(1))]], "?" },
#   { [[local fs = {}; for _, w in ipairs({ "a", "b" }) do fs[#fs + 1] = function() return w end end; return fs[1]() .. fs[2]()]], "?" },
# }

# %% tags=["raises-exception"] language="lua"
# local wrong, unanswered = 0, 0
# for n, row in ipairs(closure_predictions) do
#   local code, predicted = row[1], row[2]
#   local actual = load(code, "=snippet", "t")()
#   local verdict = "match"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= actual then
#     wrong, verdict = wrong + 1, "MISMATCH"
#   end
#   print(string.format("%d  you: %-5s Lua: %-5s %s", n, tostring(predicted), tostring(actual), verdict))
# end
# assert(unanswered == 0, unanswered .. " snippets still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# ## 2. Functions that combine functions
#
# ### Exercise L5.2 (LO-5.2, ★★, about 20 minutes)
#
# Write two global functions:
#
# - `reduce(list, fn, initial)` combines the items of `list` from left to right: starting from
#   `initial`, it replaces the running value `acc` with `fn(acc, item)` for each item, and returns
#   the last `acc`. When `initial` is `nil`, it starts from the first item and combines the rest.
#   With an empty list and no `initial`, it returns `nil`.
# - `compose(...)` takes any number of functions and returns one function that applies them from
#   right to left, passing every result of one to the next: `compose(f, g, h)(x)` is
#   `f(g(h(x)))`. `compose()` returns a function that returns its arguments unchanged.
#
# <details>
# <summary>Hint</summary>
#
# For `compose`, keep the functions with `table.pack(...)`, and inside the new function keep the
# current values the same way, so that a `nil` among them isn't lost. `table.unpack(t, 1, t.n)`
# gives them back.
# </details>

# %% tags=["answer-L5.2"] language="lua"
# function reduce(list, fn, initial)
#   -- your code here
# end
#
# function compose(...)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local function add(a, b) return a + b end
# assert(reduce({ 1, 2, 3, 4 }, add, 0) == 10, "reduce({ 1, 2, 3, 4 }, add, 0) should be 10")
# assert(reduce({ 1, 2, 3, 4 }, add) == 10, "without initial, start from the first item")
# assert(reduce({ "a", "b", "c" }, function(a, b) return a .. b end, "") == "abc", "left to right")
# assert(reduce({ 3, 1, 2 }, math.max) == 3, "reduce with math.max finds the largest")
# assert(reduce({}, add, 5) == 5, "an empty list gives initial")
# assert(reduce({}, add) == nil, "an empty list without initial gives nil")
# assert(reduce({}, add, false) == false, "an initial of false is a value, not a missing initial")
# assert(reduce({ 5 }, add) == 5, "one item without initial gives that item")
#
# local function inc(x) return x + 1 end
# local function double(x) return x * 2 end
# assert(compose(inc, double)(3) == 7, "compose(inc, double)(3) is inc(double(3)), 7")
# assert(compose(inc, double, inc)(3) == 9, "compose(inc, double, inc)(3) is inc(double(inc(3))), 9")
# assert(compose(math.max)(3, 9, 4) == 9, "every argument reaches the last function")
# assert(compose(tostring, math.max)(1, 5) == "5", "every result reaches the next function")
# local a, b, c = compose()(1, nil, 3)
# assert(a == 1 and b == nil and c == 3, "compose() returns its arguments unchanged")
# assert(select("#", compose()(1, nil)) == 2, "...including a nil at the end")
# assert(select("#", compose(function(...) return ... end)(nil, nil)) == 2, "no value may be lost")
# print("passed")

# %% [markdown]
# ## 3. Counting calls, then memoizing
#
# `slow_fib` adds one to the global `fib_calls` each time it is called. The cell after it computes
# three Fibonacci numbers and prints how many calls each took. Before you run it, predict: when `n`
# grows by 5, how many times more calls does `slow_fib(n)` make? The cell takes under a second.

# %% language="lua"
# fib_calls = 0
#
# function slow_fib(n)
#   fib_calls = fib_calls + 1
#   if n < 2 then return n end
#   return slow_fib(n - 1) + slow_fib(n - 2)
# end

# %% language="lua"
# print("  n      fib(n)       calls   seconds")
# for _, n in ipairs({ 20, 25, 30 }) do
#   fib_calls = 0
#   local start = os.clock()
#   local result = slow_fib(n)
#   print(string.format("%3d  %10d  %10d   %.3f", n, result, fib_calls, os.clock() - start))
# end

# %% [markdown]
# Each 5 more multiplies the calls by about 11, because the number of calls grows like the
# Fibonacci numbers themselves, by a factor of about 1.618 for each 1 added to `n`.
#
# ### Exercise L5.3 (LO-5.2, ★★★, about 25 minutes)
#
# 1. Write `memoize(fn)` for a function `fn` of one argument, which is never `nil`. It returns a
#    new function that calls `fn` at most once for each argument, and returns the cached result on
#    every later call, **including when the result is `nil` or `false`**.
# 2. Set the global `memo_fib` to a memoized Fibonacci function whose inner function adds one to
#    `fib_calls` on every call, as `slow_fib` does, and whose recursive calls go through the cache.
#
# <details>
# <summary>Hint 1</summary>
#
# The reading's `memoize` tests `cache[n] == nil`, which can't tell "not computed yet" from
# "computed, and the result was `nil`". Store a placeholder in the cache in place of `nil`: a new
# empty table, created once outside the returned function, is equal to nothing else.
# </details>
#
# <details>
# <summary>Hint 2</summary>
#
# Inside the inner function, call `memo_fib`, not `slow_fib`. The global `memo_fib` is looked up
# when the call happens, after you have assigned it.
# </details>

# %% tags=["answer-L5.3"] language="lua"
# function memoize(fn)
#   -- your code here
# end
#
# memo_fib = nil   -- your code here

# %% tags=["raises-exception"] language="lua"
# fib_calls = 0
# assert(memo_fib(30) == 832040, "memo_fib(30) should be 832040")
# assert(fib_calls == 31, "memo_fib(30) should call its inner function 31 times, not " .. fib_calls)
# memo_fib(30)
# assert(fib_calls == 31, "a second memo_fib(30) should take its result from the cache")
# assert(memo_fib(90) == 2880067194370816120, "memo_fib(90) should be 2880067194370816120")
# assert(fib_calls == 91, "memo_fib(90) needs only the 60 values the cache doesn't hold yet")
#
# local calls = 0
# local odd_is_nil = memoize(function(x)
#   calls = calls + 1
#   if x % 2 == 0 then return false end
#   return nil
# end)
# assert(odd_is_nil(1) == nil and odd_is_nil(1) == nil, "a nil result is returned as nil")
# assert(odd_is_nil(2) == false and odd_is_nil(2) == false, "a false result is returned as false")
# assert(calls == 2, "nil and false results must be cached too: fn ran " .. calls .. " times, not 2")
#
# local first_calls, second_calls = 0, 0
# local first = memoize(function(x) first_calls = first_calls + 1; return x end)
# local second = memoize(function(x) second_calls = second_calls + 1; return -x end)
# assert(first(4) == 4 and second(4) == -4, "each memoized function needs a cache of its own")
# print("passed")

# %% [markdown]
# ## 4. A stateful iterator
#
# ### Exercise L5.4 (LO-5.3, ★★, about 20 minutes)
#
# Write `range(from, to, step)`, which returns an iterator that the generic `for` can use to visit
# the same integers as the numeric `for i = from, to, step`. `step` defaults to 1, all three
# arguments are integers, and a step of 0 raises an error. Once the iterator has returned `nil`, it
# keeps returning `nil`.
#
# | Loop | Visits |
# | :- | :- |
# | `for v in range(1, 10, 3)` | 1, 4, 7, 10 |
# | `for v in range(5, 1, -2)` | 5, 3, 1 |
# | `for v in range(3, 3)` | 3 |
# | `for v in range(1, 0)` | nothing |
#
# <details>
# <summary>Hint</summary>
#
# Keep the next value in a local of `range`, and return a closure that tests it against `to`,
# which way depending on the sign of `step`.
# </details>

# %% tags=["answer-L5.4"] language="lua"
# function range(from, to, step)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local function visit(iterator)
#   local seen = {}
#   for v in iterator do seen[#seen + 1] = v end
#   return table.concat(seen, ",")
# end
# assert(visit(range(1, 10, 3)) == "1,4,7,10", "range(1, 10, 3) should visit 1, 4, 7, 10")
# assert(visit(range(5, 1, -2)) == "5,3,1", "range(5, 1, -2) should visit 5, 3, 1")
# assert(visit(range(3, 3)) == "3", "range(3, 3) visits 3 once")
# assert(visit(range(1, 0)) == "", "range(1, 0) visits nothing")
# for from = -3, 3 do
#   for to = -3, 3 do
#     for _, step in ipairs({ -2, -1, 1, 3 }) do
#       local expected = {}
#       for i = from, to, step do expected[#expected + 1] = i end
#       assert(visit(range(from, to, step)) == table.concat(expected, ","),
#         string.format("range(%d, %d, %d) should match the numeric for", from, to, step))
#     end
#   end
# end
# local a, b = range(1, 3), range(1, 3)
# assert(a() == 1 and a() == 2 and b() == 1, "each call of range makes an iterator of its own")
# local done = range(1, 1)
# done(); done()
# assert(done() == nil, "a used-up iterator keeps returning nil")
# assert(not pcall(range, 1, 5, 0), "a step of 0 must raise an error")
# print("passed")

# %% [markdown]
# ## 5. A stateless iterator
#
# ### Exercise L5.5 (LO-5.3, ★★, about 20 minutes)
#
# Write `reverse_ipairs(list)`, which visits a sequence from its last item to its first:
# `for i, v in reverse_ipairs({ "a", "b", "c" })` visits `3, "c"`, then `2, "b"`, then `1, "a"`.
# Make it stateless, like the reading's `my_ipairs`: it returns one step function defined once,
# outside `reverse_ipairs`; the list as the state; and `#list + 1` as the first control value,
# which is the index of the item visited last. Then answer the question in the Markdown cell after
# the check.

# %% tags=["answer-L5.5"] language="lua"
# function reverse_ipairs(list)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local seen = {}
# for i, v in reverse_ipairs({ "a", "b", "c" }) do seen[#seen + 1] = i .. v end
# assert(table.concat(seen, " ") == "3c 2b 1a", "reverse_ipairs should visit 3c, 2b, 1a")
# for _ in reverse_ipairs({}) do error("an empty list should give no passes") end
# local step, state, control = reverse_ipairs({ 10, 20 })
# assert(type(step) == "function" and step == reverse_ipairs({ 99 }),
#   "a stateless iterator returns the same step function for every list")
# assert(state[2] == 20 and control == 3, "the state is the list, and the first control value is #list + 1")
# local i1, v1 = step(state, control)
# local i2, v2 = step(state, control)
# assert(i1 == 2 and v1 == 20 and i2 == 2 and v2 == 20,
#   "calling the step function twice with the same values should give the same results")
# assert(step(state, 1) == nil, "after index 1 there is nothing left")
# print("passed")

# %% [markdown] tags=["answer-L5.5-why"]
# *Your answer here: why can every loop share `reverse_ipairs`'s step function, while every loop
# needs a new closure from `range`?*

# %% [markdown]
# ## Summary
#
# - A closure captures variables, not values, and closures made in one call share them; `for`
#   loops give each pass a new variable, and `while` loops don't.
# - `reduce` and `compose` are ordinary functions that take functions, and `table.pack` keeps every
#   value, `nil` included, when a function passes them along.
# - Naive `fib(n)` makes about 11 times more calls for each 5 added to `n`; memoized, with the
#   recursion going through the cache, it makes `n + 1`.
# - Caching `nil` and `false` needs a placeholder value, because a table can't store `nil`.
# - A stateful iterator keeps its position in a closure and is used up after one loop; a stateless
#   one keeps it in the control value, and one step function serves every loop.
#
# Next, do the [Module 5 practice](practice.md).
