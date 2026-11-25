# Module 10: Files, the operating system, and data

**Objectives:** LO-10.1, LO-10.2, LO-10.3\
**Prerequisites:** [Module 6](../06-errors-modules-and-tests/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 10](lab10.ipynb), 1.5 for the
[practice](practice.md), and 3 to finish PA4, which follows this module

Programs so far have kept their data in memory and printed their results. This module connects
them to the world outside: files, the clock, the environment, and other programs. It also covers
the two habits that keep that connection safe. Every file a program opens must be closed, on every
path out, including errors. And data that comes from outside the program must be parsed as data,
never run as code or as a shell command.

## Files

`io.open(name, mode)` opens a file and returns a **file handle**, an object with methods for
reading and writing. Like every function that touches the outside world, it returns `nil` and a
message when it fails, instead of raising an error:

```lua
local file, message = io.open("missing.txt")
print(file, message)      --> nil  missing.txt: No such file or directory
```

| Mode | Opens for | If the file exists | If it doesn't |
| :- | :- | :- | :- |
| `"r"`, the default | Reading | Reads from the start | Fails |
| `"w"` | Writing | Empties it first | Creates it |
| `"a"` | Appending | Writes after its end | Creates it |
| `"r+"` | Reading and writing | Keeps its contents | Fails |

Add `b`, as in `"rb"`, for binary files. On Linux and macOS it changes nothing; on Windows it
stops the library from changing line endings.

### Reading and writing

`file:read(format)` reads according to its format: `"l"` reads a line without its newline, `"L"`
a line with it, `"n"` a number, `"a"` everything left, and a number reads that many bytes. At the
end of the file, every format except `"a"` returns `nil`, and `"a"` returns the empty string.
`file:lines(format)` is an iterator over the same reads, and `io.lines(name)` opens a file, walks
its lines, and closes it when the loop ends:

```lua
for line in io.lines("notes.txt") do
  print(#line, line)
end
```

`file:write(...)` writes strings and numbers, with no separators or newline of its own, and
returns the file, so writes can be chained: `file:write("x = ", 42, "\n")`. Writes are buffered:
they reach the disk when the buffer fills, when you call `file:flush()`, or when the file is
closed. `file:close()` closes the file, and any later use of the handle stops with
`attempt to use a closed file`.

## Closing on every path

A program that opens a file must close it, or its last writes may never reach the disk, and a
long-running program can run out of the operating system's file handles. Lua closes a file when
the garbage collector frees its handle, but nobody can say when that is. The difficulty is the
paths out of a function: a `return` in the middle, a `break`, or an error raised by a function it
called.

Lua 5.4's answer is the **to-be-closed variable**. A local declared with the attribute `<close>`
is closed when it goes out of scope, however that happens:

```lua
local function first_line(path)
  local file <close> = assert(io.open(path))
  local line = file:read("l")
  if line == nil then
    error("empty file: " .. path)        -- the file is closed here too
  end
  return line                            -- and here
end
```

Closing means calling the value's `__close` metamethod, which file handles have. The value must
have one, or be `nil` or `false`; anything else stops with `variable 'x' got a non-closable value`.
A table of your own becomes closable when its metatable has `__close`, which receives the object
and, when the scope ended with an error, the error value:

```lua
local function timer(name)
  local start = os.clock()
  return setmetatable({}, {
    __close = function(_, err)
      print(name, os.clock() - start, err and "failed" or "ok")
    end,
  })
end

do
  local t <close> = timer("load")
  -- work that might fail
end                                      --> load, the seconds, and ok, when the block ends
```

The generic `for` uses the same mechanism: its fourth value, the closing value from module 5, is
closed when the loop ends. `io.lines` returns the file as that value, so a `break` out of an
`io.lines` loop closes the file. A local declared `<const>` can't be assigned after its
declaration, which the compiler checks.

## The operating system

The `os` library reaches the operating system: the clock, the environment, files by name, and
other programs.

### Time and dates

`os.time()` returns the current time as a number of seconds since an epoch, on Linux and macOS
midnight UTC on January 1, 1970. `os.time(t)` turns a table with the fields `year`, `month`,
`day`, `hour`, `min`, and `sec` into that number, and normalizes fields out of range: day 32 of
January becomes February 1. `os.date(format, time)` goes the other way, with C's `strftime`
formats; a format starting with `!` uses UTC instead of local time, and `"*t"` returns a table:

```lua
print(os.date("!%Y-%m-%d %H:%M:%S", 0))            --> 1970-01-01 00:00:00
local week = os.time({ year = 2026, month = 11, day = 23, hour = 12 })
           - os.time({ year = 2026, month = 11, day = 16, hour = 12 })
print(week, week // 86400)                         --> 604800  7
```

The example sets `hour = 12` on purpose. Without an hour, `os.time` uses noon in Lua 5.4, but
code that sets midnight can lose or gain an hour where daylight saving time changes, and
`// 86400` would then be off by a day. `os.difftime(t2, t1)` returns `t2 - t1` as a float, which is
portable to systems whose times aren't seconds. `os.clock()` is different: it measures the
processor time the program has used, which is what module 12 uses to time code.

### The environment and files by name

`os.getenv(name)` returns an environment variable's value, or `nil`. `os.remove(name)`,
`os.rename(old, new)`, and `os.tmpname()` work on files by name, and return `true` or `nil` and a
message, like `io.open`.

### Running other programs

`os.execute(command)` runs a command through the system's shell and returns `true` or `nil`,
then `"exit"` and the command's exit status: in the standalone `lua`, `os.execute("exit 3")`
returns `nil  exit  3`. `io.popen(command)` runs a command and returns a file handle that reads its
output. Both depend on how Lua was built. The Lua in the course's notebooks, which lupa compiles
without the options for POSIX systems, has no `io.popen` (it raises `'popen' not supported`), and
its `os.execute` reports the raw status, 768 for `exit 3`, which is the code times 256.

### Why outside input must not reach the shell

The command is one string, which the shell reads as a small program. If any part of it came from
outside the program, such as a file name a user typed, the person who chose it can make the shell
do anything they like:

```lua
local name = "x; echo INJECTED"           -- a "file name" from outside
os.execute("echo counting " .. name)      --> counting x, then INJECTED
```

The `;` ends the first command, and the shell runs the second. With `rm` or `curl` in place of
`echo`, that is a **command injection**, one of the most common ways programs are attacked. Three
defenses, from best to worst:

1. **Don't use the shell when Lua can do the job.** `os.remove(name)` removes a file without a
   shell; `io.lines(name)` counts lines without `wc`.
2. **Accept only input that matches an allowlist,** such as `^[%w_%-]+%.csv$`, and reject anything
   else before building a command.
3. **Quote it for the shell.** On Linux and macOS, wrapping a value in single quotes, and writing
   each single quote inside it as `'\''`, makes the shell treat it as one plain word. Lab 10 writes
   this function. Windows' shell has different rules, which is one more reason to prefer the first
   two defenses.

## Data formats

### CSV

A **CSV** file holds a table of text, one record per line, with fields separated by commas. Most
programs follow RFC 4180's rules: a field that contains a comma, a double quote, or a line break is
written in double quotes, and each double quote inside it is doubled:

```text
name,city,note
Ada,"London, UK","said ""hello"""
```

So `("a,b,c"):gmatch("[^,]*")` splits lines without quotes, but breaks a quoted field such as
`"London, UK"` in two. Lab 10 writes a parser that walks the line once, tracking whether it is
inside quotes. Writing CSV is the reverse: quote a field only when it needs it, and double its
quotes.

### Lua values written with `%q`

Module 4's `string.format("%q", v)` writes a string, a number, a boolean, or `nil` as Lua source
that reads back as exactly the same value: strings with every special character escaped, and
floats in hexadecimal, so no digit is lost. `%q` can't write a table, but a short recursive
function can write one as a table constructor, item by item, with `%q` for each key and value. The
result is a Lua chunk such as `return { ["name"] = "Ada", ["age"] = 36 }`.

Reading it back means running it, and a chunk can do anything code can do. Two arguments of `load`
limit that:

```lua
local function read_value(text)
  local chunk, err = load(text, "=data", "t", {})   -- text only, and an empty environment
  if not chunk then return nil, err end
  return chunk()
end
```

The mode `"t"` refuses **binary chunks**, precompiled code that can crash Lua if it was tampered
with. The empty table as the environment means the chunk sees no globals, so `os`, `io`, and the
other libraries are out of its reach: `return os.remove("x")` fails with
`attempt to index a nil value (global 'os')`. One library stays reachable: every string carries
the string methods through its metatable, so `("x"):rep(3)` still works.

That is still not safe for data from strangers: the chunk can loop forever, or fill memory with
`("x"):rep(1e9)`, and module 14 adds limits for those. Load `%q` data only from sources you trust
as much as your program, such as its own save files. For anything else, use a format that is only
data, such as CSV, and a parser that reads it without running it.

## Common misconceptions

| Belief | What Lua does | Example that breaks it |
| :- | :- | :- |
| A failed `io.open` raises an error | It returns `nil` and a message | Wrap it in `assert` when the program can't go on |
| Opening with `"w"` adds to a file | It empties the file first | Use `"a"` to append |
| Lua closes files soon enough by itself | Only when the collector frees the handle | Use `<close>`, so every path closes it |
| An error skips the cleanup at the end of a function | A `<close>` variable is closed on errors too | `pcall` around a function with `<close>` finds the file closed |
| `os.time{…}` needs fields in range | It normalizes them | Day 32 of January is February 1 |
| A file name is safe to pass to the shell | The shell reads it as code | `"x; echo INJECTED"` runs `echo` |
| `load` with an empty environment makes data safe | It still runs code | `while true do end` never returns |

## Summary

- `io.open` returns a handle or `nil` and a message; `read` takes `"l"`, `"L"`, `"n"`, `"a"`, or
  a count, and `write` returns the file for chaining.
- A `<close>` variable closes its value when its scope ends by any path, errors included; files
  are closable, and so is any table whose metatable has `__close`.
- `os.time` and `os.date` convert between tables, strings, and seconds; use `hour = 12` for date
  arithmetic, and `os.clock` for processor time.
- `os.execute` and `io.popen` hand a string to the shell. Avoid the shell, allowlist the input, or
  quote it, in that order of preference.
- CSV needs a real parser for quoted fields. `%q` writes values that read back exactly, but reading
  them back runs code: use text mode and an empty environment, and only for trusted data.

## Self-check

1. A function opens a file, reads it, and may `return` early from three places or raise an error.
   How do you make sure the file is always closed?

   <details>
   <summary>Answer</summary>

   Declare the handle with `<close>`: `local f <close> = assert(io.open(path))`. Lua closes it
   when the scope ends, whichever `return` or error ends it, so no path needs its own `close`.
   </details>

2. What do `f:read("l")` and `f:read("a")` return at the end of a file?

   <details>
   <summary>Answer</summary>

   `nil` and the empty string. A loop that reads lines stops at the `nil`; `"a"` always succeeds.
   </details>

3. A backup script runs `os.execute("cp " .. name .. " backup/")` with a name it read from a
   folder listing. Why is that dangerous, and what would you write instead?

   <details>
   <summary>Answer</summary>

   A file can be named `x; rm -rf ~`, and the shell would run the second command. Copy the file in
   Lua instead, by reading it and writing the copy, or reject names that don't match an allowlist,
   or quote the name for the shell.
   </details>

4. Why does reading a `%q` file back use `load(text, "=data", "t", {})` rather than `load(text)`?

   <details>
   <summary>Answer</summary>

   `"t"` refuses binary chunks, and the empty environment hides every global, so the chunk can't
   reach `os`, `io`, or anything else. It can still run forever, so it is only for trusted data.
   </details>

5. Which of these CSV fields need quotes: `Ada`, `London, UK`, `5'11"`, and an empty field?

   <details>
   <summary>Answer</summary>

   `London, UK`, because of the comma, and `5'11"`, because of the double quote, written as
   `"5'11"""`. `Ada` and the empty field don't.
   </details>

## Further reading

- The *Lua 5.4 Reference Manual*, sections
  [3.3.8, To-be-closed Variables](https://www.lua.org/manual/5.4/manual.html#3.3.8),
  [6.8, Input and Output Facilities](https://www.lua.org/manual/5.4/manual.html#6.8), and
  [6.9, Operating System Facilities](https://www.lua.org/manual/5.4/manual.html#6.9).
- Y. Shafranovich, [RFC 4180: Common Format and MIME Type for Comma-Separated Values (CSV)
  Files](https://www.rfc-editor.org/rfc/rfc4180), 2005. Two pages define the quoting rules that
  most programs follow.
- Roberto Ierusalimschy, *Programming in Lua*, 4th edition (Lua.org, 2016). Its chapters on the
  external world and on data files and serialization cover more of the `io` library, and a
  serializer that handles tables that share parts.
