# Module 7 practice

These exercises practice the [Module 7 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it in a `%%lua` cell or in `lua -i`.

## Worked example: a chain of defaults

A program has built-in settings, settings from a file, and settings the user typed. A setting the
user typed wins over the file's, and the file's over the built-in one. Make one table that reads
that way.

1. Each level is a table: `builtin`, `file`, and `typed`.
2. `typed` should fall back on `file`, so `file` becomes the `__index` of `typed`'s metatable.
3. `file` should fall back on `builtin` in the same way.
4. A read of `typed.k` now looks in `typed`, then `file`, then `builtin`, and stops at the first
   that has `k`.

```lua
local builtin = { theme = "light", size = 12, wrap = true }
local file = setmetatable({ size = 14 }, { __index = builtin })
local typed = setmetatable({ theme = "dark" }, { __index = file })

print(typed.theme, typed.size, typed.wrap, typed.missing)   --> dark  14  true  nil
```

Assigning `typed.size = 16` stores the value in `typed` itself, because `typed` has no
`__newindex`; `file` and `builtin` don't change.

### Exercise 7.1 (LO-7.1, ★, about 10 minutes)

`money` has a metatable with `__add` and `__concat`, each of which prints its arguments' types.
Which metamethod does each line call, with which argument types?

1. `money + 5`
2. `5 + money`
3. `"Total: " .. money`
4. `money .. money`

<details>
<summary>Answer</summary>

1. `__add(table, number)`. 2. `__add(number, table)`. 3. `__concat(string, table)`.
4. `__concat(table, table)`. In every case the operands keep their order, so each metamethod must
check which of its arguments is the table.
</details>

### Exercise 7.2 (LO-7.1, ★★, about 20 minutes)

Write a `Money` type that stores an amount in whole cents, made by `money(cents)`. `+` adds two
amounts, and raises an error if either operand isn't `Money`. `==`, `<`, and `<=` compare amounts.
`tostring(money(1250))` is `"$12.50"`.

<details>
<summary>Answer</summary>

```lua
local Money = {}

local function money(cents)
  return setmetatable({ cents = cents }, Money)
end

function Money.__add(a, b)
  if getmetatable(a) ~= Money or getmetatable(b) ~= Money then
    error("can only add money to money", 2)
  end
  return money(a.cents + b.cents)
end

function Money.__eq(a, b) return a.cents == b.cents end
function Money.__lt(a, b) return a.cents < b.cents end
function Money.__le(a, b) return a.cents <= b.cents end

function Money.__tostring(m)
  return string.format("$%d.%02d", m.cents // 100, m.cents % 100)
end

print(money(1250) + money(75), money(5) < money(10))   --> $13.25  true
```

Whole cents avoid the rounding error of floats, such as 0.1 + 0.2, from module 1. `__le` is
defined, not left to Lua, because Lua 5.4 doesn't promise to derive it. This `__tostring` handles
amounts of 0 or more only; a negative amount needs its sign handled first.
</details>

### Exercise 7.3 (LO-7.2, ★★, about 15 minutes)

Make a table `config` that records every missing key a program reads, so that you can find typos
in setting names. The first step is done for you: the keys go in a local list `missing`, which a
closure can reach.

```lua
local missing = {}
local config = setmetatable({ width = 800 }, {
  __index = function(t, key)
    -- your code here
  end,
})
```

<details>
<summary>Answer</summary>

```lua
local missing = {}
local config = setmetatable({ width = 800 }, {
  __index = function(t, key)
    missing[#missing + 1] = key
    return nil
  end,
})

local w, h = config.width, config.hieght
print(w, h, table.concat(missing, ","))   --> 800  nil  hieght
```

`config.width` exists, so it never reaches `__index`; only the misspelled `hieght` is recorded.
Returning `nil` keeps the usual behavior of a missing key.
</details>

### Exercise 7.4 (LO-7.2, ★★★, about 20 minutes)

Module 1's worst bug was a misspelled name that silently became a global. Use a metatable on the
global table, `_G`, so that reading a global that was never assigned raises an error, and so does
assigning a new global anywhere except at the top level of the main program. Explain why `rawset`
and `rawget` are needed.

<details>
<summary>Hint</summary>

`debug.getinfo(2, "S").what` is `"main"` when the code doing the assignment is the main chunk, and
`"Lua"` inside a function.
</details>

<details>
<summary>Answer</summary>

```lua
local declared = {}
setmetatable(_G, {
  __newindex = function(t, name, value)
    if debug.getinfo(2, "S").what ~= "main" then
      error("assignment to undeclared global '" .. tostring(name) .. "'", 2)
    end
    declared[name] = true
    rawset(t, name, value)
  end,
  __index = function(t, name)
    if not declared[name] then
      error("read of undeclared global '" .. tostring(name) .. "'", 2)
    end
  end,
})
```

`rawset` is needed to store the global, because `t[name] = value` inside `__newindex` would call
`__newindex` again. Existing globals such as `print` are in `_G`, so they never reach either
metamethod. A global set to `nil` stays declared, so reading it gives `nil` without an error.
A linter such as luacheck, in module 11, catches the same mistakes before the program runs,
without changing `_G`.
</details>

### Exercise 7.5 (LO-7.2, ★★, about 10 minutes)

A read-only proxy built with only `__index` and `__newindex` gives `#proxy == 0`, and `pairs`
visits nothing, but `ipairs` visits every item. Explain all three.

<details>
<summary>Answer</summary>

The proxy is an empty table. `#` and `pairs` look at the table itself, and find nothing, unless
the metatable has `__len` and `__pairs`. `ipairs` reads `proxy[1]`, `proxy[2]`, and so on, and
each of those reads misses and goes through `__index` to the real table, so it sees every item.
</details>

### Exercise 7.6 (LO-7.3, ★★, about 15 minutes)

Choose `__mode` for each cache, or say why a weak table doesn't help.

1. Extra data about each window object of a GUI library, which you can't add fields to.
2. Images loaded from disk, keyed by file name, which should be freed when no window shows them.
3. Compiled regular expressions, keyed by the pattern string.

<details>
<summary>Answer</summary>

1. Weak keys, `"k"`: an entry should go when its window does.
2. Weak values, `"v"`: the keys are strings, which are never removed, but each image is an object,
   so an entry goes when nothing else uses its image.
3. A weak table doesn't help: the key is a string, and if the value is a table that only the
   cache uses, weak values would empty the cache at every collection. Limit the cache's size
   instead, for example by keeping the 100 patterns used most recently.
</details>
