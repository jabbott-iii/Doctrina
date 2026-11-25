# Module 4: Strings and patterns

**Objectives:** LO-4.1, LO-4.2, LO-4.3, LO-4.4\
**Prerequisites:** [Module 3](../03-tables/index.md)\
**Time:** about 10 hours: 3 for this reading, 2 for [Lab 4](lab04.ipynb), 2 for the
[practice](practice.md), and 3 for PA2, which follows this module

This module covers Lua's string library: cutting and formatting text, searching it with Lua's
**patterns**, building long strings efficiently, and handling text that isn't plain ASCII.
Patterns look like regular expressions, but they are a smaller language with a few features
regular expressions lack, so this module spends time on what they can't do and what to write
instead. Module 1 introduced string literals, `..`, and `#`; this module builds on them.

## Strings and the string library

A Lua string is an immutable sequence of bytes. No function changes a string in place: every
function that "changes" one returns a new string, and the original stays as it was.

The `string` table holds the library's functions, and every string can call them as methods. A
**method call**, written with a colon, passes the value before the colon as the first argument,
so these two lines do the same thing:

```lua
local s = "hello"
print(string.upper(s))     --> HELLO
print(s:upper())           --> HELLO
```

This works because all strings share a metatable whose `__index` field is the `string` table, so
looking up `upper` on a string finds `string.upper`; module 7 explains metatables. A literal needs
parentheses before the colon: `("ab"):rep(3)` works, but `"ab":rep(3)` is a syntax error.

| Function | Result | Example |
| :- | :- | :- |
| `s:len()` | The length in bytes, the same as `#s` | `("hello"):len()` is 5 |
| `s:sub(i, j)` | The bytes from position `i` to `j` | `("hello"):sub(2, 4)` is `"ell"` |
| `s:upper()`, `s:lower()` | The string with ASCII letters changed | `("MiXeD"):lower()` is `"mixed"` |
| `s:rep(n, sep)` | `n` copies, with `sep` between them | `("ab"):rep(3, "-")` is `"ab-ab-ab"` |
| `s:reverse()` | The bytes in reverse order | `("abc"):reverse()` is `"cba"` |
| `s:byte(i, j)` | The numeric codes of the bytes | `("Hi"):byte(1, 2)` is `72, 105` |
| `string.char(...)` | The string of the given byte codes | `string.char(72, 105)` is `"Hi"` |

### Positions and negative indices

Positions count from 1, like table indices. A negative position counts from the end: -1 is the
last byte, -2 the one before it. `sub` clamps positions that fall outside the string instead of
failing, and gives the empty string when `i` comes after `j`:

```lua
local s = "hello"
print(s:sub(-3))         --> llo     (the last three bytes)
print(s:sub(-3, -2))     --> ll
print(s:sub(2))          --> ello    (j defaults to -1, the end)
print(s:sub(4, 2))       -->         (the empty string: 4 comes after 2)
print(s:sub(-100, 2))    --> he      (-100 is clamped to 1)
```

## `string.format`

`string.format(fmt, ...)` builds a string from a template, following the rules of C's `printf`.
Each **conversion**, a `%` followed by a letter, takes the next argument:

| Conversion | Formats | Example | Result |
| :- | :- | :- | :- |
| `%d` | An integer | `string.format("%d", 42)` | `42` |
| `%5d`, `%-5d`, `%05d` | Width 5: right-aligned, left-aligned, zero-padded | `string.format("%05d", 42)` | `00042` |
| `%x`, `%X` | An integer in hexadecimal | `string.format("%x", 255)` | `ff` |
| `%.2f` | A float with two decimals | `string.format("%.2f", 3.14159)` | `3.14` |
| `%e`, `%g` | Scientific, or the shorter of `%e` and `%f` | `string.format("%g", 1e20)` | `1e+20` |
| `%s`, `%10s`, `%-10s` | Any value, through `tostring`, with an optional width | `string.format("[%-4s]", "ab")` | `[ab  ]` |
| `%q` | A value written as Lua source, so it can be read back | `string.format("%q", 'say "hi"')` | `"say \"hi\""` |
| `%%` | A literal percent sign | `string.format("%d%%", 50)` | `50%` |

Three rules catch people out:

- `%d` and `%x` need an integer. A float with an integer value, such as `3.0`, works, but
  `string.format("%d", 3.5)` stops with `number has no integer representation`. Round first with
  `math.floor`, or use `%.0f`.
- A width or precision has at most two digits: `%100d` stops with
  `invalid conversion specification`.
- `%s` calls `tostring`, so it formats `nil`, booleans, and tables without an error. A float
  keeps its `.0`: `string.format("%s", 3.0)` is `"3.0"`.

`tonumber(s, base)` reads a number in any base from 2 to 36, and ignores spaces around it:
`tonumber("ff", 16)` is 255, `tonumber(" 42 ")` is 42, and `tonumber("4 2")` is `nil`.

## Patterns

A **pattern** describes a set of strings, and the functions in the next section search text for
the parts that match it. A pattern is itself a string, in which most characters match themselves
and a few have special meanings.

### Character classes

A **character class** matches any one character from a set:

| Class | Matches |
| :- | :- |
| `.` | Any character |
| `%a` | A letter |
| `%d` | A decimal digit |
| `%l`, `%u` | A lowercase or uppercase letter |
| `%s` | A whitespace character: space, tab, newline, and the like |
| `%w` | A letter or digit |
| `%p` | A punctuation character |
| `%x` | A hexadecimal digit |
| `%c` | A control character |

The uppercase version of each class matches the opposite set: `%D` is any character that isn't
a digit, and `%S` any character that isn't whitespace. These classes cover ASCII only; the section
on UTF-8 below shows what that means for other text.

A **set** in square brackets matches one character from a set you define. `[aeiou]` matches a
vowel, `[0-9a-f]` a digit or a letter from `a` to `f`, and `[%w_]` a letter, digit, or
underscore. A `^` right after the `[` inverts the set: `[^,]` matches any character except a
comma.

### Quantifiers

A **quantifier** after a class says how many times it repeats:

| Quantifier | Repeats the class | Example | Matches |
| :- | :- | :- | :- |
| `+` | One or more times, as many as possible | `%d+` | `2026` in `"in 2026"` |
| `*` | Zero or more times, as many as possible | `%s*` | Any run of spaces, even an empty one |
| `-` | Zero or more times, as few as possible | `<.->` | `<a>` in `"<a><b>"` |
| `?` | Zero or one time | `colou?r` | `color` and `colour` |

`*` and `+` are **greedy**: they take as much as they can and still let the rest of the pattern
match, so `<.*>` matches all of `"<a><b>"`. `-` is **lazy**: it takes as little as it can, so
`<.->` stops at the first `>`. A quantifier applies to one class only; there is no way to repeat
a longer piece of a pattern.

### Anchors and magic characters

A `^` at the start of a pattern anchors the match to the start of the text, and a `$` at the end
anchors it to the end. `^%d+$` matches a string made only of digits, and nothing else.

The characters `^ $ ( ) % . [ ] * + - ?` are **magic**: they have special meanings. To match one
of them literally, put `%` before it. `%.` matches a dot and `%%` a percent sign. Forgetting the
`%` is a common bug: in a pattern, `.` matches any character, and a `-` right after a class is a
quantifier, so `%d%d-%d%d` doesn't match `12-34`. Write `%-` for every hyphen you mean, even where
Lua would read a bare `-` as one.

### Captures

Parentheses around part of a pattern **capture** the text it matched, and the search functions
return each capture as a separate value:

```lua
local key, value = ("width=800"):match("(%w+)=(%w+)")
print(key, value)              --> width  800
```

Three more kinds of capture exist:

- An empty capture, `()`, captures a position instead of text: `("hello"):match("()ll()")` gives
  3 and 5, the positions where `ll` starts and where it ends plus one.
- `%1` through `%9` inside a pattern match the same text as an earlier capture.
  `(["'])(.-)%1` matches a quoted string that ends with the same kind of quote it started with.
- Captures are strings, even when they hold digits: `("x=10"):match("=(%d+)")` is the string
  `"10"`. Convert it with `tonumber` before arithmetic or comparison.

### Balanced pairs and frontiers

Two items have no equivalent in most regular-expression languages:

- `%bxy` matches a **balanced** run of text that starts with `x`, ends with `y`, and has as many
  `x`s as `y`s in between. `%b()` matches a parenthesized group, nested parentheses included:
  in `"f(a, g(b), c) x"`, it matches `(a, g(b), c)`.
- `%f[set]` is a **frontier**: it matches no characters, only the position between a character
  that isn't in `set` and one that is. `%f[%a]` matches where a word begins, and `%f[%A]` where
  one ends, so `%f[%a]cat%f[%A]` finds the word `cat` but not the `cat` inside `concatenate`.
  The start and the end of the text count as the character `\0`, so `%f[%a]` also matches at the
  start of a text that begins with a letter.

## Searching and replacing

Four functions use patterns:

| Function | Returns |
| :- | :- |
| `s:find(pattern, init, plain)` | The start and end positions of the first match, then its captures; or `nil` |
| `s:match(pattern, init)` | The captures of the first match, or the whole match if the pattern has none; or `nil` |
| `s:gmatch(pattern)` | An iterator over every match, for the generic `for` |
| `s:gsub(pattern, repl, n)` | A new string with the matches replaced, and the number of replacements |

`init` says where to start searching, and may be negative. `find`'s fourth argument, `plain`,
turns patterns off: `s:find(".", 1, true)` finds a literal dot. Use it when you search for text
that a user typed, which may hold magic characters.

`gmatch` returns an iterator, so it goes in a generic `for`. With captures, each pass gets them;
without, each pass gets the whole match:

```lua
for word in ("The quick, brown fox."):gmatch("%a+") do
  io.write(word, "|")              --> The|quick|brown|fox|
end

for k, v in ("a=1, b=2"):gmatch("(%w+)=(%w+)") do
  print(k, v)                      --> a 1, then b 2
end
```

In `gmatch`, a `^` at the start of the pattern isn't an anchor, because an anchored pattern could
match only once. Lua 5.4 treats it as a literal `^`, so `("aaa"):gmatch("^a")` finds nothing.

### `gsub`

`gsub` replaces every match, or the first `n`. Its replacement, `repl`, can be one of three
things:

```lua
-- a string, in which %1 to %9 stand for the captures and %0 for the whole match
print(("hello world"):gsub("(%w+)", "<%1>"))          --> <hello> <world>  2

-- a table, looked up with the first capture as the key
local vars = { name = "Ada", age = 36 }
print(("$name is $age"):gsub("%$(%w+)", vars))        --> Ada is 36  2

-- a function, called with the captures
print(("1 2 3"):gsub("%d", function(d) return d * 2 end))   --> 2 4 6  3
```

When the table has no entry, or the function returns `nil` or `false`, `gsub` keeps the original
match: `("$name and $x"):gsub("%$(%w+)", vars)` gives `"Ada and $x"`. A `%` in a replacement
string must be written `%%`; a lone one stops with `invalid use of '%' in replacement string`.

`gsub` returns two values, and that surprises people. `print(s:gsub("a", "b"))` prints the count
too, and `return s:gsub(...)` returns both. Wrap the call in parentheses to keep only the string:

```lua
local function no_vowels(s)
  return (s:gsub("[aeiou]", ""))
end
print(no_vowels("banana"))         --> bnn
```

## Patterns are not regular expressions

Lua patterns look like the regular expressions of Python, JavaScript, or `grep`, but they are a
smaller language. Lua's designers kept them small: in Lua 5.4.8, the whole pattern matcher, with
`find`, `match`, `gmatch`, and `gsub`, is under 600 lines of C in the file `lstrlib.c`. The
differences:

| Regular expressions | Lua patterns |
| :- | :- |
| `\d`, `\w`, `\s`, and `\.` | `%d`, `%w`, `%s`, and `%.`: the escape character is `%` |
| `*?`, a lazy star | `-` |
| `a\|b`, alternation | Not available |
| `(ab)+`, a quantifier on a group | Not available: quantifiers apply to one class |
| `x{2,4}`, a counted repeat | Not available: write `xxx?x?` |
| `(?:…)`, `(?=…)`, and other groups and lookarounds | Not available |
| Nothing standard for balanced pairs | `%b()` |
| `\b`, a word boundary | `%f[%w]` and `%f[%W]`, frontiers, which work with any set |

The missing **alternation** is the one you will miss most. Rewrite it as Lua code: match the
general shape with a pattern, then test the part that varies. For example, the regular expression
`\.(jpg|png|gif)$` matches file names with one of three extensions:

```lua
local image_types = { jpg = true, png = true, gif = true }

local function is_image(name)
  local ext = name:match("%.(%a+)$")     -- the general shape: a dot, letters, the end
  return ext ~= nil and image_types[ext:lower()] == true
end

print(is_image("cat.png"), is_image("notes.txt"), is_image("png"))   --> true  false  false
```

The table of extensions is a set, from module 3, and testing it is $O(1)$. When the alternatives
are whole patterns rather than words, try each pattern in turn. When a format needs alternation
everywhere, or nesting deeper than `%b` handles, a parser is the better tool, which the next section
introduces.

## Beyond patterns: LPeg

When patterns aren't enough, the usual next step is **LPeg**, a library by Roberto Ierusalimschy,
one of Lua's authors, for **parsing expression grammars** (PEGs): a way to describe a format by
rules that try their alternatives in order. LPeg is written in C, so it runs in the standalone
`lua`, but not in the notebooks' `%%lua` cells, which can't load C libraries. Install it with
LuaRocks, as [setting up your environment](../../setup.md) shows, and run these examples as
scripts.

An LPeg pattern is a Lua value that you build with functions and operators, not a string. A string
or a number where LPeg expects a pattern becomes one, so `lpeg.P("a") * "b"` works:

| LPeg | Matches | As a regular expression |
| :- | :- | :- |
| `lpeg.P("cat")` | The text `cat` | `cat` |
| `lpeg.R("az")` | One character in a range | `[a-z]` |
| `lpeg.S("+-")` | One character from a set | `[+-]` |
| `1` | Any one character | `.` |
| `p1 * p2` | `p1`, then `p2` | `p1p2` |
| `p1 + p2` | `p1`, or else `p2` | `p1\|p2` |
| `p^0`, `p^1`, and `p^-1` | Zero or more, one or more, and at most one `p` | `p*`, `p+`, and `p?` |
| `p1 - p2` | `p1`, where `p2` doesn't match | `(?!p2)p1` |
| `p * -1` | `p`, then the end of the text | `p$` |
| `lpeg.C(p)` | `p`, captured as a string | `(p)` |

The regular expression `^(cat|dog)s?$`, which the previous section had to rewrite as code, is one
LPeg pattern:

```lua
local lpeg = require("lpeg")
local P = lpeg.P

local pet = (P("cat") + P("dog")) * P("s")^-1 * -1
print(pet:match("cats"), pet:match("dog"), pet:match("catss"))   --> 5  4  nil
```

`match` returns the position just after the match, or `nil`. A pattern matches only at the start
of the text, as if it began with `^`.

Captures turn what matched into values. `p / f` passes `p`'s captures to the function `f` and
captures what it returns, and `lpeg.Ct(p)` collects `p`'s captures into a table. This pattern reads
a list of numbers, with a quantifier on a whole group, which Lua patterns can't do:

```lua
local R, S, C, Ct = lpeg.R, lpeg.S, lpeg.C, lpeg.Ct

local space = S(" \t")^0
local number = C(R("09")^1) / tonumber                -- capture the digits, then convert them
local list = Ct(space * number * (space * "," * space * number)^0 * space) * -1

local t = list:match("1, 22,333 ")
print(#t, t[1] + t[2] + t[3])                         --> 3  356
print(list:match("1,,2"))                             --> nil
```

A **grammar** is a table of rules that can refer to each other, and to themselves, with
`lpeg.V("name")`; its first entry names the rule to match. That handles nesting of any depth.
`%b()` knows one kind of bracket: `("([a)]"):match("%b()")` returns `([a)`. A grammar checks two
kinds, nested in any order:

```lua
local V = lpeg.V

local brackets = P({
  "pair",                                                 -- the rule to match first
  pair = "(" * V("inner") * ")" + "[" * V("inner") * "]",
  inner = ((1 - S("()[]")) + V("pair"))^0,                -- non-brackets, or nested pairs
})
print(brackets:match("([a]())"), brackets:match("([a)]"))   --> 8  nil
```

One difference from regular expressions catches everyone. LPeg's `+` is **ordered choice**: it
tries `p1`, and tries `p2` only if `p1` fails. Once `p1` has matched, a later failure doesn't go
back to try `p2`, as a regular expression's `|` would:

```lua
print(((P("a") + "ab") * "c"):match("abc"))   --> nil: "a" matched, then "c" failed at "b"
print(((P("ab") + "a") * "c"):match("abc"))   --> 4
```

Put the longer alternative first. LPeg also ships the `re` module, which writes the same patterns
in a syntax closer to regular expressions: `re.match("cats", "('cat' / 'dog') 's'? !.")` returns
5, where `/` is ordered choice and `!.` means "no character follows".

Use patterns for one field or one line, and LPeg when a format needs alternation, quantified
groups, or nesting, such as a configuration language, a query syntax, or JSON. The cost is a C
library that everyone who runs your program must install too.

## Building long strings

Because strings are immutable, `s = s .. piece` builds a new string and copies all of `s` into
it. In a loop that appends *n* pieces, the copies add up to about $n^2/2$ pieces' worth, which is
$O(n^2)$. Collect the pieces in a list and join them once with `table.concat`, which copies each
piece once:

```lua
local parts = {}
for i = 1, 3 do
  parts[#parts + 1] = string.format("line %d", i)
end
local text = table.concat(parts, "\n")
print(text)                        --> line 1, line 2, and line 3, on three lines
```

On an Intel Core i7-11800H, in Lua 5.4.8 through lupa 2.8, building a 400,000-byte string from
40,000 pieces of 10 bytes took 0.59 s with `..` in a loop, and 1.7 ms with `table.concat`. Lab 4
repeats the measurement. A few `..` in one expression, such as `a .. ", " .. b`, are fine: Lua
joins them in one step.

## Text that isn't ASCII: UTF-8

Lua's string functions work on bytes, and know nothing of characters. Most text today is
**UTF-8**, an encoding that stores each character, or **code point**, in one to four bytes:
ASCII characters take one byte, `é` takes two, and `€` three. So in UTF-8 text, a byte position
isn't a character position:

```lua
local word = "héllo"
print(#word)                 --> 6: five characters, six bytes
print(word:upper())          --> HéLLO: upper changes only ASCII letters
print(word:match("%a+"))     --> h: %a matches only ASCII letters
print(word:sub(1, 2))        --> half of é: an invalid string
```

`s:reverse()` reverses bytes, so it scrambles any character longer than one byte, and `s:sub`
can cut one in half. The `utf8` library works with characters instead:

| Function | Result | Example |
| :- | :- | :- |
| `utf8.len(s)` | The number of characters, or `nil` and the position of the first invalid byte | `utf8.len("héllo")` is 5 |
| `utf8.char(...)` | The string of the given code points | `utf8.char(72, 233)` is `"Hé"` |
| `utf8.codepoint(s, i, j)` | The code points of the characters that start between bytes `i` and `j` | `utf8.codepoint("é")` is 233 |
| `utf8.codes(s)` | An iterator over each character's byte position and code point | See below |
| `utf8.offset(s, n)` | The byte position where character `n` starts | `utf8.offset("hé€x", 3)` is 4 |
| `utf8.charpattern` | A pattern that matches one UTF-8 character | `s:gmatch(utf8.charpattern)` |

```lua
for position, code in utf8.codes("hé€") do
  io.write(position, ":", code, " ")      --> 1:104 2:233 4:8364
end
```

`€` starts at byte 4 because `é` took bytes 2 and 3. `utf8.codes` stops with
`invalid UTF-8 code` on bytes that aren't valid UTF-8, and `utf8.len` returns `nil` and the
position of the first bad byte, so test text from outside your program with `utf8.len` first.
Characters aren't everything a reader sees as one letter: an accent can also be stored as a
separate code point after its letter, so even `utf8.len` can count more characters than a reader
sees. Full Unicode text handling needs a library beyond Lua's standard one.

## Common misconceptions

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| String functions change the string | They return a new one | `s:upper()` leaves `s` as it was |
| `"ab":rep(3)` works | A literal needs parentheses | It is a syntax error; write `("ab"):rep(3)` |
| `.` in a pattern matches a dot | It matches any character | `("a.b"):gsub(".", "-")` gives `---` |
| Captures of digits are numbers | Captures are strings | `("x=10"):match("=(%d+)") + 1` works, but `== 10` is `false` |
| `return s:gsub(...)` returns the string | It returns the string and the count | `print(("aaa"):gsub("a", "b"))` prints `bbb  3` |
| Patterns support `\|` like regular expressions | There is no alternation | Match the shape, then test a set |
| LPeg's `+` works like a regular expression's `\|` | It is ordered: once the first option matches, the second is never tried | `((P("a") + "ab") * "c"):match("abc")` is `nil` |
| `^` anchors a `gmatch` pattern | It matches a literal `^` there | `("aaa"):gmatch("^a")` finds nothing |
| `s = s .. piece` in a loop is fine | It is $O(n^2)$ | 40,000 pieces took 0.59 s instead of 1.7 ms |
| `#s` counts characters | It counts bytes | `#"héllo"` is 6 |
| `%a` and `upper` handle any letter | They handle ASCII only | `("héllo"):match("%a+")` is `"h"` |

## Summary

- Strings are immutable bytes. Every string can call the `string` functions as methods, and
  negative positions count from the end.
- `string.format` follows C's `printf`: `%d` needs an integer, widths have at most two digits,
  and `%s` formats anything through `tostring`.
- Patterns are built from classes (`%d`, `[%w_]`), quantifiers (`+`, `*`, the lazy `-`, `?`),
  anchors, captures, `%b`, and `%f`; `%` escapes the magic characters.
- `find`, `match`, `gmatch`, and `gsub` search with patterns. `gsub` returns a count as well as
  the string, and takes a string, a table, or a function as its replacement.
- Patterns have no alternation and no quantifiers on groups: match the general shape, then test
  the varying part in code.
- Build long strings with `table.concat`, which is $O(n)$, not with `..` in a loop, which is
  $O(n^2)$.
- For UTF-8 text, count and walk characters with the `utf8` library; `#`, `sub`, `reverse`,
  `upper`, and `%a` work on bytes and ASCII.
- LPeg, a C library, builds patterns from functions and operators, with ordered choice (`+`),
  quantified groups, captures that become values, and grammars for nested formats.

## Self-check

1. What do `("lua"):rep(2, " ")`, `("pattern"):sub(-4, -2)`, and
   `string.format("%-6s|%3d", "ab", 7)` give?

   <details>
   <summary>Answer</summary>

   `"lua lua"`, `"ter"`, and `"ab    |  7"`. Position -4 is the `t` of `tern`, and -2 the `r`;
   `%-6s` pads `ab` on the right to six characters, and `%3d` pads 7 on the left to three.
   </details>

2. Write a pattern that matches a time such as `08:15:02` and captures the hours, minutes, and
   seconds.

   <details>
   <summary>Answer</summary>

   `(%d%d):(%d%d):(%d%d)`. The captures are strings, such as `"08"`; pass them to `tonumber` to
   compute with them.
   </details>

3. What do `("<b>bold</b>"):match("<(.*)>")` and `("<b>bold</b>"):match("<(.-)>")` give, and
   why do they differ?

   <details>
   <summary>Answer</summary>

   `"b>bold</b"` and `"b"`. `.*` is greedy, so it runs to the last `>`; `.-` is lazy, so it stops
   at the first.
   </details>

4. How would you match lines that start with `GET` or `HEAD`, which a regular expression writes
   as `^(GET|HEAD) `?

   <details>
   <summary>Answer</summary>

   Capture the word with `^(%u+) `, then test it against a set:
   `local methods = { GET = true, HEAD = true }` and `methods[word]`. Lua patterns have no
   alternation.
   </details>

5. `name` holds `"Zoë"`. What are `#name` and `utf8.len(name)`, and what does `name:reverse()`
   give?

   <details>
   <summary>Answer</summary>

   4 and 3: `ë` takes two bytes. `reverse` reverses the four bytes, which splits `ë` into its two
   bytes in the wrong order, so the result isn't valid UTF-8 and `utf8.len` of it is `nil`.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, sections
  [6.4, String Manipulation](https://www.lua.org/manual/5.4/manual.html#6.4) and
  [6.4.1, Patterns](https://www.lua.org/manual/5.4/manual.html#6.4.1). Section 6.4.1 is two pages
  long and defines every pattern item exactly; read it once in full.
- The manual's section [6.5, UTF-8 Support](https://www.lua.org/manual/5.4/manual.html#6.5), for
  the `utf8` library's optional `lax` argument, which accepts code points beyond Unicode's range
  and surrogates.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapters on
  strings and on pattern matching have longer examples of each function.
- Roberto Ierusalimschy,
  ["A Text Pattern-Matching Tool Based on Parsing Expression Grammars"](https://onlinelibrary.wiley.com/doi/10.1002/spe.892),
  *Software: Practice and Experience* 39(3), 2009. It introduces LPeg and the parsing expression
  grammars it is built on: the next step when Lua patterns aren't enough.
- [LPeg on LuaRocks](https://luarocks.org/modules/gvvaughan/lpeg). Its source package holds LPeg's
  own manual, `lpeg.html`, and the manual of the `re` module, `re.html`.
