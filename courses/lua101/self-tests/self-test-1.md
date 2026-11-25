# Self-test 1: Modules 1–7

**Objectives:** LO-1.1–1.4, LO-2.1–2.3, LO-3.1–3.3, LO-4.2, LO-4.3, LO-5.1, LO-6.1, LO-7.1,
LO-7.2\
**Prerequisites:** Modules 1–7\
**Time:** 75 minutes for the 14 questions, worth 75 points, and about 45 minutes more to check your
answers and review what you missed

This self-test mixes questions from the first seven modules, so you practice recalling what each
module taught and choosing among its methods, not only applying the one you learned last. It isn't
graded. Take it after Module 7 and before Module 8, in one sitting. The answers are in the collapsed
blocks after each question; open them only once you have written all of yours.

## How to take it

1. Set aside 75 minutes without interruptions. Use paper and a pen, with no computer, phone, or
   notes: the effort of recalling without help is what makes this practice work.
2. Write an answer to every question before you open any answer. Each question's heading gives its
   objectives and its points.
3. Open the answers and score yourself. Each answer says how its points are given. The points are
   only for scoring yourself: the course has no grades.
4. For each question you missed, its objective ID names the module to review: for example,
   LO-3.2 belongs to Module 3. Rerun the question's code in a `%%lua` cell or with `lua` to see the
   answer for yourself.

## Rules for your answers

- All code is Lua 5.4. When a question asks what a line prints, write exactly what it prints; where
  `print` separates values with a tab, a space is enough.
- If an expression or a line raises an error, write "error" and say why.

## Questions

### Question 1 (LO-1.2, 10 points)

Give the value of each expression, and its type, written as `integer` or `float` for a number. If it
raises an error, write "error" and the reason.

|  | Expression | Value | Type |
| :- | :- | :- | :- |
| (a) | `7 // 2` |  |  |
| (b) | `7 / 2` |  |  |
| (c) | `-7 // 2` |  |  |
| (d) | `7 % -3` |  |  |
| (e) | `2^2` |  |  |
| (f) | `"10" + 1` |  |  |
| (g) | `10 .. ""` |  |  |
| (h) | `"10" == 10` |  |  |
| (i) | `1 // 0` |  |  |
| (j) | `7.0 // 2` |  |  |

<details>
<summary>Answer</summary>

|  | Expression | Value | Type |
| :- | :- | :- | :- |
| (a) | `7 // 2` | 3 | integer |
| (b) | `7 / 2` | 3.5 | float |
| (c) | `-7 // 2` | $-4$ | integer |
| (d) | `7 % -3` | $-2$ | integer |
| (e) | `2^2` | 4.0 | float |
| (f) | `"10" + 1` | 11 | integer |
| (g) | `10 .. ""` | `"10"` | string |
| (h) | `"10" == 10` | `false` | boolean |
| (i) | `1 // 0` | error | (divide by zero) |
| (j) | `7.0 // 2` | 3.0 | float |

One point for each row, for the value and the type together. `//` floors toward negative infinity,
so `-7 // 2` is $-4$, and `%` takes the sign of the divisor, so `7 % -3` is $7 - (-3)(-3) = -2$. `/`
and `^` always give floats. Arithmetic converts the string in (f), but `==` never converts, so (h)
is `false`. Integer floor division by zero raises an error, while float floor division would give
infinity. Common mistakes: 3 for (j), which is a float because one operand is, and `-3` for (c).
</details>

### Question 2 (LO-1.4, 5 points)

Give the value of each expression.

(a) `nil or "x"`

(b) `false and nil`

(c) `0 and "zero"`

(d) `"" or 1`

(e) `not 0`

<details>
<summary>Answer</summary>

(a) `"x"`

(b) `false`

(c) `"zero"`

(d) `""`

(e) `false`

One point each. Only `nil` and `false` are false, so 0 and the empty string are true. `and` returns
its first operand if it is false, and otherwise its second; `or` returns its first operand if it is
true, and otherwise its second. The common mistakes are `false` for (c) and 1 for (d), from
languages where 0 and the empty string are false.
</details>

### Question 3 (LO-1.1, 3 points)

Running `lua inventory.lua` stops with this message:

```text
lua: inventory.lua:27: attempt to index a nil value (local 'row')
```

(a) (1 point) Which file and which line raised the error?

(b) (1 point) What was the program doing on that line when it failed, and with which variable?

(c) (1 point) Give one way `row` could have been `nil` there.

<details>
<summary>Answer</summary>

(a) Line 27 of `inventory.lua`.

(b) It was reading a field or an item of (indexing) the local variable `row`, whose value was `nil`.

(c) Any one cause earns the point, for example: `row` came from `rows[i]` with an index past the end
of the list; it came from a misspelled key; or a function that should have returned it returned
nothing.
</details>

### Question 4 (LO-1.3, 4 points)

This function is meant to return the mean of a list.

```lua
local function average(list)
  local total = 0
  for _, v in ipairs(list) do
    totl = total + v
  end
  return total / #list
end
print(average({ 2, 4, 6 }))
```

(a) (1 point) What does the last line print?

(b) (2 points) Line 4 has a typing mistake, yet Lua raises no error. Explain why, and what the line
does instead.

(c) (1 point) Correct the line.

<details>
<summary>Answer</summary>

(a) `0.0`

(b) Assigning to a name that is not a declared local creates or changes a global. So on every pass,
line 4 sets a new global named `totl`, and never changes the local `total`, which stays 0. Dividing
0 by 3 with `/` gives the float `0.0`. One point for "it creates a global", and one for explaining
why `total` stays 0.

(c) `total = total + v`
</details>

### Question 5 (LO-2.1, 5 points)

For (a) to (d), give the number of times the loop's body runs.

(a) `for i = 1, 10, 3 do ... end`

(b) `for i = 10, 1 do ... end`

(c) `for i = 5, 1, -2 do ... end`

(d) `for x = 0, 1, 0.25 do ... end`

(e) What does this code print? Explain in one sentence.

```lua
local i = 100
for i = 1, 3 do end
print(i)
```

<details>
<summary>Answer</summary>

(a) 4 (1, 4, 7, 10)

(b) 0

(c) 3 (5, 3, 1)

(d) 5

(e) `100`. The loop's control variable is a new local of the loop, so the outer `i` never changes.

One point each. In (b) the default step is 1, so a start above the limit runs no pass. In (d), 0.25
is exact in binary, so the last pass has $x = 1.0$ exactly.
</details>

### Question 6 (LO-2.2, 6 points)

With `local function f() return 1, 2, 3 end`, answer each part.

(a) `#{ f(), f() }`

(b) `#{ f(), 10 }`

(c) `select("#", (f()))`

(d) `select("#", f(), nil)`

(e) What `print(f(), "x")` prints

(f) The value of `d` after `local a, b, c, d = f()`

<details>
<summary>Answer</summary>

(a) 4

(b) 2

(c) 1

(d) 2

(e) `1 x`

(f) `nil`

One point each. A call gives all its results only as the last item in a list of expressions;
anywhere else, Lua adjusts it to one result, and parentheses also adjust it to one. So (a) is $1 +
3$ items, and (b), (d), and (e) each use only the first result of the first call. In (f), the
missing fourth value is `nil`.
</details>

### Question 7 (LO-2.3, 4 points)

For each `return` statement in a function, say whether it is a proper tail call, and give the reason
in a few words.

(a) `return g(x)`

(b) `return g(x) + 1`

(c) `return (g(x))`

(d) `return x > 0 and g(x)`

<details>
<summary>Answer</summary>

(a) A proper tail call: `return` followed by one call.

(b) Not a tail call: the caller adds 1 after `g` returns.

(c) Not a tail call: the parentheses adjust the results to one after `g` returns.

(d) Not a tail call: the call is an operand of `and`, not the whole expression.

One point each, for the classification with a correct reason; a classification without a reason
earns half a point.
</details>

### Question 8 (LO-3.1, LO-3.2, 6 points)

Consider this code.

```lua
local t = { "a", "b", "c" }
t[#t + 1] = "d"
t[2] = nil
```

(a) (2 points) List every border of `t`: every value that `#t` is allowed to return.

(b) (1 point) What does `for _, v in ipairs(t) do io.write(v) end` print?

(c) (1 point) What is `#{ n = 3, "x", "y" }`?

(d) (2 points) Why should a program not rely on `#t` for this `t`, and what should it do instead?

<details>
<summary>Answer</summary>

(a) 1 and 4. Index 1 is present and index 2 absent; index 4 is present and index 5 absent.

(b) `a`, because `ipairs` stops at the first `nil`.

(c) 2: the field `n` does not count.

(d) The table has a hole, so it is not a sequence, and `#t` may return either border (Lua 5.4 gives
4 here, but promises nothing). Keep the count in a field such as `n`, or never store `nil` in a
list, for example by removing items with `table.remove`. One point for the reason, one for a remedy.
</details>

### Question 9 (LO-3.3, 5 points)

What does the last line print? One point for each value.

```lua
local a = { 1, 2, 3 }
local b = a
local c = { 1, 2, 3 }
b[1] = 10
local function grow(list) list[#list + 1] = 0 end
local function reset(list) list = {} end
grow(c)
reset(a)
print(a[1], a == b, a == c, #c, #a)
```

<details>
<summary>Answer</summary>

`10  true  false  4  3`. `b` is the same table as `a`, so `b[1] = 10` changes `a[1]`, and `a == b`.
`c` is a different table with the same contents, so `a == c` is `false`. `grow` changes the table it
was passed; `reset` only points its parameter at a new table, so `a` keeps its three items.
</details>

### Question 10 (LO-4.2, 8 points)

Patterns.

(a) (1 point) What does `("2026-11-02"):match("(%d+)%-(%d+)")` return?

(b) (1 point) What does `("a.b.c"):gsub(".", "-")` return?

(c) (1 point) What does `("<b>x</b>"):match("<(.-)>")` return?

(d) (1 point) What does `("f(a(b)) g(c)"):match("%b()")` return?

(e) (4 points) Write a pattern that matches a whole line of the form `name = value` and captures the
name and the value. The name is one or more letters, digits, or underscores. Spaces may appear at
the start of the line, around the `=`, and at the end, and the value must not include the spaces at
the end.

<details>
<summary>Answer</summary>

(a) `"2026"` and `"11"`: two captures, both strings.

(b) `"-----"` and 5: the unescaped dot matches every character.

(c) `"b"`: the lazy `-` stops at the first `>`.

(d) `"(a(b))"`: the first balanced pair of parentheses, nesting included.

(e) `^%s*([%w_]+)%s*=%s*(.-)%s*$`

One point each for: anchoring both ends with `^` and `$`; the name as `([%w_]+)`; allowing spaces
with `%s*` in all four places; and a lazy `(.-)` for the value, so that the final `%s*` takes the
trailing spaces. A greedy `(.*)` keeps the trailing spaces and loses the last point.
</details>

### Question 11 (LO-4.3, 4 points)

A Python program accepts a word only if the whole word matches the regular expression `(cat|dog)s?`:
that is, only the words `cat`, `cats`, `dog`, and `dogs`.

(a) (1 point) Explain why no single Lua pattern can express this test.

(b) (3 points) Write a Lua function `is_pet(word)` that returns `true` for exactly those four words,
and `false` for every other string.

<details>
<summary>Answer</summary>

(a) Lua patterns have no alternation (`|`), and a quantifier can apply to only one character class,
not to a group of characters.

(b)

```lua
local pets = { cat = true, dog = true }

local function is_pet(word)
  return pets[word:match("^(.-)s?$")] == true
end
```

The pattern removes at most one final `s`, and the set tests the rest. Two points for a correct
approach, matching the general shape and then testing the varying part, and one for the details:
`cats` is accepted, `catss` and the empty string are rejected, and the result is a boolean. Any
correct code earns full marks, such as comparing `word` with each of the four words.
</details>

### Question 12 (LO-5.1, 5 points)

Consider this code.

```lua
local function make()
  local n = 0
  return function() n = n + 1; return n end, function() return n end
end
local inc, get = make()
local inc2 = make()
inc(); inc(); inc2()
print(get())                    -- (a)

local fs = {}
for i = 1, 3 do fs[i] = function() return i end end
print(fs[1]() + fs[3]())        -- (b)

local gs, j = {}, 1
while j <= 3 do gs[j] = function() return j end; j = j + 1 end
print(gs[1]() + gs[3]())        -- (c)
```

(a) (1 point) What does line (a) print?

(b) (1 point) What does line (b) print?

(c) (1 point) What does line (c) print?

(d) (2 points) Explain why (b) and (c) differ.

<details>
<summary>Answer</summary>

(a) `2`: `inc` and `get` share one `n`; `inc2` has its own.

(b) `4`: $1 + 3$.

(c) `8`: $4 + 4$.

(d) A closure captures a variable, not its value. Each pass of a numeric `for` has a new local `i`,
so each closure has its own; the `while` loop's `j` is one variable, shared by all three closures,
which is 4 when they run. One point for "captures the variable", one for the difference between the
loops.
</details>

### Question 13 (LO-6.1, 5 points)

Consider this function.

```lua
local function parse_age(text)
  local n = tonumber(text)
  if n == nil then return nil, "not a number: " .. text end
  if n < 0 then error("age must not be negative", 2) end
  return n
end
```

(a) (1 point) What does `print(parse_age("ten"))` print?

(b) (2 points) What does `print(pcall(parse_age, "-3"))` print? Explain why the message has no file
name or line number.

(c) (2 points) The text comes from a form that a user fills in. Is raising an error for a negative
age the right choice? Argue from the rule for choosing between an error and a `nil` result.

<details>
<summary>Answer</summary>

(a) `nil  not a number: ten`

(b) `false  age must not be negative`. Level 2 names the function that called `parse_age`, and here
that is `pcall`, a function written in C, which has no line to name. One point for the output, one
for the reason.

(c) No. Raise an error for a mistake in the calling code, and return `nil` and a message for an
expected failure the caller should handle. A user who types a negative age is an expected failure,
like one who types "ten", so both should return `nil` and a message. Full marks need the rule and
its application; the opposite answer earns a point only if it argues from the rule, for example that
the form has already rejected negative numbers.
</details>

### Question 14 (LO-7.1, LO-7.2, 5 points)

Consider this code.

```lua
local Point = {}
Point.__index = { describe = function(p) return p.x .. "," .. p.y end }
Point.__add = function(a, b)
  return setmetatable({ x = a.x + b.x, y = a.y + b.y }, Point)
end
Point.__eq = function(a, b) return a.x == b.x and a.y == b.y end
local function point(x, y) return setmetatable({ x = x, y = y }, Point) end

local p, q = point(1, 2), point(3, 4)
print((p + q):describe())           -- (a)
print(p == point(1, 2), p == 1)     -- (b)
print(rawget(p, "describe"))        -- (c)
```

(a) (1 point) What does line (a) print?

(b) (1 point) What does line (b) print?

(c) (1 point) What does line (c) print?

(d) (2 points) Write a metatable `frozen` such that assigning any new key to a table with this
metatable raises the error `"no new keys"`, naming the line that made the assignment.

<details>
<summary>Answer</summary>

(a) `4,6`

(b) `true  false`. `__eq` compares the coordinates; it runs only when both operands are tables, so a
table is never equal to a number.

(c) `nil`: `describe` is found through `__index`, but it is not stored in `p`, and `rawget` skips
metamethods.

(d) `local frozen = { __newindex = function() error("no new keys", 2) end }`

One point for `__newindex` as a function that raises the error, one for level 2.
</details>

## After the self-test

If you missed several questions from one module, reread that module's summary and redo its practice
exercises, which are on the page beside its reading. Then go on to [Module
8](../modules/08-objects-and-classes/index.md).
