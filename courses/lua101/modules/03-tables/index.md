# Module 3: Tables

**Objectives:** LO-3.1, LO-3.2, LO-3.3, LO-3.4\
**Prerequisites:** [Module 2](../02-control-flow-and-functions/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 3](lab03.ipynb), 1.5 for the
[practice](practice.md), and 3 for PA2, which follows Module 4 and covers this module and the next

Lua has one data structure, the **table**, and builds everything else from it: arrays, records,
sets, queues, modules, and, in modules 7 and 8, objects and classes. This module covers how to
build and walk tables, why the length operator `#` can mislead you, what it means that tables are
references, and how to make four classic data structures out of them. Lua's designers chose one
flexible structure over many specialized ones to keep the language small; the price is that you
must know which uses of a table are cheap and which are not.

## One structure for everything

A table maps **keys** to **values**, like a dictionary in Python, a `Map` in JavaScript, or a
`HashMap` in Java. `{}` creates an empty table, square brackets read and write an entry, and an
entry that was never set reads as `nil`:

```lua
local t = {}
t["color"] = "red"
t[1] = "first"
print(t["color"], t[1], t["size"])   --> red  first  nil
```

When a key is a string that is also a valid name, `t.color` is shorthand for `t["color"]`. Both
lines below do the same thing:

```lua
t.color = "blue"
t["color"] = "blue"
```

Three rules decide which keys exist:

1. **Any value except `nil` and NaN can be a key:** numbers, strings, booleans, functions, and
   other tables. `t[nil] = 1` stops with `table index is nil`. Reading `t[nil]` gives `nil`.
2. **Storing `nil` removes the entry.** A table never holds a `nil` value; `t.color = nil` deletes
   the key `color`.
3. **A float key with an integer value becomes that integer,** so `t[1.0]` and `t[1]` are the same
   entry. A string is never converted, so `t[1]` and `t["1"]` are two different entries.

## Constructors

A **constructor**, an expression in braces, builds a table and fills it in one step. It has three
kinds of item, which can be mixed:

```lua
local days   = { "Mon", "Tue", "Wed" }          -- list items: keys 1, 2, 3
local point  = { x = 3, y = 4 }                 -- name = value: keys "x" and "y"
local labels = { ["first name"] = "Ada", [10] = true }  -- [any expression] = value

print(days[1], point.x, labels["first name"])   --> Mon  3  Ada
```

- List items get the keys 1, 2, 3, and so on, counting only the list items: in
  `{ "a", x = 1, "b" }`, `"b"` has the key 2.
- Lua counts from 1, not 0. `days[0]` is `nil`, and a key 0 that you set yourself is an ordinary
  key that `#` and `ipairs` ignore.
- Items are separated by commas or semicolons, and a trailing comma is allowed, which keeps diffs
  clean when you add a line.

## Sequences and `ipairs`

A table whose positive integer keys are exactly 1, 2, …, *n*, with none missing, is a
**sequence**, Lua's version of an array or a list. Other keys, such as `"x"` or 0, don't stop a
table from being a sequence. For a sequence, `#t` gives *n*, and `ipairs` walks the items in
order:

```lua
local fruits = { "fig", "pear", "plum" }
fruits[#fruits + 1] = "kiwi"         -- append: the next index is #fruits + 1
print(#fruits)                       --> 4
for i, fruit in ipairs(fruits) do
  io.write(i, "=", fruit, " ")       --> 1=fig 2=pear 3=plum 4=kiwi
end
```

`ipairs` starts at 1 and stops at the first index whose value is `nil`.

### The `table` library

The `table` library works on sequences:

| Call | What it does | Cost for a list of *n* items |
| :- | :- | :- |
| `table.insert(t, v)` | Appends `v` | Constant on average |
| `table.insert(t, pos, v)` | Inserts `v` at `pos`, moving later items up one | Grows with the items after `pos` |
| `table.remove(t)` | Removes and returns the last item | Constant |
| `table.remove(t, pos)` | Removes and returns `t[pos]`, moving later items down one | Grows with the items after `pos` |
| `table.concat(t, sep)` | Joins the items, which must be strings or numbers, with `sep` between them | Grows with the total length |
| `table.sort(t, comp)` | Sorts in place, with `<` or with the function `comp` | About *n* log *n* comparisons on average |
| `table.unpack(t, i, j)` | Returns `t[i]` through `t[j]` as separate values | Grows with `j - i` |

`table.insert(t, 1, v)` and `table.remove(t, 1)` look cheap but move every other item, which
matters in a loop; the section on queues below measures it. `table.concat` stops with an error
such as `invalid value (table) at index 2 in table for 'concat'` when an item is neither a string
nor a number.

### Sorting with a comparator

`table.sort` uses `<` unless you give it a function that takes two items and returns `true` when
the first must come before the second. To sort by age, oldest first, and by name among people of
the same age:

```lua
local people = {
  { name = "Ana", age = 31 },
  { name = "Bo",  age = 25 },
  { name = "Cy",  age = 31 },
}
table.sort(people, function(a, b)
  if a.age ~= b.age then return a.age > b.age end
  return a.name < b.name
end)
for _, p in ipairs(people) do io.write(p.name, " ") end   --> Ana Cy Bo
```

The comparator must be a strict order: it returns `false` when the two items are equal. A
comparator written with `<=` breaks that rule, and on a list with equal items `table.sort` can stop
with `invalid order function for sorting` or return the items out of order. The sort is also not
stable, so items that compare as equal can change places; that is why the example breaks ties by
name.

## Records and `pairs`

A table used as a **record** has a fixed set of named fields, like a struct or an object with no
methods:

```lua
local book = { title = "Dune", year = 1965, pages = 412 }
book.year = 1966                -- change a field
book.isbn = nil                 -- removing a field that isn't there is harmless
```

`pairs` walks every key and value in a table, whatever the keys are:

```lua
for key, value in pairs(book) do
  print(key, value)
end
```

**The order of `pairs` is unspecified.** It isn't the order of the constructor or of insertion,
and in Lua 5.4 it can change from one run of a program to the next, because Lua seeds its string
hashes from the clock and from memory addresses that change between runs. Running a loop like the
one above over six string keys, six times, printed six different orders. When order matters,
collect the keys, sort them, and walk the sorted list:

```lua
local keys = {}
for key in pairs(book) do keys[#keys + 1] = key end
table.sort(keys)
for _, key in ipairs(keys) do print(key, book[key]) end   --> pages, then title, then year
```

Two more rules about `pairs`:

- During a traversal, you may change or remove (set to `nil`) the fields that exist, but never add
  a new key; the manual leaves the result of that undefined.
- `#book` is 0, because `book` has no integer keys. To test whether any table is empty, use
  `next(book) == nil`: `next` returns a table's first key in `pairs` order, or `nil` when there is
  none.

## Nested tables

A table's values can be tables, which gives you records of lists, lists of records, and any other
shape:

```lua
local config = {
  window = { width = 800, height = 600 },
  recent = { "notes.txt", "todo.md" },
}
print(config.window.width, config.recent[2])   --> 800  todo.md
```

Reading through a level that is missing is an error, and the message names the missing field:

```lua
local settings = {}
print(settings.window.width)
--> attempt to index a nil value (field 'window')
```

When a level may be missing, test it first: `settings.window and settings.window.width` gives
`nil` instead of an error.

## The length operator and holes

`#t` is exact for a sequence. For any other table, it can mislead you, and the reason is in its
definition. The manual defines `#t` as a **border** of `t`: an index whose value is present and
whose next index is absent, or 0 when `t[1]` is absent. A sequence has exactly one border, its
length. A table with a **hole**, a `nil` between present values, has more than one:

```lua
local t = { 10, 20, nil, 40 }   -- borders: 2 (t[3] is nil) and 4 (t[5] is nil)
```

For such a table, `#t` may return any of its borders, and which one depends on how the table was
built. These two tables hold the same keys and the same values:

```lua
local a = { 1, nil, 3 }

local b = {}
b[1] = 1
b[3] = 3

print(#a, #b)    --> 3  1
```

The constructor sized `a` for three items, so Lua found the border 3; `b` grew one assignment at a
time, and Lua found the border 1. Neither answer is wrong, because both are borders, and Lua 5.4
promises nothing more. (Module 12 explains the array part and the hash part behind this.)
Computing `#t` takes at most a number of steps that grows with the logarithm of the largest
integer key, so it is fast, but it doesn't count items.

Three habits keep the length reliable:

- **Remove from the end only:** `t[#t] = nil` or `table.remove(t)` keeps a sequence a sequence.
  Setting a middle item to `nil` makes a hole.
- **Don't store `nil` in a list.** If an item can be missing, store a placeholder value such as
  `false` instead.
- **When a list must hold `nil`, keep the count yourself,** in a field named `n`, the convention
  `table.pack` follows from module 2:

  ```lua
  local results = table.pack(1, nil, 3)   -- { 1, nil, 3, n = 3 }
  for i = 1, results.n do
    print(i, results[i])                  --> 1 1, then 2 nil, then 3 3
  end
  ```

## Tables are references

A table value is a **reference**: a handle to one table that lives elsewhere in memory. Assigning
a table, passing it to a function, or storing it in another table copies the reference, never the
table. Both names below refer to the same table:

```lua
local a = { 1, 2, 3 }
local b = a          -- b refers to the same table
b[1] = 99
print(a[1])          --> 99
```

The same holds for **equality**: `==` on two tables asks whether they are the same table, not
whether they hold the same contents.

```lua
print({} == {})          --> false: two different tables
print(a == b)            --> true: one table, two names
```

A function that receives a table can change the caller's table, because it has the same
reference. Assigning a new table to the parameter only changes where the parameter points:

```lua
local function clear(list)
  for i = #list, 1, -1 do list[i] = nil end    -- changes the caller's table
end

local function reset(list)
  list = {}                                    -- changes only the local name
end

local nums = { 1, 2, 3 }
reset(nums); print(#nums)    --> 3
clear(nums); print(#nums)    --> 0
```

### Copying a table

A **shallow copy** makes a new table with the same keys and values. Any value that is itself a
table is still shared, because copying it copies its reference:

```lua
local function shallow_copy(t)
  local copy = {}
  for k, v in pairs(t) do copy[k] = v end
  return copy
end

local original = { name = "plan", steps = { "draft", "review" } }
local copy = shallow_copy(original)
copy.name = "copy"               -- independent: original.name is still "plan"
copy.steps[1] = "outline"        -- shared: original.steps[1] is now "outline" too
```

A **deep copy** copies every table it reaches, so nothing is shared. The direct way recurses into
each value that is a table, and into each key that is one, since keys can be tables too:

```lua
local function deep_copy(value)
  if type(value) ~= "table" then return value end
  local copy = {}
  for k, v in pairs(value) do
    copy[deep_copy(k)] = deep_copy(v)
  end
  return copy
end
```

This version has two flaws. A table that contains itself, such as `t` after `t.self = t`, makes
it recurse until it stops with `stack overflow`. And a table that appears twice in the original
becomes two separate tables in the copy, so the copy no longer has the original's shape. The fix
is a second table, `seen`, that maps each original table to its copy: before copying a table, the
function looks it up in `seen`, and returns the copy it already made. Lab 3 has you write it.

Neither copy keeps the original's metatable, which module 7 introduces. Copy only when you need
an independent table: copying takes time and memory in proportion to the size of what you copy.

## Four data structures

Each structure below is a table used in a particular way. The cost of an operation is given in
the notation $O(n)$, read "order *n*": the time grows in proportion to *n*, the number of items.
$O(1)$ means the time doesn't depend on *n*. Adding a key to a table is $O(1)$ on average: now and
then the table must grow, which takes longer, and module 12 explains how.

### A stack

A **stack** adds and removes at the same end, last in, first out. A sequence does it in $O(1)$:

```lua
local stack = {}
stack[#stack + 1] = "a"            -- push
stack[#stack + 1] = "b"
local top = stack[#stack]          -- peek: "b"
stack[#stack] = nil                -- pop
print(top, #stack)                 --> b  1
```

### A queue

A **queue** adds at one end and removes at the other, first in, first out. `table.insert(q, v)`
and `table.remove(q, 1)` work, but each removal moves every remaining item down one place, so it
costs $O(n)$, and emptying a queue of *n* items costs about $n^2/2$ moves. Instead, keep two
indices, one for each end, and never move anything:

```lua
local function new_queue()
  return { first = 1, last = 0, items = {} }
end

local function push(q, value)
  q.last = q.last + 1
  q.items[q.last] = value
end

local function pop(q)
  if q.first > q.last then return nil end     -- empty
  local value = q.items[q.first]
  q.items[q.first] = nil                      -- let the item be collected
  q.first = q.first + 1
  return value
end
```

Both operations are $O(1)$. On an Intel Core i7-11800H, in Lua 5.4.8 through lupa 2.8, emptying a
10,000-item list with `table.remove(t, 1)` took 0.39 s, and emptying the same items from this queue
took 0.5 ms, about 800 times less. Lab 3 repeats the measurement on your machine.

### A set

A **set** holds each value at most once, and answers "is `x` in it?". Store each member as a key
whose value is `true`:

```lua
local seen = {}
for _, word in ipairs({ "to", "be", "or", "not", "to", "be" }) do
  seen[word] = true                        -- adding a member twice changes nothing
end
print(seen["be"], seen["maybe"])           --> true  nil
seen["or"] = nil                           -- remove a member
```

Testing membership is $O(1)$ on average, because Lua finds a key by hashing it, while searching a
list for a value is $O(n)$. A set has no useful `#`, because its keys aren't 1 to *n*; count its
members with `pairs`, or keep a count as you add and remove them.

### A matrix

A **matrix** is a table of rows, each row a table of values, read as `m[i][j]`:

```lua
local function new_matrix(rows, cols, fill)
  local m = {}
  for i = 1, rows do
    local row = {}                   -- a new table for every row
    for j = 1, cols do row[j] = fill end
    m[i] = row
  end
  return m
end

local grid = new_matrix(2, 3, 0)
grid[1][2] = 5
print(grid[1][2], grid[2][2])        --> 5  0
```

The line that creates `row` inside the outer loop matters. Creating one row before the loop and
storing it in every `m[i]` stores the same reference three times, so a write to `m[1][1]` appears
in every row. Reading or writing one cell is $O(1)$.

| Structure | Built from | Operation | Cost |
| :- | :- | :- | :- |
| Stack | A sequence | Push, pop, peek | $O(1)$ |
| Queue | A sequence with `table.remove(q, 1)` | Pop | $O(n)$ |
| Queue | Two indices over a table | Push, pop | $O(1)$ |
| List | A sequence | Is `x` in it? | $O(n)$ |
| Set | Keys whose values are `true` | Is `x` in it? Add, remove | $O(1)$ on average |
| Set | Keys whose values are `true` | Count the members | $O(n)$, unless you keep a count |
| Matrix | A table of row tables | Read or write `m[i][j]` | $O(1)$ |

## Common misconceptions

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| Lists start at index 0 | They start at 1; a key 0 is an ordinary key | `#{ [0] = "a", "b" }` is 1 |
| `#t` counts every entry | It finds a border among the integer keys | `#{ x = 1, y = 2 }` is 0 |
| `#t` is reliable on a table with holes | It can return any border | `{ 1, nil, 3 }` gives 3; the same keys set one at a time give 1 |
| `pairs` visits keys in insertion order | Its order is unspecified, and can change between runs | Run a `pairs` loop over string keys twice |
| `t[1]` and `t["1"]` are the same entry | Strings are never converted to numbers as keys | `t[1] = "a"; t["1"] = "b"` makes two entries |
| `b = a` copies a table | It copies the reference | `b[1] = 99` changes `a[1]` |
| `{} == {}` compares contents | It compares identity | It is `false` |
| A shallow copy is independent | Nested tables are shared | Changing `copy.steps[1]` changes the original's |
| `table.remove(t, 1)` is cheap | It moves every other item | Emptying 10,000 items took 0.39 s instead of 0.5 ms |
| `<=` works as a sort comparator | The comparator must be strict | Sorting 100 equal numbers with `<=` stopped with `invalid order function for sorting` |

## Summary

- A table maps any key except `nil` and NaN to any value except `nil`; storing `nil` removes the
  entry, and `t.name` is shorthand for `t["name"]`.
- A sequence has the keys 1 to *n* with no holes; for a sequence, `#t` is *n* and `ipairs` walks
  it in order.
- `pairs` walks every key, in an order that is unspecified and can change between runs; sort the
  keys when order matters.
- On a table with holes, `#t` can return any border. Remove from the end, don't store `nil` in a
  list, or keep the count in `n`.
- Tables are references: assignment, passing, and `==` all work on the reference. A shallow copy
  shares nested tables; a deep copy with a `seen` table shares nothing.
- A stack is a sequence used at one end; a queue needs two indices to stay $O(1)$; a set stores
  members as keys; a matrix needs a new table for each row.

## Self-check

1. What does `local t = { "a", "b", x = "c", "d" }` give for `t[3]`, `t.x`, and `#t`?

   <details>
   <summary>Answer</summary>

   `t[3]` is `"d"`, `t.x` is `"c"`, and `#t` is 3. List items are numbered among themselves, so
   `"d"` is the third, and the field `x` doesn't affect the length.
   </details>

2. `local t = {}; t[1] = "a"; t[2] = "b"; t[4] = "d"`. Which values can `#t` return, and which
   items does `ipairs(t)` visit?

   <details>
   <summary>Answer</summary>

   Its borders are 2 (because `t[3]` is `nil`) and 4 (because `t[5]` is `nil`), so `#t` may be
   either. `ipairs` visits only 1 and 2, because it stops at the first `nil`.
   </details>

3. After `local a = { 1, 2 }; local b = a; b = { 3, 4 }`, what is `a[1]`?

   <details>
   <summary>Answer</summary>

   1. `b = { 3, 4 }` points `b` at a new table and leaves the first table, which `a` still
   refers to, unchanged. Only writing through `b`, as in `b[1] = 3`, changes what `a` sees.
   </details>

4. Why does a deep copy need its `seen` table? Give a table that the copy can't finish without it.

   <details>
   <summary>Answer</summary>

   Without it, every table reached is copied again, so a table that contains itself recurses
   until the stack overflows: `local t = {}; t.self = t`. `seen` also keeps a table that appears
   twice in the original as one shared table in the copy.
   </details>

5. A program keeps the names of 100,000 users in a list, and checks a name against it on every
   login. What would you change, and why?

   <details>
   <summary>Answer</summary>

   Keep the names in a set, `names[name] = true`, and test `names[name]`. Each check on the list
   is $O(n)$, about 100,000 comparisons in the worst case; each check on the set is $O(1)$ on
   average.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, sections
  [2.1, Values and Types](https://www.lua.org/manual/5.4/manual.html#2.1),
  [3.4.7, The Length Operator](https://www.lua.org/manual/5.4/manual.html#3.4.7), and
  [3.4.9, Table Constructors](https://www.lua.org/manual/5.4/manual.html#3.4.9). Section 3.4.7
  defines borders exactly, with more examples of tables that aren't sequences.
- The manual's section [6.6, Table Manipulation](https://www.lua.org/manual/5.4/manual.html#6.6),
  for every function in the `table` library, including `table.move`, which copies a range of a
  list in one call. Its entry for [`next`](https://www.lua.org/manual/5.4/manual.html#pdf-next)
  states the rules for changing a table while you traverse it.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapters on tables
  and on data structures build more structures from tables, such as linked lists and graphs.
