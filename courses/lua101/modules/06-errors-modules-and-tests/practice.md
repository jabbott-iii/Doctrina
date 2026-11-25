# Module 6 practice

These exercises practice the [Module 6 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it in a `%%lua` cell, in `lua -i`, or with
busted.

## Worked example: testing a failure path

`parse_percent(s)` turns text such as `"45%"` into the number 45, and returns `nil` and the
message `not a percentage: ` followed by the text for anything else. It raises an error if `s`
isn't a string. Write busted tests for its failures.

1. **List the promises about failure.** There are two: a string that isn't a percentage gives
   `nil` and a message, and an argument that isn't a string raises an error.
2. **Pick inputs that are wrong in different ways.** For the first promise: `"45"` (no `%`),
   `"%"` (no number), and `"abc%"`. For the second: `nil` and `45`.
3. **Check both results of a `nil` return,** so that a version that returns `nil` with the wrong
   message, or no message, fails the test.
4. **Wrap each call that should raise an error in a function,** so that `has_error` makes the
   call.

```lua
describe("parse_percent", function()
  it("returns nil and a message for text that isn't a percentage", function()
    for _, text in ipairs({ "45", "%", "abc%" }) do
      local value, message = parse_percent(text)
      assert.is_nil(value)
      assert.are.equal("not a percentage: " .. text, message)
    end
  end)

  it("raises an error when the argument isn't a string", function()
    assert.has_error(function() parse_percent(nil) end)
    assert.has_error(function() parse_percent(45) end)
  end)
end)
```

The second test gives no message to `has_error`, so it passes for any error. Give the message
when the statement specifies one.

### Exercise 6.1 (LO-6.1, ★, about 10 minutes)

For each function, should the failure raise an error or return `nil` and a message? Say why.

1. `find_user(id)` is given an id that no user has.
2. `average(list)` is given a number instead of a table.
3. `parse_date(text)` is given `"2026-13-45"`, typed by a user.
4. `withdraw(account, amount)` is given a negative amount by another function in the same
   program.

<details>
<summary>Answer</summary>

1. Return `nil` and a message: asking about an id that may not exist is an ordinary question, and
   the caller can show "no such user".
2. Raise an error: the caller passed the wrong type, which is a bug to fix.
3. Return `nil` and a message: people mistype dates, so the program should expect it and ask
   again.
4. Raise an error: the amount came from code, not from a person, so a negative one means that
   code is wrong. If the amount came straight from a form, the code that reads the form should
   check it first and report the problem to the user.
</details>

### Exercise 6.2 (LO-6.1, ★★, about 15 minutes)

This file is `levels.lua`. Predict the three lines it prints.

```lua
local function need_string(s)
  if type(s) ~= "string" then error("need a string", 2) end
  return s
end

local function plain(s)
  local result = need_string(s)
  return result
end

local function tail(s)
  return need_string(s)
end

print(pcall(plain, 1))
print(pcall(tail, 1))
print(pcall(need_string, 1))
```

<details>
<summary>Hint</summary>

Level 2 names the line that called `need_string`, if a Lua function called it and its frame is
still on the stack.
</details>

<details>
<summary>Answer</summary>

```text
false   levels.lua:7: need a string
false   need a string
false   need a string
```

In `plain`, line 7 calls `need_string`, so level 2 names it. `tail` makes a proper tail call, so
its frame is gone, and `pcall` calls `need_string` directly in the third line; in both cases the
caller at level 2 is `pcall`, a C function, which has no line to name.
</details>

### Exercise 6.3 (LO-6.1, ★★, about 15 minutes)

Write `to_result(fn)`, which returns a new function that calls `fn` with its arguments and
returns `fn`'s results, but returns `nil` and the error value when `fn` raises an error. It turns
a function that raises errors into one that follows the `nil, message` convention.
`to_result(math.floor)("x")` returns `nil` and the message about the bad argument.

<details>
<summary>Answer</summary>

```lua
local function to_result(fn)
  return function(...)
    local results = table.pack(pcall(fn, ...))
    if not results[1] then
      return nil, results[2]
    end
    return table.unpack(results, 2, results.n)
  end
end

local floor = to_result(math.floor)
print(floor(2.7))     --> 2
print(floor("x"))     --> nil  bad argument #1 to 'math.floor' (number expected, got string)
```

`table.unpack(results, 2, results.n)` returns every result of `fn`, skipping `pcall`'s `true`.
The message says `'math.floor'` rather than `'floor'`, the name a direct call gives, because
`pcall` called the function, and Lua found its name by searching the loaded modules.
Use a wrapper like this at a boundary, such as a request handler, and not around every call: it
turns bugs into `nil` results that a caller can silently ignore.
</details>

### Exercise 6.4 (LO-6.2, ★★, about 10 minutes)

`package.path` is `"./?.lua;./lib/?.lua;./lib/?/init.lua"`. Which files does
`require("http.client")` try, in order? And if a program calls `require("http.client")` in two
different files, how many times does `client.lua` run?

<details>
<summary>Answer</summary>

`./http/client.lua`, `./lib/http/client.lua`, then `./lib/http/client/init.lua`, after checking
`package.preload`. The file runs once: the first `require` stores its result in
`package.loaded["http.client"]`, and the second returns that same value.
</details>

### Exercise 6.5 (LO-6.2, ★★, about 15 minutes)

`counter.lua` below is meant to be a module with `counter.increment()` and `counter.value()`.
Name every problem, and fix it. What does `require("counter")` return as it is?

```lua
count = 0

function increment()
  count = count + 1
end

function value()
  return count
end
```

<details>
<summary>Answer</summary>

It returns `true`. A file that returns nothing still loads, and `require` stores `true` in
`package.loaded`. The three functions and `count` are all globals, so any other code can change
them, and two modules that use the name `count` would clash. The fix makes everything local and
returns a table:

```lua
local counter = {}
local count = 0

function counter.increment()
  count = count + 1
end

function counter.value()
  return count
end

return counter
```

`count` is now private: only the module's functions can reach it.
</details>

### Exercise 6.6 (LO-6.3, ★★, about 20 minutes)

`clamp(x, lo, hi)` returns `lo` if `x < lo`, `hi` if `x > hi`, and `x` otherwise. It raises the
error `"clamp: lo is greater than hi"` when `lo > hi`. Write a busted spec for it, assuming it is
the only function in the module `numbers`.

<details>
<summary>Answer</summary>

```lua
local numbers = require("numbers")

describe("numbers.clamp", function()
  it("returns x when it is inside the range", function()
    assert.are.equal(5, numbers.clamp(5, 0, 10))
  end)

  it("returns the bound that x is past", function()
    assert.are.equal(0, numbers.clamp(-3, 0, 10))
    assert.are.equal(10, numbers.clamp(42, 0, 10))
  end)

  it("keeps the bounds themselves", function()
    assert.are.equal(0, numbers.clamp(0, 0, 10))
    assert.are.equal(10, numbers.clamp(10, 0, 10))
  end)

  it("raises an error when lo is greater than hi", function()
    assert.has_error(function() numbers.clamp(5, 10, 0) end, "clamp: lo is greater than hi")
  end)
end)
```

The test of the bounds themselves catches a version written with `<=` and `>=` that returns the
other bound, and the error test catches a version that swaps the bounds silently.
</details>

### Exercise 6.7 (LO-6.3, ★★★, about 15 minutes)

A suite for `mean(list)` has these two tests, and both pass. Write a wrong `mean` that passes them
too, and the test that would catch it.

```lua
it("averages two numbers", function() assert.are.equal(3, mean({ 2, 4 })) end)
it("averages one number", function() assert.are.equal(7, mean({ 7 })) end)
```

<details>
<summary>Answer</summary>

One that passes: `function mean(list) return (list[1] + list[#list]) / 2 end`, which averages only
the first and last items. It gives 3 and 7, but `mean({ 1, 2, 6 })` gives 3.5 instead of 3. Add
`assert.are.equal(3, mean({ 1, 2, 6 }))`: a list of three or more items whose middle matters.
Every test should be able to fail for some wrong version, and a set of tests is strong when no
small mistake passes all of them.
</details>

### Exercise 6.8 (LO-6.2, ★★, about 15 minutes)

A file `config.lua`, on the path, returns `{ debug = false }`. A program runs these lines in order:

```lua
package.preload.config = function() return { debug = true } end
print(require("config").debug)   -- (a)
package.loaded.config = nil
print(require("config").debug)   -- (b)
package.preload.config = nil
package.loaded.config = nil
print(require("config").debug)   -- (c)
```

1. What do lines (a), (b), and (c) print?
2. A test must make `require("clock")` return `{ now = function() return 0 end }` for the code
   under test, without a file. Write the line it needs.

<details>
<summary>Hint</summary>

`require` checks `package.loaded` first, then asks the searchers in order, and `package.preload`
is the first of them.
</details>

<details>
<summary>Answer</summary>

1. `true`, `true`, and `false`. In (a), the first searcher finds the loader in `package.preload`
   before any file is tried. In (b), clearing `package.loaded.config` makes `require` search again,
   and `package.preload` still wins. In (c), with both cleared, the file searcher finds
   `config.lua`.
2. `package.loaded.clock = { now = function() return 0 end }`, before the code under test runs
   `require("clock")`. Setting `package.preload.clock` to a function that returns the table works
   too.
</details>
