# Module 9 practice

These exercises practice the [Module 9 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it in a `%%lua` cell or in `lua -i`.

## Worked example: following values through a coroutine

What does this program print?

```lua
local acc = coroutine.wrap(function(start)
  local total = start
  while true do
    local amount = coroutine.yield(total)
    total = total + amount
  end
end)

print(acc(10), acc(5), acc(-3))
```

1. `acc(10)` is the first resume, so 10 becomes `start`. `total` is 10, and the first `yield`
   hands it out: the first value is 10.
2. `acc(5)` resumes the waiting `yield`, which returns 5 as `amount`. `total` becomes 15, and the
   loop yields it: the second value is 15.
3. `acc(-3)` does the same with -3: `total` becomes 12, the third value.

So it prints `10  15  12`. The coroutine never returns, so it stays suspended, ready for the next
amount: it is a running total whose state lives on the coroutine's stack.

### Exercise 9.1 (LO-9.1, ★, about 10 minutes)

Give the status of `co` at each of the four points marked in comments.

```lua
local co
co = coroutine.create(function()
  print(coroutine.status(co))      -- (b)
  coroutine.yield()
end)
print(coroutine.status(co))        -- (a)
coroutine.resume(co)
print(coroutine.status(co))        -- (c)
coroutine.resume(co)
print(coroutine.status(co))        -- (d)
```

<details>
<summary>Answer</summary>

(a) `suspended`: created, not started. (b) `running`: it is asking about itself. (c)
`suspended`: paused in its `yield`. (d) `dead`: the second resume ran it to the end.
</details>

### Exercise 9.2 (LO-9.1, ★★, about 15 minutes)

Predict the three lines this prints.

```lua
local co = coroutine.create(function(a)
  local b, c = coroutine.yield(a * 2, "first")
  local d = coroutine.yield(b + c)
  return d, "end"
end)
print(coroutine.resume(co, 5))
print(coroutine.resume(co, 1, 2))
print(coroutine.resume(co, "last"))
```

<details>
<summary>Answer</summary>

```text
true    10      first
true    3
true    last    end
```

A `yield` with two values gives `resume` two extra results. The second resume's 1 and 2 become
`b` and `c`. The third's `"last"` becomes `d`, and the function's two return values come out of
the last `resume`.
</details>

### Exercise 9.3 (LO-9.2, ★★, about 10 minutes)

Write `fibonacci(limit)`, a generator for the generic `for` of the Fibonacci numbers 0, 1, 1, 2,
3, 5, … that are at most `limit`.

<details>
<summary>Answer</summary>

```lua
local function fibonacci(limit)
  return coroutine.wrap(function()
    local a, b = 0, 1
    while a <= limit do
      coroutine.yield(a)
      a, b = b, a + b
    end
  end)
end

for f in fibonacci(20) do io.write(f, " ") end   --> 0 1 1 2 3 5 8 13
```

The loop's `a` and `b` are the generator's whole state, and they stay on the coroutine's stack
between values.
</details>

### Exercise 9.4 (LO-9.2, ★★, about 20 minutes)

Write `leaves(t)`, a generator of every value in a nested list that isn't itself a table, from
left to right: `leaves({ 1, { 2, { 3, 4 } }, 5 })` gives 1, 2, 3, 4, 5.

<details>
<summary>Answer</summary>

```lua
local function leaves(t)
  return coroutine.wrap(function()
    local function walk(node)
      for _, v in ipairs(node) do
        if type(v) == "table" then walk(v) else coroutine.yield(v) end
      end
    end
    walk(t)
  end)
end
```

The recursion goes as deep as the nesting does, and each `yield` pauses all of it. A closure-based
iterator would need its own stack of lists and positions to do the same.
</details>

### Exercise 9.5 (LO-9.3, ★★, about 15 minutes)

Using the reading's `spawn` and `sleep`, write `every(seconds, fn)`, which spawns a task that calls
`fn` every `seconds`, starting at once, until `fn` returns `false`.

<details>
<summary>Answer</summary>

```lua
local function every(seconds, fn)
  spawn(function()
    while fn() ~= false do
      sleep(seconds)
    end
  end)
end
```

When `fn` returns `false`, the loop ends, the task's function returns, the coroutine is dead, and
the scheduler drops it. Testing `~= false` rather than `not fn()` lets an `fn` that returns
nothing keep running.
</details>

### Exercise 9.6 (LO-9.3, ★★, about 15 minutes)

On the reading's scheduler, one task sets a global `done = true` after `sleep(5)`. Another task
waits for it with `while not done do end`, then prints `"finished"`. The waiting task starts
first. What happens? Fix the waiting task.

<details>
<summary>Answer</summary>

The waiting task loops forever without yielding, so the scheduler never gets control back, the
other task never runs, and `done` is never set: the program hangs. Yield inside the loop, so the
scheduler can run other tasks between checks:

```lua
spawn(function()
  while not done do sleep(1) end
  print("finished")
end)
```

`sleep(0)` would also work, but checking every second wastes fewer resumes. With cooperative
tasks, every wait must be a yield.
</details>
