# Module 12: Performance and memory

**Objectives:** LO-12.1, LO-12.2, LO-12.3\
**Prerequisites:** [Module 3](../03-tables/index.md),
[Module 4](../04-strings-and-patterns/index.md), and [Module 7](../07-metatables/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 12](lab12.ipynb), 1.5 for the
[practice](practice.md), and 3 to finish PA5, which follows this module

Most code is fast enough, and the code that isn't is rarely where you would guess. This module
teaches the method that finds it: measure, form a hypothesis from how Lua stores data, change one
thing, and measure again. It covers how to time code and count memory so that the numbers mean
something, how tables and strings are laid out in memory, which is what makes some operations cheap
and others not, and which changes reliably speed up a hot path.

## Measuring

### Time

`os.clock()` returns the processor time the program has used, in seconds, as a float. The
difference between two calls measures the code between them. Three rules make the number
trustworthy:

1. **Repeat, and keep the minimum.** Other programs, the garbage collector, and the processor's
   own power management all add delays, never subtract them, so the fastest of several runs is
   the closest to the code's own cost. Report the median as well when the spread matters.
2. **Collect garbage first.** Call `collectgarbage()` before each run, so one run doesn't pay for
   the garbage the previous one left.
3. **Measure enough work.** `os.clock` counts in small steps, and a run of a few microseconds is
   mostly noise; repeat the operation until a run takes at least about 10 ms.

```lua
local function bench(fn, runs)
  local best = math.huge
  for _ = 1, runs or 5 do
    collectgarbage()
    local start = os.clock()
    fn()
    best = math.min(best, os.clock() - start)
  end
  return best
end
```

A measurement means nothing without its conditions, so report them with it: the processor, the
operating system, the Lua version and build, and how busy the machine was. This module's numbers
come from an Intel Core i7-11800H under Ubuntu, running Lua 5.4.8 through lupa 2.8, as the best of
five runs, while the machine's load average was about 15 on 16 hardware threads; on a quieter
machine they would be lower and steadier.

**Compare only measurements from the same interpreter, build, and machine.** The course has two
builds of Lua 5.4.8, the notebooks' and the standalone `lua`. They differ in more than speed: the
standalone `lua` starts its garbage collector in generational mode and lupa's in incremental mode,
and the standalone build has Lua 5.3's compatibility options. Measured on the same busy machine,
the two were sometimes equally fast and sometimes far apart, by as much as three times for one
benchmark, and the cause wasn't established.

### Memory

`collectgarbage("count")` returns the memory Lua is using, in kilobytes, as a float. To measure
what a structure costs, collect garbage, read the count, build the structure, collect again, and
read the count again; the difference, divided by the number of entries, is the cost of each:

```lua
collectgarbage()
local before = collectgarbage("count")
local t = {}
for i = 1, 1000000 do t[i] = i end
collectgarbage()
print((collectgarbage("count") - before) * 1024 / 1000000)   --> 16.8 bytes per entry
```

## How Lua stores tables

A Lua table has two parts:

- The **array part** stores the values of integer keys from 1 up to some size, in order, as a
  plain array of values. Reading `t[i]` there is an index into the array, with no hashing.
- The **hash part** stores every other key: strings, floats, tables, and integers outside the array
  part's range. Each entry holds the key, the value, and a link for collisions, so it costs more
  memory, and a lookup computes a hash.

When a part fills up, Lua **rehashes** the table: it counts the keys of each kind, picks new sizes,
both powers of two, and moves every entry into the new parts. That is why appending to a list is
fast on average but not on every append. Watching memory while appending to an empty table, the
array part was reallocated when the items 1, 2, 3, 5, 9, 17, 33, and 65 were added, doubling each
time. Over many appends the copying adds up to about one more copy of the list, so each append
costs $O(1)$ on average, but an append that triggers a rehash costs $O(n)$.

The two parts explain module 3's puzzles. `#t` searches the array part for a border, so how a table
was built decides which border it finds. And memory differs a lot: a million integers stored by
index took 16.8 bytes each, while a million entries with the string keys `"k1"` to `"k1000000"`
took 73.8 bytes each, counting the strings themselves.

Lua 5.4 has no way to set a table's sizes in advance, except a constructor: `{ 0, 0, 0 }` starts
with an array part of three. Lua 5.5 adds `table.create(narray, nhash)`, and LuaJIT has
`table.new`.

## How Lua stores strings

Strings are immutable, which module 4 used to explain why `..` in a loop costs $O(n^2)$. Lua also
**interns** short strings, up to 40 bytes in Lua 5.4: it keeps one copy of each, so creating a short
string that already exists returns the existing one, and comparing two short strings, or looking
one up as a table key, compares a single pointer. Longer strings are created anew each time and
compared byte by byte when their lengths and hashes match. So short strings are good table keys,
and building many distinct strings, such as `"k" .. i` for a million `i`, costs both time and
memory.

## What makes code slow, measured

The table shows typical costs in this module's setup. The ratios matter more than the times, which
change from machine to machine.

| Code | Time | Why |
| :- | :- | :- |
| A million appends with `t[i] = i`, using a counter | 0.014 s | An index into the array part |
| A million appends with `t[#t + 1] = i` | 0.025 s | `#t` must find a border on every append, which a counter avoids |
| A million appends with `table.insert(t, i)` | 0.052 s | A function call, which also computes `#t` |
| `math.sin(i)` a million times | 0.042 s | Two table lookups, `math` in the globals and `sin` in `math`, on every call |
| `local sin = math.sin` first, then `sin(i)` | 0.038 s | A local is a register; the gain is small in Lua 5.4 |
| Summing 200 arguments with `select(i, ...)`, 2,000 times | 0.065 s | Each `select` copies every argument after `i`, so the loop is $O(n^2)$ |
| The same with `table.pack(...)` | 0.011 s | One copy, then indexing |
| Creating a closure on every pass, a million passes | 0.099 s | Each `function … end` allocates a closure |
| The same loop without the closure | 0.006 s | No allocation |

The lesson is not the list. It is that the costs follow from how Lua works: allocation is
expensive, table lookups are cheap but not free, and anything inside a loop is paid once per pass.

## Speeding up a hot path

A **hot path** is the code that takes most of the time, often a loop inside a loop. To speed one
up:

1. **Measure the whole task** with realistic input, and keep the number.
2. **Find where the time goes.** Time the parts separately, or remove one part at a time. A
   function that is called a million times is a better target than one called once.
3. **Change one thing, guided by a reason** from how Lua works: an $O(n^2)$ step that has an $O(n)$
   form, an allocation inside a loop, a search that a table lookup could replace.
4. **Measure again**, with the same input and method, and check that the output is unchanged.
   Keep the change only if it made a difference larger than the noise; otherwise undo it.

The biggest gains come from algorithms, not from local tricks: replacing a linear search with a
table lookup, or `..` in a loop with `table.concat`, changes how the cost grows with the input,
while caching a global in a local saves a few percent. Lab 12 applies the method to a word counter
and measures each change.

## Common misconceptions

| Belief | What happens | Example that breaks it |
| :- | :- | :- |
| One timing run is enough | Noise only adds time, and varies | Take the minimum of several runs |
| Numbers from two machines or builds compare | Hardware, build, and load all change them | The course's two builds differed by up to three times on one benchmark |
| `table.insert(t, v)` is the fastest way to append | It is a function call that also computes `#t` | `t[n] = v` with a counter took about a quarter of the time |
| Caching globals in locals is the main speedup | It saves a few percent in Lua 5.4 | 0.042 s against 0.038 s for a million `math.sin` calls |
| Every append to a table costs the same | Some trigger a rehash of the whole array | Appending item 65 doubled the array to 128 |
| A string key costs about as much as an integer key | String keys use the hash part, and the strings themselves | 73.8 bytes per entry against 16.8 |
| `select(i, ...)` in a loop is linear | Each call copies the rest of the arguments | 200 arguments took six times longer than with `table.pack` |

## Summary

- Time with `os.clock` over several runs, after a full collection, and keep the minimum; report
  the hardware, the build, and the load with every number.
- Measure memory with `collectgarbage("count")` before and after building a structure, with a
  collection before each reading.
- A table has an array part, for integer keys from 1, and a hash part, for everything else; both
  grow by doubling, through a rehash.
- Short strings are interned, so comparing them is cheap; creating many distinct strings is not.
- Speed up a hot path by measuring, changing one thing for a reason, and measuring again; the large
  gains come from better algorithms and from fewer allocations in loops.

## Self-check

1. A benchmark gives 0.31 s, 0.29 s, 0.52 s, and 0.30 s. Which number do you report, and what else
   do you say?

   <details>
   <summary>Answer</summary>

   0.29 s, the minimum, perhaps with the median, 0.305 s. Report the processor, the operating
   system, the Lua version and build, and how busy the machine was. The 0.52 s run was interrupted
   by something else and says nothing about the code.
   </details>

2. Why does `t = {}; t[1] = 1; t[3] = 3` put the key 3 in the hash part, while `{ 1, nil, 3 }`
   puts it in the array part?

   <details>
   <summary>Answer</summary>

   The constructor sizes the array part for three items before storing anything. Assignment one
   key at a time grows the array part only when the keys from 1 up are dense enough; with 2
   missing, Lua keeps 3 in the hash part. That is also why `#` gave 3 and 1 in module 3.
   </details>

3. A function sums its arguments with `for i = 1, select("#", ...) do s = s + select(i, ...) end`.
   Why is it slow for many arguments, and what is the fix?

   <details>
   <summary>Answer</summary>

   Each `select(i, ...)` returns, and so copies, every argument from `i` to the end, so the loop
   copies about $n^2/2$ values. Pack them once with `local t = table.pack(...)`, and loop over
   `t[1]` to `t[t.n]`.
   </details>

4. A program keeps a cache with a million entries keyed by strings such as `"user:" .. id`. How
   could it use less memory?

   <details>
   <summary>Answer</summary>

   Key the cache by the integer `id` itself. Integer keys from 1 up go in the array part, at about
   16 bytes each, and the program no longer creates a million strings.
   </details>

5. Caching `table.insert` in a local made a loop 3% faster in one run. Should you keep the change?

   <details>
   <summary>Answer</summary>

   Only if repeated measurements show the gain is larger than the noise; 3% is within the noise
   of a busy machine. A larger gain is available anyway: replace `table.insert(t, v)` with
   `t[n] = v` and a counter.
   </details>

## Further reading

- Roberto Ierusalimschy,
  ["Lua Performance Tips"](https://www.lua.org/gems/sample.pdf), chapter 2 of *Lua Programming
  Gems* (Lua.org, 2008). Measured advice on locals, tables, and strings, from Lua's designer; its
  numbers come from older versions, so measure before you rely on one.
- Roberto Ierusalimschy, Luiz Henrique de Figueiredo, and Waldemar Celes,
  ["The Implementation of Lua 5.0"](https://www.lua.org/doc/jucs05.pdf), *Journal of Universal
  Computer Science* 11(7), 2005. Section 4 explains the array part and the hash part, and how a
  rehash chooses their sizes.
- The *Lua 5.4 Reference Manual*, section
  [2.5, Garbage Collection](https://www.lua.org/manual/5.4/manual.html#2.5), which describes the
  incremental and generational modes, and the function
  [`collectgarbage`](https://www.lua.org/manual/5.4/manual.html#pdf-collectgarbage).
