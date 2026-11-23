# PA5: A command-line tool

**Objectives:** LO-10.1, LO-10.3, LO-11.1, LO-11.2, LO-11.3, LO-11.4, and, revisited, LO-4.2,
LO-6.1, and LO-8.1\
**Due:** week 12, as the [schedule](../../README.md#schedule) gives it\
**Weight:** 9% of the course grade: 70 points from hidden tests, and 30 from the rubric below\
**Time:** about 6 hours, spread over modules 11 and 12

You will build `csvstats`, a rock that installs a command of the same name. Given a CSV file, the
command prints one line of statistics for each column. For the starter's sample file,

```bash
csvstats data/sample.csv
```

prints:

```text
city: text, 4 values, 0 missing, 3 distinct, most common Oslo
temp: number, 4 values, 0 missing, min -2, max 19, mean 8.88
note: text, 3 values, 1 missing, 3 distinct, most common cold
```

The code is small; the point is the project around it. It is packaged as a rock with a rockspec,
passes luacheck and StyLua with no findings, documents its interface with LuaCATS annotations that
lua-language-server checks, and comes with tests whose coverage you measure.

## What to hand in

Submit the whole project folder through the learning management system, without `lua_modules/`:

- `csvstats-1.0-1.rockspec`, which you write;
- `src/csvstats.lua`, the module, with its second line saying which tools you used, and how, or
  "none", and its third line naming everyone you discussed the assignment with, or "no one";
- `bin/csvstats`, the command;
- `spec/`, your tests, and `luacov.report.out`, your last coverage report;
- `.luacheckrc`, `stylua.toml`, and `.luacov`, which the starter provides and you shouldn't need
  to change.

## Getting started

1. Copy this folder, `assignments/pa5/`, to a folder of your own, and run
   `source .venv/lua/bin/activate` from the repository's root, as [setting up](../../setup.md)
   describes. You also need StyLua and lua-language-server from setting up. The folder holds the
   stubs [`src/csvstats.lua`](src/csvstats.lua) and `bin/csvstats`, two example tests in
   [`spec/csvstats_spec.lua`](spec/csvstats_spec.lua), the sample file
   [`data/sample.csv`](data/sample.csv), and the tools' settings in `.luacheckrc`,
   [`stylua.toml`](stylua.toml), and `.luacov`. The website offers the linked files for download;
   copy the others from the course's repository.
2. From your copy, run the tests with `busted --lpath=./src/?.lua`. They fail until you write the
   module. Run the command, before it is installed, with
   `LUA_PATH='./src/?.lua;;' lua bin/csvstats data/sample.csv`.
3. Write the rockspec, and install the rock into a tree of the project's own with
   `luarocks --tree lua_modules make`. Then `lua_modules/bin/csvstats data/sample.csv` runs the
   installed command.

## The module

`src/csvstats.lua` returns a table with these functions and one class. Annotate each of them, and
the class and its fields, with LuaCATS.

### `csvstats.split_line(line)`

Returns the list of fields of one line of CSV, as Lab 10's `csv_split` does: a field in double
quotes may contain commas, a doubled double quote inside it stands for one double quote, and the
quotes around a field aren't part of it. An empty line has one empty field.

### `csvstats.read(path)`

Reads a CSV file whose first line that isn't empty names the columns, and returns the list of
column names and the list of rows, each a list of fields. Empty lines are skipped. A file is data
from outside the program, so problems are reported by returning `nil` and a message, never by
raising an error:

| Problem | Message |
| :- | :- |
| The file can't be opened | `io.open`'s message, such as `data.csv: No such file or directory` |
| The file has no line that isn't empty | `<path>: no header line` |
| A row has a different number of fields from the header | `<path>:<n>: expected <k> fields, got <m>`, for the first such row, where `<n>` counts every line of the file, empty lines included, from 1 |

Close the file on every path, with `<close>`.

### `csvstats.Column`

A class, with its methods in `csvstats.Column`:

- `Column.new(name)` returns an empty column.
- `column:add(text)` adds one field. An empty field counts as missing; any other field is a value.
- `column:summary()` returns a table with the fields `name`, `kind`, `count` (the number of
  values), and `missing` (the number of empty fields), and depending on the kind:
  - `kind = "number"` when every value is a number, as `tonumber` reads it, with `min`, `max`, and
    `mean`, the mean as a float;
  - `kind = "text"` when there is at least one value and not every value is a number, with
    `distinct`, the number of different values as written (so `1` and `1.0` are different), and
    `top`, the most common value, the alphabetically first among those that tie;
  - `kind = "empty"` when there are no values.

### `csvstats.analyze(header, rows)` and `csvstats.format(summaries)`

`analyze` returns the summary of each column, in the order of `header`. `format` returns one line
for each summary, joined with newlines, with no newline at the end:

| Kind | Line |
| :- | :- |
| `number` | `<name>: number, <count> values, <missing> missing, min <min>, max <max>, mean <mean>` |
| `text` | `<name>: text, <count> values, <missing> missing, <distinct> distinct, most common <top>` |
| `empty` | `<name>: empty, 0 values, <missing> missing` |

Write `min` and `max` with `string.format("%g", …)`, and `mean` with `"%.2f"`.

## The command

`bin/csvstats` takes exactly one argument, the path of a CSV file:

| Situation | Standard output | Standard error | Exit status |
| :- | :- | :- | :- |
| The report succeeds | The report, followed by a newline | Nothing | 0 |
| Not exactly one argument | Nothing | `usage: csvstats FILE.csv` and a newline | 2 |
| `csvstats.read` returns `nil` and a message | Nothing | `csvstats: ` followed by the message, and a newline | 1 |

Use `io.stderr:write` for errors and `os.exit(status)` for the status. The script loads the module
with `require("csvstats")`.

## The rockspec

Write `csvstats-1.0-1.rockspec`, version 1.0, revision 1, with a `source.url` of your choice, a
`description` with a `summary` and a `license`, a dependency on Lua 5.4, and a `builtin` build that
maps the module `csvstats` to `src/csvstats.lua` and installs `bin/csvstats` as a command. The
[rockspec format](https://github.com/luarocks/luarocks/blob/main/docs/rockspec_format.md) documents
`build.install.bin`, the field for commands. `luarocks lint` must accept it, and
`luarocks --tree lua_modules make` must build it.

## Your tests

Write tests for every promise in this handout, the command's included. To run the command from a
test and capture what it prints, redirect its output to temporary files:

```lua
local out, err = os.tmpname(), os.tmpname()
local _, _, status = os.execute(
  "LUA_PATH='./src/?.lua;;' lua bin/csvstats data/sample.csv > " .. out .. " 2> " .. err
)
```

Then read both files, and remove them. Measure coverage with `busted --coverage --lpath=./src/?.lua`
and `luacov`, and add tests for every line the report marks as never run. As in PA3 and PA4, the
grader runs your tests against a correct project and against 10 versions of it that each break one
promise in this handout.

## How it is graded

### Hidden tests: 70 points

| Part | Points |
| :- | :- |
| `csvstats.split_line` | 8 |
| `csvstats.read` | 14 |
| `csvstats.Column` | 18 |
| `csvstats.analyze` and `csvstats.format` | 14 |
| The command | 16 |

### Rubric: 30 points

| Criterion | Full marks | Partial | Little or none |
| :- | :- | :- | :- |
| **Tests** (10) | Every test passes on a correct project, the tests catch at least 9 of the 10 broken versions, and your coverage report shows no line of `src/csvstats.lua` that never ran: 10 points | 7–8 caught: 7 points; 4–6: 4 points; 1–3: 1 point; lines never run cost 1 point each, up to 3 | No tests, or none that catch a broken version: 0 points. Each test that fails on a correct project costs 2 points |
| **Package and tools** (10) | `luarocks lint` accepts the rockspec, `luarocks make` builds it, and luacheck, `stylua --check`, and lua-language-server report nothing, with no warning silenced except a named one on its line, for a reason given in a comment. Every public function and the class are annotated: 10 points | Each tool that reports something, or each part without annotations, costs 2 points | A rockspec that doesn't build: 4 points or fewer |
| **Design and style** (10) | `Column` keeps its methods in the class; `read` reports failures with `nil` and a message and closes its file with `<close>`; the command does only argument handling and printing; descriptive names, a comment wherever the reason for the code isn't obvious, and no dead code | Works, but with repeated code or mixed responsibilities: 6 points | Hard to follow, or errors raised where the handout asks for `nil` and a message: 3 points or fewer |

## Policies

The course's [policies](../../README.md#policies) apply. Late work uses your grace days, then
loses 10% a day for up to three days. Discuss ideas with anyone, but write your own code and
tests, and name everyone you discussed the assignment with on the third line of
`src/csvstats.lua`. Generative AI tools may explain concepts and error messages to you, but may not
write any part of the project; say on the second line of `src/csvstats.lua` which tools you used,
and how, or write "none".
