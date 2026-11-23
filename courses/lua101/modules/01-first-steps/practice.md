# Module 1 practice

These exercises practice retrieving what the [Module 1 reading](index.md) explained. They aren't
graded. Work each one on paper or in your head first, then check your answer, and only then run
the code in a `%%lua` cell or in `lua -i` to confirm it. The answers are in the collapsed blocks;
open one only after you have an answer of your own.

## Worked example: predicting a mixed expression

What does `print(10 // 3 + 10 % 3 * 2.0)` print?

1. Precedence puts `//`, `%`, and `*` before `+`, and the three of them run left to right:
   `(10 // 3) + ((10 % 3) * 2.0)`.
2. `10 // 3` is `3`, an integer, because both operands are integers.
3. `10 % 3` is `1`, an integer.
4. `1 * 2.0` is `2.0`, a float, because one operand is a float.
5. `3 + 2.0` is `5.0`, a float, for the same reason.

So it prints `5.0`. A single float operand anywhere in a chain of `+`, `-`, and `*` makes the
result a float from that point on.

### Exercise 1.1 (LO-1.2, ★, about 10 minutes)

Give the value of each expression. The first is done for you.

1. `-9 // 4` is `-3`: the exact quotient is -2.25, and floor division rounds down to -3.
2. `-9 % 4`
3. `9 // -4`
4. `9 % -4`

<details>
<summary>Hint</summary>

Use `a % b == a - (a // b) * b`, with the value of `a // b` you work out first.
</details>

<details>
<summary>Answer</summary>

2. `3`, because `-9 - (-3) * 4` is `-9 + 12`.
3. `-3`: the exact quotient is -2.25 again, which rounds down to -3.
4. `-3`, because `9 - (-3) * (-4)` is `9 - 12`. The result has the divisor's sign.
</details>

### Exercise 1.2 (LO-1.2, ★★, about 15 minutes)

For each expression, give its value and, if it is a number, its subtype. If it raises an error,
say so and give the reason.

1. `"5" * "2"`
2. `"5" .. 2`
3. `"5" == 5`
4. `"5" < 10`
5. `#("ab" .. "cd")`
6. `math.type(10 / 2)`
7. `tostring(1e15)`

<details>
<summary>Hint</summary>

Arithmetic converts strings to numbers, `..` converts numbers to strings, and comparisons convert
nothing.
</details>

<details>
<summary>Answer</summary>

1. `10`, an integer: arithmetic converts both strings, and both look like integers.
2. `"52"`: `..` converts the number to a string.
3. `false`: `==` never converts, so a string never equals a number.
4. An error, `attempt to compare string with number`: `<` doesn't convert either.
5. `4`: the concatenation is `"abcd"`, four bytes.
6. `"float"`: `/` always gives a float, here `5.0`.
7. `"1e+15"`: `1e15` is a float, and floats print with 14 significant digits, which this one
   needs an exponent to show.
</details>

### Exercise 1.3 (LO-1.4, ★★, about 15 minutes)

Give the value of each expression, and say for each `and` or `or` whether its right-hand side is
evaluated at all.

1. `nil and false`
2. `false or nil`
3. `0 or error("unreachable")`
4. `"" and 1 or 2`
5. `not not nil`
6. `nil == false`

<details>
<summary>Answer</summary>

1. `nil`. `nil` is falsy, so `and` returns it without evaluating `false`.
2. `nil`. `false` is falsy, so `or` evaluates and returns its right-hand side.
3. `0`. `0` is truthy, so `or` returns it and never calls `error`.
4. `1`. `""` is truthy, so `"" and 1` is `1`, which is truthy, so `or` returns it without
   evaluating `2`.
5. `false`. `not nil` is `true`, and `not true` is `false`. No `and` or `or` here.
6. `false`. Both are falsy, but they are different values of different types, and `==` doesn't
   convert.
</details>

### Exercise 1.4 (LO-1.3, ★★, about 15 minutes)

Predict both lines this script prints. Then name the one-word change that makes the second line
print `unchanged`, and explain why `describe`'s own `result` is unaffected by the bug.

```lua
local function area(width, height)
  result = width * height
  return result
end

local function describe(width, height)
  local result = "room"
  local size = area(width, height)
  return result .. " of " .. size .. " square meters"
end

result = "unchanged"
print(describe(3, 4))
print(result)
```

<details>
<summary>Hint</summary>

Which `result` does each function's assignment or read refer to? Look for the `local` that
declares it, and if there is none, it is the global.
</details>

<details>
<summary>Answer</summary>

It prints `room of 12 square meters`, then `12`. `area` assigns `result` without `local`, so it
overwrites the global `result`, which held `"unchanged"`. The fix is `local result = width *
height` in `area`. `describe` declares its own `local result`, which shadows the global inside
`describe`, so `area`'s assignment to the global doesn't touch it.
</details>

### Exercise 1.5 (LO-1.1, ★★, about 15 minutes)

For each error message, say whether it is a compile error or a runtime error, which line to look
at first, and the most likely cause.

1. `lua: main.lua:2: attempt to concatenate a nil value (local 'name')`, with a stack traceback
   whose next line is `main.lua:4: in main chunk`
2. `lua: report.lua:12: attempt to compare number with string`
3. `lua: config.lua:8: 'end' expected (to close 'if' at line 4) near <eof>`

<details>
<summary>Hint</summary>

A compile error describes what Lua expected to read. A runtime error describes an operation on
values, and runtime errors come with a stack traceback.
</details>

<details>
<summary>Answer</summary>

1. A runtime error. Line 2 concatenates a local `name` that is `nil`. The traceback says line 4
   made the call, so the most likely cause is a call on line 4 that passed no argument, or `nil`,
   for `name`. Look at line 2, then line 4.
2. A runtime error. Line 12 compares a number with a string, probably a value read as text, such
   as input, that should have gone through `tonumber` first.
3. A compile error, so nothing in the file ran. The `if` on line 4 has no `end`. Lua reached the
   end of the file (`<eof>`) at line 8 still waiting for it, so line 8 is only where it gave up.
</details>

### Exercise 1.6 (LO-1.2, ★★★, about 20 minutes)

This code splits a duration in seconds into hours, minutes, and seconds:

```lua
local t = 3725
local hours = t // 3600
local rest = t % 3600
print(hours, rest // 60, rest % 60)
```

1. What does it print for `t = 3725`?
2. What does it print for `t = -3725`?
3. Is the result for `-3725` wrong? Check it by computing `hours * 3600 + minutes * 60 +
   seconds`.
4. Would the code print the same for `t = 3725.0`? If not, what changes?

<details>
<summary>Hint</summary>

For part 2, work out `-3725 // 3600` first; floor division rounds down. For part 4, recall which
subtype `//` and `%` return when an operand is a float.
</details>

<details>
<summary>Answer</summary>

1. `1  2  5`: one hour, two minutes, and five seconds.
2. `-2  57  55`. `-3725 // 3600` rounds -1.03 down to `-2`, and `-3725 % 3600` is `3475`, which
   splits into 57 minutes and 55 seconds.
3. It isn't wrong: `-2 * 3600 + 57 * 60 + 55` is `-3725`. Floor division and modulo always
   recombine into the original number. It is only an unusual way to write a negative duration;
   to print "-1 h 2 min 5 s", split the absolute value and add the sign afterward.
4. It prints the same numbers as floats: `1.0  2.0  5.0`. `//` and `%` give floats when an
   operand is a float.
</details>
