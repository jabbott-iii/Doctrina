# Module 6: Errors, modules, and tests

**Objectives:** LO-6.1, LO-6.2, LO-6.3\
**Prerequisites:** [Module 5](../05-closures-and-iterators/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 6](lab06.ipynb), 1.5 for the
[practice](practice.md), and 3 for PA3, which follows this module

Programs so far have lived in one file or one notebook, and stopped at the first error. This
module turns them into code other code can rely on. It covers how a Lua function reports that it
failed, and how its caller catches the failure; how to split a program into **modules**, files
that `require` loads; and how to test a module with **busted**, the most widely used Lua test
framework. PA3 asks for all three.

## Two ways to report a failure

A Lua function can report a failure in two ways, and the standard library uses both:

- **Raise an error** with `error(message)`. The error stops the function and every caller in turn,
  until something catches it or the program ends with the message.
- **Return `nil` and a message.** The function returns normally, and the caller checks the first
  result.

`io.open` shows the second way. Opening a file that doesn't exist isn't a bug; the caller asked
about the outside world, and the answer was no:

```lua
local file, message = io.open("missing.txt")
print(file, message)      --> nil  missing.txt: No such file or directory
```

Passing it the wrong type of argument is a bug in the calling code, so it raises an error instead:
`io.open(42, {})` stops with `bad argument #2 to 'open' (string expected, got table)`. The rule
the library follows, and a good rule for your own code:

| The failure is… | Example | Report it by… |
| :- | :- | :- |
| A mistake in the calling code | A wrong argument type, a missing argument, an empty list where one is required | Raising an error |
| An expected outcome the caller should handle | A missing file, text that isn't a number, a key that isn't there | Returning `nil` and a message |

A caller can't forget to handle an error, because it stops the program; it can forget to check a
`nil`. So raise an error when continuing would hide a bug, and return `nil` when the caller has a
sensible next step, such as asking for another file name.

### `error` and its level

`error(message, level)` raises an error. When `message` is a string, Lua puts a position in front
of it, `file:line:`, and `level` says whose position:

- Level 1, the default, is the line that called `error`.
- Level 2 is the line that called the function that called `error`. Use it when the error is the
  caller's fault, such as a bad argument, so that the message points at the code to fix.
- Level 0 adds no position.

```lua
local function check_age(age)
  if type(age) ~= "number" then
    error("age must be a number", 2)
  end
  return age
end

local function register()
  local age = check_age("ten")     -- line 9: the message names this line
  return age
end

print(pcall(register))    --> false  example.lua:9: age must be a number
```

`register` calls `check_age` in an ordinary statement here. If it wrote `return check_age("ten")`,
a proper tail call from module 2, `register` would have no stack frame left, and level 2 would
find no line to name.

An error doesn't have to be a string. `error({ code = 404, reason = "missing" })` raises a table,
which gets no position, and lets the code that catches it read its fields. Use a table when the
catcher must tell kinds of failure apart; use a string when a person will read it.

### `assert`

`assert(value, message)` raises an error with `message` when `value` is `nil` or `false`, and
otherwise returns all its arguments. That makes it a one-line way to turn a `nil, message` result
into an error, when your program can't go on without the value:

```lua
local file = assert(io.open("config.txt"))
--> config.txt: No such file or directory, if the file is missing
```

`assert` passes `io.open`'s message along as its own, and adds the position of the line that
called it. Without a message, it raises `assertion failed!`.

## Catching errors

`pcall(f, ...)` calls `f` with the given arguments in **protected mode**: if `f` raises an error,
`pcall` catches it and returns `false` and the error value; otherwise it returns `true` and all of
`f`'s results:

```lua
print(pcall(function(a, b) return a + b, a * b end, 2, 3))    --> true  5  6
print(pcall(error, "boom", 0))                                --> false  boom
local ok, err = pcall(error, { code = 404 })
print(ok, err.code)                                           --> false  404
```

By the time `pcall` returns, the functions that raised the error have already returned, so the
stack that led to the error is gone. `xpcall(f, handler, ...)` calls `handler` with the error
value first, while that stack still exists. `debug.traceback` is the usual handler: it returns
the message with a list of the calls that led to it.

```lua
local function inner() local settings = nil; return settings.width end
local function outer() return inner() + 1 end
print(xpcall(outer, debug.traceback))
--> false  example.lua:1: attempt to index a nil value (local 'settings')
--> stack traceback:
-->         example.lua:1: in upvalue 'inner'
-->         …
```

Three rules keep error handling honest:

- **Catch only what you can handle.** A `pcall` that ignores its first result hides every bug
  inside it.
- **Catch at the boundary,** where a failure turns into something a person sees: a message, a
  retry, an HTTP response. Code in between can let errors pass.
- **To rethrow, use level 0:** `error(err, 0)`. The message already has its position, and a
  second one would make it `a.lua:5: a.lua:2: boom`.

## Modules

A **module** is a Lua file that returns a value, almost always a table of functions. Lua's own
libraries are modules: `string` and `table` are tables of functions. A module keeps its helpers
private by declaring them `local`, and creates no globals:

```lua
-- geometry.lua
local geometry = {}

local function square(x)          -- private: not in the returned table
  return x * x
end

function geometry.distance(x1, y1, x2, y2)
  return math.sqrt(square(x2 - x1) + square(y2 - y1))
end

return geometry
```

Another file loads it with `require`, which returns the module's value. By convention the local
that holds it has the module's name:

```lua
local geometry = require("geometry")
print(geometry.distance(0, 0, 3, 4))       --> 5.0
```

### How `require` finds and keeps modules

`require(name)` does two things:

1. **It looks in `package.loaded`** first. This table holds every module already loaded, under its
   name. If `name` is there, `require` returns it without running the file again. So a module's
   code runs once per program, and every file that requires it gets the same table.
2. **Otherwise it searches `package.path`** for the file. `package.path` is a string of
   **templates** separated by semicolons, such as `./?.lua;./?/init.lua;…`. `require` replaces
   each `?` with the module's name, with its dots turned into directory separators, and loads the
   first file that exists. It stores the file's result in `package.loaded[name]`, and returns it,
   with the file's path as a second result.

So `require("geo.point")` with the template `./?.lua` loads `./geo/point.lua`. When no template
matches, the error lists every file it tried:

```text
module 'nope' not found:
        no field package.preload['nope']
        no file './nope.lua'
        no file '/home/ada/.venv/lua/share/lua/5.4/nope.lua'
        …
```

That list is the first thing to read when a module won't load: it shows exactly where Lua
looked. `package.searchpath(name, package.path)` runs the same search without loading anything.
Two consequences catch people out:

- **Changing a module's file doesn't change a running program.** In a notebook or in `lua -i`,
  set `package.loaded.geometry = nil` before requiring it again.
- **The paths are relative to the current directory,** the one the program was started from, not
  to the file that calls `require`. A program run from another folder can fail to find a module
  that sits next to it.

### Every place `require` looks

Searching `package.path` is one of four ways `require` finds a module. It asks each function in
the list `package.searchers` in turn, and the first one that finds the module wins. The error
above has a line from each searcher it asked:

1. **`package.preload`**, a table of loader functions by module name. A program that carries a
   module inside itself, instead of in a file, registers it here.
2. **Lua files,** along `package.path`, as the previous section describes.
3. **C libraries,** along `package.cpath`, which is how Module 13 loads a module compiled from C.
4. **One C library for several modules:** for `require("a.b")`, the library for `a`, if it has a
   function named `luaopen_a_b`.

A loader is a function that runs the module and returns its value. It receives the module's name,
and a second value from the searcher that found it, which `require` also returns as its second
result: the file's path for a file, and the string `":preload:"` for `package.preload`.

```lua
package.preload.greet = function(name, extra)
  return { hello = function() return "hi from " .. name .. " (" .. extra .. ")" end }
end
print(require("greet").hello())   --> hi from greet (:preload:)
```

A searcher of your own is a function that takes the module's name and returns a loader and the
second value. If it can't find the module, it returns a string saying why, and `require` adds that
string to its error message. This one serves modules kept in a table of source text, as a program
bundled into one file might:

```lua
local sources = { shapes = "local M = {} function M.area(w, h) return w * h end return M" }

table.insert(package.searchers, 2, function(name)   -- after preload, before the files
  local code = sources[name]
  if not code then return "no embedded module '" .. name .. "'" end
  return assert(load(code, "=" .. name, "t")), "embedded:" .. name
end)

local shapes, where = require("shapes")
print(shapes.area(3, 4), where)   --> 12  embedded:shapes
```

After this, `require("nope")` reports `no embedded module 'nope'` between the line for
`package.preload` and the lines for files. Tests use the first searcher in a simpler way: setting
`package.loaded.clock`, or `package.preload.clock`, before the code under test requires `clock`
gives that code a stand-in instead of the real module. Lua 5.1 and LuaJIT call the list
`package.loaders`.

## Testing with busted

A **unit test** calls one function with chosen inputs and checks its results. busted, installed
with LuaRocks in [setting up](../../setup.md), runs tests written in **spec files**, whose names
end in `_spec.lua`:

```lua
-- spec/geometry_spec.lua
local geometry = require("geometry")

describe("geometry.distance", function()
  it("measures a 3-4-5 triangle", function()
    assert.are.equal(5, geometry.distance(0, 0, 3, 4))
  end)

  it("is zero from a point to itself", function()
    assert.are.equal(0, geometry.distance(2, 7, 2, 7))
  end)
end)
```

`describe` groups tests, and `it` defines one test, which passes if its function finishes and
fails at the first assertion that doesn't hold. Run `busted` from the project's folder, which runs
every spec in `spec/`, or name a spec file. `--lpath=PATH` adds a template to `package.path`:

```bash
busted --lpath="./?.lua" spec/geometry_spec.lua
```

```text
●●
2 successes / 0 failures / 0 errors / 0 pending : 0.002 seconds
```

In a terminal, each green `●` is a passing test, and a failing one is a red `◼`; when busted's
output goes to a file or a notebook instead, it prints `+` and `-`. For each failure, busted
prints which assertion failed, the value it got, and the value it expected. busted exits with a
nonzero status when any test fails, so scripts and continuous integration can rely on it.

### Assertions

| Assertion | Passes when |
| :- | :- |
| `assert.are.equal(expected, actual)` | `expected == actual`; for tables, that means the same table |
| `assert.are.same(expected, actual)` | The two values have the same contents, compared deeply |
| `assert.is_true(v)`, `assert.is_nil(v)` | `v` is exactly `true`, or `nil` |
| `assert.has_error(fn, message)` | Calling `fn` raises an error whose message, without its position, is `message` |
| `assert.has_no.errors(fn)` | Calling `fn` raises no error |
| `assert.error_matches(fn, pattern)` | Calling `fn` raises an error whose message matches the Lua pattern |

`has_error` takes a function, not a call: `assert.has_error(function() stats.mean({}) end, "…")`.
Writing `assert.has_error(stats.mean({}))` calls `stats.mean` before the assertion runs, so the
error stops the test instead of being checked.

### Testing the failure paths

A test of a function that only checks its normal results misses half of what it promises. For
each function, test:

- the normal case, with a small input whose answer you worked out by hand;
- the edges: an empty list, one item, zero, the largest value, a string with no matches;
- every failure: each error it raises, with its message, and each `nil, message` it returns.

```lua
describe("stats.parse", function()
  it("returns nil and a message for text that isn't a number", function()
    local value, message = stats.parse("ten")
    assert.is_nil(value)
    assert.are.equal("not a number: ten", message)
  end)
end)

describe("stats.mean", function()
  it("raises an error for an empty list", function()
    assert.has_error(function() stats.mean({}) end, "mean: expected a non-empty list")
  end)
end)
```

A good way to judge a test suite is to break the code on purpose and see whether a test fails.
A suite that still passes when `mean` returns 0 for an empty list instead of raising an error
doesn't test that error. Lab 6 checks your tests this way.

## Common misconceptions

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| Every failure should raise an error | The library returns `nil, message` for expected failures | `io.open("missing.txt")` returns `nil` and a message |
| `error(msg, 2)` always names the caller's line | Not after a tail call, which leaves no caller frame | `return check_age("ten")` gives a message with no position |
| `pcall(f(x))` protects the call | It calls `f(x)` first, then passes the result to `pcall` | Write `pcall(f, x)` |
| An error must be a string | Any value can be raised | `error({ code = 404 })` |
| `require` reruns the file each time | It returns the cached value from `package.loaded` | Edit a module in a notebook, and `require` still gives the old one |
| `require` looks next to the calling file | It searches `package.path`, from the current directory | A program started from another folder can't find its module |
| `assert.has_error(f())` checks `f`'s error | It calls `f` too early | Pass `function() f() end` |
| Tests of the normal case are enough | Failure paths need tests of their own | A broken error check passes every normal-case test |

## Summary

- Raise an error for a mistake in the calling code, and return `nil, message` for an expected
  failure the caller should handle.
- `error(msg, 2)` blames the caller; level 0 adds no position, which is right for rethrowing. Any
  value, such as a table with fields, can be an error.
- `assert(v, msg)` turns a `nil, message` result into an error, and returns its arguments when
  `v` is truthy.
- `pcall(f, ...)` returns `true` and the results, or `false` and the error; `xpcall` calls a
  handler such as `debug.traceback` before the stack unwinds.
- A module is a file that returns a table; `require` loads it once, from the first template in
  `package.path` that matches, and caches it in `package.loaded`. Before the files, it checks
  `package.preload`, and a searcher of your own can be added to `package.searchers`.
- busted runs `describe` and `it` blocks from spec files; test every function's normal cases,
  edges, and failures, and check that the tests fail when the code is broken.

## Self-check

1. A function `load_config(name)` reads a settings file. Should a missing file raise an error or
   return `nil, message`? Should a `name` that isn't a string?

   <details>
   <summary>Answer</summary>

   A missing file should return `nil, message`: it is an expected outcome, and the caller may
   want to fall back to the defaults. A `name` that isn't a string is a bug in the calling code,
   so it should raise an error, at level 2.
   </details>

2. What does `print(pcall(error, "boom"))` print, and what does `print(pcall(error("boom")))` do?

   <details>
   <summary>Answer</summary>

   The first prints `false  boom`: `pcall` calls `error` directly, from C, so there is no Lua line
   to name. The second calls `error("boom")` before `pcall` runs, so the error isn't caught, and
   the program stops.
   </details>

3. A notebook cell runs `local m = require("stats")` after you fixed a bug in `stats.lua`, but the
   bug is still there. Why, and what is the fix?

   <details>
   <summary>Answer</summary>

   `require` found `stats` in `package.loaded` and returned the module it loaded before the fix.
   Run `package.loaded.stats = nil` first, then `require` loads the file again.
   </details>

4. With `package.path` set to `"./lib/?.lua;./?.lua"`, which files does `require("text.wrap")`
   try, and in what order?

   <details>
   <summary>Answer</summary>

   `./lib/text/wrap.lua`, then `./text/wrap.lua`. The dot becomes a directory separator, and the
   templates are tried from left to right. (`package.preload` is checked before either.)
   </details>

5. A test suite for `mean` checks `mean({ 2, 4 }) == 3` and nothing else. Give a broken version of
   `mean` that still passes, and the test that would catch it.

   <details>
   <summary>Answer</summary>

   A version that returns 0 for an empty list, instead of raising an error, passes. So does one
   that returns `list[1] + 1`. Add `assert.has_error(function() mean({}) end, "…")`, and a second
   case such as `mean({ 1, 2, 6 }) == 3`.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, sections
  [2.3, Error Handling](https://www.lua.org/manual/5.4/manual.html#2.3), and
  [6.3, Modules](https://www.lua.org/manual/5.4/manual.html#6.3), which describes every step of
  `require` and the searchers it uses, including the one that loads C modules (module 13).
- The [busted documentation](https://lunarmodules.github.io/busted/), for the full list of
  assertions, `before_each` and `after_each` for setting up each test, and the command's options.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapters on
  errors and on modules and packages have more examples of both.
