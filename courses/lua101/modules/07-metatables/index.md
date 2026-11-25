# Module 7: Metatables

**Objectives:** LO-7.1, LO-7.2, LO-7.3\
**Prerequisites:** [Module 3](../03-tables/index.md) and
[Module 5](../05-closures-and-iterators/index.md)\
**Time:** about 8 hours: 2.5 for this reading, 2 for [Lab 7](lab07.ipynb), 1.5 for the
[practice](practice.md), and 2 for [Self-test 1](../../self-tests/self-test-1.md), which follows
this module

Lua has no classes, no operator overloading, and no properties, yet Lua programs have all three.
They build them from one mechanism: the **metatable**, a table that changes how another table
behaves. This module shows how to give a table its own `+`, `==`, and `tostring`; how to supply
missing keys and catch new ones, for default values, proxies, and read-only tables; and how to
make a cache that doesn't keep its keys alive. Module 8 builds classes from the same pieces.

## What a metatable is

Any table can have a metatable. `setmetatable(t, mt)` gives `t` the metatable `mt` and returns
`t`, and `getmetatable(t)` returns it:

```lua
local mt = {}
local t = setmetatable({}, mt)
print(getmetatable(t) == mt)      --> true
```

The metatable's fields whose names start with two underscores, such as `__add` and `__index`, are
**metamethods**. When Lua meets an operation that a table doesn't support on its own, such as
`t + 1` or reading a missing key, it looks in the table's metatable for the matching metamethod,
and calls it if it is there. Without one, the operation does what it always did: `t + 1` raises
`attempt to perform arithmetic on a table value`, and a missing key reads as `nil`.

Many tables can share one metatable, and usually do: every vector shares one, every account
another. Strings all share one too, which is how `("x"):rep(3)` works (module 4). From Lua code
you can set the metatable of tables only; `setmetatable("x", {})` stops with
`table expected, got string`.

## Operators

The arithmetic metamethods are `__add`, `__sub`, `__mul`, `__div`, `__mod`, `__pow`, `__unm`
(unary minus), and `__idiv` (`//`). The bitwise operators have their own, such as `__band`, and so
do `..` (`__concat`) and `#` (`__len`). Here is a two-dimensional vector:

```lua
local Vector = {}

local function vec(x, y)
  return setmetatable({ x = x, y = y }, Vector)
end

function Vector.__add(a, b)
  return vec(a.x + b.x, a.y + b.y)
end

function Vector.__mul(a, b)
  if type(a) == "number" then return vec(a * b.x, a * b.y) end     -- 2 * v
  if type(b) == "number" then return vec(a.x * b, a.y * b) end     -- v * 2
  return a.x * b.x + a.y * b.y                                     -- v * w: the dot product
end

function Vector.__tostring(v)
  return "(" .. v.x .. ", " .. v.y .. ")"
end

local a, b = vec(1, 2), vec(3, 4)
print(a + b, 2 * a, a * 2, a * b)     --> (4, 6)  (2, 4)  (2, 4)  11
```

To pick the metamethod for a binary operator, Lua looks at the first operand's metatable, and then
at the second's. It passes both operands in their original order. So `2 * a` calls
`Vector.__mul(2, a)`, with the number first, even though the number has no metatable. A
metamethod for an operator that mixes types must check which side is which, as `__mul` does.

`print` and `tostring` call `__tostring` when there is one. Without it, they print the address,
such as `table: 0x5c3e…`; a metatable field `__name` replaces the word `table` with a name of
your choosing.

### Comparison

`__eq`, `__lt`, and `__le` define `==`, `<`, and `<=`. Lua derives the other three: `a ~= b` is
`not (a == b)`, `a > b` is `b < a`, and `a >= b` is `b <= a`. Three details matter:

- `__eq` is called only when both operands are tables, and they aren't the same table. A table
  is never equal to a number, whatever its metamethods say, and a table is always equal to
  itself.
- The result of a comparison is always a boolean: Lua converts whatever the metamethod returns.
- Define `__le` yourself. The Lua 5.4 manual doesn't derive `<=` from `__lt`. The makefile in
  Lua's own source release does turn on a compatibility option that still derives it, so a `lua`
  built from it may accept `a <= b` with only `__lt`, while the Lua in the course's notebooks
  raises `attempt to compare two table values`. Code that defines both works everywhere.

### Calling a table

`__call` makes a table callable like a function. The table itself arrives as the first argument:

```lua
local greeter = setmetatable({ greeting = "Hello" }, {
  __call = function(self, name) return self.greeting .. ", " .. name end,
})
print(greeter("Ada"))      --> Hello, Ada
```

## Missing keys: `__index`

When you read a key that a table doesn't have, Lua looks for `__index` in its metatable. It can be
a table or a function.

**A table:** Lua looks the key up in that table instead, which may have its own metatable, and so
on. This is how a table falls back on defaults:

```lua
local defaults = { color = "red", size = 1 }
local shape = setmetatable({ size = 5 }, { __index = defaults })
print(shape.color, shape.size)    --> red  5
print(rawget(shape, "color"))     --> nil
```

`shape.size` is found in `shape` itself, so `defaults` is never consulted for it. **`rawget(t, k)`
reads `t[k]` without metamethods**, which shows that `color` isn't in `shape`: it only appears to
be. Module 8 makes classes from this: the methods live in one table, and every object's
`__index` points at it.

**A function:** Lua calls it with the table and the key, and its result is the value read. Use a
function when the value must be computed:

```lua
local counts = setmetatable({}, { __index = function(t, key) return 0 end })
counts.apples = counts.apples + 1
print(counts.apples, counts.pears)    --> 1  0
```

Reading `counts.pears` returns 0 but stores nothing; only the assignment to `counts.apples`
created a key.

## New keys: `__newindex`

Assigning to a key that a table doesn't have calls `__newindex(t, key, value)` instead of storing
the value. Assigning to a key the table already has never calls it. **`rawset(t, k, v)` stores a
value without metamethods**, so a `__newindex` that wants the assignment to happen after all uses
`rawset`, not `t[k] = v`, which would call it again forever:

```lua
local log = {}
local watched = setmetatable({ existing = 1 }, {
  __newindex = function(t, key, value)
    log[#log + 1] = key
    rawset(t, key, value)
  end,
})
watched.existing = 2      -- the key exists: no call
watched.added = 3         -- a new key: __newindex runs and stores it
watched.added = 4         -- it exists now: no call
print(table.concat(log, ","))     --> added
```

### Proxies and read-only tables

Because the metamethods run only for keys that are absent, the way to control every read and
every write is a **proxy**: an empty table that stands in for the real one. All reads miss, so
they reach `__index`; all writes are new keys, so they reach `__newindex`. A read-only view is a
proxy whose `__newindex` refuses:

```lua
local function read_only(t)
  return setmetatable({}, {
    __index = t,
    __newindex = function() error("attempt to change a read-only table", 2) end,
    __len = function() return #t end,
    __pairs = function() return next, t, nil end,
  })
end

local days = read_only({ "Mon", "Tue" })
print(days[1], #days)       --> Mon  2
days[3] = "Wed"             --> error: attempt to change a read-only table
```

The proxy itself is empty, so without `__len` its length would be 0, and without `__pairs`, a
`pairs` loop over it would visit nothing; `pairs` calls `__pairs` when there is one. `ipairs`
reads through `__index`, so it works already. A proxy doesn't stop everything: `rawset(days, 3,
"Wed")` stores the value in the proxy anyway, and the real table is still writable by any code
that has a reference to it.

## Weak tables

A table normally keeps its keys and values alive: the garbage collector, which frees memory no
longer reachable from the program, won't free a value while a table holds it. That is a problem
for a cache. A table that maps each object to some computed data keeps every object alive
forever, even after the rest of the program has forgotten it.

A **weak table** holds its keys, its values, or both, without keeping them alive. The metatable
field `__mode` says which: `"k"` for weak keys, `"v"` for weak values, `"kv"` for both. When the
collector frees an object, it removes every entry of a weak table whose weak part was that object:

```lua
local area_cache = setmetatable({}, { __mode = "k" })

local function area(shape)
  local result = area_cache[shape]
  if result == nil then
    result = shape.width * shape.height
    area_cache[shape] = result
  end
  return result
end

local box = { width = 2, height = 3 }
print(area(box))          --> 6, cached under the key box
box = nil                 -- the program no longer refers to the box
collectgarbage()          -- a full collection frees it, and removes its entry
print(next(area_cache))   --> nil
```

Three rules say what a weak table loses, and when:

1. **Only objects are removed:** tables, functions, coroutines, and userdata. Numbers and booleans
   aren't collected, and strings, although they are, behave like values here, so an entry whose
   weak part is a number, a boolean, or a string is never removed.
2. **An entry goes only when its weak part is unreachable from anywhere else.** In a weak-key
   table, an entry whose value refers to its own key still goes: Lua treats such a table as an
   **ephemeron table**, where a value counts as reachable only if its key is.
3. **Removal happens during garbage collection,** which runs on its own as the program allocates
   memory. Between collections, an unreachable entry is still there. `collectgarbage()` forces a
   full collection, which is how tests and Lab 7 make removal happen at a known moment.

Use weak keys to attach data to objects that you don't own, such as the cache above. Use weak
values for a cache of objects that are expensive to build, which may be dropped when nothing else
uses them.

## Protecting a metatable

A metatable field `__metatable` hides and locks the metatable: `getmetatable` returns the field's
value instead, and `setmetatable` on the table raises `cannot change a protected metatable`. A
module can use it so that code outside the module can't replace the metatable its objects rely
on.

## Common misconceptions

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| `2 * v` calls `__mul(v, 2)` | Operands keep their order | `__mul` must check whether its first argument is a number |
| `__eq` makes a table equal to a number | `__eq` runs only when both operands are tables | `v == 1` is `false`, with no call |
| Defining `__lt` defines `<=` | Lua 5.4 doesn't promise it | lupa's Lua raises `attempt to compare two table values` |
| `__index` runs on every read | Only for keys the table doesn't have | `shape.size` never consults the defaults |
| `__newindex` runs on every write | Only for new keys | `watched.added = 4` makes no call |
| `t[k] = v` inside `__newindex` stores the value | It calls `__newindex` again, forever | Use `rawset(t, k, v)` |
| A read-only proxy can't be changed at all | `rawset` bypasses it, and the original is still writable | `rawset(days, 3, "Wed")` works |
| A weak table loses an entry as soon as its object is unused | Only at the next collection | Count the entries before and after `collectgarbage()` |
| Weak keys drop string keys too | Strings behave like values | `weak["name"]` survives every collection |

## Summary

- A metatable is a table of metamethods that tells Lua what to do when an operation isn't defined
  for a table; `setmetatable` returns its table, so you can write it inline.
- Arithmetic, `..`, `#`, comparison, `tostring`, and calls each have a metamethod. Binary
  operators try the first operand's metatable, then the second's, and pass both in order.
- Define `__eq`, `__lt`, and `__le` explicitly; Lua derives `~=`, `>`, and `>=` from them, and
  converts results to booleans.
- `__index` supplies keys a table lacks, from a table or a function; `__newindex` handles
  assignments to new keys. `rawget` and `rawset` bypass both.
- An empty proxy table sees every read and write, which is how read-only tables work; it needs
  `__len` and `__pairs` to answer `#` and `pairs`.
- A weak table, with `__mode` set to `"k"`, `"v"`, or `"kv"`, lets the collector remove entries
  whose weak part is an unreachable object, at the next collection.

## Self-check

1. With `Vector` from the reading, what does `a * 3` call, with which arguments, and what does
   `3 * a * a` give for `a = vec(1, 2)`?

   <details>
   <summary>Answer</summary>

   `Vector.__mul(a, 3)`, which returns `vec(3, 6)`. `3 * a * a` is `(3 * a) * a`: first
   `__mul(3, a)` gives `vec(3, 6)`, then `__mul(vec(3, 6), a)` gives the dot product,
   3 · 1 + 6 · 2 = 15.
   </details>

2. `local t = setmetatable({}, { __index = function(t, k) return k .. "!" end })`. What are `t.hi`,
   `rawget(t, "hi")`, and `t[1]`?

   <details>
   <summary>Answer</summary>

   `"hi!"`, `nil`, and `"1!"`. The function runs for every missing key, and `..` converts the
   number 1 to a string. Nothing is stored, so `rawget` finds nothing.
   </details>

3. Why does a read-only table need to be an empty proxy rather than the real table with a
   `__newindex` metamethod?

   <details>
   <summary>Answer</summary>

   `__newindex` runs only for keys the table doesn't have. On the real table, assigning to an
   existing key, such as `t[1] = "x"`, would change it without a call. In an empty proxy every key
   is missing, so every assignment reaches `__newindex`.
   </details>

4. A weak-value table holds `{ a = {}, b = "text", c = saved }`, where `saved` is a local still in
   use. Which entries remain after `collectgarbage()`?

   <details>
   <summary>Answer</summary>

   `b` and `c`. The table at `a` is reachable only through the weak table, so it is collected and
   the entry removed. The string at `b` is never removed, and `saved` is still reachable.
   </details>

5. When would you use a weak-key table rather than a field stored in the object itself?

   <details>
   <summary>Answer</summary>

   When the objects aren't yours to change, such as tables another module created, or when the
   data shouldn't be visible to `pairs` over the object. The weak keys let the objects be
   collected as if the extra data weren't there.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, section
  [2.4, Metatables and Metamethods](https://www.lua.org/manual/5.4/manual.html#2.4), which lists
  every metamethod and the exact rules for choosing one, and section
  [2.5.4, Weak Tables](https://www.lua.org/manual/5.4/manual.html#2.5.4).
- Roberto Ierusalimschy, Luiz Henrique de Figueiredo, and Waldemar Celes,
  ["A Look at the Design of Lua"](https://dl.acm.org/doi/10.1145/3186277), *Communications of the
  ACM* 61(11), 2018. It explains why Lua offers mechanisms such as metatables instead of features
  such as classes.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapters on
  metatables and metamethods and on garbage collection have more examples of proxies and weak
  tables.
