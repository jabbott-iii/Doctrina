# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: tags,-all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lab 10: Files, the operating system, and data
#
# **Objectives:** LO-10.1, LO-10.2, LO-10.3\
# **Prerequisites:** the [Module 10 reading](index.md) and [Lab 9](../09-coroutines/lab09.ipynb)\
# **Time:** about 2 hours
#
# You will write a helper that always closes its file, a CSV parser and writer that handle quoted
# fields, a reader that turns a CSV file into records and reports bad lines, a serializer whose
# output reads back safely, and a shell quoter and a date calculator. As in the earlier labs, each
# check cell prints `passed` or fails with a message, and the checks fail until you finish their
# exercise. Section 5 runs commands through the shell, so it needs Linux or macOS.

# %% [markdown]
# ## Setup
#
# The lab writes its files into its `scratch` folder, which Git ignores. The second cell prints the
# Lua version, which should be `Lua 5.4`.

# %%
# %load_ext lualab
import os
import sys

import lupa

os.makedirs("scratch", exist_ok=True)
print("Python", sys.version.split()[0], "| lupa", lupa.__version__)

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. Closing on every path
#
# ### Exercise L10.1 (LO-10.1, ★★, about 20 minutes)
#
# Write `with_file(path, mode, fn)`. It opens `path` in `mode`; if that fails, it returns `nil` and
# `io.open`'s message. Otherwise it calls `fn(file)` and returns all of `fn`'s results. The file
# must be closed when `with_file` returns, and also when `fn` raises an error, which `with_file`
# lets through to its caller. Don't call `file:close()` yourself.
#
# <details>
# <summary>Hint</summary>
#
# Declare the handle with `<close>` after checking that `io.open` succeeded, and `return fn(file)`
# from the same scope.
# </details>

# %% tags=["answer-L10.1"] language="lua"
# function with_file(path, mode, fn)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local seen
# local ok = with_file("scratch/hello.txt", "w", function(f) seen = f; f:write("hello\n", 42, "\n") return true end)
# assert(ok == true and io.type(seen) == "closed file", "with_file should return fn's result and close the file")
# local line, number = with_file("scratch/hello.txt", "r", function(f) return f:read("l"), f:read("n") end)
# assert(line == "hello" and number == 42, "with_file should return every result of fn")
# local caught
# local passed, err = pcall(with_file, "scratch/hello.txt", "r", function(f) caught = f; error("reader failed", 0) end)
# assert(not passed and err == "reader failed", "an error in fn must reach the caller unchanged")
# assert(io.type(caught) == "closed file", "the file must be closed even when fn raises an error")
# local missing, message = with_file("scratch/no/such/file.txt", "r", function() error("must not run") end)
# assert(missing == nil and message:find("No such file", 1, true), "a failed open gives nil and the message")
# print("passed")

# %% [markdown]
# ## 2. CSV
#
# ### Exercise L10.2 (LO-10.3, ★★★, about 30 minutes)
#
# Write two functions for lines of CSV without line breaks inside fields:
#
# - `csv_split(line)` returns a list of the fields of `line`. A field in double quotes may contain
#   commas, and a doubled double quote inside it stands for one double quote; the quotes around a
#   field aren't part of its value. An empty line has one empty field.
# - `csv_join(fields)` returns the line for a list of strings, putting a field in double quotes,
#   with its double quotes doubled, only if it contains a comma or a double quote.
#
# | Line | Fields |
# | :- | :- |
# | `a,b,c` | `a`, `b`, `c` |
# | `Ada,"London, UK",36` | `Ada`, `London, UK`, `36` |
# | `"said ""hi""",x` | `said "hi"`, `x` |
# | `,,` | three empty fields |
#
# <details>
# <summary>Hint 1</summary>
#
# Walk the line one character at a time with a flag that says whether you are inside quotes. A
# comma ends a field only outside quotes.
# </details>
#
# <details>
# <summary>Hint 2</summary>
#
# Inside quotes, a `"` followed by another `"` is one quote character, so skip ahead two characters;
# a `"` followed by anything else ends the quoted part.
# </details>

# %% tags=["answer-L10.2"] language="lua"
# function csv_split(line)
#   -- your code here
# end
#
# function csv_join(fields)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local function same(a, b)
#   if #a ~= #b then return false end
#   for i = 1, #a do if a[i] ~= b[i] then return false end end
#   return true
# end
# assert(same(csv_split("a,b,c"), { "a", "b", "c" }), "a,b,c has three fields")
# assert(same(csv_split('Ada,"London, UK",36'), { "Ada", "London, UK", "36" }), "a comma inside quotes")
# assert(same(csv_split('"said ""hi""",x'), { 'said "hi"', "x" }), "doubled quotes inside quotes")
# assert(same(csv_split(",,"), { "", "", "" }), ",, has three empty fields")
# assert(same(csv_split(""), { "" }), "an empty line has one empty field")
# assert(same(csv_split('"",x'), { "", "x" }), "an empty quoted field")
# assert(csv_join({ "a", "b" }) == "a,b", "plain fields need no quotes")
# assert(csv_join({ "London, UK", 'say "hi"', "" }) == '"London, UK","say ""hi""",',
#   "quote fields with commas or quotes, and double the quotes")
# for _, fields in ipairs({ { "x" }, { "", "" }, { 'a,"b"', "c,", '"' }, { "plain", "1,2,3" } }) do
#   assert(same(csv_split(csv_join(fields)), fields), "splitting a joined line must give the fields back")
# end
# print("passed")

# %% [markdown]
# ## 3. From a file to records
#
# The next cell writes a small CSV file whose first line names the columns. Line 4 has a field
# missing.

# %% language="lua"
# local f <close> = assert(io.open("scratch/people.csv", "w"))
# f:write('name,city,age\n', 'Ada,"London, UK",36\n', 'Bo,Oslo,25\n', 'Cy,Lima\n', 'Di,"Rome",41\n')

# %% [markdown]
# ### Exercise L10.3 (LO-10.1, LO-10.3, ★★, about 20 minutes)
#
# Write `read_records(path)`, which reads a CSV file whose first line names the columns, and returns
# a list of records, one table per line, keyed by the column names. Use your `csv_split`. A file
# is data from outside the program, so report problems by returning `nil` and a message, not by
# raising an error: `io.open`'s message if the file can't be opened, or
# `"line <n>: expected <k> fields, got <m>"` for the first line with the wrong number of fields,
# counting the header as line 1. Close the file on every path.

# %% tags=["answer-L10.3"] language="lua"
# function read_records(path)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local records, err = read_records("scratch/people.csv")
# assert(records == nil and err == "line 4: expected 3 fields, got 2",
#   "people.csv's line 4 has 2 fields; got " .. tostring(err))
# local f <close> = assert(io.open("scratch/good.csv", "w"))
# f:write('name,city,age\n', 'Ada,"London, UK",36\n', 'Bo,Oslo,25\n')
# f:close()
# local good = assert(read_records("scratch/good.csv"))
# assert(#good == 2 and good[1].city == "London, UK" and good[2].age == "25", "records keyed by column")
# local missing, message = read_records("scratch/none.csv")
# assert(missing == nil and message:find("No such file", 1, true), "a missing file gives nil and the message")
# print("passed")

# %% [markdown]
# ## 4. Writing Lua values, and reading them back
#
# ### Exercise L10.4 (LO-10.3, ★★, about 25 minutes)
#
# Write two functions:
#
# - `serialize(value)` returns a Lua chunk, `return …`, that rebuilds `value`: a string, a number,
#   a boolean, or a table whose keys are strings or numbers and whose values are any of these,
#   nested to any depth. Write every string and number with `%q`, and each table's keys in sorted
#   order, numbers before strings, so the same value always gives the same text.
# - `deserialize(text)` runs such a chunk with `load` in text mode and an empty environment, and
#   returns the value; if the chunk doesn't compile, or raises an error, it returns `nil` and the
#   message.
#
# <details>
# <summary>Hint</summary>
#
# Write a recursive helper that returns the literal for one value, and builds a table's literal as
# `{[key]=value,...}` from its sorted keys. Sort with a comparator that compares the keys' types
# first, then the keys.
# </details>

# %% tags=["answer-L10.4"] language="lua"
# function serialize(value)
#   -- your code here
# end
#
# function deserialize(text)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local function deep_equal(a, b)
#   if type(a) ~= "table" or type(b) ~= "table" then return a == b and math.type(a) == math.type(b) end
#   for k, v in pairs(a) do if not deep_equal(v, b[k]) then return false end end
#   for k in pairs(b) do if a[k] == nil then return false end end
#   return true
# end
# local value = { name = "Ada \"the first\"\n", age = 36, ratio = 0.1, tags = { "x", "y" },
#   nested = { deeper = { flag = false, [10] = math.mininteger } } }
# local text = serialize(value)
# assert(type(text) == "string" and text:sub(1, 7) == "return ", "serialize returns a chunk starting with return")
# assert(deep_equal(deserialize(text), value), "deserialize(serialize(v)) must equal v exactly, number types included")
# assert(serialize({ b = 1, a = 2, [2] = "x", [1] = "y" }) == serialize({ [1] = "y", a = 2, [2] = "x", b = 1 }),
#   "the same table must always give the same text")
# assert(deserialize(serialize("plain")) == "plain" and deserialize(serialize(-0.5)) == -0.5, "plain values too")
# local blocked, why = deserialize("return os.remove('x')")
# assert(blocked == nil and why:find("global 'os'", 1, true), "the chunk must not see any global")
# local binary, reason = deserialize(string.dump(function() return 1 end))
# assert(binary == nil and reason:find("binary chunk", 1, true), "binary chunks must be refused")
# assert(deserialize("return {") == nil, "a chunk that doesn't compile gives nil")
# print("passed")

# %% [markdown]
# ## 5. The shell and the clock
#
# Run the next cell. It builds a command from a "file name" that came from outside the program.
# The output of `echo INJECTED` shows that the shell ran a second command.

# %% language="lua"
# local name = "x; echo INJECTED"
# os.execute("echo counting " .. name)

# %% [markdown]
# ### Exercise L10.5 (LO-10.2, ★★, about 20 minutes)
#
# Write two functions:
#
# - `shell_quote(s)` returns `s` in single quotes for a Linux or macOS shell, with each single quote
#   inside it written as `'\''`, so that the shell reads the result as one plain word.
# - `days_between(from, to)` takes two dates written `YYYY-MM-DD` and returns the number of days
#   from `from` to `to`, as an integer, negative if `to` comes first. For a string that isn't a date
#   of that form, it returns `nil` and the message `"not a date: "` followed by the string. Make it
#   right across changes to and from daylight saving time.

# %% tags=["answer-L10.5"] language="lua"
# function shell_quote(s)
#   -- your code here
# end
#
# function days_between(from, to)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# for _, s in ipairs({ "plain", "two words", "it's", "x; echo INJECTED", "$(whoami) `id` \"q\" \\ *" }) do
#   os.execute("printf '%s' " .. shell_quote(s) .. " > scratch/quoted.txt")
#   local f <close> = assert(io.open("scratch/quoted.txt"))
#   local back = f:read("a")
#   assert(back == s, "the shell should get back exactly " .. s .. ", not " .. back)
# end
# assert(days_between("2026-11-16", "2026-11-23") == 7, "one week is 7 days")
# assert(math.type(days_between("2026-11-16", "2026-11-23")) == "integer", "the result is an integer")
# assert(days_between("2024-02-28", "2024-03-01") == 2, "2024 is a leap year")
# assert(days_between("2026-03-01", "2026-04-01") == 31, "across the change to daylight saving time")
# assert(days_between("2026-10-20", "2026-11-10") == 21, "across the change back")
# assert(days_between("2026-01-10", "2026-01-01") == -9, "earlier dates give negative counts")
# local bad, message = days_between("2026-1-5", "2026-01-06")
# assert(bad == nil and message == "not a date: 2026-1-5", "a malformed date gives nil and a message")
# print("passed")

# %% [markdown]
# ## Summary
#
# - A `<close>` handle is closed on every path out of its scope, errors included, so helpers like
#   `with_file` need no `close` of their own.
# - CSV needs a parser that tracks quotes; splitting on commas breaks quoted fields, and a reader
#   of outside data reports bad lines with `nil` and a message.
# - `%q` and sorted keys make a serializer whose output reads back exactly and always looks the
#   same; reading it back with `load` in text mode and an empty environment keeps it away from
#   every library, but it is still code.
# - Outside input reaches the shell only quoted, and date arithmetic stays exact with noon times and
#   whole days.
#
# Next, do the [Module 10 practice](practice.md).
