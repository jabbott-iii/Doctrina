# Module 1: First steps

**Objectives:** LO-1.1, LO-1.2, LO-1.3, LO-1.4\
**Prerequisites:** the course's prerequisites; this is the first module\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 1](lab01.ipynb), 1.5 for the
[practice](practice.md), and 3 toward PA1, which follows Module 2

This module gets you running Lua and predicting what small pieces of Lua do. You will run code
three ways, read the error messages Lua gives when code fails, and learn the four simplest of
Lua's types: `nil`, booleans, numbers, and strings. Two rules in this module cause more bugs
for newcomers than anything else in the language. Variables are global unless you declare them
`local`, and only `nil` and `false` count as false.

## Why Lua looks the way it does

Lua was designed in 1993 at the Pontifical Catholic University of Rio de Janeiro (PUC-Rio) as a
language for configuring and extending other programs, and that is still its main job. The
interpreter is a C library: a host program, such as a game engine, an editor, or a database,
links it in and lets users script the host in Lua. Because the library has to fit inside other
programs, its designers keep the language small. They prefer a few general mechanisms to many
special features. The best example is the table, which you meet in module 3: Lua has no separate
arrays, dictionaries, records, modules, or classes, because tables do all of those jobs.

Each version of Lua is a new language in small ways, and code written for one may not run on
another. This course teaches Lua 5.4. Module 14 compares it with Lua 5.1, LuaJIT, and Lua 5.5,
which many hosts still embed or have adopted.

## Running Lua

Lua compiles and runs code in units called **chunks**. A chunk is a file, a line typed at the
interactive prompt, or a notebook cell. Lua compiles the whole chunk first and runs it only if it
compiles, so a syntax error anywhere in a file stops all of it.

### The interactive interpreter

Run `lua` with no arguments to start the interactive interpreter. It prints its version and a
`>` prompt, then runs each line you type:

```text
$ lua
Lua 5.4.8  Copyright (C) 1994-2025 Lua.org, PUC-Rio
> print("hello")
hello
> 1 + 2
3
```

When a line is an expression, such as `1 + 2`, the interpreter prints its value. When a line is
incomplete, such as a `function` without its `end`, the interpreter shows a `>>` prompt and waits
for the rest. To leave, press Ctrl+D on Linux and macOS, or call `os.exit()`.

Each line you type is its own chunk, and that has a consequence you will see again in notebooks.
A `local` variable lasts only until the end of its chunk, so it is gone by the next line:

```text
> local x = 1
> x
nil
> y = 2
> y
2
```

`y`, which has no `local`, is a global variable, and globals last for the whole session.

### Scripts

Put a program in a file and pass the file to `lua`. Save this as `hello.lua`:

```lua
-- hello.lua: the first program.
local name = "Lua"
print("Hello from " .. name)
```

Then run it:

```bash
lua hello.lua
```

It prints `Hello from Lua`. Two other options help while you learn. `lua -e 'print(2^10)'` runs
the code in quotes, and `lua -i hello.lua` runs the script and then gives you the prompt, with the
script's global variables still there to try out.

### Notebook cells

The labs run Lua inside Jupyter notebooks through `lualab`, a small helper written for this
course. A lab's first code cell loads it with `%load_ext lualab`. After that, any cell that starts
with `%%lua` runs as Lua 5.4:

```text
%%lua
local greeting = "Hello"
print(greeting .. " from a cell")
```

A cell behaves like a line at the interactive prompt. It is one chunk, so its local variables
disappear when it ends, but its global variables are still there in later cells. A cell that is a
single expression shows its value. A Lua error fails the cell, and `lualab` shows Lua's message
below it.

### Reading an error message

Lua reports two kinds of error. A **compile error** means the chunk isn't valid Lua, and nothing
in it runs. A **runtime error** happens while the chunk runs, and everything before the failing
line has already happened.

Here is a script with a runtime error. Read it before you read the message, and see whether you
can find the bug:

```lua
-- average.lua: prints the average of three scores.
local total = 0
local count = 0

local function add(score)
  total = total + score
  count = count + 1
end

add(90)
add(72)
add(81)
print("average:", totl / count)
```

Running it prints:

```text
lua: average.lua:13: attempt to perform arithmetic on a nil value (global 'totl')
stack traceback:
        average.lua:13: in main chunk
        [C]: in ?
```

Read the first line from left to right:

1. `lua:` is the program that reports the error.
2. `average.lua:13:` is the chunk and the line. Go to line 13 first.
3. `attempt to perform arithmetic on a nil value` is what went wrong: the code did arithmetic on
   `nil`, the value that means "no value".
4. `(global 'totl')` says where the `nil` came from: a global variable named `totl`. Line 13
   misspells `total`, and a name that was never assigned is a global whose value is `nil`.

The **stack traceback** lists the functions that were running, innermost first. Here only the
main chunk was running. `[C]: in ?` is the interpreter's own C code, which started the chunk; you
can ignore it. In a notebook the same error reads `LuaError: cell:13: …`, with `cell` in place of
the file name.

A compile error names the line where Lua gave up, which can be after the real mistake:

```text
lua: syntax.lua:3: ')' expected (to close '(' at line 2) near 'print'
```

Line 2 left a parenthesis open, and Lua noticed only when line 3 began with `print`. Nothing in
the file ran, not even its first line.

## Values and types

Lua is **dynamically typed**: variables have no types, and values do. Any variable can hold any
value, and the function `type` returns the name of a value's type as a string:

```lua
print(type(42))       --> number
print(type("42"))     --> string
print(type(nil))      --> nil
print(type(type))     --> function
```

Lua has eight types. This module covers the first four:

| Type | Values | Module |
| :- | :- | :- |
| `nil` | `nil` alone | 1 |
| `boolean` | `true` and `false` | 1 |
| `number` | integers such as `42` and floats such as `4.2` | 1 |
| `string` | immutable sequences of bytes, such as `"hi"` | 1 and 4 |
| `function` | functions, which are values like any other | 2 and 5 |
| `table` | Lua's one data structure | 3 |
| `userdata` | blocks of memory owned by C code, such as open files | 10 and 13 |
| `thread` | coroutines | 9 |

## `nil`

`nil` is a value whose job is to be different from every other value. It means "no useful value":
a variable that was never assigned holds `nil`, and so does a table field that doesn't exist.
Assigning `nil` to a global variable deletes it.

Most operations on `nil` are runtime errors. Arithmetic, concatenation, and calling `nil` all
fail, and the message says which variable held it. You saw `attempt to perform arithmetic on a nil
value (global 'totl')` above. Calling a misspelled function gives
`attempt to call a nil value (global 'pritn')`.

## Booleans and truthiness

The boolean type has two values, `true` and `false`. Conditions in Lua don't require booleans,
though. Any value can be a condition, and the rule is short:

> **Only `nil` and `false` are false.** Every other value is true, including `0` and the empty
> string `""`.

This differs from Python, JavaScript, and C, where `0` and empty strings are false:

```lua
if 0 then print("0 is true") end       --> 0 is true
if "" then print("'' is true") end     --> '' is true
if nil then print("never printed") end
```

The rest of this module calls values "truthy" or "falsy" when what matters is how a condition
treats them: `nil` and `false` are falsy, and everything else is truthy.

## Numbers: integers and floats

Lua 5.4 has one number type with two **subtypes**: integers, which are 64-bit whole numbers in the
standard build, and floats, which are 64-bit floating-point numbers ("doubles" in C). `math.type`
tells them apart:

```lua
print(math.type(3))      --> integer
print(math.type(3.0))    --> float
print(3 == 3.0)          --> true
```

A literal with a decimal point or an exponent is a float: `3.0`, `.5`, `1e3`. A literal without
one is an integer: `3`, `0xff` (hexadecimal for 255). `3` and `3.0` are equal, but they print
differently, and some operations care which one they get.

### Arithmetic

The arithmetic operators decide the result's subtype by these rules:

| Operator | Meaning | Result |
| :- | :- | :- |
| `+`, `-`, `*` | add, subtract, multiply | an integer if both operands are integers; otherwise a float |
| `/` | division | always a float, even for `6 / 2` |
| `//` | floor division: divide, then round down toward minus infinity | an integer if both operands are integers; otherwise a float |
| `%` | modulo: the remainder after floor division, with the sign of the divisor | an integer if both operands are integers; otherwise a float |
| `^` | exponentiation | always a float |

Here they are on a few values, as the interpreter prints them:

```lua
print(7 / 2, 6 / 2)        --> 3.5     3.0
print(7 // 2, -7 // 2)     --> 3       -4
print(7.0 // 2)            --> 3.0
print(7 % 3, -7 % 3)       --> 1       2
print(7 % -3)              --> -2
print(2 ^ 10)              --> 1024.0
print(3 + 4, 3 + 4.0)      --> 7       7.0
```

Two of these surprise programmers from other languages. First, `-7 // 2` is `-4`, not `-3`,
because floor division rounds down, not toward zero. Second, `-7 % 3` is `2`, not `-1`, because
the result takes the divisor's sign. The two operators always agree, so that
`a == (a // b) * b + a % b` for any integers `a` and `b` where `b` isn't zero. For `a = -7` and
`b = 3`, that is `(-3) * 3 + 2`, which is `-7`.

Precedence follows mathematics, with one rule to remember: `^` binds tighter than unary minus, so
`-2^2` is `-4.0`, not `4.0`. Use parentheses when in doubt.

### Limits

Integers are exact, but they have limits. The largest is `math.maxinteger`
(9223372036854775807), and integer arithmetic **wraps around** past it:
`math.maxinteger + 1 == math.mininteger` is `true`, and no error tells you it happened.

Floats have limits of a different kind. They can't represent most decimal fractions exactly, so
`0.1 + 0.2 == 0.3` is `false`. What makes this confusing in Lua is that `print(0.1 + 0.2)` prints
`0.3`. `print` shows floats with 14 significant digits, which hides the difference.
`string.format("%.17g", 0.1 + 0.2)` shows all of it: `0.30000000000000004`. Compare floats with a
tolerance, such as `math.abs(a - b) < 1e-9`, and never use floats for money; module 10 shows the
alternative.

### Division by zero

Dividing by zero follows the operand types. Float division (`/`) never fails: `1 / 0` is
`inf` (positive infinity, also `math.huge`), `-1 / 0` is `-inf`, and `0 / 0` is NaN ("not a
number"), which prints as `nan` or `-nan` depending on the platform. Integer floor division and
modulo by zero are runtime errors: `1 // 0` raises `attempt to divide by zero`, and `1 % 0`
raises `attempt to perform 'n%%0'`.

## Strings

A string is an immutable sequence of bytes. Write a string literal in double or single quotes,
which mean the same thing, or in **long brackets**, `[[` and `]]`, which can span lines and treat
backslashes as ordinary characters:

```lua
local a = "say \"hi\"\n"     -- \" is a quote, \n a newline
local b = 'it\'s'            -- single quotes work the same way
local c = [[C:\temp
two lines]]                  -- no escapes inside long brackets
```

The operator `..` concatenates two strings, and it converts numbers to strings on the way.
`"Lua " .. 5.4` is `"Lua 5.4"`. Put spaces around `..` when a number is on its left: `1 .. 2` is
`"12"`, but `1..2` is a compile error (`malformed number near '1..2'`), because Lua reads it as a
badly written number.

The **length operator** `#` gives a string's length in **bytes**, not characters. `#"hello"` is
5, but `#"é"` is 2, because UTF-8 stores `é` in two bytes. Module 4 shows how to count characters.

### Strings and numbers don't mix freely

Lua converts a string to a number when you do arithmetic on it, and that makes code look as if
strings and numbers were interchangeable. They aren't:

```lua
print("10" + 1)      --> 11
print("10" == 10)    --> false
print(10 .. "")      --> 10
```

`"10" + 1` works because arithmetic converts the string. `"10" == 10` is `false` because `==`
never converts: a string and a number are never equal. `<` doesn't convert either, and comparing a
number with a string is an error (`attempt to compare number with string`). Between two strings,
`<` compares them as text, byte by byte in the default locale, so `"10" < "9"` is `true`, and
every uppercase letter comes before every lowercase one (`"Z" < "a"` is `true`).

Convert on purpose instead of relying on these rules. `tonumber(s)` returns the number a string
holds, or `nil` if it holds none, and `tostring(v)` turns any value into a string:

```lua
print(tonumber("42"), tonumber("4.5"), tonumber("abc"))   --> 42  4.5  nil
print(tostring(3.0), tostring(nil))                       --> 3.0 nil
```

## Variables: global unless you say `local`

An assignment to a name that hasn't been declared creates a **global variable**, visible to the
whole program. A `local` declaration creates a **local variable**, visible from the declaration
to the end of its block. A block is a chunk, a function body, the body of a control structure,
or an explicit `do … end`:

```lua
local x = 1
do
  local x = 2      -- a new variable that shadows the outer x
  print(x)         --> 2
end
print(x)           --> 1
```

Declaring several variables at once assigns values by position. Missing values become `nil`, and
extra values are dropped:

```lua
local a, b = 1          -- b is nil
local c, d = 1, 2, 3    -- the 3 is dropped
a, b = b, a             -- swaps a and b
```

### The bug a missing `local` causes

Because a forgotten `local` still runs, the bug it causes shows up far from its cause. This
function counts the words in a string, and the program also keeps a count of its own in a global
`n`:

```lua
local function count_words(text)
  n = 0                          -- meant to be local
  for _ in text:gmatch("%S+") do -- loops once per word (module 4 explains)
    n = n + 1
  end
  return n
end

n = 100
print(count_words("one two three"))  --> 3
print(n)                             --> 3, not 100
```

`n = 0` inside the function has no `local`, so it assigns the global `n` and wipes out the 100
that the rest of the program relied on. The function returns the right answer, so a test of
`count_words` alone passes. The bug appears only where the program later reads `n`. The fix is
one word: `local n = 0`.

A misspelled name causes the second kind of bug. Assigning to a misspelling creates a new global,
and reading one gives `nil`, as `totl` did in `average.lua`.

The defense is a habit: **declare every variable `local`**, at the point where you first need it.
Locals are also faster than globals, because Lua finds a local by its position instead of looking
its name up in the table of globals, and module 12 measures the difference. Module 11 adds
luacheck, a tool that reports every global your code creates or reads by mistake.

## Logical operators

`and`, `or`, and `not` treat their operands by truthiness, and `and` and `or` return one of their
operands rather than `true` or `false`:

- `a and b` returns `a` if `a` is falsy, and otherwise `b`.
- `a or b` returns `a` if `a` is truthy, and otherwise `b`.
- `not a` returns `true` if `a` is falsy, and otherwise `false`. It always returns a boolean.

Both `and` and `or` **short-circuit**: they evaluate `b` only when they need it, so
`false and error("never")` never calls `error`.

```lua
print(nil or "default")    --> default
print(0 and "yes")         --> yes
print(nil and 1)           --> nil
print(not 0)               --> false
```

Two idioms come from these rules. `x = x or 10` gives `x` a default when it is `nil`, and you will
see it often in Lua code. `cond and a or b` picks `a` when `cond` is truthy and `b`
otherwise, like the `?:` operator in C. Both have a trap: if `a` is `false` or `nil`,
`cond and a or b` returns `b` even when `cond` is true, because `cond and a` is falsy. Module 2
returns to this trap in default values.

The comparison operators are `==`, `~=` (not equal; `!=` is a compile error), `<`, `>`, `<=`, and
`>=`, and they always return a boolean. `not` binds tighter than `==`, so `not x == y` means
`(not x) == y`. Write `x ~= y` or `not (x == y)` instead.

## Comments

`--` starts a comment that runs to the end of the line. `--[[` starts a comment that runs to the
next `]]`, across lines. Comments explain why the code does something; the code already says what
it does.

## Common misconceptions

Each of these is a belief that other languages teach, and each example breaks it.

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| `0` and `""` are false | Only `nil` and `false` are false | `if 0 then print("yes") end` prints `yes` |
| Dividing two integers gives an integer | `/` always gives a float | `6 / 2` is `3.0`; use `//` for an integer |
| Integer division rounds toward zero | `//` rounds down | `-7 // 2` is `-4` |
| A variable without `local` is local to its function | It is global | The `count_words` example changes the global `n` |
| `#` counts characters | `#` counts bytes | `#"é"` is 2 |
| `"10"` and `10` are the same, since `"10" + 1` works | `==` never converts | `"10" == 10` is `false` |
| If `print` shows `0.3`, the value is 0.3 | `print` shows 14 significant digits | `0.1 + 0.2 == 0.3` is `false` |

## Summary

- Lua runs code in chunks: a file, a line at the prompt, or a notebook cell. A compile error stops
  the whole chunk; a runtime error stops it at the failing line.
- An error message gives the chunk, the line, what went wrong, and often the variable involved.
  Read it from left to right, and go to the line it names first.
- Values have types, and variables don't. `type` names a value's type.
- Numbers are integers or floats. `/` and `^` always give floats; `//` rounds down; `%` takes the
  divisor's sign. Integers wrap around on overflow, and floats are inexact.
- Strings are immutable bytes. `..` joins them, `#` counts bytes, and `==` never treats a string
  as equal to a number.
- Only `nil` and `false` are false. `and` and `or` return one of their operands.
- Variables are global unless declared `local`, so declare every variable `local`.

## Self-check

Answer each question before you open its answer.

1. What do `7 // 2`, `7 / 2`, and `-7 // 2` evaluate to, and what is each one's subtype?

   <details>
   <summary>Answer</summary>

   `3` (integer), `3.5` (float), and `-4` (integer). `//` gives an integer when both operands
   are integers, and it rounds down, so `-3.5` becomes `-4`.
   </details>

2. A script prints `lua: report.lua:8: attempt to call a nil value (global 'formatt')`. What is
   the most likely cause, and where do you look?

   <details>
   <summary>Answer</summary>

   Line 8 of `report.lua` calls `formatt`, which no code ever assigned, most likely a
   misspelling of a function's name. Look at line 8 first.
   </details>

3. What does `print(0 and "zero" or "none")` print, and why?

   <details>
   <summary>Answer</summary>

   `zero`. `0` is truthy, so `0 and "zero"` is `"zero"`, which is truthy, so the `or` returns it.
   </details>

4. Why does `print(0.1 + 0.2)` print `0.3` when `0.1 + 0.2 == 0.3` is `false`?

   <details>
   <summary>Answer</summary>

   The sum is 0.30000000000000004, because floats can't represent 0.1, 0.2, or 0.3 exactly.
   `print` shows only 14 significant digits, which rounds the sum to `0.3`.
   </details>

5. A function assigns `count = 0` without `local`. The function's own tests pass. What can still
   go wrong, and where would you see it?

   <details>
   <summary>Answer</summary>

   The assignment creates or overwrites a global `count`. Any other code that uses a global
   named `count` now sees the function's value, so the failure shows up in that other code, not
   in the function.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, sections [2.1, Values and Types](https://www.lua.org/manual/5.4/manual.html#2.1),
  [3.4.1, Arithmetic Operators](https://www.lua.org/manual/5.4/manual.html#3.4.1), and
  [3.4.3, Coercions and Conversions](https://www.lua.org/manual/5.4/manual.html#3.4.3). The
  manual is short and exact; these sections are the rules this module explains, stated in full.
- The manual's section [7, Lua Standalone](https://www.lua.org/manual/5.4/manual.html#7), for
  every option of the `lua` command.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). The standard
  textbook, written for Lua 5.3, which agrees with 5.4 on everything in this module. Its opening
  chapters cover this module's material at greater length.
- Roberto Ierusalimschy, Luiz Henrique de Figueiredo, and Waldemar Celes, "The Evolution of Lua,"
  in *Proceedings of the Third ACM SIGPLAN Conference on History of Programming Languages*
  (2007), DOI [10.1145/1238844.1238846](https://dl.acm.org/doi/10.1145/1238844.1238846). Lua's
  designers explain where the language came from and why it stays small.
