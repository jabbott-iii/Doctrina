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
# # Lab 6: Errors, modules, and tests
#
# **Objectives:** LO-6.1, LO-6.2, LO-6.3\
# **Prerequisites:** the [Module 6 reading](index.md),
# [Lab 5](../05-closures-and-iterators/lab05.ipynb), and busted, installed as
# [setting up](../../setup.md) describes\
# **Time:** about 2 hours
#
# You will sort the standard library's failures into errors and `nil` results, write a function
# that classifies any failure, turn a script full of globals into a module, and write busted tests
# for it. The last check grades your tests the way the reading suggests: it breaks the module in
# four ways, and your tests must catch every one. As in the earlier labs, each check cell prints
# `passed` or fails with a message, and the checks fail until you finish their exercise.

# %% [markdown]
# ## Setup
#
# Nothing in this lab is random. The first cell finds busted, which runs in a terminal process of
# its own, outside the notebook. If it prints `not found`, follow [setting up](../../setup.md)
# before section 3. The second cell prints the Lua version, which should be `Lua 5.4`.

# %%
# %load_ext lualab
import json
import os
import pathlib
import shutil
import subprocess
import sys

import lualab
import lupa

os.makedirs("scratch", exist_ok=True)  # the lab writes its module and tests here
BUSTED = pathlib.Path(sys.prefix) / "lua" / "bin" / "busted"  # where setting up installs it
if not BUSTED.exists():
    BUSTED = shutil.which("busted")
print("Python", sys.version.split()[0], "| lupa", lupa.__version__)
print("busted:", BUSTED or "not found")

# %% language="lua"
# print(_VERSION)

# %% [markdown]
# ## 1. Errors and `nil` results
#
# Run the next cell. It calls `check_age` from a chunk named `caller`, once with each error level,
# and prints the message `pcall` caught. Compare each message's position with the level that made
# it, then change a level and run it again.

# %% language="lua"
# function check_age(age, level)
#   if type(age) ~= "number" then
#     error("age must be a number", level)
#   end
#   return age
# end
#
# for _, level in ipairs({ 1, 2, 0 }) do
#   local call = load("local age = check_age('ten', " .. level .. ")", "=caller", "t")
#   print("level " .. level .. ":", select(2, pcall(call)))
# end

# %% [markdown]
# Level 1 names `cell:3`, the line in this cell that calls `error`. Level 2 names `caller:1`, the
# line that called `check_age`, which is the line to fix. Level 0 names no line.
#
# ### Exercise L6.1 (LO-6.1, ★, about 10 minutes)
#
# Each call below fails. Predict how: replace each `"?"` with `"error"` if it raises an error, or
# `"nil"` if it returns `nil`. Use the reading's rule: a mistake in the calling code raises an
# error, and an expected failure returns `nil`.

# %% tags=["answer-L6.1"] language="lua"
# failure_predictions = {
#   { [[tonumber("12abc")]],            "?" },
#   { [[math.floor("12abc")]],          "?" },
#   { [[io.open("no/such/file.txt")]],  "?" },
#   { [[string.rep("ab")]],             "?" },
#   { [[utf8.len("caf\xe9")]],          "?" },
#   { [[string.format("%d", 2.5)]],     "?" },
#   { [[os.remove("no/such/file.txt")]], "?" },
#   { [[require("no_such_module")]],    "?" },
# }

# %% tags=["raises-exception"] language="lua"
# local wrong, unanswered = 0, 0
# for n, row in ipairs(failure_predictions) do
#   local code, predicted = row[1], row[2]
#   local ok, result, message = pcall(load("return " .. code, "=call", "t"))
#   local actual = ok and "nil" or "error"
#   local detail = ok and tostring(message) or tostring(result):gsub("\n.*", " ...")
#   local verdict = "match"
#   if predicted == "?" then
#     unanswered, verdict = unanswered + 1, "no prediction yet"
#   elseif predicted ~= actual then
#     wrong, verdict = wrong + 1, "MISMATCH"
#   end
#   print(string.format("%d  %-30s you: %-6s Lua: %-6s %s", n, code, predicted, actual, verdict))
#   print("     " .. detail)
# end
# assert(unanswered == 0, unanswered .. " calls still have no prediction")
# assert(wrong == 0, wrong .. " predictions don't match; correct them and run both cells again")
# print("passed")

# %% [markdown]
# ### Exercise L6.2 (LO-6.1, ★★, about 15 minutes)
#
# Write `classify(fn, ...)`, which calls `fn` with the remaining arguments in protected mode and
# returns exactly two values that say how the call went:
#
# | The call… | `classify` returns |
# | :- | :- |
# | raised an error | `"error"` and the error value |
# | returned `nil` as its first result, or no results | `"failure"` and the second result, the message, if any |
# | returned anything else first, `false` included | `"ok"` and the first result |
#
# <details>
# <summary>Hint</summary>
#
# `table.pack(pcall(fn, ...))` keeps every result of the call, in order, after `pcall`'s own
# `true` or `false`.
# </details>

# %% tags=["answer-L6.2"] language="lua"
# function classify(fn, ...)
#   -- your code here
# end

# %% tags=["raises-exception"] language="lua"
# local kind, value = classify(math.floor, 2.7)
# assert(kind == "ok" and value == 2, "math.floor(2.7) succeeds with 2")
# kind, value = classify(math.floor, "x")
# assert(kind == "error" and value:find("number expected"), "math.floor('x') raises an error")
# kind, value = classify(io.open, "no/such/file.txt")
# assert(kind == "failure" and value:find("No such file"), "io.open of a missing file fails with a message")
# kind, value = classify(tonumber, "abc")
# assert(kind == "failure" and value == nil, "tonumber('abc') fails without a message")
# kind, value = classify(error, { code = 7 })
# assert(kind == "error" and type(value) == "table" and value.code == 7, "an error value can be a table")
# kind, value = classify(function() return false end)
# assert(kind == "ok" and value == false, "false is a result, not a failure")
# kind, value = classify(function(a, b) return a + b end, 2, 3)
# assert(kind == "ok" and value == 5, "classify passes the arguments on")
# assert(classify(function() end) == "failure", "no results count as a failure")
# assert(select("#", classify(tonumber, "abc")) == 2, "classify returns exactly two values")
# print("passed")

# %% [markdown]
# `pcall` loses the stack the error came from; `xpcall` with `debug.traceback` keeps it. Run this
# cell and read the traceback from the top: the first line is the error, and the lines under it are
# the calls that led there, innermost first. The last two lines belong to lualab, which runs each
# cell inside an `xpcall` of its own; in a script run with `lua`, the list ends with the main
# chunk and `[C]: in ?`.

# %% language="lua"
# local function inner() local settings = nil; return settings.width end
# local function outer() return inner() + 1 end
# print(pcall(outer))
# print(xpcall(outer, debug.traceback))

# %% [markdown]
# ## 2. From a script to a module
#
# This script reads sensor readings, one `name=value` per line, and prints how many were good,
# their mean, and how many lines were bad. It works, but every variable is global, and nothing in
# it can be reused or tested. Run it.

# %% language="lua"
# text = [[
# kitchen=21.5
# hall=19
# garage=cold
# attic=24.25
# ]]
# values = {}
# bad = 0
# for line in text:gmatch("[^\n]+") do
#   name, value = line:match("^([%w_]+)=(.+)$")
#   value = tonumber(value)
#   if value then values[#values + 1] = value else bad = bad + 1 end
# end
# total = 0
# for _, v in ipairs(values) do total = total + v end
# print(#values, total / #values, bad)

# %% [markdown]
# ### Exercise L6.3 (LO-6.2, LO-6.1, ★★, about 30 minutes)
#
# Turn the script into the module `scratch/readings.lua`, by finishing the cell below. Running the
# cell writes the file. The module creates no globals, and returns a table with three functions:
#
# - `readings.parse_line(line)` returns the name and the value of a line `name=value`, where the
#   name is letters, digits, and underscores, and the value is a number. For any other line, it
#   returns `nil` and the message `"bad line: "` followed by the line.
# - `readings.mean(values)` returns the mean of a non-empty sequence of numbers. If `values` is
#   empty or isn't a table, it raises the error `"mean: expected a non-empty list"` at level 2.
# - `readings.summary(text)` returns a table `{ count = …, mean = …, bad = … }` for the non-empty
#   lines of `text`: the number of good lines, their mean, and the number of bad lines. When no
#   line is good, `mean` is `nil`, and `summary` raises no error.
#
# Which kind of failure should each function report, and why? The statement chooses for you; make
# sure you can say why.
#
# <details>
# <summary>Hint</summary>
#
# Have `summary` call `readings.parse_line` and `readings.mean`, so that each rule lives in one
# place. Check for an empty list before calling `mean`.
# </details>

# %% tags=["answer-L6.3"]
# %%writefile scratch/readings.lua
-- readings.lua: parse sensor readings and summarize them.
local readings = {}

function readings.parse_line(line)
  error("not implemented")
end

function readings.mean(values)
  error("not implemented")
end

function readings.summary(text)
  error("not implemented")
end

return readings

# %% [markdown]
# The check adds `./scratch/?.lua` to `package.path`, so that `require("readings")` finds your file,
# and clears `package.loaded.readings`, so that it loads the file as it is now. When you change the
# module, run its cell again to rewrite the file, then run the check.

# %% tags=["raises-exception"] language="lua"
# package.path = "./scratch/?.lua;" .. package.path
# package.loaded.readings = nil
# -- Clear the script's globals, so that any global the module creates shows up at the end.
# text, values, bad, name, value, total = nil, nil, nil, nil, nil, nil
# local before = {}
# for k in pairs(_G) do before[k] = true end
# local readings, where = require("readings")
# assert(type(readings) == "table", "the module must return a table")
# assert(where == "./scratch/readings.lua", "require should have loaded ./scratch/readings.lua")
# assert(require("readings") == readings and package.loaded.readings == readings,
#   "a second require should return the same table, from package.loaded")
#
# local name, value = readings.parse_line("kitchen=21.5")
# assert(name == "kitchen" and value == 21.5, "parse_line('kitchen=21.5') should give 'kitchen', 21.5")
# assert(math.type(select(2, readings.parse_line("hall=19"))) == "integer", "keep 19 an integer")
# local bad_name, message = readings.parse_line("garage=cold")
# assert(bad_name == nil and message == "bad line: garage=cold",
#   "parse_line('garage=cold') should return nil and 'bad line: garage=cold'")
# assert(readings.parse_line("=5") == nil and readings.parse_line("x=") == nil, "both parts are required")
#
# assert(readings.mean({ 1, 2, 3, 4 }) == 2.5, "mean({ 1, 2, 3, 4 }) should be 2.5")
# for _, arg in ipairs({ "{}", "'x'" }) do
#   local ok, err = pcall(load("local readings = require('readings')\nreadings.mean(" .. arg .. ")",
#     "=caller", "t"))
#   assert(not ok and err == "caller:2: mean: expected a non-empty list",
#     "mean(" .. arg .. ") should raise 'mean: expected a non-empty list' at level 2, naming the " ..
#     "caller's line; it raised " .. tostring(err))
# end
#
# local s = readings.summary("kitchen=21.5\nhall=19\ngarage=cold\nattic=24.25\n")
# assert(s.count == 3 and s.bad == 1, "summary should count 3 good lines and 1 bad one")
# assert(math.abs(s.mean - 64.75 / 3) < 1e-12, "summary's mean of the good lines should be 21.58...")
# local none = readings.summary("a=b\n")
# assert(none.count == 0 and none.bad == 1 and none.mean == nil, "no good lines: count 0, mean nil")
# local empty = readings.summary("")
# assert(empty.count == 0 and empty.bad == 0 and empty.mean == nil, "empty text: all zero, mean nil")
# for k in pairs(_G) do
#   assert(before[k], "the module created the global '" .. tostring(k) .. "'; make it local")
# end
# print("passed")

# %% [markdown]
# Two more things to try before you go on. The next cell asks Lua where it would find the module,
# without loading it, then lists the module's functions. Change the module's cell, for example by
# adding a `print` at its top, rerun that cell, and run this one twice: once as it is, and once
# after uncommenting the line that clears the cache. Only the second run shows your `print`.

# %% language="lua"
# print(package.searchpath("readings", package.path))
# -- package.loaded.readings = nil
# local readings = require("readings")
# for name in pairs(readings) do print(name) end

# %% [markdown]
# ## 3. Tests with busted
#
# ### Exercise L6.4 (LO-6.3, ★★★, about 35 minutes)
#
# Finish the spec file `scratch/readings_spec.lua` in the cell below, and run the cell to write it.
# The first test is done for you. Add tests until every promise in Exercise L6.3's statement is
# tested: each function's normal results, the edges, and each failure, with its message.
#
# The check runs your tests twice over. First against your module, where every test must pass.
# Then against four broken versions of it, each made by wrapping your module and changing one
# behavior; for each one, at least one of your tests must fail. The check names the broken
# versions your tests miss, but not how they are broken: work that out from what your tests
# don't yet check.
#
# <details>
# <summary>Hint</summary>
#
# Go through the statement of Exercise L6.3 sentence by sentence. Each sentence that says what a
# function returns or raises needs a test. `assert.has_error(function() … end, "message")` tests
# an error, and `assert.are.same` compares whole tables.
# </details>

# %% tags=["answer-L6.4"]
# %%writefile scratch/readings_spec.lua
local readings = require("readings")

describe("readings.parse_line", function()
  it("reads a name and a value", function()
    local name, value = readings.parse_line("kitchen=21.5")
    assert.are.equal("kitchen", name)
    assert.are.equal(21.5, value)
  end)

  -- your tests here
end)

# %% [markdown]
# Run your tests on your module, and read busted's report:

# %%
if BUSTED:
    report = subprocess.run(
        [str(BUSTED), "-o", "plainTerminal", "--lpath=scratch/?.lua", "scratch/readings_spec.lua"],
        capture_output=True,
        text=True,
    )
    print(report.stdout, report.stderr)
else:
    print("busted wasn't found; install it as setting up describes, then rerun the setup cell")

# %% [markdown]
# The check writes the four broken versions to `scratch/broken/`, runs your tests against each
# one, and reports which your tests caught.

# %% tags=["raises-exception"]
BROKEN = {
    "parse_line": """
local M = dofile("scratch/readings.lua")
local real = M.parse_line
function M.parse_line(line)
  local name, value = real(line)
  if name == nil then return "?", 0 end
  return name, value
end
return M
""",
    "mean_errors": """
local M = dofile("scratch/readings.lua")
local real = M.mean
function M.mean(values)
  if type(values) == "table" and #values == 0 then return 0 end
  return real(values)
end
return M
""",
    "mean_values": """
local M = dofile("scratch/readings.lua")
local real = M.mean
function M.mean(values)
  return real(values) + 1
end
return M
""",
    "summary": """
local M = dofile("scratch/readings.lua")
local real = M.summary
function M.summary(text)
  local s = real(text)
  s.count = s.count + s.bad
  return s
end
return M
""",
}


def run_spec(lpath):
    result = subprocess.run(
        [str(BUSTED), "-o", "json", f"--lpath={lpath}", "scratch/readings_spec.lua"],
        capture_output=True,
        text=True,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise AssertionError(f"busted couldn't run the spec:\n{result.stdout}{result.stderr}")


assert BUSTED, "busted wasn't found; install it as setting up describes, then rerun the setup cell"
own = run_spec("scratch/?.lua")
total = len(own["successes"]) + len(own["failures"]) + len(own["errors"])
print(f"your module: {len(own['successes'])} of {total} tests pass")
assert not own["failures"] and not own["errors"], "every test must pass on your module first"
missed = []
for name, source in BROKEN.items():
    folder = pathlib.Path("scratch/broken") / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "readings.lua").write_text(source)
    result = run_spec(f"{folder}/?.lua")
    caught = bool(result["failures"] or result["errors"])
    print(f"broken version '{name}':", "caught" if caught else "MISSED: no test failed")
    if not caught:
        missed.append(name)
assert not missed, f"your tests miss {len(missed)} broken version(s): {', '.join(missed)}"
print("passed")

# %% [markdown]
# ## Summary
#
# - The standard library raises errors for mistakes in the calling code and returns `nil` for
#   failures the caller should expect, and `classify` can tell the two apart with `pcall`.
# - `error(msg, 2)` names the caller's line, which is the line to fix.
# - A module is a file that returns a table and creates no globals; `require` finds it through
#   `package.path` and keeps it in `package.loaded`, so a changed file needs the cache cleared.
# - busted runs `describe` and `it` blocks. A test suite is good when breaking the code makes it
#   fail: tests of the normal case alone missed some of the broken versions.
#
# Next, do the [Module 6 practice](practice.md), then finish PA3.
