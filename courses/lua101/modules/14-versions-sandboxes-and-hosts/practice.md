# Module 14 practice

These exercises practice the [Module 14 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then check it in a `%%lua` cell, with `--version 5.1`,
`--version luajit`, or `--version 5.5` where the exercise names another Lua.

## Worked example: porting `table.pack`

A function counts its arguments, `nil`s included, with `table.pack`, which Lua 5.1 and LuaJIT
don't have. Make it run on all four Luas.

```lua
local function count_args(...)
  return table.pack(...).n
end
```

1. **Name what is missing, and where.** `table.pack` is missing on 5.1 and LuaJIT. The rest, `...`
   and a table's field `n`, works everywhere.
2. **Detect the feature, not the version.** `table.pack or …` uses the real function wherever it
   exists.
3. **Write the fallback from what every version has.** `select("#", ...)` counts the arguments,
   `nil`s included, in every version, and `{ ... }` collects them.

```lua
local pack = table.pack or function(...)
  return { n = select("#", ...), ... }
end

local function count_args(...)
  return pack(...).n
end
```

`count_args(1, nil, 3)` returns 3 on 5.1, LuaJIT, 5.4, and 5.5. Writing `#{ ... }` instead would be
wrong: with a `nil` among the items, the table has a hole, and `#` may give 1 or 3.

### Exercise 14.1 (LO-14.1, ★, about 10 minutes)

Which of these lines compile on Lua 5.1, and which on LuaJIT?

1. `local x <const> = 1`
2. `goto done ::done::`
3. `local y = 7 // 2`
4. `local z = 2 ^ 10`

<details>
<summary>Answer</summary>

1. Neither: attributes such as `<const>` arrived in Lua 5.4.
2. LuaJIT only: it took `goto` from Lua 5.2; 5.1 reads `goto` as a variable name and fails with
   `'=' expected near 'done'`.
3. Neither: there is no `//` without integers. Compile it from a string where it works, as the
   reading shows.
4. Both: `^` exists in every version, and always gives a float, which 5.4 and 5.5 print as
   `1024.0`.
</details>

### Exercise 14.2 (LO-14.1, ★★, about 10 minutes)

A test passes on Lua 5.4 and fails on Lua 5.5. Why, and how would you fix it?

```lua
assert(tostring(0.1 + 0.2) == "0.3")
```

<details>
<summary>Answer</summary>

`0.1 + 0.2` isn't exactly 0.3 in binary floating point. Lua 5.4 prints floats with 14 significant
digits, which round it to `0.3`; Lua 5.5 printed `0.30000000000000004`, because 14 digits don't give
back the same number. The test depended on how many digits `tostring` prints. Compare numbers, not
text, with a tolerance: `assert(math.abs((0.1 + 0.2) - 0.3) < 1e-12)`. If the text is what you are
testing, fix the format yourself: `string.format("%.14g", 0.1 + 0.2)` is `"0.3"` on all four Luas.
</details>

### Exercise 14.3 (LO-14.1, ★★, about 15 minutes)

This loop is meant to skip the character after each backslash. It compiles on Lua 5.4 but not on
Lua 5.5. What does it do on 5.4, and why did Lua 5.5 make it an error?

```lua
for i = 1, #s do
  if s:sub(i, i) == "\\" then
    i = i + 1
  end
  -- … use s:sub(i, i) …
end
```

<details>
<summary>Answer</summary>

On 5.4 it skips nothing: the loop keeps its own counter, and `i` is a copy that the next pass
replaces. A loop that assigned `i = i + 1` on every pass still printed `1 2 3`. The assignment
changes `i` only for the rest of the current pass, which is rarely what the writer meant, so 5.5
makes the variable read-only and reports `attempt to assign to const variable 'i'`. To skip
characters, use a `while` loop with a counter of your own.
</details>

### Exercise 14.4 (LO-14.2, ★★, about 15 minutes)

For each function, say whether adding it to a sandbox's allowlist would let a plugin escape a
limit or reach the host, and how: `load`, `getmetatable`, `rawequal`, `string.format`,
`coroutine.wrap`, and `setmetatable`.

<details>
<summary>Answer</summary>

- `load`: yes. A chunk loaded without an environment gets the real globals:
  `load("return os")()` is the host's `os`.
- `getmetatable`: yes. `getmetatable("").__index` is the host's real `string` table, which the
  plugin can change.
- `rawequal`: no. It compares two values without metamethods, and reaches nothing.
- `string.format`: no. It works only on its arguments, and rejects a huge width such as `%99999999d`
  with `invalid conversion specification`.
- `coroutine.wrap`: yes. A new coroutine has no hook. In a test, a plugin's own coroutine counted
  to 10 million while the sandbox's hook, set to stop it after 100,000 instructions, never fired.
  A sandbox that offers coroutines must set its hook in each one it creates.
- `setmetatable`: yes. A `__gc` finalizer runs with hooks turned off, at a later collection, so a
  loop in it is outside every limit.
</details>

### Exercise 14.5 (LO-14.2, ★★★, about 20 minutes)

A plugin system lets plugins search text with patterns of their own, through `string.find`. A
colleague proposes limiting the text to 1,000 characters to prevent the backtracking attack. Does
that work? Propose a defense that does, and say what it costs.

<details>
<summary>Answer</summary>

It doesn't. In the reading's tests, `".-.-b"` took 1.17 seconds on 1,000 characters, and
`".-.-.-b"` took 8.2 seconds on 400. The time grows as a power of the text's length, and each
repetition item in the pattern raises the power: with `".-.-b"`, 600 characters took 0.23 seconds
and 1,000 took 1.21, about the cube of the ratio of the lengths. So the pattern matters as much as
the text. Defenses that work:

- **Run plugins in a separate process, and kill it after a deadline.** It bounds every kind of
  work, in Lua or in C, but each call to a plugin now crosses a process boundary, which costs time
  and means passing data as text or bytes.
- **Don't take patterns from plugins.** Offer `string.find(s, word, 1, true)`, a plain search,
  whose time grows only with the text's length times the word's, or a few fixed patterns the host
  chose. It is fast and safe, and plugins lose expressiveness.
- **Limit the pattern too,** for example to at most one repetition item (`*`, `+`, or `-`). That
  bounds the cost by about the text's length squared, but every rule like it must be checked
  against the whole pattern syntax, and is easy to get wrong.
</details>

### Exercise 14.6 (LO-14.3, ★★, about 15 minutes)

This Redis script fails. Why? And why shouldn't a Redis script loop over a million keys, even
correctly?

```lua
count = redis.call("GET", KEYS[1])
return count
```

<details>
<summary>Answer</summary>

Redis's sandbox doesn't let scripts create global variables, and `count` is one: the script fails
with an error that says it attempted to create a global variable. Declare it `local count`. A long
script is a problem because Redis runs a script atomically: the whole server is blocked while it
runs, and no other client's command runs until it finishes. A script must do a small amount of work
and return, as code for any host's event loop must.
</details>

### Exercise 14.7 (LO-14.1, ★★, about 15 minutes)

This code runs on LuaJIT.

```lua
local ffi = require("ffi")
local a = ffi.new("int[?]", 3)
for i = 1, 3 do a[i - 1] = i * 10 end
print(a[0], a[2], ffi.sizeof(a))
```

1. What does the last line print on LuaJIT?
2. What happens on Lua 5.4, and why?
3. A teammate wants to return `a` from a function and let callers loop over it with `ipairs`. Give
   two reasons not to.

<details>
<summary>Hint</summary>

An `int` takes 4 bytes. For part 3, think about where the array starts, what checks its bounds, and
what `ipairs` expects.
</details>

<details>
<summary>Answer</summary>

1. `10  30  12`. The loop fills indices 0, 1, and 2 with 10, 20, and 30, and three 4-byte `int`s
   take 12 bytes.
2. `require("ffi")` raises an error, `module 'ffi' not found`: only LuaJIT has the FFI. Portable
   code calls `pcall(require, "ffi")` and keeps a plain-Lua path.
3. Any two of these. The array starts at index 0, so a caller's 1-based loop misses the first item
   and reads one past the end. Nothing checks its bounds, so that read returns whatever memory
   follows, without an error. And it isn't a table: `ipairs(a)` raises an error that says the
   array has no `__ipairs` metamethod, and `#a` raises one too.
</details>

### Exercise 14.8 (LO-14.2, ★★, about 15 minutes)

Predict what this code prints on Lua 5.4. Then say why this `env` is no good for a sandbox.

```lua
count = 1
local env = setmetatable({}, { __index = _G })
local chunk = load("count = count + 1; seen = true; return count", "=chunk", "t", env)
print(chunk(), count, env.count, seen, env.seen)
```

<details>
<summary>Hint</summary>

The chunk's globals are fields of `env`. Reading a field that `env` lacks goes through `__index`;
writing one doesn't.
</details>

<details>
<summary>Answer</summary>

`2  1  2  nil  true`. In the chunk, `count` reads `env.count`, which isn't there, so `__index`
finds the global `count`, 1. The assignment then stores 2 in `env` itself, because only reading
goes through `__index`. So the global `count` stays 1, and `seen` exists only in `env`.

This `env` lets a chunk read every global, so `load("return os.remove", "=x", "t", env)()` returns
the real `os.remove`. The pattern suits code you trust that should keep its own globals, never a
sandbox, which must start from an allowlist.
</details>

