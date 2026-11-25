# Module 9: Coroutines

**Objectives:** LO-9.1, LO-9.2, LO-9.3\
**Prerequisites:** [Module 5](../05-closures-and-iterators/index.md) and
[Module 6](../06-errors-modules-and-tests/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 9](lab09.ipynb), 1.5 for the
[practice](practice.md), and 3 for PA4, which follows Module 10

A **coroutine** is a function that can pause in the middle, hand values back to whoever started
it, and later continue exactly where it stopped, with its local variables intact. Lua's
coroutines are the language's one tool for concurrency: they let a recursive traversal hand out
its results one at a time, let stages of a pipeline pass data along without building lists, and
let many tasks share one thread by taking turns. This module covers how values move in and out of
a coroutine, generators and pipelines built from them, and a scheduler that runs tasks with
timers, which PA4 builds on.

## Coroutines are cooperative

A coroutine is not an operating-system thread. Only one coroutine runs at a time, and it runs
until it chooses to pause by calling `coroutine.yield`. Nothing interrupts it. That is
**cooperative** multitasking, in contrast with the **preemptive** threads of Java or C, which the
system can stop at any instruction. Cooperation has a cost and a benefit. The cost: a coroutine
that never yields stops every other one. The benefit: no two coroutines ever run at the same time,
so they need no locks to share data.

Lua's coroutines are also **asymmetric**: a coroutine is started and continued with `resume`, and
it always returns control, with `yield`, to the code that resumed it, never to some other
coroutine of its choosing.

## Creating and resuming

`coroutine.create(f)` makes a coroutine from a function, without running it. `coroutine.resume`
runs it until it yields or returns. Values travel both ways:

- The arguments of the first `resume` become the function's parameters.
- The arguments of `yield` become the extra results of the `resume` that is waiting for them.
- The arguments of each later `resume` become the results of the `yield` that is waiting for them.
- The function's return values become the extra results of the last `resume`.

```lua
local co = coroutine.create(function(a, b)
  local x = coroutine.yield(a + b)        -- hands out 3, then waits
  local y, z = coroutine.yield(x * 2)     -- hands out 20, then waits
  return "done", y + z
end)

print(coroutine.resume(co, 1, 2))     --> true  3        (a = 1, b = 2)
print(coroutine.resume(co, 10))       --> true  20       (x = 10)
print(coroutine.resume(co, 3, 4))     --> true  done  7  (y = 3, z = 4)
print(coroutine.resume(co))           --> false  cannot resume dead coroutine
```

`resume`'s first result says whether the coroutine ran without an error, as `pcall`'s does.

### Status

`coroutine.status(co)` returns one of four strings:

| Status | Meaning |
| :- | :- |
| `"suspended"` | Created and not started, or paused in a `yield`: it can be resumed |
| `"running"` | It is the coroutine calling `status` |
| `"normal"` | It resumed another coroutine, and is waiting for that one to yield or finish |
| `"dead"` | Its function returned or raised an error: it can't be resumed again |

### Errors

An error inside a coroutine stops it and makes it dead, and `resume` returns `false` and the error
message, the way `pcall` does; the error doesn't reach the code that called `resume`.
`debug.traceback(co)` returns the dead coroutine's stack, which shows where it failed.

### `coroutine.wrap`

`coroutine.wrap(f)` makes a coroutine and returns a function that resumes it. Calling the function
passes its arguments to `resume` and returns what the coroutine yields or returns, without the
`true` in front. If the coroutine raises an error, the call raises it too, as if the coroutine
were an ordinary function. Use `wrap` when the caller only wants the values, as in the generators
below, and `create` with `resume` when it must check status or catch errors, as a scheduler must.

### Where a coroutine can't yield

`coroutine.yield` called outside any coroutine fails with
`attempt to yield from outside a coroutine`. A yield also can't pass through a function written in
C that doesn't support it: yielding inside a comparator that `table.sort` calls fails with
`attempt to yield across a C-call boundary`. Since Lua 5.2, `pcall` and metamethods do support it,
so a coroutine can yield from inside a `pcall`. `coroutine.close(co)`, new in Lua 5.4, ends a
suspended coroutine that will never be resumed, and runs any pending cleanup.

## Generators

A coroutine that yields values one at a time is a **generator**. Wrapped, it is a function that
returns the next value on each call, and `nil` when it has finished, which is exactly what the
generic `for` expects of a stateful iterator from module 5:

```lua
local function squares(n)
  return coroutine.wrap(function()
    for i = 1, n do coroutine.yield(i * i) end
  end)
end

for sq in squares(4) do io.write(sq, " ") end     --> 1 4 9 16
```

The generator's position lives in the coroutine's own stack, so it can be anywhere, even deep in a
recursion. That is where coroutines beat closures. Walking a binary tree in order needs a stack of
the nodes not yet visited, which a closure-based iterator would have to manage by hand. A
coroutine keeps that stack for free, in its paused recursive calls:

```lua
local function in_order(node)
  return coroutine.wrap(function()
    local function walk(n)
      if n == nil then return end
      walk(n.left)
      coroutine.yield(n.value)
      walk(n.right)
    end
    walk(node)
  end)
end

local tree = { value = 5, left = { value = 2 }, right = { value = 8, left = { value = 6 } } }
for v in in_order(tree) do io.write(v, " ") end   --> 2 5 6 8
```

Each `yield` pauses all the recursive calls of `walk` at once, and the next call of the generator
resumes them.

## Pipelines

A **pipeline** passes values through a chain of stages. With generators, each stage takes the
stage before it, a function that returns the next value, and is itself such a function. The last
stage, the **consumer**, pulls values through the chain one at a time; nothing is computed before
the consumer asks for it, and no stage builds a list:

```lua
local function lines_of(text)                 -- the producer
  return coroutine.wrap(function()
    for line in text:gmatch("[^\n]+") do coroutine.yield(line) end
  end)
end

local function grep(pattern, source)          -- a filter
  return coroutine.wrap(function()
    for line in source do
      if line:find(pattern) then coroutine.yield(line) end
    end
  end)
end

local log = "ok start\nERROR disk full\nok retry\nERROR timeout\n"
for line in grep("^ERROR", lines_of(log)) do  -- the consumer
  print(line)                                 --> ERROR disk full, then ERROR timeout
end
```

`for line in source` works because `source` is a function that returns the next line, as the
generic `for` expects. Adding a stage means wrapping the chain once more, and each stage stays a
plain loop, which is clearer than an iterator that must save its position between calls.

## A cooperative scheduler

Coroutines can also run several **tasks** at once, by taking turns. A task is a coroutine that
yields whenever it waits for something. Here the only thing tasks wait for is time: a task calls
`sleep(seconds)`, which yields the delay, and a **scheduler** resumes each task when its time
comes. The scheduler keeps a simulated clock, `now`, so the tasks wait no real time and every run
is the same:

```lua
local now = 0
local waiting = {}                            -- entries { wake = time, task = coroutine }

local function spawn(fn)
  waiting[#waiting + 1] = { wake = now, task = coroutine.create(fn) }
end

local function sleep(seconds)
  coroutine.yield(seconds)
end

local function run()
  while #waiting > 0 do
    local next_index = 1                      -- find the earliest wake time; ties go to
    for i = 2, #waiting do                    -- the entry that has waited longest
      if waiting[i].wake < waiting[next_index].wake then next_index = i end
    end
    local entry = table.remove(waiting, next_index)
    now = entry.wake
    local ok, delay = coroutine.resume(entry.task)
    if not ok then error(delay, 0) end
    if coroutine.status(entry.task) ~= "dead" then
      entry.wake = now + delay
      waiting[#waiting + 1] = entry
    end
  end
end

spawn(function()
  for i = 1, 3 do print(now, "tick " .. i); sleep(2) end
end)
spawn(function()
  print(now, "tock"); sleep(3); print(now, "tock again")
end)
run()
--> 0  tick 1, 0  tock, 2  tick 2, 3  tock again, 4  tick 3
```

The scheduler is a loop: take the task whose time is earliest, move the clock to that time, resume
the task, and put it back with its new wake time, unless it has finished. PA4 runs a queue
simulation, with customers and servers, on a scheduler like this one.

### One task that never yields stops them all

Because nothing interrupts a coroutine, a task that runs a long computation without calling
`sleep` holds the whole program until it finishes, and one with an endless loop holds it forever.
No other task, however urgent, runs in the meantime. Hosts that run Lua inside an event loop live
with this rule. OpenResty, which runs Lua in the Nginx web server, runs each request's code in a
coroutine, and gives it network functions that yield while they wait; Neovim runs plugins on the
same loop that redraws the screen, so a plugin that computes for seconds freezes the editor. A
long computation must be cut into pieces that yield between them, and code that waits for a file
or a network must use the host's functions that yield while they wait, not ones that block.

## Common misconceptions

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| Coroutines run in parallel | One runs at a time, until it yields | A task with an endless loop stops every other task |
| The first `resume`'s arguments go to `yield` | They become the function's parameters | `resume(co, 1, 2)` sets `a` and `b` |
| `yield` returns what it yielded | It returns the next `resume`'s arguments | `local x = coroutine.yield(3)` gets 10 from `resume(co, 10)` |
| An error inside a coroutine reaches the caller | `resume` catches it, like `pcall` | `resume` returns `false` and the message |
| A finished coroutine can be resumed again | It is dead | `cannot resume dead coroutine` |
| A coroutine can yield from anywhere | Not from outside one, nor across some C functions | Yielding in a `table.sort` comparator fails |
| A generator made with `wrap` can be restarted | Each `wrap` makes one coroutine | Call the generator's factory again for a second loop |

## Summary

- A coroutine pauses at `yield` and continues at the next `resume`, keeping its locals. Only one
  runs at a time, and only `yield` switches.
- `resume`'s arguments go in as parameters, then as `yield`'s results; `yield`'s arguments and
  the function's returns come out as `resume`'s results, after `true` or `false`.
- A coroutine is suspended, running, normal, or dead; an error makes it dead, and `resume` reports
  the error instead of raising it.
- `coroutine.wrap` turns a coroutine into a function, which makes generators for the generic
  `for`, including ones that walk recursive structures.
- Generators chain into pipelines in which the consumer pulls each value through every stage.
- A scheduler resumes tasks in order of their wake times; it works only if every task yields
  regularly.

## Self-check

1. What does this print?

   ```lua
   local co = coroutine.create(function(x)
     local y = coroutine.yield(x + 1)
     return y * 2
   end)
   print(coroutine.resume(co, 5))
   print(coroutine.resume(co, 7))
   print(coroutine.status(co))
   ```

   <details>
   <summary>Answer</summary>

   `true  6`, then `true  14`, then `dead`. The first `resume` passes 5 as `x`, and the `yield`
   hands out 6. The second passes 7 as `yield`'s result, and the function returns 14.
   </details>

2. When would you use `coroutine.create` and `resume` rather than `coroutine.wrap`?

   <details>
   <summary>Answer</summary>

   When the caller must check a coroutine's status or catch its errors, as a scheduler must. A
   wrapped coroutine raises its errors in the caller, and gives no way to ask whether it has
   finished except calling it.
   </details>

3. Why does a coroutine make an in-order tree walk easier to write as an iterator than a closure
   does?

   <details>
   <summary>Answer</summary>

   The walk is naturally recursive, and the coroutine keeps every paused recursive call on its own
   stack between values. A closure-based iterator must return after each value, so it would have
   to keep its own explicit stack of the nodes still to visit.
   </details>

4. In the reading's scheduler, two tasks are due at time 4. Which one runs first, and why?

   <details>
   <summary>Answer</summary>

   The one that was put back into `waiting` first, because the search takes the first entry with
   the smallest wake time, and entries are added at the end. Ties go to the task that has waited
   longest.
   </details>

5. A task in the scheduler computes a large report for 10 seconds without calling `sleep`. What
   happens to the other tasks, and how would you fix it?

   <details>
   <summary>Answer</summary>

   None of them runs for those 10 seconds, whatever their wake times, because only `yield` returns
   control to the scheduler. Split the report into parts, and call `sleep(0)` between them, which
   yields and lets every task that is due run before the report continues.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, sections
  [2.6, Coroutines](https://www.lua.org/manual/5.4/manual.html#2.6), with a longer example of
  values passing through `resume` and `yield`, and
  [6.2, Coroutine Manipulation](https://www.lua.org/manual/5.4/manual.html#6.2), for every function
  in the `coroutine` library.
- Ana Lúcia de Moura and Roberto Ierusalimschy,
  ["Revisiting Coroutines"](https://dl.acm.org/doi/10.1145/1462166.1462167), *ACM Transactions on
  Programming Languages and Systems* 31(2), 2009. It classifies kinds of coroutines, and shows that
  Lua's asymmetric ones can express generators, schedulers, and more.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapter on
  coroutines builds generators, pipelines, and a small multitasking system step by step.
