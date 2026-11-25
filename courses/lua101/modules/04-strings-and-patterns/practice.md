# Module 4 practice

These exercises practice the [Module 4 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it in a `%%lua` cell or in `lua -i`.

## Worked example: building a pattern step by step

A settings file has lines such as `width = 800` and `  title=My notes  `: a name made of
letters, digits, and underscores, an `=`, and a value, with spaces allowed around each part.
Write a pattern that captures the name and the value without the spaces.

1. Anchor both ends, so the whole line must fit: `^…$`.
2. Allow leading spaces, then capture the name: `^%s*([%w_]+)`. The set `[%w_]` adds the
   underscore to the letters and digits.
3. Allow spaces around the `=`: `%s*=%s*`. The `=` isn't magic, so it needs no `%`.
4. Capture the value, then allow trailing spaces: `(.-)%s*$`. The value must be lazy. With `(.*)`,
   the value would take the trailing spaces too, and `%s*` would match the empty string before
   `$`.

```lua
local pattern = "^%s*([%w_]+)%s*=%s*(.-)%s*$"
print(("width = 800"):match(pattern))           --> width  800
print(("  title=My notes  "):match(pattern))    --> title  My notes
print(("no equals sign"):match(pattern))        --> nil
```

The value `My notes` keeps its inner space, because only the spaces at the end are outside the
capture.

### Exercise 4.1 (LO-4.1, ★, about 10 minutes)

Write one `string.format` call that turns the name `"Ada"`, the age 36, and the height 1.754 into
`Ada        36  1.75`: the name left-aligned in 10 characters, the age right-aligned in 3, two
spaces, and the height with two decimals.

<details>
<summary>Answer</summary>

`string.format("%-10s%3d  %.2f", "Ada", 36, 1.754)`. `%-10s` pads `Ada` with seven spaces on the
right, and `%3d` adds one space before `36`. `%.2f` rounds 1.754 to `1.75`.
</details>

### Exercise 4.2 (LO-4.2, ★★, about 15 minutes)

Write `trim(s)`, which returns `s` without the whitespace at its start and end. The first step is
done for you: the pattern starts `^%s*`, which skips the leading whitespace. Finish the pattern,
and explain why one part of it must be lazy.

<details>
<summary>Answer</summary>

```lua
local function trim(s)
  return (s:match("^%s*(.-)%s*$"))
end
print("[" .. trim("  two words \n") .. "]")   --> [two words]
```

With a greedy `(.*)`, the capture would take everything to the end, trailing spaces included,
because `%s*` can match the empty string. The lazy `(.-)` takes as little as it can, so the
trailing whitespace is left for `%s*`. The outer parentheses keep only the first value, which here
is the only one anyway. `trim("")` and `trim("   ")` both give `""`.
</details>

### Exercise 4.3 (LO-4.2, ★★, about 15 minutes)

Write `title_case(s)`, which capitalizes the first letter of every word: `"the lord of the
rings"` becomes `"The Lord Of The Rings"`. Use one call to `gsub`.

<details>
<summary>Hint</summary>

A frontier finds the start of each word, and `gsub` accepts a function as the replacement.
`string.upper` is a function.
</details>

<details>
<summary>Answer</summary>

```lua
local function title_case(s)
  return (s:gsub("%f[%a]%a", string.upper))
end
```

`%f[%a]%a` matches one letter at the start of a word, and `gsub` replaces it with the result of
`string.upper`. Passing `string.upper` directly works because `gsub` calls the function with the
match. Like `%a`, this handles only ASCII letters.
</details>

### Exercise 4.4 (LO-4.2, ★★, about 15 minutes)

Predict exactly what each line prints.

```lua
print(("a,b,,c"):find(","))
print(("a,b,,c"):gsub(",", ";"))
print(("x = 10, y = 20"):match("(%a) = (%d+)"))
print(("2+2=4"):find("2+2", 1, true))
print(("2+2=4"):find("2+2"))
```

<details>
<summary>Answer</summary>

1. `2  2`: `find` returns the start and the end of the first comma.
2. `a;b;;c  3`: `gsub` returns the new string and the number of replacements.
3. `x  10`: `match` returns the captures of the first match only.
4. `1  3`: with `plain` set to `true`, the `+` is an ordinary character.
5. `nil`: as a pattern, `2+2` means "one or more 2s, then a 2", which needs two 2s in a row, and
   `"2+2=4"` has none.
</details>

### Exercise 4.5 (LO-4.3, ★★, about 15 minutes)

A style sheet checker validates lengths with the regular expression `^(\d+)(px|em|%)$`, which
accepts `12px`, `3em`, and `50%`. Write `parse_length(s)` in Lua, which returns the number as an
integer and the unit, or `nil` for anything else, such as `12pt`, `px`, or `1.5em`.

<details>
<summary>Answer</summary>

```lua
local units = { px = true, em = true, ["%"] = true }

local function parse_length(s)
  local digits, unit = s:match("^(%d+)(%D+)$")
  if digits and units[unit] then
    return tonumber(digits), unit
  end
  return nil
end
```

`%D+` captures everything after the digits, and the set accepts only the three units. `12pt`
matches the pattern, but `pt` isn't in the set. `1.5em` doesn't match the pattern at all: after
`1`, `%D+` takes the `.` but can't take the digit `5`, so `$` fails.
The key `"%"` needs brackets in the constructor, because it isn't a valid name, but it needs no
escape: only patterns treat `%` specially.
</details>

### Exercise 4.6 (LO-4.4, ★★, about 15 minutes)

A program builds a CSV file of 100,000 rows of 20 bytes each with `csv = csv .. row` in a loop.
About how many bytes does it copy in total? What would `table.concat` copy?

<details>
<summary>Hint</summary>

The *i*-th concatenation builds a string of $20i$ bytes.
</details>

<details>
<summary>Answer</summary>

The *i*-th step copies about $20i$ bytes, so the total is
$20 \cdot (1 + 2 + \cdots + n) = 20 \cdot n(n+1)/2$. For $n = 100{,}000$, that is about
$10^{11}$ bytes, 100 GB, to build a 2 MB file. `table.concat` copies each row once into the
result, about 2,000,000 bytes, so the work grows in proportion to $n$ instead of $n^2$.
</details>

### Exercise 4.7 (LO-4.4, ★★, about 15 minutes)

Write `char_at(s, i)`, which returns the `i`-th character of the UTF-8 string `s`, or `nil` when
`s` has fewer than `i` characters. `char_at("hé€", 2)` is `"é"`, and `char_at("hé€", 4)` is
`nil`.

<details>
<summary>Hint</summary>

`utf8.offset(s, i)` gives the byte where character `i` starts. It returns `#s + 1` for the
position just past the last character, and `nil` beyond that.
</details>

<details>
<summary>Answer</summary>

```lua
local function char_at(s, i)
  local start = utf8.offset(s, i)
  if start == nil or start > #s then return nil end
  return s:match(utf8.charpattern, start)
end
```

`utf8.charpattern` matches exactly one character from `start`, however many bytes it takes. For
`i` one past the end, `utf8.offset` gives `#s + 1`, which the test `start > #s` catches.
</details>

### Exercise 4.8 (LO-4.3, ★★, about 20 minutes)

Run this exercise as a script with the standalone `lua`, after `luarocks install lpeg`.

1. Write an LPeg pattern `request` that matches a whole line of the form `GET /path` or
   `POST /path`, where the path is a `/` followed by any number of lowercase letters and slashes,
   and captures the method and the path. `request:match("GET /index")` should return `"GET"` and
   `"/index"`, and `request:match("PUT /x")` should return `nil`.
2. A teammate writes `(P("GET") + P("GETS")) * " "` to accept both words. Which line does it fail
   on, and how do you fix it?

<details>
<summary>Hint</summary>

The pieces are `lpeg.C`, `+` for the two methods, `lpeg.R("az")` for the letters, `^0` for "any
number", and `-1` for the end of the line. For part 2, remember that `+` is ordered choice.
</details>

<details>
<summary>Answer</summary>

1. One pattern, built from the pieces in the reading:

   ```lua
   local lpeg = require("lpeg")
   local P, R, C = lpeg.P, lpeg.R, lpeg.C

   local request = C(P("GET") + P("POST")) * " " * C("/" * (R("az") + "/")^0) * -1
   print(request:match("GET /index"))   --> GET  /index
   print(request:match("PUT /x"))       --> nil
   ```

   It also rejects `GET index`, with no slash, and `GET /Index`, with a capital letter.
2. It fails on `GETS /x`. `P("GET")` matches the first three letters, then `" "` fails at `S`,
   and ordered choice never goes back to try `P("GETS")`. Put the longer word first:
   `(P("GETS") + P("GET")) * " "`.
</details>

