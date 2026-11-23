# Module 5 practice

These exercises practice the [Module 5 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it in a `%%lua` cell or in `lua -i`.

## Worked example: tracing a closure factory

What does this program print?

```lua
local function make_account(balance)
  local function deposit(amount)
    balance = balance + amount
    return balance
  end
  local function check()
    return balance
  end
  return deposit, check
end

local deposit, check = make_account(100)
local deposit2, check2 = make_account(0)
deposit(50)
deposit(-30)
deposit2(5)
print(check(), check2())
```

1. `make_account(100)` creates a variable `balance` holding 100, and two closures that share it.
   `deposit` and `check` hold those two closures.
2. `make_account(0)` is a second call, so it creates a second `balance`, holding 0, and two new
   closures that share that one.
3. `deposit(50)` and `deposit(-30)` change the first `balance` to 150, then 120.
   `deposit2(5)` changes the second to 5.
4. `check()` reads the first `balance`, and `check2()` the second.

So it prints `120  5`. Nothing outside the closures can read or change either balance.

### Exercise 5.1 (LO-5.1, ★, about 10 minutes)

Predict what this prints.

```lua
local function make_greeter(greeting)
  return function(name) return greeting .. ", " .. name end
end

local hi = make_greeter("Hi")
local hello = make_greeter("Hello")
print(hi("Ana"), hello("Bo"), hi("Cy"))
```

<details>
<summary>Answer</summary>

`Hi, Ana  Hello, Bo  Hi, Cy`. Each call of `make_greeter` captures its own `greeting`, and a
closure keeps it for as long as the closure exists.
</details>

### Exercise 5.2 (LO-5.1, ★★, about 15 minutes)

This code should make three handlers that print `task 1`, `task 2`, and `task 3`, but all three
print `task 4`. Fix it with the smallest change, and explain the bug.

```lua
local handlers = {}
local n = 1
while n <= 3 do
  handlers[n] = function() print("task " .. n) end
  n = n + 1
end
handlers[1]()
```

**Step 1.** Every handler refers to `n`. Count how many variables named `n` this code creates.
Now finish the fix.

<details>
<summary>Answer</summary>

There is only one `n`, declared before the loop, so all three closures share it, and it is 4 when
they run. Declare a new local in the body, which is a new variable on every pass:

```lua
while n <= 3 do
  local current = n
  handlers[n] = function() print("task " .. current) end
  n = n + 1
end
```

Rewriting the loop as `for n = 1, 3 do` also works, because a numeric `for` gives each pass its
own `n`.
</details>

### Exercise 5.3 (LO-5.2, ★★, about 15 minutes)

Write `once(fn)`, which returns a function that calls `fn` the first time it is called, with the
arguments it got, and on every later call returns the same results as the first call, without
calling `fn` again. Keep every result, even if there are several.

<details>
<summary>Hint</summary>

Keep a flag and the packed results as upvalues. `table.pack` keeps the results and their number.
</details>

<details>
<summary>Answer</summary>

```lua
local function once(fn)
  local done, results = false, nil
  return function(...)
    if not done then
      results = table.pack(fn(...))
      done = true
    end
    return table.unpack(results, 1, results.n)
  end
end

local setup = once(function() print("setting up") return "ready", 42 end)
print(setup())      --> setting up, then ready  42
print(setup())      --> ready  42
```

A separate `done` flag is needed because `fn` might return nothing, or `nil`, so `results` alone
can't say whether `fn` has run. The arguments of later calls are ignored.
</details>

### Exercise 5.4 (LO-5.2, ★★★, about 20 minutes)

Write `partial(fn, ...)`, which fixes the first arguments of `fn` and returns a function that
takes the rest. `partial(string.rep, "ab")(3)` is `string.rep("ab", 3)`, `"ababab"`. Make it work
when a fixed argument is `nil`: `partial(select, "#", nil)(nil)` should be 2.

<details>
<summary>Hint</summary>

Pack the fixed arguments once. When the new function is called, build one list of all the
arguments, fixed ones first, using the `n` fields to place each one, and unpack it.
</details>

<details>
<summary>Answer</summary>

```lua
local function partial(fn, ...)
  local fixed = table.pack(...)
  return function(...)
    local args = table.pack(table.unpack(fixed, 1, fixed.n))
    local rest = table.pack(...)
    for i = 1, rest.n do
      args[fixed.n + i] = rest[i]
    end
    return fn(table.unpack(args, 1, fixed.n + rest.n))
  end
end
```

The positions come from `fixed.n` and `rest.n`, never from `#`, because `#` can't count past a
`nil`. Copying `fixed` into a new `args` on each call keeps one call from changing the next.
</details>

### Exercise 5.5 (LO-5.2, ★★, about 15 minutes)

Which of these functions can you memoize safely, and why? (a) `math.sqrt`. (b) `os.time`, called
with no arguments. (c) A function that returns the number of lines in a file, given its name.
(d) A function that takes a table and returns the sum of its items.

<details>
<summary>Answer</summary>

Only (a). Memoizing is safe only for a pure function, whose result depends on nothing but its
arguments. (b) returns the current time, which changes. (c) depends on the file, which can change
between calls. (d) looks pure, but its argument is a table, which is a reference: the same table
can hold different items later, and the cache would return the old sum. The cache would also keep
every table it saw from being collected.
</details>

### Exercise 5.6 (LO-5.3, ★★, about 15 minutes)

Write a stateless iterator `chars(s)` for ASCII strings, so that `for i, c in chars("abc")`
visits `1, "a"`, then `2, "b"`, then `3, "c"`. Which values does `chars` return?

<details>
<summary>Answer</summary>

```lua
local function chars_step(s, i)
  i = i + 1
  if i <= #s then return i, s:sub(i, i) end
end

local function chars(s)
  return chars_step, s, 0
end
```

`chars` returns the step function, the string as the state, and 0 as the first control value.
The loop calls `chars_step(s, 0)`, then `chars_step(s, 1)`, and so on, until it returns nothing.
</details>

### Exercise 5.7 (LO-5.3, ★★, about 20 minutes)

Write a stateful iterator `chunks(list, size)` that visits a sequence in pieces of `size` items:
`for piece in chunks({ 1, 2, 3, 4, 5 }, 2)` visits `{ 1, 2 }`, `{ 3, 4 }`, and `{ 5 }`.

<details>
<summary>Answer</summary>

```lua
local function chunks(list, size)
  local start = 1
  return function()
    if start > #list then return nil end
    local piece = table.move(list, start, math.min(start + size - 1, #list), 1, {})
    start = start + size
    return piece
  end
end
```

The position `start` lives in the closure, so each call of `chunks` gets a new one.
`table.move(list, a, b, 1, {})` copies items `a` to `b` into a new table, starting at index 1.
Each piece is a new table, so changing one doesn't change `list`.
</details>

### Exercise 5.8 (LO-5.3, ★★, about 10 minutes)

Explain why `for k, v in next, t do` visits every key of `t`, and why `for x in { 1, 2 } do`
stops with an error. What does the error message say?

<details>
<summary>Answer</summary>

The generic `for` takes the iterator function, the state, and the first control value from its
expression list. `next, t` supplies `next` and `t`, and the missing third value is `nil`, which
is exactly what `pairs(t)` returns, so the loop calls `next(t, nil)`, then `next(t, k)` for each
key. In `for x in { 1, 2 } do`, the first value is a table, so the first call fails with
`attempt to call a table value`. A table needs `ipairs` or `pairs` to be walked.
</details>
