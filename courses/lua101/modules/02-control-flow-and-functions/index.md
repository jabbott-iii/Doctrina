# Module 2: Control flow and functions

**Objectives:** LO-2.1, LO-2.2, LO-2.3, LO-2.4\
**Prerequisites:** [Module 1](../01-first-steps/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 2](lab02.ipynb), 1.5 for the
[practice](practice.md), and 3 for PA1, which follows this module

This module covers the statements that decide what runs and how often, and the functions that
package code for reuse. Most of it will look familiar from other languages. Three parts won't:
a function can return several values, and Lua quietly adjusts how many arrive; a call in one
particular position, the proper tail call, uses no stack at all; and Lua has no named
parameters, so you pass a table of options instead.

## Conditions

`if` tests a condition, with optional `elseif` and `else` branches, and ends with `end`:

```lua
local x = 10
if x > 5 then
  print("big")
elseif x > 0 then
  print("small")
else
  print("not positive")
end
```

Conditions follow module 1's rule: only `nil` and `false` are false. Lua has no `switch`
statement; a chain of `elseif` branches, or a table that maps keys to values (module 3), does the
same job.

## Loops

Lua has four loops. This section covers three of them fully and introduces the fourth, the
generic `for`, which modules 3 and 5 return to.

### `while` and `repeat`

`while` tests its condition before each pass, so its body may never run. `repeat … until` tests
after each pass, so its body always runs at least once:

```lua
local i = 1
while i <= 4 do
  i = i * 2
end
print(i)            --> 8

local tries = 0
repeat
  tries = tries + 1
  local done = tries >= 3
until done          -- the condition can see the body's locals
print(tries)        --> 3
```

The `until` condition can read the body's local variables, such as `done` above. That is unusual
among languages, and it lets the condition use a value the body has just computed.

### The numeric `for`

`for i = start, stop, step do … end` counts from `start` to `stop` in steps of `step`, which
defaults to 1:

```lua
for i = 1, 3 do io.write(i, " ") end      --> 1 2 3
for i = 3, 1, -1 do io.write(i, " ") end  --> 3 2 1
for i = 10, 1 do print("never") end       -- runs zero times
```

Four rules decide what such a loop does, and each one has caught out programmers from other
languages:

1. **The bounds are evaluated once,** before the first pass. Changing the variable that held
   `stop` inside the loop doesn't change how many times it runs:

   ```lua
   local n = 3
   for i = 1, n do n = 10 end   -- runs 3 times, not 10
   ```

2. **The control variable is a new local** for the loop. It doesn't exist after the loop, and an
   `i` declared before the loop is a different variable that the loop doesn't change.
3. **Don't assign to the control variable.** In Lua 5.4, assigning to `i` changes `i` for the rest
   of that pass, but not the count. In Lua 5.5 the assignment is a compile error.
4. **A float step accumulates rounding error.** `for x = 0, 1, 0.1` runs 11 times, and its last
   `x` is 0.99999999999999989, not 1. Whether the last pass happens depends on rounding. Loop over
   integers and compute the float instead: `for i = 0, 10 do local x = i / 10 … end`.

A step of 0 is a runtime error (`'for' step is zero`). When `start` and `stop` are integers, the
loop counts in integers and never wraps around, even next to `math.maxinteger`.

### The generic `for`

The generic `for` runs once for each value that an **iterator**, a function that produces values
one at a time, gives it. The two you use most walk a table, which module 3 introduces:

```lua
local days = { "Mon", "Tue", "Wed" }
for i, day in ipairs(days) do
  print(i, day)     --> 1 Mon, then 2 Tue, then 3 Wed
end
```

`ipairs` gives each index and value in order, and `pairs` gives every key and value in no
particular order. Module 5 shows how to write iterators of your own.

### `break`, and the missing `continue`

`break` leaves the innermost loop. Lua has no `continue` statement. To skip to the next pass, jump
to a label at the end of the body with `goto`:

```lua
for i = 1, 5 do
  if i % 2 == 0 then goto continue end
  io.write(i, " ")
  ::continue::
end
--> 1 3 5
```

`::continue::` is a label, and `continue` is an ordinary name here, not a keyword. Use `goto` for
this pattern and for leaving nested loops; for anything else, a loop or a function reads better.

### Choosing a loop

| You know… | Use |
| :- | :- |
| how many passes, or the range of a counter | the numeric `for` |
| the collection or iterator to walk | the generic `for` |
| a condition to check before each pass | `while` |
| that the body must run once before the condition makes sense | `repeat … until` |

## Functions

A function definition is an expression that creates a function value, and `function name()` is
shorthand for assigning that value to a name:

```lua
local function area(width, height)   -- a local function
  return width * height
end

local square = function(side)        -- the same thing, written as an assignment
  return area(side, side)
end

print(area(3, 4), square(5))         --> 12  25
```

A call can pass fewer arguments than the function has parameters, and the missing parameters are
`nil`. It can pass more, and the extras are dropped. Lua checks neither, so a function that needs
an argument has to check for it itself (module 6 shows how).

### `local function` and recursion

Always define a local function with `local function name`, not `local name = function`. The two
differ in one way, and it matters for recursion:

```lua
local fact = function(n)
  if n <= 1 then return 1 end
  return n * fact(n - 1)    -- this `fact` is the global, which is nil
end
print(fact(5))
--> fact.lua:3: attempt to call a nil value (global 'fact')
```

A `local` declaration takes effect only after its expression, so inside the function the name
`fact` still means the global `fact`. `local function fact(n)` declares the local first and then
assigns the function, so the body's `fact` is the local. It is shorthand for
`local fact; fact = function(n) … end`.

## Multiple results

A function can return several values, and a caller can receive them all:

```lua
local function min_max(a, b)
  if a < b then return a, b end
  return b, a
end

local lo, hi = min_max(7, 3)
print(lo, hi)            --> 3  7
```

### Adjustment

How many of a call's results arrive depends on where the call is. The **adjustment** rule is
short, and the rest of this section is its consequences:

> A call that is the **last** item in a list of expressions gives all of its results. A call
> anywhere else gives exactly one: its first result, or `nil` if it returned none.

"A list of expressions" means the right side of an assignment, the arguments of a call, the items
of a table constructor, and the values after `return`. With `local function two() return 1, 2
end`:

```lua
local a, b, c = two()        -- a = 1, b = 2, c = nil (too few values)
local d, e = two(), 10       -- d = 1, e = 10 (two() isn't last, so one result)
print(two(), two())          --> 1  1  2
print((two()))               --> 1 (parentheses keep only the first result)
local t = { two(), 3 }       -- { 1, 3 }
local u = { 3, two() }       -- { 3, 1, 2 }
```

A call that returns nothing gives zero values when it is last, which can surprise you. `type(f())`
raises `bad argument #1 to 'type' (value expected)` when `f` returns nothing, because `type`
received no argument at all, not even `nil`.

### Variadic functions

A function whose parameter list ends in `...` takes any number of extra arguments. Inside it,
`...` is an expression that stands for all of them, and it follows the adjustment rule like a
call:

```lua
local function sum(...)
  local total = 0
  for i = 1, select("#", ...) do
    total = total + (select(i, ...))
  end
  return total
end
print(sum(1, 2, 3), sum())   --> 6  0
```

Two functions handle varargs:

- `select("#", ...)` gives the number of extra arguments, counting `nil` ones. `select(i, ...)`
  gives the arguments from position `i` on, so `(select(i, ...))` is the `i`th alone.
- `table.pack(...)` gives a table holding the arguments, with their number in its field `n`.
  `table.unpack(t, 1, t.n)` turns that table back into separate values.

Never count varargs with `#{...}`. A table can't tell a missing value from `nil`, so
`#{1, nil, nil}` is 1 while `select("#", 1, nil, nil)` is 3. Module 3 explains why.

## Recursion and proper tail calls

A recursive function calls itself. Every call that hasn't returned yet keeps a frame on Lua's call
stack, and the stack has a limit:

```lua
local function depth(n)
  if n == 0 then return 0 end
  return 1 + depth(n - 1)
end
```

On Lua 5.4.8, `depth(499990)` worked and `depth(499991)` failed with `stack overflow`. The limit
is a number of stack slots, a million in the standard build, so a function whose frames are
larger overflows sooner.

### Proper tail calls

A call in the form `return f(args)` is a **proper tail call**. The caller has nothing left to do
after `f` returns, so Lua reuses the caller's stack frame for `f` instead of adding one. A chain
of tail calls can be as long as you like:

```lua
local function count_up(n, acc)
  if n == 0 then return acc end
  return count_up(n - 1, acc + 1)      -- a proper tail call
end
print(count_up(10000000, 0))           --> 10000000
```

That call ran 10 million levels deep in 0.15 s, on Lua 5.4.8 on an Intel Core i7-11800H. The
version that recursed without a tail call failed before 500,000. The extra parameter `acc` is an
**accumulator**: it carries the partial result forward, so nothing is left to do after the
recursive call.

Only the exact form `return f(args)` is a tail call. Each of these leaves work for the caller, so
none of them is:

```lua
return 1 + f(x)     -- adds after f returns
return (f(x))       -- keeps only the first result after f returns
return x, f(x)      -- builds a list of results
f(x); return        -- f's result isn't returned
```

A tail call leaves no frame, so it leaves no line in a stack traceback either. Lua marks the gap
with `(...tail calls...)`.

## Named options with a table

Lua has no named or default parameters. A function that takes several optional settings takes
one table of options instead, and a call can then name each setting. When the only argument is a
table constructor (or a string), the parentheses can go:

```lua
local function draw_box(opts)
  opts = opts or {}                -- allow draw_box() with no table at all
  local width = opts.width or 40
  local title = opts.title or ""
  -- ...
end

draw_box{ width = 20, title = "Totals" }   -- the same as draw_box({ ... })
draw_box()
```

`{ width = 20 }` builds a table with a field named `width`, and `opts.width` reads it; module 3
covers tables fully. A missing field reads as `nil`, which is why `opts.width or 40` supplies the
default.

### When `x or default` is wrong

`x or default` replaces every falsy `x`, and `false` is falsy. For an option whose valid values
include `false`, the default always wins:

```lua
local border = opts.border or true    -- wrong: border = false gives true
```

A caller who passes `{ border = false }` gets a border anyway. Test for `nil` instead, which is
what "not given" means:

```lua
local border = opts.border
if border == nil then
  border = true
end
```

The same trap catches `cond and a or b` from module 1, for the same reason. The rule of thumb:
`x or default` is safe when `false` isn't a valid value of `x`, such as a width, a name, or a
table. For booleans, compare with `nil`.

## Common misconceptions

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| A `for` loop rereads its bounds each pass | It evaluates them once | `for i = 1, n do n = 10 end` runs `n`'s first value times |
| The loop variable is still there after the loop | It is local to the loop | `print(i)` after `for i = 1, 3` prints the outer `i`, often `nil` |
| A float step lands exactly on the bound | Rounding error accumulates | `for x = 0, 1, 0.1` ends at 0.99999999999999989 |
| A call always gives all its results | Only as the last item in a list | `{ two(), 3 }` is `{ 1, 3 }` |
| `#{...}` counts the arguments | It can miss trailing `nil`s | `#{1, nil, nil}` is 1 |
| `return f(x) + 1` is a tail call | Only `return f(args)` is | Deep recursion with `1 + f(x)` overflows the stack |
| `local f = function` can call itself as `f` | Inside, `f` is still the global | Use `local function f` |
| `opts.flag or true` gives a default | It makes `false` impossible | `{ flag = false }` gives `true` |

## Summary

- `while` tests before each pass and `repeat` after; `repeat`'s condition sees the body's locals.
- The numeric `for` evaluates its bounds once and makes a new local control variable. Count in
  integers, and compute floats from the count.
- Lua has no `continue`; use `goto continue` with a `::continue::` label.
- Define local functions with `local function`, so that they can call themselves.
- A call gives all its results only as the last item in a list; elsewhere it gives one.
  Parentheses keep one.
- Count varargs with `select("#", ...)` or `table.pack(...).n`, never with `#{...}`.
- `return f(args)` is a proper tail call and uses no stack, so a recursion written that way can't
  overflow.
- Pass optional settings in a table, and test a boolean option for `nil`, not with `or`.

## Self-check

1. How many times does `for i = 1, 3 do i = 10 end` run in Lua 5.4, and what happens in Lua 5.5?

   <details>
   <summary>Answer</summary>

   Three times: the count is fixed before the first pass, and assigning to `i` changes only that
   pass's copy. In Lua 5.5 the assignment is a compile error, so the loop doesn't run at all.
   </details>

2. With `local function two() return 1, 2 end`, what does `print(two(), "x", two())` print?

   <details>
   <summary>Answer</summary>

   `1  x  1  2`. The first call isn't last, so it gives one result; the second is last, so it
   gives both.
   </details>

3. Which of these is a proper tail call: `return f(x)`, `return (f(x))`, `return f(x), 1`?

   <details>
   <summary>Answer</summary>

   Only `return f(x)`. The parentheses and the extra value both leave the caller work to do after
   `f` returns.
   </details>

4. Why does `local fact = function(n) … fact(n - 1) … end` fail, and what is the fix?

   <details>
   <summary>Answer</summary>

   The local `fact` exists only after the whole declaration, so inside the function `fact` is the
   global, which is `nil`. Write `local function fact(n)`, which declares the local before it
   assigns the function.
   </details>

5. A function reads `local verbose = opts.verbose or true`. What goes wrong, and how do you fix
   it?

   <details>
   <summary>Answer</summary>

   A caller can't turn `verbose` off: `false or true` is `true`. Read `opts.verbose`, and set it
   to `true` only if it is `nil`.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, sections
  [3.3.4, Control Structures](https://www.lua.org/manual/5.4/manual.html#3.3.4),
  [3.3.5, For Statement](https://www.lua.org/manual/5.4/manual.html#3.3.5), and
  [3.4.12, Lists of expressions, multiple results, and adjustment](https://www.lua.org/manual/5.4/manual.html#3.4.12).
  Section 3.3.5 states exactly how the numeric `for` computes its count, which explains the float
  rule above.
- The manual's sections [3.4.10, Function Calls](https://www.lua.org/manual/5.4/manual.html#3.4.10)
  and [3.4.11, Function Definitions](https://www.lua.org/manual/5.4/manual.html#3.4.11), for the
  definition of a proper tail call and of varargs.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapter on
  functions covers multiple results and varargs with more examples.
