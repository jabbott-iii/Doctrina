# Module 5: Closures and iterators

**Objectives:** LO-5.1, LO-5.2, LO-5.3\
**Prerequisites:** [Module 2](../02-control-flow-and-functions/index.md) and
[Module 3](../03-tables/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 5](lab05.ipynb), 1.5 for the
[practice](practice.md), and 3 to start PA3, which is due in week 7

Module 2 showed that a function is a value you can store and pass around. This module adds the
idea that makes that useful: a function can keep the local variables of the function that created
it, even after that function has returned. Such a function is a **closure**. With closures you can
build counters and caches that keep their state private, write functions that make or transform
other functions, and write your own iterators for the generic `for`.

## Functions are values

A function can go anywhere a value can: in a variable, in a table, as an argument, or as a
result. A table of functions is a common way to choose an operation by name:

```lua
local operations = {
  add = function(a, b) return a + b end,
  mul = function(a, b) return a * b end,
}
print(operations.add(2, 3), operations["mul"](2, 3))   --> 5  6
```

A function that takes or returns another function is a **higher-order function**. You have used
one already: `table.sort` takes a comparator.

## Closures

A function defined inside another function can read and write the outer function's local
variables. Lua calls such a variable, seen from the inner function, an **upvalue**. The inner
function keeps its upvalues alive for as long as it exists, so they outlive the call that created
them:

```lua
local function new_counter()
  local count = 0
  return function()
    count = count + 1
    return count
  end
end

local a = new_counter()
local b = new_counter()
print(a(), a(), b(), a())      --> 1  2  1  3
```

Each call of `new_counter` creates a new local `count` and a new function that uses it. `a` and
`b` are two closures with two separate counts, and no other code can reach either count: the only
way to change it is to call the closure. That is how closures hide state, without objects.

Two rules decide what a closure sees:

1. **A closure captures the variable, not its value at the time.** If the variable changes later,
   the closure sees the new value:

   ```lua
   local x = 1
   local f = function() return x end
   x = 2
   print(f())                  --> 2
   ```

2. **Closures created in the same call share that call's variables.** Here `get` and `set` share
   one `value`:

   ```lua
   local function make_box(value)
     local function get() return value end
     local function set(new) value = new end
     return get, set
   end

   local get, set = make_box(1)
   set(5)
   print(get())                --> 5
   ```

## Closures in loops

Both rules matter most in loops. Every pass of a numeric or generic `for` gets a new copy of the
loop variable, so a closure made in each pass captures a different variable:

```lua
local fns = {}
for i = 1, 3 do
  fns[i] = function() return i end
end
print(fns[1](), fns[2](), fns[3]())       --> 1  2  3
```

A `while` loop has no loop variable of its own. A counter declared before the loop is one
variable, so every closure shares it, and sees its last value:

```lua
local fns, i = {}, 1
while i <= 3 do
  fns[i] = function() return i end
  i = i + 1
end
print(fns[1](), fns[2](), fns[3]())       --> 4  4  4
```

The fix is a local declared inside the body, which is a new variable on every pass:
`local current = i`, then `function() return current end`. If you know Python, its closures
behave like the `while` version: `[lambda: i for i in range(3)]` makes three functions that all
return 2.

## Higher-order functions

Three functions do most of the work of processing lists in a functional style. `map` applies a
function to every item, `filter` keeps the items that pass a test, and `reduce` combines the items
into one value:

```lua
local function map(list, fn)
  local result = {}
  for i, v in ipairs(list) do result[i] = fn(v) end
  return result
end

local function filter(list, keep)
  local result = {}
  for _, v in ipairs(list) do
    if keep(v) then result[#result + 1] = v end
  end
  return result
end

local squares = map({ 1, 2, 3 }, function(v) return v * v end)
local evens = filter({ 1, 2, 3, 4 }, function(v) return v % 2 == 0 end)
print(table.concat(squares, ","), table.concat(evens, ","))    --> 1,4,9  2,4
```

A function can also return a new function built from others. `compose(f, g)` returns a function
that applies `g`, then `f`, passing along every result:

```lua
local function compose(f, g)
  return function(...) return f(g(...)) end
end

local inc_then_double = compose(function(v) return v * 2 end, function(v) return v + 1 end)
print(inc_then_double(3))       --> 8
```

Every time Lua evaluates a `function … end` expression, it creates a new closure, which takes
memory. In a loop that runs millions of times, creating a closure on every pass can cost more than
the work it does; module 12 measures it.

## Memoization

A **pure function** returns the same result whenever it gets the same arguments, and changes
nothing else. Its results can be cached: the first call with an argument computes the result, and
later calls look it up. This is **memoization**, and a closure keeps the cache private:

```lua
local function memoize(fn)
  local cache = {}
  return function(n)
    local result = cache[n]
    if result == nil then
      result = fn(n)
      cache[n] = result
    end
    return result
  end
end
```

The classic test is the Fibonacci function, which recomputes the same values again and again:

```lua
local function fib(n)
  if n < 2 then return n end
  return fib(n - 1) + fib(n - 2)
end
```

`fib(30)` makes 2,692,537 calls to compute 832,040. Memoizing it only helps if the recursive calls
go through the cache too. `local fast = memoize(fib)` caches only the top call: `fast(25)` still
makes all 242,785 calls of `fib` the first time, and `fast(26)` makes 392,835 more, because `fib`
calls itself, not `fast`. Make the recursion use the memoized function instead:

```lua
local memo_fib
memo_fib = memoize(function(n)
  if n < 2 then return n end
  return memo_fib(n - 1) + memo_fib(n - 2)
end)
print(memo_fib(30))      --> 832040, after 31 calls of the inner function
```

The local is declared first, on its own line, so that the function inside can refer to it; the
same reason made `local function` necessary for recursion in module 2. This version of `memoize`
has three limits:

- It only caches functions of one argument. For more, build a key from the arguments, or nest one
  cache table per argument.
- A result of `nil` is never cached, because `cache[n] = nil` stores nothing, so the function runs
  again on every call. Lab 5 has you fix that.
- The cache only grows. A weak table, in module 7, lets Lua discard entries no one uses.

## Iterators and the generic `for`

An **iterator** is a function that produces the next value of a sequence each time it is called.
The generic `for` calls it until it returns `nil`. Knowing exactly what the loop does lets you
write your own.

### What the generic `for` keeps

`for var_1, …, var_n in explist do body end` starts by evaluating `explist` and keeping its first
values:

1. the **iterator function**;
2. the **state**, a value the loop passes to the iterator on every call and never changes;
3. the **control value**, which starts as the third value and becomes the first result of each
   call.

Lua 5.4 also keeps a fourth value, the **closing value**, which it closes when the loop ends,
however it ends; it is usually `nil`, and module 10 shows what it is for. On each pass, the loop
calls `iterator(state, control)`, assigns the results to `var_1, …, var_n`, stops if `var_1` is
`nil`, and otherwise runs the body with `var_1` as the new control value. Leaving out the closing
value, the loop works like this:

```lua
do
  local iterator, state, control = explist
  while true do
    local var_1, var_2 = iterator(state, control)
    if var_1 == nil then break end
    control = var_1
    -- body
  end
end
```

`ipairs` and `pairs` return these values; you can print them:

```lua
local t = { "a", "b" }
print(ipairs(t))      --> function: 0x…  table: 0x…  0
print(pairs(t))       --> function: 0x…  table: 0x…  nil
print(select(1, pairs(t)) == next)      --> true
```

`pairs(t)` returns `next`, `t`, and `nil`, so `for k, v in pairs(t)` calls `next(t, nil)`, then
`next(t, k)` with each key, until `next` returns `nil`. That is why `for k, v in next, t do`
works too.

### Stateless iterators

A **stateless iterator** keeps nothing between calls: everything it needs comes in as the state
and the control value. Here is `ipairs`, written in Lua:

```lua
local function ipairs_step(list, i)
  i = i + 1
  local v = list[i]
  if v ~= nil then return i, v end
end

local function my_ipairs(list)
  return ipairs_step, list, 0
end

for i, v in my_ipairs({ "x", "y", nil, "z" }) do io.write(i, v, " ") end   --> 1x 2y
```

`ipairs_step` is one function for every loop, because it holds no state of its own; calling
`ipairs_step(list, 1)` twice gives the same answer both times.

### Stateful iterators

When the state doesn't fit in one state value and one control value, keep it in a closure
instead. The iterator then ignores the arguments the loop passes, and the loop needs only the
function:

```lua
local function evens_up_to(limit)
  local n = 0
  return function()
    n = n + 2
    if n <= limit then return n end
  end
end

for n in evens_up_to(7) do io.write(n, " ") end      --> 2 4 6
```

Each call of `evens_up_to` makes a new closure with its own `n`, so two loops over it don't
interfere, but one closure can be walked only once: after it returns `nil`, it is used up.
`string.gmatch` works this way, which is why `for word in s:gmatch("%a+")` needs no other values.

| Kind | Where the position lives | Example | Can one iterator function serve many loops? |
| :- | :- | :- | :- |
| Stateless | In the control value the loop passes back | `ipairs`, `pairs`, `my_ipairs` | Yes |
| Stateful | In the closure's upvalues | `string.gmatch`, `evens_up_to` | No: each loop needs a new closure |

Prefer a stateless iterator when the position fits in one value, because it creates no closure.
Use a closure when the iterator must remember more, such as two positions, a buffer, or a count.
In either kind, don't assign to the control variable inside the loop: the manual says you should
not, and Lua 5.5 makes it a compile error.

## Common misconceptions

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| A closure copies the values it uses | It captures the variables | Changing `x` after making `f` changes what `f` returns |
| Two closures from one factory share state | Each call of the factory makes new variables | `a()` and `b()` from two `new_counter()` calls count separately |
| Every loop gives each closure its own variable | Only `for` loops make a new variable per pass | A `while` loop's counter is shared: `4  4  4` |
| `memoize(fib)` makes `fib` fast | Only if the recursive calls use the memoized version | `fast(26)` after `fast(25)` still made 392,835 calls |
| A memoized function never reruns for an argument | It reruns whenever the result was `nil` | `cache[n] = nil` stores nothing |
| The generic `for` keeps only the iterator function | It keeps the function, a state, and a control value, plus a closing value in Lua 5.4 | `for k, v in next, t do` works |
| A stateful iterator can be restarted | Once it returns `nil`, it is used up | Call `evens_up_to(7)` again for a second loop |

## Summary

- Functions are values; a higher-order function takes or returns one.
- A closure is a function together with the outer local variables it uses, its upvalues. It
  captures variables, not values, and closures created in one call share them.
- Numeric and generic `for` loops make a new loop variable on every pass; a `while` loop's counter
  is one variable shared by every closure made in the loop.
- `map`, `filter`, `reduce`, and `compose` are ordinary functions built from closures.
- Memoization caches a pure function's results in a private table; a recursive function must call
  the memoized version for it to help.
- The generic `for` keeps an iterator function, a state, and a control value (and, in Lua 5.4, a
  closing value), and calls `iterator(state, control)` until the first result is `nil`.
- A stateless iterator keeps its position in the control value; a stateful one keeps it in a
  closure, and can be walked once.

## Self-check

1. What does this print?

   ```lua
   local function make()
     local n = 10
     return function() n = n + 1; return n end, function() return n end
   end
   local bump, peek = make()
   bump(); bump()
   print(peek())
   ```

   <details>
   <summary>Answer</summary>

   12. `bump` and `peek` were created in the same call of `make`, so they share one `n`.
   </details>

2. A program builds buttons in a `while` loop and gives each one
   `function() print("button", i) end`. Every button prints the same number. Why, and how do you
   fix it?

   <details>
   <summary>Answer</summary>

   All the closures capture the one variable `i`, which the loop changes, so they print its value
   after the loop. Declare `local n = i` inside the loop body and print `n`, or use a numeric
   `for`, which gives each pass its own variable.
   </details>

3. Why does `memoize` above recompute `f(x)` on every call when `f(x)` is `nil`, and what would
   fix it?

   <details>
   <summary>Answer</summary>

   It tests `cache[n] == nil` to decide whether to compute, and storing `nil` in a table stores
   nothing, so the test is true every time. Store a special value in the cache in place of `nil`,
   such as a table created once for the purpose, and turn it back into `nil` when you return it.
   </details>

4. What three values does `ipairs(t)` return, and what does the loop do with each?

   <details>
   <summary>Answer</summary>

   An iterator function, the table `t` as the state, and 0 as the first control value. The loop
   calls the function with `t` and the control value, assigns the results to its variables, and
   uses the first result, the index, as the next control value, until it is `nil`.
   </details>

5. When would you write a stateful iterator instead of a stateless one?

   <details>
   <summary>Answer</summary>

   When the iterator must remember more than one value between calls, such as positions in two
   lists, or a running total, so the position doesn't fit in the one control value the loop
   passes back. A stateless iterator is cheaper, because it needs no closure.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, sections
  [3.3.5, For Statement](https://www.lua.org/manual/5.4/manual.html#3.3.5), which defines the
  generic `for` and its four values exactly, and
  [3.5, Visibility Rules](https://www.lua.org/manual/5.4/manual.html#3.5), which shows how each
  pass of a loop creates new local variables for closures to capture.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapters on
  closures and on iterators and the generic `for` have more examples of both kinds of iterator.
