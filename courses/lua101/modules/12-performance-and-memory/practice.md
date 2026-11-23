# Module 12 practice

These exercises practice the [Module 12 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it with measurements in a `%%lua` cell.

## Worked example: is the change worth it?

A function builds a list of squares with `table.insert(t, i * i)`. A colleague proposes
`t[i] = i * i`. Decide with measurements.

1. **Write both versions, with the same input,** a million items.
2. **Time each several times** with the reading's `bench`, which collects garbage before each run
   and keeps the minimum.
3. **Compare the minimums, and judge against the noise.** Run each benchmark twice more; if the two
   versions' times overlap from run to run, the difference is noise.
4. **Check that the results are the same.** A faster wrong answer isn't an optimization.

In the module's setup, a million appends took 0.052 s with `table.insert` and 0.014 s with an index,
a difference far larger than the run-to-run spread, so the change is worth making in a hot path.
In a function called once, it saves 38 ms and isn't worth a less familiar line.

### Exercise 12.1 (LO-12.1, ★, about 10 minutes)

A teammate reports "the parser takes 0.8 seconds". List what is missing from that report before
anyone can act on it.

<details>
<summary>Answer</summary>

The input (its size and kind), how many runs and which statistic (minimum, median), the hardware,
the operating system, the Lua version and build, and how busy the machine was. Without them, the
number can't be compared with a later one, or with anyone else's.
</details>

### Exercise 12.2 (LO-12.2, ★★, about 15 minutes)

For each table, say which keys are likely in the array part and which in the hash part.

1. `{ 10, 20, 30 }`
2. `{ x = 1, y = 2 }`
3. `local t = {}; for i = 1, 100 do t[i] = i end`
4. `local t = {}; t[1000] = true`
5. `{ [1] = "a", [2] = "b", name = "pair" }`

<details>
<summary>Answer</summary>

1. All three in the array part: the constructor sizes it for three items.
2. Both in the hash part: string keys always are.
3. All in the array part, which grew by doubling to 128 slots as the loop appended.
4. In the hash part: an array part of 1,000 slots for one key would be mostly empty, and a rehash
   uses an array size only when more than half of it would be used.
5. Probably 1 and 2 in the hash part, with `name`: the bracketed keys of a constructor go to the
   hash part when it is built. A later rehash may move them into the array part. The program can't
   tell, and shouldn't need to: only speed and memory differ.
</details>

### Exercise 12.3 (LO-12.3, ★★, about 15 minutes)

This function returns the largest of its arguments. Why is it slow for many arguments? Rewrite it,
and say how its cost grows before and after.

```lua
local function max_of(...)
  local best = (select(1, ...))
  for i = 2, select("#", ...) do
    best = math.max(best, (select(i, ...)))
  end
  return best
end
```

<details>
<summary>Answer</summary>

Each `select(i, ...)` copies every argument from `i` on, so the loop copies about $n^2/2$ values:
it is $O(n^2)$. Pack the arguments once, which is $O(n)$:

```lua
local function max_of(...)
  local args = table.pack(...)
  local best = args[1]
  for i = 2, args.n do
    if args[i] > best then best = args[i] end
  end
  return best
end
```

`math.max(...)` is shorter still, and does the same in C, but it raises an error for no arguments
where this version returns `nil`.
</details>

### Exercise 12.4 (LO-12.2, ★★, about 10 minutes)

Comparing two strings with `==` usually takes the same time however long the strings are. When
doesn't it, and why?

<details>
<summary>Answer</summary>

Short strings, of 40 bytes or fewer in Lua 5.4, are interned: Lua keeps one copy of each, so `==`
compares two pointers. Longer strings aren't interned, so two equal long strings made separately
are different objects, and `==` must compare them byte by byte, after checking that their lengths
match. That takes time in proportion to their length.
</details>

### Exercise 12.5 (LO-12.3, ★★, about 10 minutes)

A program spends 2% of its time in a function that formats its output, and 85% in a loop that
looks up each of 50,000 records in a list of 10,000 names. Which would you work on first, and what
change would you try?

<details>
<summary>Answer</summary>

The loop: even making the formatter infinitely fast saves only 2%. The lookup searches the list
for each record, about $50{,}000 \cdot 5{,}000$ comparisons on average; build a set of the names
once, and each lookup becomes one table access. Then measure again, to see whether the loop is
still the hot path.
</details>
