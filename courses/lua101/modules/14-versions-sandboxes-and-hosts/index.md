# Module 14: Versions, sandboxes, and hosts

**Objectives:** LO-14.1, LO-14.2, LO-14.3\
**Prerequisites:** [Module 6](../06-errors-modules-and-tests/index.md),
[Module 9](../09-coroutines/index.md), and [Module 10](../10-files-os-and-data/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 14](lab14.ipynb), 1.5 for the
[practice](practice.md), and 3 for the final project

Most Lua code doesn't run in the standalone `lua`. It runs inside a host: an editor, a database, a
document converter, or a game. The host chooses which Lua runs your code, what your code can reach,
and when it runs. This module covers the three consequences. Your code may meet a Lua other than
5.4, so it detects what it can use. A host that runs other people's code must limit what that code
can do. And code written for a host is shaped by that host's API, which tests replace with a
stand-in.

## The Luas you will meet

Four Luas are in wide use, and the course's notebook environment has all four:
`%%lua --version 5.1`, `--version luajit`, and `--version 5.5` run a cell on the others.

- **Lua 5.1**, an older release that many hosts adopted and still use. Redis runs scripts on
  it.
- **LuaJIT**, a separate implementation of Lua 5.1 with a just-in-time compiler (one that turns
  frequently run Lua code into machine code while the program runs), a few features from later
  versions, and its own extensions. Neovim's Lua interface is Lua 5.1, and its documentation
  recommends building Neovim with LuaJIT.
- **Lua 5.4**, which this course teaches. Pandoc runs its filters on it.
- **Lua 5.5**, the newest release.

The differences that matter most, measured in the course's notebook environment:

| Feature | 5.1 | LuaJIT 2.1 | 5.4 | 5.5 |
| :- | :- | :- | :- | :- |
| Integers: `10 / 2` prints | `5` (no integers) | `5` (no integers) | `5.0` | `5.0` |
| `7 // 2` and `6 & 3` | Syntax errors | Syntax errors (the `bit` library instead) | `3` and `2` | `3` and `2` |
| `goto` | Syntax error | Yes | Yes | Yes |
| `<const>` and `<close>` | Syntax error | Syntax error | Yes | Yes |
| Unpacking a list | `unpack` | `unpack` | `table.unpack` | `table.unpack` |
| `table.pack`, `utf8`, `math.type` | None | None | All | All |
| `load` with a string, a mode, and an environment | No: `loadstring` and `setfenv` | Yes | Yes | Yes |
| `string.format("%d", 3.5)` | `3` | `3` | Error: no integer representation | Same error |
| `tostring(0.1 + 0.2)` | `0.3` | `0.3` | `0.3` | `0.30000000000000004` |

Earlier versions print a float with 14 significant digits. The notebook environment's Lua 5.5
printed 17 whenever 14 didn't give back the same number: `1/3` as `0.33333333333333331`, and
`100 * 1.1` as `110.00000000000001`. The manual doesn't list this among the incompatibilities, but
a test that compares printed output fails on it.

### What Lua 5.5 changes

Section 8 of the *Lua 5.5 Reference Manual* lists the changes that can break 5.4 code:

- `global` is a reserved word, for the new `global` declarations, unless Lua is compiled with the
  option `LUA_COMPAT_GLOBAL`. The notebook environment's Lua 5.5 still accepted `local global = 1`,
  so neither use of the word is safe in code meant for every build.
- The control variable of a `for` loop is read-only: `for i = 1, 3 do i = i * 2 end` fails to
  compile with `attempt to assign to const variable 'i'`. In a generic `for`, only the first
  variable is read-only, so in `for k, v in pairs(t)`, assigning to `k` fails and assigning to `v`
  doesn't. Declare a local with the same name in the body to get a copy you can change.
- A chain of `__call` metamethods can have at most 15 objects.
- `error(nil)` raises the message `<no error object>` instead of `nil`.
- `collectgarbage` sets the collector's parameters with a new option, `"param"`, and no longer with
  `"incremental"` and `"generational"`.

## Detect features, not versions

Code that must run on several Luas asks for each feature it needs, instead of reading the version.
`_VERSION` is `"Lua 5.1"` in LuaJIT, which nonetheless has `goto` and the newer `load`; a test of
the version gets both wrong.

```lua
-- A missing function: use the one that exists.
local unpack = table.unpack or unpack

-- A missing library: fall back to an equivalent.
local function utf8_len(s)
  if utf8 then return utf8.len(s) end
  return select(2, s:gsub("[^\128-\191]", ""))  -- count the bytes that start a character
end

-- Missing syntax: try to compile it. On 5.1 and LuaJIT, the chunk doesn't compile, and the
-- fallback gives the same result, because every number there is a float.
local chunk = (loadstring or load)("return function(a, b) return a // b end")
local idiv = chunk and chunk() or function(a, b) return math.floor(a / b) end
```

The last example can't write `a // b` directly: a file that contains it fails to compile on 5.1
before any line runs. Code that must compile everywhere keeps newer syntax inside a string and
compiles it only where it works. `math.type`, `jit` (a global table that only LuaJIT has), and
`pcall(load, "return 1", "=probe", "t", {})`, which fails on 5.1, are other useful probes.

Two differences can't be detected away. On 5.1 and LuaJIT every number is a 64-bit float, so
integers above $2^{53}$, about $9 \times 10^{15}$, lose precision. Code that handles 64-bit values,
such as database keys or the current time in nanoseconds (about $1.8 \times 10^{18}$), needs Lua
5.3 or later. And the loader differs in safety, which the next section explains.

## Sandboxes

A **sandbox** runs code you don't trust, such as a plugin or a user's script, so that it can do
only what you allow. Lua has no sandbox built in, but it has the parts to build one, each covering
one way the code could do harm:

| Threat | Part | Where the course covers it |
| :- | :- | :- |
| Reaching the file system, the OS, or the host's globals | An environment built from an allowlist | Modules 6 and 10 |
| Running bytecode that crashes the interpreter | `load` in text mode | Module 10 |
| Running forever | An instruction-count hook, in the plugin's own coroutine | This module; coroutines in Module 9 |
| Using all the memory | A memory check in the same hook | This module; `collectgarbage("count")` in Module 12 |

### The environment

`load(code, "=plugin", "t", env)` compiles the plugin with `env` as its globals, so the plugin
sees only what `env` holds. Build `env` from an **allowlist**, a list of what plugins may use, never
by copying `_G` and deleting what looks dangerous: a list of what to remove misses whatever you
didn't think of, and whatever a later version adds. A typical allowlist holds `assert`, `error`,
`ipairs`, `next`, `pairs`, `print`, `select`, `tonumber`, `tostring`, and `type`, and copies of
the `string`, `table`, and `math` tables, so that a plugin that changes `string.upper` changes only
its own copy.

Each function left out has a reason:

- **`load`, `loadstring`, `dofile`, and `require`** compile or run more code. `load("return os")()`
  returns the host's real `os`, because a chunk loaded without an environment gets the real global
  table.
- **`getmetatable`** reaches the metatable that every string shares, whose `__index` is the host's
  real `string` table: `getmetatable("").__index.upper = nil` breaks `upper` for the host.
- **`setmetatable`** lets a plugin attach a `__gc` finalizer. The collector runs finalizers with
  hooks turned off, so a finalizer runs outside the plugin's time limit.
- **`coroutine`** creates coroutines, which have no hook (see below).
- **`debug`, `io`, `os`, `collectgarbage`, and the `raw…` functions** reach the interpreter, the
  machine, and the limits themselves.

String methods stay reachable even so: `("x"):rep(3)` works with an empty environment, because it
goes through the string metatable, not through a global. That is safe as long as the plugin can't
get the metatable itself.

### Text mode

The `"t"` in `load(code, name, "t", env)` refuses precompiled bytecode with
`attempt to load a binary chunk (mode is 't')`. Lua checks that a binary chunk is well formed, but
not that its instructions make sense, and the manual warns that maliciously crafted bytecode can
crash the interpreter. On Lua 5.1, `loadstring` has no mode: it accepted a chunk made with
`string.dump` and ran it, so a 5.1 sandbox must refuse a chunk whose first byte is 27, the escape
character that every binary chunk starts with.

### Time and memory

The `debug` library, which a host keeps for itself, can set a **hook**: a function that Lua calls
when certain events happen. `debug.sethook(co, hook, "", n)` calls `hook` after every `n`
instructions that the coroutine `co` runs; the empty string asks for no other events. A sandbox runs
the plugin in a coroutine of its own and sets the hook there, because a hook belongs to one
coroutine: a coroutine created later has none, so a plugin given `coroutine` could escape a hook set
on the main one. The hook adds `n` to a count of instructions used, checks `collectgarbage("count")`
against the memory the sandbox started with, and raises an error when either goes over its limit.

One error isn't enough, because the plugin can catch it. If plugins get `pcall`, this one survives
the first error and keeps going:

```lua
while true do
  pcall(function() while true do end end)
end
```

So once the limit is reached, the hook switches to every instruction, with
`debug.sethook(co, stop, "", 1)`, and raises the error each time. The plugin's code between
`pcall`s then fails too, and the error reaches the top of the coroutine, where `coroutine.resume`
returns it to the sandbox. Lab 14 builds this sandbox.

A second escape is harder to see. Lua limits how deeply C calls can nest (about 200 levels in
Lua 5.4), and calling a hook written in Lua is a C call, so a plugin that recurses through `pcall`
until the C stack is nearly full leaves no room to call the hook:

```lua
local function f() while true do pcall(f) end end
f()
```

The hook fails with `C stack overflow` before its first line runs, and the plugin's `pcall` catches
that error too. In a test with the standalone `lua`, the instruction limit never stopped this
plugin; the memory check happened to stop it after 13.6 seconds. In the notebook environment's
Lua 5.4, a sandbox without a memory check was still running when it was killed after two minutes.
The fix is to give plugins a `pcall` that catches ordinary errors but passes the sandbox's own,
and stack overflows, on to its caller; Lab 14 has you write it. With it, the same plugin stopped
at once with `C stack overflow`.

### What a sandbox in Lua can't stop

The hook runs between Lua instructions, and the manual says the count event happens only while Lua
runs a Lua function. Work done inside one C function call is invisible to it:

- **One large allocation.** `("x"):rep(1e8)` builds a 100 MB string in one call. The memory check
  sees it only after it exists, and in a test, a plugin that returned `#("x"):rep(2e8)` finished,
  holding 200 MB, before the hook ran again.
- **One long computation.** `("a"):rep(1000):find(".-.-b")` searches by backtracking, trying every
  way to split the string between the two `.-` before it gives up. It ran for 1.17 seconds in one
  call, under a limit of a million instructions, and `".-.-.-b"` on 400 characters ran for 8.2
  seconds. A plugin that chooses the pattern chooses how long the host waits.
- **Compiled code on LuaJIT.** With its compiler on, LuaJIT turned an endless loop into machine
  code that never called the count hook: the loop was still running when it was killed after 20
  seconds. After `jit.off()`, the same hook stopped it in 2 milliseconds.

The remedies are outside Lua. The C API's `lua_newstate` takes an allocator function, which can
refuse to allocate past a limit; lupa offers the same as `LuaRuntime(max_memory=…)`, and with a
limit of 50 MB, `pcall(string.rep, "x", 2e8)` returned `false` and `not enough memory`. A time
limit that holds whatever the plugin does needs a second thread or process that can stop the
first: a plugin in its own OS process can be killed. A sandbox's documentation should list these
gaps, as the final project's sandbox track asks in its `THREATS.md`.

## Writing for a host

A host decides three things that shape your code:

- **Which Lua.** Code for Neovim or Redis runs on Lua 5.1 or LuaJIT, so it can't use integers,
  `//`, `<close>`, or `utf8`, and detects anything newer.
- **Which globals.** The host adds its own and may take some away. Neovim adds `vim`, with its API
  in `vim.api`. Redis adds `redis`, keeps only `os.clock` from the `os` library, disables `require`,
  and raises an error when a script creates a global variable, so every name must be `local`.
- **When your code runs.** A host calls your functions from its own loop, and your code must return
  quickly. A Redis script blocks the whole server while it runs: no other client's command runs
  until it finishes. Neovim runs plugins on its main event loop. At some moments it forbids
  changing a buffer, which its documentation calls textlock, and in callbacks from its event-loop
  library, `vim.uv`, most API calls fail. `vim.schedule(fn)` runs `fn` on the main loop's next
  turn, when those calls are allowed.

### Keep the host in a thin layer

Code that calls the host's API directly can be tested only inside the host. Split it: put the logic
in functions that take and return plain values, and the calls to the host in a thin layer that
does nothing else. Here is a Neovim plugin that removes the spaces and tabs at the ends of a
buffer's lines:

```lua
local trim = {}

-- The logic, which never touches the host: the trimmed lines, and how many changed.
function trim.lines(lines)
  local out, changed = {}, 0
  for i, line in ipairs(lines) do
    out[i] = line:gsub("[ \t]+$", "")
    if out[i] ~= line then changed = changed + 1 end
  end
  return out, changed
end

-- The thin layer: reads the buffer through the host's API, and writes it only if a line changed.
function trim.buffer(api, buf)
  local lines = api.nvim_buf_get_lines(buf, 0, -1, false)
  local out, changed = trim.lines(lines)
  if changed > 0 then api.nvim_buf_set_lines(buf, 0, -1, false, out) end
  return changed
end
```

Neovim's API counts lines from 0, ends ranges before their last index, and reads -1 as "after the
last line", so `0, -1` is the whole buffer. `false` turns off strict indexing, which would make an
out-of-range index an error instead of clamping it to the buffer.

`trim.buffer` takes `api` as an argument instead of reading the global `vim.api`, so a test can pass
a **stand-in**: a table with the same functions, which keeps the lines in a list and records each
call. The test then checks the records, for example that the plugin read the buffer once and didn't
write it when no line changed. Lab 14 builds this stand-in, adds a version of the plugin that waits
for `vim.schedule`, and runs the tests on LuaJIT, which Neovim's documentation recommends building
it with, as well as on 5.4. A stand-in shows that your code uses the API the way you meant; it can't
show that you understood the API correctly, so try the plugin in the real host too.

## Common misconceptions

| Belief | What is true | Example that breaks it |
| :- | :- | :- |
| `_VERSION` tells you what you can use | LuaJIT reports `Lua 5.1` and has features 5.1 lacks | `goto` works on LuaJIT |
| A file can test for `//` before using it | A file with `//` doesn't compile on 5.1 at all | Compile newer syntax from a string with `load` |
| Removing `os` and `io` from `_G` makes a sandbox | Whatever you didn't think of stays | `load("return os")()` |
| An empty environment hides the string library | String methods come through the string metatable | `("x"):rep(3)` |
| One error from the hook stops a plugin | The plugin's `pcall` catches it | `while true do pcall(f) end` |
| The count hook bounds a plugin's time | It runs only between Lua instructions | `("a"):rep(1000):find(".-.-b")` |
| A test with a stand-in proves the plugin works in the host | It proves the plugin calls the stand-in as you meant | Try it in the real host too |

## Summary

- Lua 5.1, LuaJIT, 5.4, and 5.5 differ in numbers, syntax, and libraries. Portable code detects
  each feature it needs, and compiles newer syntax from a string only where it works.
- A sandbox combines an allowlist environment, `load` in text mode, and a hook in the plugin's own
  coroutine that limits instructions and memory and, once a limit is reached, raises an error at
  every instruction. A `pcall` that passes the sandbox's errors and stack overflows on closes the
  two escapes through `pcall`.
- A hook can't see work done inside one C call, or compiled LuaJIT code; an allocator limit and a
  separate process cover what the hook can't.
- A host chooses the Lua, the globals, and when your code runs. Keep its API in a thin layer, and
  test the logic with the host replaced by a stand-in.

## Self-check

1. A function uses `table.unpack` and `math.type`. Which of the four Luas can run it unchanged, and
   how would you make it run on the others?

   <details>
   <summary>Answer</summary>

   Lua 5.4 and 5.5. On 5.1 and LuaJIT, use `local unpack = table.unpack or unpack`, and replace
   `math.type(x) == "integer"` with a check that makes sense where every number is a float, such as
   `x == math.floor(x)`, which accepts `3.0` as well.
   </details>

2. Why does a sandbox run the plugin in a coroutine of its own, instead of setting the hook on the
   coroutine the host runs in?

   <details>
   <summary>Answer</summary>

   A hook belongs to one coroutine, so setting it on the plugin's coroutine limits the plugin
   without slowing the host. It also lets the hook keep raising errors at every instruction after a
   limit is reached: the host's own code, which runs on another coroutine, isn't affected.
   </details>

3. A sandbox's allowlist includes `setmetatable`. What can a plugin do with it that runs outside
   the sandbox's time limit?

   <details>
   <summary>Answer</summary>

   Attach a `__gc` finalizer to a table: `setmetatable({}, { __gc = function() while true do end
   end })`. The collector runs finalizers with hooks turned off, whichever coroutine is running:
   in a test, a finalizer that looped for 2 seconds inside the plugin's own coroutine never
   triggered its hook. This loop would run forever, at the next collection after the table becomes
   garbage, which may be long after the plugin returned.
   </details>

4. A Neovim plugin works in its tests, which use a stand-in for `vim.api`, but in Neovim it fails
   when called from a timer callback. What is the likely cause, and the fix?

   <details>
   <summary>Answer</summary>

   Timer callbacks come from `vim.uv`, where most API functions aren't allowed. Wrap the work in
   `vim.schedule`, so it runs on the main loop's next turn. The stand-in didn't enforce that rule;
   a stand-in only checks what you built into it.
   </details>

## Further reading

- The *Lua 5.5 Reference Manual*,
  [section 8, Incompatibilities with the Previous Version](https://www.lua.org/manual/5.5/manual.html#8),
  and the same section of the
  [Lua 5.4 manual](https://www.lua.org/manual/5.4/manual.html#8), for every change that can break
  code moving forward one version.
- The Neovim documentation on [its Lua engine](https://neovim.io/doc/user/lua/) and
  [its API](https://neovim.io/doc/user/api/), for `vim.schedule`, textlock, and the buffer
  functions' indexing.
- The Redis documentation's [introduction to scripting](https://redis.io/docs/latest/develop/programmability/eval-intro/),
  for a host that runs Lua 5.1 in a sandbox of its own.
- The Pandoc documentation on [Lua filters](https://pandoc.org/lua-filters.html), for a host on
  Lua 5.4 that calls your functions for each element of a document.
