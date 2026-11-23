# Module 3 practice

These exercises practice the [Module 3 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it in a `%%lua` cell or in `lua -i`.

## Worked example: tracing references

What does this program print?

```lua
local function rename(record, name)
  record.name = name
  record = { name = "fresh" }
  return record
end

local a = { name = "old" }
local b = rename(a, "new")
print(a.name, b.name, a == b)
```

1. `rename(a, "new")` copies the reference in `a` into the parameter `record`, so both refer to
   the same table.
2. `record.name = name` writes through that reference: the table `a` refers to now has the name
   `"new"`.
3. `record = { name = "fresh" }` points the parameter at a new table. `a` still refers to the
   first one, which doesn't change.
4. The function returns the new table, so `b` refers to it.

So it prints `new  fresh  false`: `a` and `b` refer to two different tables.

### Exercise 3.1 (LO-3.1, ★, about 10 minutes)

Write one constructor for a record `city` with a `name` of `"Lyon"`, a `population` of 522,250,
and a list `districts` of the first three of its districts: `"1st"`, `"2nd"`, and `"3rd"`. Then
write the expression for its second district, and a loop that prints each district with its
position.

<details>
<summary>Answer</summary>

```lua
local city = {
  name = "Lyon",
  population = 522250,
  districts = { "1st", "2nd", "3rd" },
}
print(city.districts[2])                 --> 2nd
for i, district in ipairs(city.districts) do
  print(i, district)                     --> 1 1st, then 2 2nd, then 3 3rd
end
```

`ipairs` is the right loop because the districts are a sequence whose order matters. Writing
`522,250` in the code would make two list items, 522 and 250: Lua numbers have no thousands
separator.
</details>

### Exercise 3.2 (LO-3.2, ★★, about 10 minutes)

For each table, say whether it is a sequence, and list every value `#t` may return.

1. `{ "a", "b", nil, "d" }`
2. `{ [1] = "a", [3] = "c" }`
3. `{ "a", "b", n = 5 }`
4. `t` after `local t = { 1, 2, 3 }; t[2] = nil`
5. `t` after `local t = { 1, 2, 3 }; t[#t] = nil`

<details>
<summary>Hint</summary>

Find the borders: each present index followed by an absent one, and 0 if index 1 is absent.
</details>

<details>
<summary>Answer</summary>

1. Not a sequence: borders 2 and 4.
2. Not a sequence: borders 1 and 3.
3. A sequence: `#t` is 2. The field `n` doesn't count, even though its value is 5.
4. Not a sequence: borders 1 and 3. Setting a middle item to `nil` made a hole.
5. A sequence: `#t` is 2. Removing the last item keeps a sequence.
</details>

### Exercise 3.3 (LO-3.3, ★★, about 15 minutes)

Predict the four values this program prints. The first step is done for you.

```lua
local function add_tag(item, tag)
  item.tags[#item.tags + 1] = tag
  return item
end

local base = { name = "note", tags = { "draft" } }
local copy = {}
for k, v in pairs(base) do copy[k] = v end
local result = add_tag(copy, "urgent")
print(#base.tags, result == copy, base == copy, copy.tags == base.tags)
```

**Step 1.** The loop makes a shallow copy: `copy` is a new table, but `copy.tags` holds the same
reference as `base.tags`, because the value it copied is a reference to a table. Now finish the
trace.

<details>
<summary>Answer</summary>

`2  true  false  true`.

- `add_tag` appends `"urgent"` to `copy.tags`, which is `base.tags`, so `#base.tags` is 2.
- `add_tag` returns the table it was given, so `result == copy`.
- `copy` is a new table, so `base == copy` is `false`.
- The two `tags` fields hold one reference, so `copy.tags == base.tags`.
</details>

### Exercise 3.4 (LO-3.4, ★★, about 20 minutes)

Write `balanced(s)`, which returns `true` when every `(`, `[`, and `{` in the string `s` is closed
by the matching bracket in the right order, and `false` otherwise. Other characters don't matter.
`s:sub(i, i)` gives the character at position `i`; module 4 covers it.

| Call | Result |
| :- | :- |
| `balanced("(a[b]{c})")` | `true` |
| `balanced("(]")` | `false` |
| `balanced("((")` | `false` |
| `balanced(")")` | `false` |
| `balanced("")` | `true` |

<details>
<summary>Hint 1</summary>

Use a stack. When you meet an opening bracket, push the closing bracket you now expect.
</details>

<details>
<summary>Hint 2</summary>

When you meet a closing bracket, it must equal the top of the stack; pop it if so. At the end,
the stack must be empty.
</details>

<details>
<summary>Answer</summary>

```lua
local function balanced(s)
  local closer = { ["("] = ")", ["["] = "]", ["{"] = "}" }
  local expected = {}                  -- a stack of the closing brackets still owed
  for i = 1, #s do
    local c = s:sub(i, i)
    if closer[c] then
      expected[#expected + 1] = closer[c]
    elseif c == ")" or c == "]" or c == "}" then
      if expected[#expected] ~= c then return false end
      expected[#expected] = nil
    end
  end
  return #expected == 0
end
```

For `")"`, the stack is empty, so `expected[#expected]` is `expected[0]`, which is `nil` and not
`")"`, and the function returns `false` without a special case. Each character is handled in
$O(1)$, so the function is $O(n)$ in the length of `s`.
</details>

### Exercise 3.5 (LO-3.4, ★★, about 15 minutes)

Write `unique(list)`, which returns a new list with the values of `list` in their original
order, keeping only the first time each one appears. `unique({ 3, 1, 3, 2, 1 })` is
`{ 3, 1, 2 }`. Make it $O(n)$: checking each value against the result so far, with a loop, would
make it $O(n^2)$.

<details>
<summary>Hint</summary>

Keep a set of the values you have already added.
</details>

<details>
<summary>Answer</summary>

```lua
local function unique(list)
  local seen, result = {}, {}
  for _, v in ipairs(list) do
    if not seen[v] then
      seen[v] = true
      result[#result + 1] = v
    end
  end
  return result
end
```

The set makes each test $O(1)$ on average, so the whole function is $O(n)$. `seen[v]` would fail
for a `nil` in the list, but `ipairs` stops before one, and it works for `false`, because
`seen[false]` is an ordinary key.
</details>

### Exercise 3.6 (LO-3.4, ★★, about 15 minutes)

Choose a structure from the reading for each task, and give the cost of the operation the task
does most.

1. An editor's undo history: each change is recorded, and **Undo** reverses the latest one.
2. A printer's jobs, printed in the order they arrive.
3. Checking, at sign-up, whether a username is already taken.
4. A 9-by-9 Sudoku board, read and written by row and column.

<details>
<summary>Answer</summary>

1. A stack: recording a change is a push, and **Undo** is a pop, both $O(1)$.
2. A queue with two indices: adding a job and taking the next one are both $O(1)$. A list with
   `table.remove(jobs, 1)` would be $O(n)$ for each job printed.
3. A set of the usernames: each check is $O(1)$ on average, where searching a list is $O(n)$.
4. A matrix, with a new table for each row: reading or writing a square is $O(1)$.
</details>

### Exercise 3.7 (LO-3.1, ★★, about 15 minutes)

Sort a list of records such as `{ name = "Ana", score = 90 }` by score, highest first, and by name
among equal scores. Then explain what is wrong with this comparator:

```lua
table.sort(players, function(a, b) return a.score >= b.score end)
```

<details>
<summary>Answer</summary>

```lua
table.sort(players, function(a, b)
  if a.score ~= b.score then return a.score > b.score end
  return a.name < b.name
end)
```

The comparator with `>=` returns `true` for two players with equal scores in both orders, so it
isn't a strict order. With equal scores in the list, `table.sort` can stop with
`invalid order function for sorting` or leave the list out of order. Even with `>` alone, players
with equal scores could come out in any order, because the sort isn't stable; comparing names
fixes their order.
</details>
