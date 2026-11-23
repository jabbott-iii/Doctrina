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
# # Lab 11: Packages and tooling
#
# **Objectives:** LO-11.1, LO-11.2, LO-11.3, LO-11.4\
# **Prerequisites:** the [Module 11 reading](index.md), and LuaRocks, busted, luacheck, LuaCov,
# StyLua, and lua-language-server, installed as [setting up](../../setup.md) describes\
# **Time:** about 2 hours
#
# This lab works on files, not notebook cells: each exercise writes Lua files into the lab's
# `scratch/project` folder, and Python cells run the community's tools on them, as you would in a
# terminal. You will write a rockspec and build two rocks into a project tree, clean up a module
# until luacheck and StyLua have nothing to say, annotate a module so that lua-language-server
# catches the mistakes in its caller, and add tests until LuaCov finds no line they skip. As in
# the earlier labs, each check cell prints `passed` or fails with a message.

# %% [markdown]
# ## Setup
#
# The first cell finds the tools and defines `run`, which runs one in a project folder and returns
# its exit status and output. If any tool shows `NOT FOUND`, install it as setting up describes,
# then run the cell again. The second cell writes the files the exercises start from, replacing
# any earlier copies, so run it again whenever you want to start over.

# %%
# %load_ext lualab
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

import lupa

PROJECT = pathlib.Path("scratch/project").resolve()
LUA_BIN = pathlib.Path(sys.prefix) / "lua" / "bin"


def find(name, *folders):
    for folder in (LUA_BIN, *folders):
        if (pathlib.Path(folder) / name).exists():
            return str(pathlib.Path(folder) / name)
    return shutil.which(name)


TOOLS = {
    "lua": find("lua"),
    "luarocks": find("luarocks"),
    "luacheck": find("luacheck"),
    "busted": find("busted"),
    "luacov": find("luacov"),
    "stylua": find("stylua", pathlib.Path.home() / ".cargo" / "bin"),
    "lua-language-server": find("lua-language-server", pathlib.Path(sys.prefix) / "luals" / "bin"),
}
ENV = dict(os.environ, PATH=f"{LUA_BIN}{os.pathsep}{os.environ['PATH']}")


def run(tool, *args, folder):
    """Runs a tool in a folder of the project; returns its exit status and its output."""
    result = subprocess.run([TOOLS[tool], *args], cwd=PROJECT / folder, env=ENV,
                            capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


print("Python", sys.version.split()[0], "| lupa", lupa.__version__)
for name, path in TOOLS.items():
    print(f"{name:20} {path or 'NOT FOUND'}")

# %%
FILES = {
    "textutil/textutil-0.1-1.rockspec": """\
package = "textutil"
version = "0.1-1"
source = { url = "git+https://example.org/textutil.git" }
description = { summary = "Splits text into words.", license = "MIT" }
dependencies = { "lua >= 5.4" }
build = { type = "builtin", modules = { textutil = "src/textutil.lua" } }
""",
    "textutil/src/textutil.lua": """\
local textutil = {}

function textutil.words(text)
  local words = {}
  for word in text:lower():gmatch("%a+") do
    words[#words + 1] = word
  end
  return words
end

return textutil
""",
    "wordfreq/src/wordfreq.lua": """\
local textutil = require("textutil")
local wordfreq = {}

function wordfreq.top(text, n)
  local counts = {}
  for _, word in ipairs(textutil.words(text)) do
    counts[word] = (counts[word] or 0) + 1
  end
  local list = {}
  for word, count in pairs(counts) do
    list[#list + 1] = { word = word, count = count }
  end
  table.sort(list, function(a, b)
    if a.count ~= b.count then
      return a.count > b.count
    end
    return a.word < b.word
  end)
  return { table.unpack(list, 1, math.min(n, #list)) }
end

return wordfreq
""",
    "stats/.luacheckrc": 'std = "lua54"\nfiles["spec"] = { std = "+busted" }\n',
    "stats/stylua.toml": 'syntax = "Lua54"\nindent_type = "Spaces"\nindent_width = 2\ncolumn_width = 100\n',
    "stats/spec/stats_spec.lua": """\
local stats = require("stats")

describe("stats", function()
  it("averages a list", function()
    assert.are.equal(2.0, stats.mean({ 1, 2, 3 }))
  end)

  it("finds the largest item", function()
    assert.are.equal(9, stats.max({ 3, 9, 4 }))
  end)
end)
""",
    "shapes/caller.lua": """\
local shapes = require("shapes")
local box = shapes.rect(3, 4)
local doubled = shapes.scale(box, "2")
print(shapes.area(doubled), shapes.area(12))
""",
    "grades/.luacov": 'return { include = { "src/grades" } }\n',
    "grades/src/grades.lua": """\
local grades = {}

function grades.letter(score)
  if type(score) ~= "number" or score < 0 or score > 100 then
    error("score must be a number from 0 to 100", 2)
  end
  if score >= 90 then
    return "A"
  elseif score >= 80 then
    return "B"
  elseif score >= 70 then
    return "C"
  end
  return "F"
end

function grades.summary(scores)
  local counts = { A = 0, B = 0, C = 0, F = 0 }
  for _, score in ipairs(scores) do
    local letter = grades.letter(score)
    counts[letter] = counts[letter] + 1
  end
  return counts
end

return grades
""",
}
shutil.rmtree(PROJECT, ignore_errors=True)
for name, text in FILES.items():
    path = PROJECT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
for folder in ("stats/src", "grades/spec"):  # for the files the exercises' cells write
    (PROJECT / folder).mkdir(parents=True, exist_ok=True)
print("wrote", len(FILES), "files under", PROJECT.relative_to(pathlib.Path.cwd()))

# %% [markdown]
# ## 1. A rockspec, and a tree for the project
#
# `textutil` is a finished rock. `wordfreq` uses it, and needs a rockspec.
#
# ### Exercise L11.1 (LO-11.1, ★★, about 25 minutes)
#
# Finish the rockspec for `wordfreq`, version 0.1, rockspec revision 1. It needs the fields
# `package`, `version`, `source` (any `url`; nothing fetches it here), `description` with a
# `summary` and a `license`, `dependencies` on Lua 5.4 and on `textutil` version 0.1 or later, and a
# `builtin` build that maps the module `wordfreq` to `src/wordfreq.lua`. Run the cell to write the
# file, then run the two checks.

# %% tags=["answer-L11.1"]
# %%writefile scratch/project/wordfreq/wordfreq-0.1-1.rockspec
package = "wordfreq"
-- your fields here

# %% [markdown]
# The first check reads the rockspec as Lua, in an empty environment, and looks at its fields.

# %% tags=["raises-exception"] language="lua"
# local spec = {}
# local chunk = assert(loadfile("scratch/project/wordfreq/wordfreq-0.1-1.rockspec", "t", spec))
# chunk()
# assert(spec.package == "wordfreq" and spec.version == "0.1-1", "package and version: wordfreq, 0.1-1")
# assert(type(spec.description) == "table" and spec.description.license and spec.description.summary,
#   "description needs a summary and a license")
# local deps = table.concat(spec.dependencies or {}, ", ")
# assert(deps:find("^lua >= 5%.4") or deps:find(", lua >= 5%.4"), "depend on lua >= 5.4; got: " .. deps)
# assert(deps:find("textutil >= 0%.1"), "depend on textutil >= 0.1; got: " .. deps)
# assert(spec.build and spec.build.type == "builtin" and spec.build.modules
#   and spec.build.modules.wordfreq == "src/wordfreq.lua", "build wordfreq from src/wordfreq.lua")
# print("passed")

# %% [markdown]
# The second check lints the rockspec, builds `textutil` and then `wordfreq` into the project's
# tree, `scratch/project/lua_modules`, and runs the installed module with `lua`.

# %% tags=["raises-exception"]
status, output = run("luarocks", "lint", "wordfreq-0.1-1.rockspec", folder="wordfreq")
assert status == 0, "luarocks lint failed:\n" + output
for rock in ("textutil", "wordfreq"):
    status, output = run("luarocks", "--tree", "../lua_modules", "make", folder=rock)
    assert status == 0, f"building {rock} failed:\n{output}"
    print(output.strip().splitlines()[-1])
status, output = run("lua", "-e", 'package.path = "lua_modules/share/lua/5.4/?.lua;" .. package.path '
                     'print(require("wordfreq").top("b a b c b a", 2)[2].word)', folder=".")
assert status == 0 and output.strip() == "a", "the installed wordfreq should work:\n" + output
print("passed")

# %% [markdown]
# ## 2. Lint and layout
#
# `stats.lua` below works for `mean`, but luacheck has eight findings, StyLua would change its
# layout, and one of busted's two tests in `spec/stats_spec.lua` fails. Run the cell, and the cell
# after it, which runs all three tools and prints what they say.

# %% tags=["answer-L11.2"]
# %%writefile scratch/project/stats/src/stats.lua
local stats = {}
local unused_limit = 100

function stats.mean(list)
  total = 0
  for i, v in ipairs(list) do total = total + v end
  return total / #list
end

function stats.max(list)
  local best = list[1]
  for _, v in ipairs(list) do
    local best = math.max(best, v)
  end
  return best
end

return stats

# %%
for tool, args in (("luacheck", ["--no-color", "src", "spec"]),
                   ("stylua", ["--check", "src", "spec"]),
                   ("busted", ["-o", "plainTerminal", "--lpath=./src/?.lua"])):
    status, output = run(tool, *args, folder="stats")
    print(f"--- {tool}: exit status {status}\n{output}")

# %% [markdown]
# ### Exercise L11.2 (LO-11.2, ★★, about 30 minutes)
#
# Fix every luacheck finding in `stats.lua` by changing the code, not by silencing luacheck:
# no `luacheck:` comment and no change to `.luacheckrc`. One finding is the cause of the failing
# test. Then run the next cell, which lets StyLua lay the file out, and run the check. Rewrite the
# `%%writefile` cell above, not the file: running that cell again replaces the file, so run the
# StyLua cell after it each time.

# %%
status, output = run("stylua", "src", "spec", folder="stats")
print("stylua exit status", status, output)

# %% tags=["raises-exception"]
source = (PROJECT / "stats/src/stats.lua").read_text()
assert "luacheck:" not in source, "fix the findings instead of silencing luacheck"
status, output = run("luacheck", "--no-color", "src", "spec", folder="stats")
assert status == 0, "luacheck still has findings:\n" + output
status, output = run("stylua", "--check", "src", "spec", folder="stats")
assert status == 0, "StyLua would still change the layout:\n" + output
status, output = run("busted", "-o", "plainTerminal", "--lpath=./src/?.lua", folder="stats")
assert status == 0, "the tests should pass:\n" + output
print("passed")

# %% [markdown]
# ## 3. Types the checker can see
#
# `shapes/caller.lua` makes two mistakes: it scales by the string `"2"`, and asks for the area of a
# number. Run the next cell, which writes `shapes.lua` without annotations, and the cell after it,
# which runs lua-language-server on the folder. It finds nothing, because nothing says what types
# the functions expect.

# %% tags=["answer-L11.3"]
# %%writefile scratch/project/shapes/shapes.lua
local shapes = {}

function shapes.rect(width, height)
  return { width = width, height = height }
end

function shapes.area(rect)
  return rect.width * rect.height
end

function shapes.scale(rect, factor)
  return shapes.rect(rect.width * factor, rect.height * factor)
end

return shapes


# %%
def check_types(folder):
    """Runs lua-language-server on a folder; returns (file, line, code) for each problem."""
    report = PROJECT / "luals-report.json"
    report.unlink(missing_ok=True)
    run("lua-language-server", f"--check={PROJECT / folder}", "--checklevel=Warning",
        "--check_format=json", f"--check_out_path={report}",
        f"--logpath={PROJECT / 'luals-log'}", folder=folder)
    found = json.loads(report.read_text()) if report.exists() and report.stat().st_size > 2 else {}
    return sorted((uri.rsplit("/", 1)[-1], item["range"]["start"]["line"] + 1, item["code"])
                  for uri, items in found.items() for item in items)


print(check_types("shapes") or "no problems found")

# %% [markdown]
# ### Exercise L11.3 (LO-11.3, ★★, about 25 minutes)
#
# Annotate `shapes.lua` with LuaCATS: a class `Rect` with number fields `width` and `height`, and
# `@param` and `@return` annotations for all three functions, with a one-line description of each.
# Then run both cells again. The checker should report the two mistakes in `caller.lua`, on lines 3
# and 4, and nothing in `shapes.lua`. Don't change `caller.lua`.
#
# <details>
# <summary>Hint</summary>
#
# A class is declared in comments: `---@class Rect`, then one `---@field` line per field. After
# that, `---@param rect Rect` and `---@return Rect` can name it.
# </details>

# %% tags=["raises-exception"]
problems = check_types("shapes")
print(problems)
assert ("caller.lua", 3, "param-type-mismatch") in problems, "the checker should catch line 3's \"2\""
assert ("caller.lua", 4, "param-type-mismatch") in problems, "the checker should catch area(12) on line 4"
assert not [p for p in problems if p[0] == "shapes.lua"], "shapes.lua itself should have no problems"
source = (PROJECT / "shapes/shapes.lua").read_text()
assert source.count("---@return") >= 3 and "---@class Rect" in source, "annotate all three functions"
print("passed")

# %% [markdown]
# ## 4. Coverage
#
# `grades.lua` turns scores into letter grades, and raises an error for a score out of range. The
# spec below tests only two cases. Run it, then the cell after it, which runs the tests with
# coverage and prints LuaCov's report for `grades.lua`: every line marked `*0` is a line no test
# ran.

# %% tags=["answer-L11.4"]
# %%writefile scratch/project/grades/spec/grades_spec.lua
local grades = require("grades")

describe("grades.letter", function()
  it("gives an A for 95", function()
    assert.are.equal("A", grades.letter(95))
  end)
end)

describe("grades.summary", function()
  it("counts nothing in an empty list", function()
    assert.are.same({ A = 0, B = 0, C = 0, F = 0 }, grades.summary({}))
  end)
end)


# %%
def coverage(folder):
    """Runs the tests with coverage; returns busted's status and output, and LuaCov's report."""
    for stale in ("luacov.stats.out", "luacov.report.out"):
        (PROJECT / folder / stale).unlink(missing_ok=True)
    status, output = run("busted", "--coverage", "-o", "plainTerminal", "--lpath=./src/?.lua",
                         folder=folder)
    run("luacov", folder=folder)
    report = (PROJECT / folder / "luacov.report.out").read_text()
    return status, output, report


status, output, report = coverage("grades")
print(output)
print(report)

# %% [markdown]
# ### Exercise L11.4 (LO-11.4, ★★, about 25 minutes)
#
# Add tests to the spec until LuaCov marks no line of `grades.lua` with `*0`. Each test must check a
# result, not only call the function. Run the spec's cell and the coverage cell after each change,
# and read which lines are still marked.

# %% tags=["raises-exception"]
status, output, report = coverage("grades")
assert status == 0, "every test must pass:\n" + output
missed = [line for line in report.splitlines() if re.match(r"\*+0 ", line)]
assert not missed, f"{len(missed)} lines never ran:\n" + "\n".join(missed)
assert "100.00%" in report.split("Summary", 1)[1], "the summary should show 100.00% coverage"
print("passed")

# %% [markdown]
# ## Summary
#
# - A rockspec lists a rock's dependencies and modules; `luarocks --tree … make` builds rocks into
#   a tree of the project's own, resolving a dependency from that tree.
# - luacheck's findings were real: a missing `local` and a shadowed variable that broke `max`.
#   StyLua settled the layout without discussion.
# - Without annotations the checker had nothing to check against; with them, it caught both of the
#   caller's mistakes without running anything.
# - LuaCov pointed at each line the tests skipped, including the error branch.
#
# Next, do the [Module 11 practice](practice.md), then start PA5.
