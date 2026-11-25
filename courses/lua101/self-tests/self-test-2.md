# Self-test 2: All Modules

**Objectives:** LO-3.3, LO-4.4, LO-5.1, LO-7.3, LO-8.1–8.3, LO-9.1–9.3, LO-10.2, LO-10.3,
LO-12.1–12.3, LO-13.1–13.4, LO-14.1–14.3\
**Prerequisites:** Modules 1–14\
**Time:** 125 minutes for the 20 questions, worth 105 points, and about an hour more to check your
answers and review what you missed

This self-test covers the whole course, weighted toward Modules 8–14, and mixes question types from
every module, so you practice choosing a method as well as applying one. It isn't graded. Take it
after Module 14, in one sitting. The answers are in the collapsed blocks after each question; open
them only once you have written all of yours.

## How to take it

1. Set aside 125 minutes without interruptions. Use paper and a pen, with no computer, phone, or
   notes: the effort of recalling without help is what makes this practice work.
2. Write an answer to every question before you open any answer. Each question's heading gives its
   objectives and its points.
3. Open the answers and score yourself. Each answer says how its points are given. The points are
   only for scoring yourself: the course has no grades.
4. For each question you missed, its objective ID names the module to review: for example,
   LO-3.2 belongs to Module 3. Rerun the question's code in a `%%lua` cell or with `lua` to see the
   answer for yourself.

## Rules for your answers

- All code is Lua 5.4 unless a question names another version. When a question asks what a line
  prints, write exactly what it prints; where `print` separates values with a tab, a space is
  enough.
- If an expression or a line raises an error, write "error" and say why.
- C code uses the Lua 5.4 C API, with `lua.h`, `lauxlib.h`, and `lualib.h` included. Small mistakes
  in C syntax don't matter if the meaning is clear.

## Questions

### Question 1 (LO-3.3, 5 points)

Consider this code.

```lua
local function shallow(t)
  local c = {}
  for k, v in pairs(t) do c[k] = v end
  return c
end
local a = { n = 1, list = { 1, 2 } }
local b = shallow(a)
b.n = 2
b.list[1] = 10
print(a.n, a.list[1], a.list == b.list)
```

(a) (3 points) What does the last line print? One point for each value.

(b) (2 points) Write `deep(t)`, which copies a table and every table inside it, for tables without
cycles. Other values are returned as they are.

<details>
<summary>Answer</summary>

(a) `1  10  true`. The copy has its own field `n`, so changing `b.n` leaves `a.n` alone; but
`b.list` is the same table as `a.list`, because a shallow copy copies the reference, so
`b.list[1] = 10` changes `a.list[1]`.

(b)

```lua
local function deep(t)
  if type(t) ~= "table" then return t end
  local c = {}
  for k, v in pairs(t) do c[k] = deep(v) end
  return c
end
```

One point for recursing on the values, one for returning values that are not tables unchanged.
Copying the keys with `deep` as well, or the metatable, is also correct.
</details>

### Question 2 (LO-4.4, 5 points)

Let `s` be the five-letter word naïve, written in UTF-8, in which the letter ï takes two bytes and
every other letter one.

(a) (1 point) What is `#s`?

(b) (1 point) What is `utf8.len(s)`?

(c) (1 point) What does `s:sub(3, 3)` return?

(d) (2 points) A loop builds a report with `out = out .. line .. "\n"` for each of 10,000 lines.
Explain why this is slow, and how `table.concat` avoids it.

<details>
<summary>Answer</summary>

(a) 6: `#` counts bytes.

(b) 5: it counts characters.

(c) A string of one byte, the first of the two bytes of ï, which is not a character on its own:
`string.sub` counts bytes, not characters.

(d) Strings cannot change, so each `..` builds a new string and copies everything built so far: the
total copying grows with the square of the number of lines. Collecting the lines in a list and
calling `table.concat(lines, "\n")` copies each byte once. One point for the repeated copying, one
for the remedy.
</details>

### Question 3 (LO-5.1, 4 points)

Consider this code.

```lua
local adders, total = {}, 0
for i = 1, 3 do
  adders[i] = function(x) total = total + i * x; return total end
end
local a1 = adders[1](1)
local a3 = adders[3](1)
local a2 = adders[2](10)
print(a1, a3, a2)
```

(a) (2 points) What does the last line print?

(b) (2 points) Which variables do the three closures share, and which does each have its own copy
of?

<details>
<summary>Answer</summary>

(a) `1  4  24`: `total` becomes $0 + 1 \cdot 1 = 1$, then $1 + 3 \cdot 1 = 4$, then $4 + 2 \cdot 10
= 24$. Two points for all three values; one point for two of them.

(b) They share `total`, one local declared outside the loop. Each has its own `i`, because each pass
of a numeric `for` creates a new local `i`. One point for each.
</details>

### Question 4 (LO-7.3, 5 points)

A program caches the area of each rectangle.

```lua
local cache = setmetatable({}, { __mode = "k" })
local function area(rect)
  local a = cache[rect]
  if not a then a = rect.w * rect.h; cache[rect] = a end
  return a
end
local r = { w = 2, h = 3 }
print(area(r))
r = nil
collectgarbage()
```

(a) (1 point) After the last line, does `cache` still hold an entry? Why?

(b) (2 points) What would change with `__mode = "v"` instead, and why?

(c) (2 points) Without the call to `collectgarbage`, when would the entry disappear?

<details>
<summary>Answer</summary>

(a) No. With `__mode = "k"` the keys are weak, and the rectangle is no longer referred to from
anywhere else, so the full collection removes the entry.

(b) The entry would stay. The keys would then be strong, so the cache itself would keep every
rectangle alive, and the values are numbers, which the collector never removes from a weak table.
The cache would grow forever. One point for "the entry stays", one for the reason.

(c) At some collection after the rectangle becomes unreachable: when the collector next finishes a
cycle that finds it unreachable, which depends on how much the program allocates. Entries are not
removed at the moment the last strong reference goes. One point for "at a later collection", one for
"not immediately".
</details>

### Question 5 (LO-8.1, LO-8.2, 9 points)

Consider this code.

```lua
local Account = {}
Account.__index = Account
function Account.new(owner, balance)
  return setmetatable({ owner = owner, balance = balance or 0 }, Account)
end
function Account:deposit(amount) self.balance = self.balance + amount end
function Account:describe() return self.owner .. ": " .. self.balance end

local Savings = setmetatable({}, { __index = Account })
Savings.__index = Savings
function Savings.new(owner, balance, rate)
  local s = Account.new(owner, balance)
  s.rate = rate
  return setmetatable(s, Savings)
end
function Savings:add_interest() self:deposit(self.balance * self.rate) end
function Savings:describe() return Account.describe(self) .. " (savings)" end

local s = Savings.new("Ada", 100, 0.5)
s:add_interest()
print(s:describe())                                    -- (a)
print(getmetatable(s) == Savings, rawget(s, "deposit")) -- (b)
```

(a) (1 point) What does line (a) print?

(b) (2 points) What does line (b) print? Explain how `s:deposit` is found.

(c) (1 point) What happens on `Account.new("Bo"):add_interest()`?

(d) (2 points) What happens on `s.deposit(10)`, and why?

(e) (3 points) A `Report` must write its text either to a file or to a list in memory, chosen when
the report is created, and more destinations may come later. Would you make the destinations
subclasses of `Report`, or give each report a destination object it calls? Defend your choice.

<details>
<summary>Answer</summary>

(a) `Ada: 150.0 (savings)`: the interest is a float, so the balance becomes `150.0`.

(b) `true  nil`. `deposit` is not stored in `s`. Looking it up in `s` fails, so Lua follows `s`'s
metatable's `__index`, which is `Savings`; it is not there either, so Lua follows `Savings`'s
metatable's `__index`, which is `Account`, where it is found. One point for the output, one for the
chain.

(c) An error: `attempt to call a nil value (method 'add_interest')`. An `Account` does not inherit
from `Savings`.

(d) An error, `attempt to index a number value (local 'self')`. With a dot, 10 is passed as `self`,
and `amount` is `nil`; the method then tries to read `self.balance` from a number. The colon in
`s:deposit(10)` passes `s` as `self`.

(e) Composition: give each report a `sink` with a `write(text)` method, such as a file sink and a
memory sink. The destination is chosen when the report is created, and new destinations need no
change to `Report`; with subclasses, every kind of report would need one subclass per destination,
and a report could not change destination. Inheritance fits when the subclass is a kind of the
parent and adds or changes its behavior, which a destination is not. Three points for a clear choice
defended with these trade-offs. An answer that chooses inheritance earns full marks only if it
argues from the same trade-offs, for example that there will only ever be two destinations and no
other kinds of report.
</details>

### Question 6 (LO-8.3, 4 points)

Consider this constructor.

```lua
local function counter()
  local n = 0
  return {
    inc = function() n = n + 1; return n end,
    get = function() return n end,
  }
end
```

(a) (1 point) Why can no code outside `counter` change `n` except through `inc`?

(b) (2 points) A program creates 100,000 counters. Compare the memory this design uses with a class
whose methods are in a metatable shared by every counter.

(c) (1 point) Give one thing that is easier with metatable-based counters.

<details>
<summary>Answer</summary>

(a) `n` is a local of `counter`; only the two closures created in the call refer to it, and it is
not a field of the returned table.

(b) Each closure-based counter holds its own table, two new closures, and the upvalue `n`, so the
memory per counter is several objects. Metatable-based counters each hold one table with a field
`n`, and all share one copy of the methods. One point for "two closures per counter", one for
"shared methods".

(c) Any one of: changing or adding a method for every counter at once, in the class; inheriting from
the class; or reading and saving a counter's state, which is in its fields.
</details>

### Question 7 (LO-9.1, 6 points)

Write everything this code prints, in order.

```lua
local co = coroutine.create(function(x, y)
  print("start", x, y)
  local c = coroutine.yield(x + y)
  print("got", c)
  local p, q = coroutine.yield(c * 2)
  return p + q
end)
print(coroutine.resume(co, 1, 2))
print(coroutine.status(co))
print(coroutine.resume(co, 10))
print(coroutine.resume(co, 3, 4))
print(coroutine.status(co))
print(coroutine.resume(co))
```

<details>
<summary>Answer</summary>

```text
start  1  2
true  3
suspended
got  10
true  20
true  7
dead
false  cannot resume dead coroutine
```

One point for each of the six `print` statements at the end, with what the coroutine prints while it
runs counted with the `resume` that runs it. The first `resume` passes 1 and 2 as arguments; later
ones pass their values as the results of `yield`; the coroutine's return value comes back from the
`resume` that ends it.
</details>

### Question 8 (LO-9.2, 6 points)

Generators with `coroutine.wrap`.

(a) (2 points) Write `range(n)`, which returns a generator, for use in a generic `for`, that yields
the integers from 1 to `n`.

(b) (3 points) Write `map(f, gen)`, which returns a new generator that yields `f(v)` for each value
`v` that the generator `gen` yields.

(c) (1 point) What does this print?

```lua
for x in map(function(v) return v * v end, range(3)) do io.write(x, " ") end
```

<details>
<summary>Answer</summary>

(a)

```lua
local function range(n)
  return coroutine.wrap(function()
    for i = 1, n do coroutine.yield(i) end
  end)
end
```

(b)

```lua
local function map(f, gen)
  return coroutine.wrap(function()
    for v in gen do coroutine.yield(f(v)) end
  end)
end
```

One point for returning a wrapped coroutine, one for consuming `gen` inside it, and one for yielding
`f(v)`.

(c) `1 4 9 `
</details>

### Question 9 (LO-9.3, 6 points)

This scheduler runs tasks that sleep. `sleep(t)` yields the number of time units to sleep, and `run`
always resumes the task that wakes earliest; when two tasks wake at the same time, it resumes the
one that was spawned first.

```lua
local clock, tasks = 0, {}
local function spawn(fn)
  tasks[#tasks + 1] = { co = coroutine.create(fn), wake = 0 }
end
local function sleep(t) coroutine.yield(t) end
local function run()
  while #tasks > 0 do
    local best = 1
    for i = 2, #tasks do
      if tasks[i].wake < tasks[best].wake then best = i end
    end
    local t = tasks[best]
    clock = t.wake
    local _, delay = coroutine.resume(t.co)
    if coroutine.status(t.co) == "dead" then table.remove(tasks, best)
    else t.wake = clock + delay end
  end
end
spawn(function() for i = 1, 2 do print(clock, "A", i); sleep(3) end end)
spawn(function() for i = 1, 3 do print(clock, "B", i); sleep(2) end end)
run()
```

(a) (3 points) Write everything it prints, in order.

(b) (2 points) Before `run()` starts, this line spawns a third task. What happens, and why?

```lua
spawn(function() while true do end end)
```

(c) (1 point) Name one way to guard a scheduler against such a task.

<details>
<summary>Answer</summary>

(a)

```text
0  A  1
0  B  1
2  B  2
3  A  2
4  B  3
```

Three points for all five lines in order; two for one line out of place; one for the right lines in
a wrong order.

(b) The program hangs once that task runs: it never yields, and a cooperative scheduler can switch
tasks only when a task yields, so neither of the other tasks runs again. One point for "it hangs and
stops the others", one for the reason.

(c) Any one of: run each task under an instruction-count hook that raises an error after too many
instructions; or review tasks so each loop yields. A pure cooperative scheduler cannot take the
processor from a task that never yields.
</details>

### Question 10 (LO-10.2, 4 points)

A web service counts the lines of a file that a user names:

```lua
local function count_lines(path)
  return os.execute("wc -l " .. path)
end
```

(a) (1 point) Give a value of `path` that makes this function delete a file named `data.db`.

(b) (2 points) Describe two safer ways to count the lines.

(c) (1 point) What does this expression return?

```lua
os.date("%Y-%m-%d", os.time({ year = 2026, month = 2, day = 30, hour = 12 }))
```

<details>
<summary>Answer</summary>

(a) `x; rm data.db`: the semicolon ends the `wc` command and starts another. Any value with a shell
separator or a substitution works, such as `$(rm data.db)`.

(b) Count them in Lua, with no shell at all: `for _ in io.lines(path) do n = n + 1 end`. Or, if a
command is needed, quote the path for the shell (in single quotes, with each single quote inside
written as `'\''`), after checking that it names a file the user may read. One point each.

(c) `"2026-03-02"`: `os.time` normalizes February 30 to March 2, because February 2026 has 28 days.
</details>

### Question 11 (LO-10.3, 6 points)

Data that must not run as code.

(a) (3 points) A program saves its settings as a Lua chunk, `return { name = "..." }`, and reads
them back with `dofile("settings.lua")`. Explain the risk if another user can edit the file, and
describe how to read the settings safely.

(b) (2 points) Give the fields of this CSV line, in which a quoted field may hold commas and a
doubled quote stands for one quote: `a,"b,c","d""e"`

(c) (1 point) Why does a program that writes Lua values with `string.format("%q", v)` not need to
escape quotes or newlines itself?

<details>
<summary>Answer</summary>

(a) `dofile` runs whatever the file contains, with the program's globals, so an edited file can call
`os.execute`, read files, or change the program. A safer reader parses the format instead of running
it. If the file must stay a Lua chunk, load it in text mode with an empty environment,
`load(text, "=settings", "t", {})`, so that bytecode is refused and no library is reachable; but the
chunk can still loop forever, so a parser is safest. One point for the risk, one for the empty
environment and text mode, one for naming what `load` still allows, or for parsing instead.

(b) Three fields: `a`, `b,c`, and `d"e`. One point for three fields, one for the contents of the
second and third.

(c) `%q` writes a string as a Lua literal that reads back as the same string, escaping quotes,
backslashes, and newlines, and control characters.
</details>

### Question 12 (LO-12.1, LO-12.3, 5 points)

Measuring and speeding up.

(a) (2 points) A teammate reports: "Version B is faster: A took 0.21 s and B took 0.19 s." Each
version ran once, on a laptop with other programs open. Why does the measurement not support the
claim, and what must the report include?

(b) (2 points) This function is a program's hot path, called with thousands of lines and a stop list
of 200 words. Rewrite it to be faster, and say why the change helps.

```lua
local function count_words(lines, stop)
  local n = 0
  for _, line in ipairs(lines) do
    for word in line:gmatch("%a+") do
      local skip = false
      for _, s in ipairs(stop) do
        if s == word then skip = true end
      end
      if not skip then n = n + 1 end
    end
  end
  return n
end
```

(c) (1 point) How would you show that the change was worth making?

<details>
<summary>Answer</summary>

(a) One run of each cannot separate a difference of 10% from the noise of a busy machine. Run each
version several times, collecting garbage before each run, and report the minimum or the median,
with the input, the hardware, the operating system, and the Lua version. One point for the reason,
one for what to report.

(b) Build a set of the stop words once, and look each word up in it:

```lua
local is_stop = {}
for _, s in ipairs(stop) do is_stop[s] = true end
-- in the loop:
if not is_stop[word] then n = n + 1 end
```

Each word then costs one table lookup instead of 200 comparisons. One point for the set, one for the
reason.

(c) Time both versions on the same, realistic input, several times each, check that they return the
same count, and report both times with their conditions.
</details>

### Question 13 (LO-12.2, 5 points)

How Lua stores tables and strings.

(a) (2 points) Compare the cost of `t[#t + 1] = x` with the cost of `table.insert(t, 1, x)`, for a
list of 100,000 items.

(b) (1 point) In `local t = { 10, 20, x = 1 }`, where are the values stored?

(c) (2 points) Why can comparing two equal strings of 1,000 characters with `==` take longer than
comparing two equal strings of 10 characters?

<details>
<summary>Answer</summary>

(a) Appending costs about the same however long the list is (the array part grows by doubling, so
its occasional resizes average out). Inserting at position 1 moves every item up one place, so its
cost grows with the length of the list: here, 100,000 moves for each insertion.

(b) 10 and 20 in the array part, at indices 1 and 2; `x` in the hash part.

(c) Lua 5.4 interns short strings, of 40 bytes or fewer: it keeps one copy of each, so `==` compares
two pointers. Long strings are not interned, so two equal long strings made separately are different
objects, and `==` compares them byte by byte. One point for interning, one for the byte-by-byte
comparison.
</details>

### Question 14 (LO-13.1, 6 points)

The stack holds `'a' 'b'`, bottom first. Give the stack after each call, bottom first. Each call
starts from the stack the previous one left.

|  | Call | Stack afterward |
| :- | :- | :- |
| (a) | `lua_pushinteger(L, 1)` |  |
| (b) | `lua_pushvalue(L, -2)` |  |
| (c) | `lua_insert(L, 1)` |  |
| (d) | `lua_remove(L, 2)` |  |
| (e) | `lua_settop(L, 4)` |  |
| (f) | `lua_replace(L, -3)` |  |

<details>
<summary>Answer</summary>

|  | Call | Stack afterward |
| :- | :- | :- |
| (a) | `lua_pushinteger(L, 1)` | `'a' 'b' 1` |
| (b) | `lua_pushvalue(L, -2)` | `'a' 'b' 1 'b'` |
| (c) | `lua_insert(L, 1)` | `'b' 'a' 'b' 1` |
| (d) | `lua_remove(L, 2)` | `'b' 'b' 1` |
| (e) | `lua_settop(L, 4)` | `'b' 'b' 1 nil` |
| (f) | `lua_replace(L, -3)` | `'b' nil 1` |

One point for each row (6 points). `pushvalue(L, -2)` copies the value second from the top, `'b'`.
`insert(L, 1)` moves the top value to the bottom. `settop` fills new places with `nil`.
`replace(L, -3)` pops the top value, `nil`, into the place that was third from the top before the
pop, index 2. A C program that prints the stack after each call confirms every row.
</details>

### Question 15 (LO-13.2, 6 points)

Write the C function `l_count` of a module `strx`, so that `strx.count(s, c)` returns the number of
times the one-character string `c` occurs in the string `s`. A wrong argument must raise an error
that names it; in particular, `strx.count("banana", "an")` must raise this error:

```text
bad argument #2 to 'count' (one character expected)
```

Also write the list of functions and the `luaopen_strx` function that `require("strx")` calls.

<details>
<summary>Answer</summary>

```c
static int l_count(lua_State *L) {
  size_t len, clen;
  const char *s = luaL_checklstring(L, 1, &len);
  const char *c = luaL_checklstring(L, 2, &clen);
  luaL_argcheck(L, clen == 1, 2, "one character expected");
  lua_Integer n = 0;
  for (size_t i = 0; i < len; i++) {
    if (s[i] == c[0]) n++;
  }
  lua_pushinteger(L, n);
  return 1;
}

static const luaL_Reg functions[] = {
  { "count", l_count },
  { NULL, NULL },
};

int luaopen_strx(lua_State *L) {
  luaL_newlib(L, functions);
  return 1;
}
```

Two points for checking both arguments, with `luaL_checklstring`, and for checking the length of
`c`, with `luaL_argcheck`; two for the count, pushed with `lua_pushinteger` and with `return 1`; two
for the list, ended by `{ NULL, NULL }`, and `luaopen_strx` with `luaL_newlib`. Using the length
from `luaL_checklstring`, rather than `strlen`, also counts characters after a zero byte; either
earns full marks. Compiled and run, this code returns 3 for `strx.count("banana", "a")` and raises
the required error.
</details>

### Question 16 (LO-13.3, 5 points)

A C program passes each event to a script's function `handle`, and prints what it returns.

```c
static void handle_all(lua_State *L, const char **events, int n) {
  for (int i = 0; i < n; i++) {
    lua_getglobal(L, "handle");
    lua_pushstring(L, events[i]);
    lua_call(L, 1, 1);
    printf("%s\n", lua_tostring(L, -1));
  }
}
```

(a) (3 points) Name three problems in this loop, and what each causes.

(b) (2 points) Rewrite the body of the loop to fix all three.

<details>
<summary>Answer</summary>

(a) (1) `lua_call` is unprotected: an error in `handle` reaches the panic function, which aborts the
whole program. (2) The result is never popped, so the stack grows by one value per event, until it
overflows after about a million. (3) `lua_tostring` returns `NULL` when the result is neither a
string nor a number, and passing `NULL` to `printf` for `%s` is undefined behavior. One point each.

(b)

```c
lua_getglobal(L, "handle");
lua_pushstring(L, events[i]);
if (lua_pcall(L, 1, 1, 0) != LUA_OK) {
  fprintf(stderr, "handle: %s\n", lua_tostring(L, -1));
} else {
  const char *text = lua_tostring(L, -1);
  printf("%s\n", text ? text : "(no text)");
}
lua_pop(L, 1);   /* the result, or the error message */
```

One point for `lua_pcall` with its status checked, one for the single `lua_pop` on both paths with
the `NULL` case handled.
</details>

### Question 17 (LO-13.4, 3 points)

A module exposes a C struct `Image`, whose field `pixels` points to memory from `malloc`, as full
userdata with a metatable registered as `"Image"`.

(a) (1 point) Why does its `__gc` set `img->pixels = NULL` after freeing it?

(b) (1 point) Why do its methods get the struct with `luaL_checkudata(L, 1, "Image")`, and not with
`lua_touserdata(L, 1)`?

(c) (1 point) A loop creates many images and keeps none, yet the process grows to gigabytes before
the collector frees any. Why?

<details>
<summary>Answer</summary>

(a) So that a second call cannot free the memory twice: a program can call `__gc` or a `close`
method itself, and the collector calls `__gc` again later.

(b) `luaL_checkudata` checks that the value is a userdata with the `Image` metatable, and raises an
error naming the argument otherwise; `lua_touserdata` accepts any userdata, such as a file handle,
and the method would misread its memory.

(c) The collector paces itself by the memory Lua allocates, and sees only each userdata's small
struct, not the pixels that `malloc` allocated, so it runs too rarely.
</details>

### Question 18 (LO-14.1, 5 points)

Consider this function, written for Lua 5.4.

```lua
local function halves(list)
  local out = {}
  for i = 1, #list do out[i] = list[i] // 2 end
  return table.unpack(out)
end
```

(a) (2 points) Give two reasons it does not run on Lua 5.1.

(b) (3 points) Rewrite it so that one file runs on Lua 5.1, LuaJIT, Lua 5.4, and Lua 5.5, and gives
5.4's results on 5.4. Detect features; do not test `_VERSION`.

<details>
<summary>Answer</summary>

(a) `//` does not exist in Lua 5.1, so the file fails to compile, before any line runs; and
`table.unpack` is `nil` in 5.1, where the function is the global `unpack`. One point each.

(b)

```lua
local unpack = table.unpack or unpack
local chunk = (loadstring or load)("return function(a, b) return a // b end")
local idiv = chunk and chunk() or function(a, b) return math.floor(a / b) end

local function halves(list)
  local out = {}
  for i = 1, #list do out[i] = idiv(list[i], 2) end
  return unpack(out)
end
```

One point for `table.unpack or unpack`, one for keeping `//` out of the file's own text (compiling
it from a string), and one for a fallback that rounds down. On each of the four Luas,
`halves({ 7, -7, 4 })` returns `3 -4 2`.
</details>

### Question 19 (LO-14.2, 5 points)

A program runs plugins in a sandbox: an environment built from an allowlist, `load` in text mode,
and an instruction-count hook in the plugin's own coroutine.

(a) (1 point) The allowlist includes `load`. Write one line of plugin code that reaches the host's
real `os` library.

(b) (1 point) When the instruction limit is reached, the hook raises an error, and from then on
raises it again at every instruction. Why is raising it once not enough?

(c) (2 points) Name two kinds of work that the hook cannot stop, and for each, a remedy outside Lua.

(d) (1 point) Why does the sandbox load plugins in text mode?

<details>
<summary>Answer</summary>

(a) `local os = load("return os")()`: a chunk loaded without an environment gets the real global
table.

(b) The plugin can catch one error with `pcall` and keep going, as `while true do pcall(f) end`
does. Raising at every instruction makes the code outside the `pcall` fail too.

(c) Any two, one point each with its remedy: one huge allocation in one C call, such as
`("x"):rep(1e9)` (an allocator that refuses to allocate past a limit); a long computation in one C
call, such as a pattern that backtracks (running the plugin in a separate process that is killed
after a deadline); compiled LuaJIT code, which does not call the count hook (turning the compiler
off with `jit.off()`, or a separate process).

(d) To refuse precompiled bytecode: Lua does not check that a binary chunk's instructions make
sense, and crafted bytecode can crash the interpreter.
</details>



### Question 20 (LO-14.3, 5 points)

A Neovim plugin counts the lines of a buffer that are longer than a limit. As Module 14 advises, it
takes the API as an argument instead of reading the global `vim.api`.

```lua
local long = {}

function long.report(api, buf, limit)
  local lines = api.nvim_buf_get_lines(buf, 0, -1, false)
  local n = 0
  for _, line in ipairs(lines) do
    if #line > limit then n = n + 1 end
  end
  return n
end

return long
```

(a) (3 points) Write a busted test with a stand-in for the API. The buffer holds the lines `"short"`
and `"a much longer line"`, and the limit is 10. Check the result, and check that the plugin read
the whole buffer exactly once.

(b) (1 point) Neovim runs plugins on LuaJIT. Name one Lua 5.4 feature this plugin must not use, and
say why.

(c) (1 point) The test passes. A later version calls `long.report` from the callback of a timer made
with `vim.uv`, and it fails in Neovim. Why didn't the test catch the failure, and what fixes it?

<details>
<summary>Answer</summary>

(a)

```lua
local long = require("long")

describe("long.report", function()
  it("counts the long lines, reading the whole buffer once", function()
    local calls = {}
    local api = {
      nvim_buf_get_lines = function(buf, first, last, strict)
        calls[#calls + 1] = { buf, first, last, strict }
        return { "short", "a much longer line" }
      end,
    }
    assert.are.equal(1, long.report(api, 0, 10))
    assert.are.same({ { 0, 0, -1, false } }, calls)
  end)
end)
```

One point for a stand-in table whose `nvim_buf_get_lines` returns the lines, one for checking the
count, and one for recording each call and checking that there was one, with the range `0, -1` that
means the whole buffer. Run with busted, this test passes; it fails for a version that counts lines
of 5 characters or more.

(b) Any one of `//`, `<const>` or `<close>`, the `utf8` library, or `math.type`. LuaJIT implements
Lua 5.1, which has none of them: the operators and attributes don't compile, and the library and the
function are `nil`.

(c) Neovim forbids most API calls in `vim.uv` callbacks, and the stand-in doesn't enforce that rule:
a stand-in checks only what you built into it. Wrap the call in `vim.schedule(function() … end)`,
which runs it on the main loop's next turn, when the call is allowed. One point for both halves.
</details>

## After the self-test

For each objective you missed, reread that module's summary and redo its practice exercises. Then
finish your [capstone project](../assignments/final-project/README.md), which brings most of the
course together in one package.
