# Module 10 practice

These exercises practice the [Module 10 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it in a `%%lua` cell or with the standalone
`lua`.

## Worked example: counting words in a file

Write `count_words(path)`, which returns the number of words in a text file, or `nil` and a
message if the file can't be opened.

1. **Open, and report failure as data.** `io.open(path)` returns `nil` and a message for a missing
   file, and a missing file is an expected failure, so pass both on.
2. **Make closing automatic.** Declare the handle `<close>` once the open has succeeded; every path
   out of the function now closes it.
3. **Read in the smallest useful pieces.** `file:lines()` gives one line at a time, so a large file
   never has to fit in memory at once.
4. **Count with a pattern.** `%S+` matches a run of characters that aren't whitespace, which is a
   word for this purpose.

```lua
local function count_words(path)
  local file, err = io.open(path)
  if not file then return nil, err end
  local f <close> = file
  local count = 0
  for line in f:lines() do
    for _ in line:gmatch("%S+") do count = count + 1 end
  end
  return count
end
```

### Exercise 10.1 (LO-10.1, ★, about 10 minutes)

Which mode would you pass to `io.open` for each file, and what happens to what is already in it?

1. A log that each run of the program adds lines to.
2. A settings file that the program rewrites from scratch when the user saves.
3. A data file that the program only reads.

<details>
<summary>Answer</summary>

1. `"a"`: writes go after the end, and the old lines stay.
2. `"w"`: the file is emptied when it is opened, so a program that fails between opening and
   writing leaves an empty file. Safer: write to a temporary file, then `os.rename` it over the old
   one.
3. `"r"`, the default: nothing changes, and a missing file makes `io.open` return `nil`.
</details>

### Exercise 10.2 (LO-10.1, ★★, about 15 minutes)

This function leaks a file handle on some paths. Which ones? Fix it.

```lua
local function header_of(path)
  local f = assert(io.open(path))
  local line = f:read("l")
  if line == nil then
    return nil
  end
  local fields = csv_split(line)
  f:close()
  return fields
end
```

<details>
<summary>Answer</summary>

An empty file returns before `f:close()`, and an error inside `csv_split` skips it too. Declare
the handle `<close>` and delete the explicit `close`:

```lua
local function header_of(path)
  local f <close> = assert(io.open(path))
  local line = f:read("l")
  if line == nil then return nil end
  return csv_split(line)
end
```

`return csv_split(line)` isn't a tail call here, because a `<close>` variable is in scope, so the
file stays open until `csv_split` has finished.
</details>

### Exercise 10.3 (LO-10.2, ★★, about 15 minutes)

Write the expressions that give (a) today's date as `2026-11-23`, (b) the current time in UTC as
`14:05`, and (c) the day of the week, as a number from 1 for Sunday to 7, of November 23, 2026.

<details>
<summary>Answer</summary>

(a) `os.date("%Y-%m-%d")`. (b) `os.date("!%H:%M")`: the `!` asks for UTC. (c)
`os.date("*t", os.time({ year = 2026, month = 11, day = 23, hour = 12 })).wday`, which is 2,
because November 23, 2026, is a Monday. The table that `"*t"` returns also has `yday`, the day of
the year, and `isdst`.
</details>

### Exercise 10.4 (LO-10.2, ★★, about 15 minutes)

A web service makes a folder for each new user with `os.execute("mkdir data/" .. username)`. What
can a user who chooses the name `a; rm -rf data` do? Rewrite the line so it is safe, and say why
your version is safe.

<details>
<summary>Answer</summary>

The shell runs `mkdir data/a`, then `rm -rf data`, which deletes every user's data. Check the name
against an allowlist before it reaches the shell:

```lua
if not username:match("^[%w_]+$") then
  return nil, "a user name may contain only letters, digits, and underscores"
end
os.execute("mkdir data/" .. username)
```

A name that passes contains no space, `;`, quote, `$`, or other character the shell treats
specially, so the shell reads it as plain text. Quoting it with Lab 10's `shell_quote` would work
too, but an allowlist also keeps names out that would cause other trouble, such as `..`.
</details>

### Exercise 10.5 (LO-10.3, ★★, about 15 minutes)

Write the CSV line for the fields `Ada`, `Lovelace, Countess`, `the "Enchantress"`, and an empty
field. Then give the fields of the line `"x,""y""",,z`.

<details>
<summary>Answer</summary>

`Ada,"Lovelace, Countess","the ""Enchantress""",`. The empty field leaves nothing after the last
comma. The second line has three fields: `x,"y"`, an empty field, and `z`.
</details>

### Exercise 10.6 (LO-10.3, ★★★, about 15 minutes)

A program loads level files that players share online with
`load(text, "=level", "t", {})()`. The empty environment hides `os` and `io`. Name two things a
malicious level file can still do, and say what the program should do instead.

<details>
<summary>Answer</summary>

It can loop forever, with `while true do end`, which freezes the game. It can also fill memory:
the string methods are still reachable through every string's metatable, so
`local s = ("x"):rep(1e9)` allocates a gigabyte. The program should store levels in a format that
is only data, such as CSV or JSON, and read them with a parser that never runs them. Module 14
shows how to limit a chunk that must run, with a hook that counts instructions.
</details>

### Exercise 10.7 (LO-10.3, ★★, about 15 minutes)

A game saves each score as `string.pack(">I4 s1", score, name)`.

1. How many bytes does `string.pack(">I4 s1", 1000, "Ada")` take?
2. Write `read_score(data)`, which returns the score and the name, or `nil` and a message when the
   data is too short, without raising an error.
3. A file holds many of these records, one after another. How does a reader find where the second
   one starts?

<details>
<summary>Hint</summary>

`string.unpack` raises an error on data that is too short, and its last result is a position.
</details>

<details>
<summary>Answer</summary>

1. 8: 4 bytes for the score, 1 for the name's length, and 3 for "Ada".
2. Catch the error with `pcall`, which also passes on every result of `unpack`:

   ```lua
   local function read_score(data)
     local ok, score, name = pcall(string.unpack, ">I4 s1", data)
     if not ok then return nil, score end   -- on failure, score holds the message
     return score, name
   end
   ```

   With the first 6 bytes of a record, it returns `nil` and
   `bad argument #2 to 'string.unpack' (data string too short)`.
3. `string.unpack(">I4 s1", data)` returns the score, the name, and the position just after the
   record, 9 for the record above. Pass that position as the third argument of the next `unpack`.
</details>
