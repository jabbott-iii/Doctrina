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
# # Lab 14: Versions, sandboxes, and hosts
#
# **Objectives:** LO-14.1, LO-14.2, LO-14.3\
# **Prerequisites:** the [Module 14 reading](index.md) and
# [Lab 10](../10-files-os-and-data/lab10.ipynb)\
# **Time:** about 2 hours
#
# You will write one module that runs unchanged on Lua 5.1, LuaJIT, Lua 5.4, and Lua 5.5; build a
# sandbox and attack it until it holds; see what no sandbox written in Lua can stop; and write a
# Neovim plugin whose tests replace Neovim with a stand-in. Each exercise writes a Lua file into the
# lab's `scratch` folder. As in the earlier labs, each check cell prints `passed` or fails with a
# message.

# %% [markdown]
# ## Setup
#
# The first cell loads `%%lua` and defines `on_every_lua`, which runs Lua code on each of the four
# Luas and says which one failed. The sandbox's attacks run in the standalone `lua`, in a process of
# their own with a time limit, so that a plugin the sandbox fails to stop can't freeze the notebook.

# %%
# %load_ext lualab
import pathlib
import shutil
import subprocess
import sys

import lualab
import lupa
import lupa.lua54

SCRATCH = pathlib.Path("scratch").resolve()
SCRATCH.mkdir(exist_ok=True)
LUA_BIN = pathlib.Path(sys.prefix) / "lua" / "bin"
LUA = str(LUA_BIN / "lua") if (LUA_BIN / "lua").exists() else shutil.which("lua")
VERSIONS = ["5.1", "luajit", "5.4", "5.5"]


def on_every_lua(code):
    """Runs Lua code on each of the four Luas; raises AssertionError naming the first that fails."""
    for version in VERSIONS:
        try:
            lualab.run(code, version)
        except lualab.LuaError as error:
            raise AssertionError(f"on Lua {version}: {error}") from None


print("Python", sys.version.split()[0], "| lupa", lupa.__version__)
print("standalone lua:", subprocess.run([LUA, "-v"], capture_output=True, text=True).stdout.strip()
      if LUA else "NOT FOUND")

# %% [markdown]
# ## 1. One module, four Luas
#
# Before you run the next cell, predict what each Lua prints for `10 / 2`, and which of them have
# `table.unpack` and `utf8`.

# %%
for version in VERSIONS:
    lualab.run('print(_VERSION, jit and jit.version or "", 10 / 2, '
               'table.unpack ~= nil, utf8 ~= nil)', version)

# %% [markdown]
# LuaJIT calls itself `Lua 5.1`, though it has features that 5.1 lacks, such as `goto`. Change the
# code in the cell to try others: `7 // 2`, `math.type(3)`, `#"héllo"`, or
# `string.format("%d", 3.5)`. Expressions with `//` don't compile at all on 5.1 and LuaJIT, so the
# cell fails there; that is the point of the next exercise.
#
# ### Exercise L14.1 (LO-14.1, ★★, about 25 minutes)
#
# Write `compat.lua`, so that the same file runs on all four Luas:
#
# - `compat.unpack(list)` returns the items of `list`, as `table.unpack` does.
# - `compat.idiv(a, b)` returns `a // b`, rounded down: `idiv(-7, 2)` is -4. Where Lua has
#   integers, two integers give an integer.
# - `compat.load_text(code, name, env)` compiles `code` as text, never as a binary chunk, with
#   `env` as its globals. It returns the function, or `nil` and a message.
# - `compat.utf8_len(s)` returns the number of UTF-8 characters in `s`.
#
# Detect each feature; don't test `_VERSION`. Run the cell to write the file, then run the check,
# which loads the file on each Lua in turn.
#
# <details>
# <summary>Hint</summary>
#
# The file can't contain `//`, or it won't compile on 5.1. Compile a function that uses `//` from a
# string, with `(loadstring or load)`, and use `math.floor(a / b)` where that fails. On 5.1,
# `loadstring(code, name)` compiles and `setfenv(fn, env)` sets the globals, but `loadstring` also
# accepts binary chunks, which start with the byte 27.
# </details>

# %% tags=["answer-L14.1"]
# %%writefile scratch/compat.lua
-- compat: the same four functions on Lua 5.1, LuaJIT, Lua 5.4, and Lua 5.5.
local compat = {}

-- compat.unpack(list): the items of list.
compat.unpack = nil -- your code here

-- compat.idiv(a, b): a // b, rounded down.
function compat.idiv(a, b)
  -- your code here
end

-- compat.load_text(code, name, env): code compiled as text, with env as its globals.
function compat.load_text(code, name, env)
  -- your code here
end

-- compat.utf8_len(s): the number of UTF-8 characters in s.
function compat.utf8_len(s)
  -- your code here
end

return compat

# %% tags=["raises-exception"]
on_every_lua(r'''
local compat = dofile("scratch/compat.lua")
assert(type(compat.unpack) == "function", "compat.unpack should be a function")
assert(select("#", compat.unpack({ 1, 2, 3 })) == 3, "unpack({1, 2, 3}) should return 3 values")
assert(compat.idiv(7, 2) == 3 and compat.idiv(-7, 2) == -4 and compat.idiv(7.5, 2) == 3,
  "idiv should round down: 7, 2 gives 3; -7, 2 gives -4")
if math.type then
  assert(math.type(compat.idiv(7, 2)) == "integer", "two integers should give an integer")
end
local fn = assert(compat.load_text("return x + 1", "=test", { x = 41 }))
assert(fn() == 42, "the loaded code should see env's x")
assert(compat.load_text("return print", "=test", {})() == nil, "the code should see only env")
local binary = string.dump(function() return 1 end)
local loaded, message = compat.load_text(binary, "=test", {})
assert(loaded == nil and message, "a binary chunk should be refused, with a message")
assert(compat.utf8_len("héllo") == 5 and compat.utf8_len("日本") == 2 and compat.utf8_len("") == 0,
  "utf8_len should count characters, not bytes")
print(_VERSION .. (jit and " (LuaJIT)" or "") .. ": passed")
''')

# %% [markdown]
# ## 2. A sandbox
#
# The sandbox is two files. `guard.lua` holds the start of every message the sandbox uses to stop
# a plugin, and the `pcall` it gives plugins; for now that is the real `pcall`, and Exercise L14.3
# changes it. `attack.lua` runs the plugin in `plugin.txt` in the sandbox and prints what happened,
# for the Python function `attack`. Run the next three cells.

# %%
# %%writefile scratch/guard.lua
-- guard: the pcall that the sandbox gives plugins.
local guard = {}

-- Every error the sandbox raises to stop a plugin starts with this.
guard.STOPPED = "sandbox: stopped"

-- Returns the function that plugins get as pcall. Exercise L14.3 changes it.
function guard.wrap(real_pcall)
  return real_pcall
end

return guard

# %%
# %%writefile scratch/attack.lua
-- Runs the plugin in plugin.txt in the sandbox, with the limits given as a Lua table in arg[1],
-- and prints the time it took, then the type and value of each result, one per line.
local sandbox = require("sandbox")
local file = assert(io.open("plugin.txt", "rb"))
local code = file:read("a")
file:close()
local limits = assert(load("return " .. (arg[1] or "nil")))()
local start = os.clock()
local results = table.pack(sandbox.run(code, limits))
io.write(("%.3f\n"):format(os.clock() - start))
for i = 1, results.n do
  io.write(type(results[i]), "\t", (tostring(results[i]):gsub("\n", " ")), "\n")
end


# %%
def attack(code, limits="nil", timeout=10):
    """Runs a plugin in the sandbox, in a new lua process. Returns None if it ran past the
    timeout, or a dict with the seconds it took, ok (the first result), and the other values."""
    (SCRATCH / "plugin.txt").write_bytes(code.encode("utf-8"))
    try:
        result = subprocess.run([LUA, "attack.lua", limits], cwd=SCRATCH, capture_output=True,
                                text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    assert result.returncode == 0, "the sandbox itself failed:\n" + result.stdout + result.stderr
    lines = result.stdout.splitlines()
    convert = {"number": float, "boolean": lambda text: text == "true", "nil": lambda text: None}
    values = [convert.get(kind, str)(text)
              for kind, _, text in (line.partition("\t") for line in lines[1:])]
    return {"seconds": float(lines[0]), "ok": values[0], "values": values[1:]}


def demo(code, timeout=10):
    """Runs a plugin with attack, and prints what happened, or that the sandbox isn't ready."""
    try:
        result = attack(code, timeout=timeout)
    except AssertionError as error:
        found = [line for line in str(error).splitlines() if "sandbox.lua" in line]
        print("Finish Exercise L14.2 first:", found[0].split(": ", 1)[-1] if found else error)
        return
    print(f"still running after {timeout} s: the sandbox didn't stop it" if result is None
          else result)


# %% [markdown]
# ### Exercise L14.2 (LO-14.2, ★★★, about 35 minutes)
#
# Write the two functions of `sandbox.lua`:
#
# - `sandbox.env()` returns a new table holding the functions named in `sandbox.SAFE`, copies of
#   the tables named in `sandbox.LIBRARIES`, and `pcall` set to `guard.wrap(pcall)`.
# - `sandbox.run(code, limits)` compiles `code` in text mode, with the chunk name `"=plugin"` and a
#   new `sandbox.env()`, and runs it in a coroutine of its own. A hook on that coroutine, called
#   every 1,000 instructions, stops the plugin when it has run more than `limits.instructions`
#   instructions (default 1e6), or when `collectgarbage("count")` has grown by more than
#   `limits.memory_kb` kilobytes since the start (default 10,240). To stop it, the hook raises
#   `guard.STOPPED .. ": instruction limit"` or `guard.STOPPED .. ": memory limit"`, and from then
#   on raises the same error at every instruction. `run` returns `true` and all of the plugin's
#   results, or `false` and a message, as a string, for any error.
#
# <details>
# <summary>Hint</summary>
#
# `coroutine.resume` returns what `pcall` would: `true` and the results, or `false` and the error.
# Pack them with `table.pack`, so that `nil` results aren't lost. Inside the hook,
# `debug.sethook(co, raise, "", 1)` replaces the hook with one that runs at every instruction.
# </details>

# %% tags=["answer-L14.2"]
# %%writefile scratch/sandbox.lua
-- sandbox: runs untrusted Lua with an allowlist of globals and limits on time and memory.
local guard = require("guard")
local sandbox = {}

-- The globals a plugin gets from the host, and the libraries it gets copies of.
sandbox.SAFE = { "assert", "error", "ipairs", "next", "pairs", "print", "select", "tonumber",
                 "tostring", "type" }
sandbox.LIBRARIES = { "string", "table", "math" }

-- Returns a new environment for one plugin.
function sandbox.env()
  error("env isn't written yet")
end

-- Runs code as a plugin, within limits.instructions and limits.memory_kb. Returns true and the
-- plugin's results, or false and a message.
function sandbox.run(code, limits)
  error("run isn't written yet")
end

return sandbox

# %% [markdown]
# The check attacks the sandbox. Each plugin must give the result shown in its message.

# %% tags=["raises-exception"]
def expect(code, ok, first=None, limits="nil", contains=None):
    result = attack(code, limits)
    assert result is not None, f"the sandbox didn't stop this plugin within 10 s:\n{code}"
    assert result["ok"] is ok, f"run should return {ok} for:\n{code}\ngot: {result}"
    if first is not None:
        assert result["values"][:1] == [first], f"for:\n{code}\nexpected {first!r}, got {result}"
    if contains is not None:
        assert contains in str(result["values"][0]), \
            f"for:\n{code}\nexpected {contains!r} in {result}"
    return result


STOPPED = "sandbox: stopped: "
assert expect("return 1 + 1, nil, 'two'", True)["values"] == [2.0, None, "two"], \
    "run should return every result, nils included"
expect("return = 1", False, contains="plugin:1:")
expect("\x1bLua", False, contains="binary")
names = "os, io, load, require, debug, getmetatable, setmetatable, coroutine, collectgarbage, " \
        "rawset, _G, dofile"
assert expect(f"return {names}", True)["values"] == [None] * 12, f"none of {names} should exist"
expect("string.upper = nil return ('x'):upper()", True, "X")
expect("local s = 0 for i = 1, 1e5 do s = s + i end return s", True, 5000050000.0)
expect("local s = 0 for i = 1, 1e5 do s = s + i end return s", False, STOPPED + "instruction limit",
       limits="{ instructions = 1e4 }")
expect("while true do end", False, STOPPED + "instruction limit")
expect("while true do pcall(function() while true do end end) end", False,
       STOPPED + "instruction limit")
expect("local t = {} for i = 1, 1e6 do t[i] = ('x'):rep(100) .. i end", False,
       STOPPED + "memory limit", limits="{ instructions = 1e9, memory_kb = 20480 }")
result = expect("error({})", False)
assert isinstance(result["values"][0], str), "an error that isn't a string should become one"
print("passed")

# %% [markdown]
# Now an attack that passes the instruction limit, which the reading explains: the plugin recurses
# through `pcall` until the C stack is nearly full, where Lua can't call the hook. Run the next
# cell, which gives the plugin 5 seconds.

# %%
demo("local function f() while true do pcall(f) end end f()", timeout=5)

# %% [markdown]
# ### Exercise L14.3 (LO-14.2, ★★, about 20 minutes)
#
# Change `guard.wrap` so that the `pcall` it returns catches errors as `pcall` does, except two
# kinds, which it raises again, unchanged, with `error(message, 0)`: the sandbox's own errors,
# which contain `guard.STOPPED`, and stack overflows, whose message contains `stack overflow` or
# `error in error handling`. Errors that aren't strings are never of those kinds. Then run the
# cell above again: the plugin should now stop at once.

# %% tags=["answer-L14.3"]
# %%writefile scratch/guard.lua
-- guard: the pcall that the sandbox gives plugins.
local guard = {}

-- Every error the sandbox raises to stop a plugin starts with this.
guard.STOPPED = "sandbox: stopped"

-- Returns the function that plugins get as pcall.
function guard.wrap(real_pcall)
  -- your code here
  return real_pcall
end

return guard

# %% tags=["raises-exception"]
for plugin in ("local function f() while true do pcall(f) end end f()",
               "local function f() while true do pcall(function() ('x'):gsub('.', f) end) end end"
               " f()"):
    result = attack(plugin)
    assert result is not None, f"the sandbox didn't stop this plugin within 10 s:\n{plugin}"
    assert result["ok"] is False and ("stack overflow" in result["values"][0]
                                      or STOPPED in result["values"][0]), f"{plugin}\n{result}"
result = expect("local ok, e = pcall(error, 'boom', 0) "
                "return ok, e, pcall(function() return 1, nil, 3 end)", True)
assert result["values"] == [False, "boom", True, 1.0, None, 3.0], \
    "the plugins' pcall should still catch ordinary errors and return every result: " + str(result)
expect("local ok, e = pcall(error, {}) return ok, type(e)", True, False)
expect("while true do pcall(function() while true do end end) end", False,
       STOPPED + "instruction limit")
print("passed")

# %% [markdown]
# ## 3. What the sandbox can't stop
#
# The hook runs between Lua instructions, so work done inside one C function call is invisible to
# it. Before you run each cell, predict whether the sandbox stops the plugin. The first builds a
# 100 MB string in one call to `string.rep`; the second runs a pattern that backtracks.

# %%
demo("return #('x'):rep(1e8)")

# %%
demo("return ('a'):rep(1000):find('.-.-b')")

# %% [markdown]
# Both finished, under limits of 10 MB and a million instructions. The memory one can be stopped
# from outside Lua, by an allocator that refuses to allocate past a limit. lupa offers one for each
# Lua it runs; with a limit of 50 MB, the same call fails with `not enough memory`, which Lua can
# catch like any other error:

# %%
limited = lupa.lua54.LuaRuntime(max_memory=50_000_000)
print(limited.execute('return pcall(string.rep, "x", 1e8)'))

# %% [markdown]
# LuaJIT adds a gap of its own: its compiler turns a hot loop into machine code, and compiled code
# doesn't call the count hook. The next cell runs an endless loop under a hook on LuaJIT twice, in a
# new Python process each time, with 5 seconds to finish: once with the compiler on, and once after
# `jit.off()`.

# %%
PROBE = r'''
import sys, lupa.luajit21
print(lupa.luajit21.LuaRuntime().execute("""
  if ... == "off" then jit.off() end
  local fires = 0
  local co = coroutine.create(function() local x = 0 while true do x = x + 1 end end)
  debug.sethook(co, function()
    fires = fires + 1
    if fires >= 1000 then error("stopped", 0) end
  end, "", 1000)
  local start = os.clock()
  local ok, message = coroutine.resume(co)
  return ("%s after %.3f s"):format(message, os.clock() - start)
""", sys.argv[1]))
'''
for mode in ("on", "off"):
    try:
        run = subprocess.run([sys.executable, "-c", PROBE, mode], capture_output=True, text=True,
                             timeout=5)
        print(f"compiler {mode}: {run.stdout.strip() or run.stderr.strip()}")
    except subprocess.TimeoutExpired:
        print(f"compiler {mode}: still running after 5 s; the hook never stopped it")

# %% [markdown]
# ## 4. A plugin for a host
#
# `fake.lua` is a stand-in for the parts of Neovim's `vim` that the next exercise uses. It keeps
# one buffer's lines, records every call to `vim.api`, and queues the functions given to
# `vim.schedule` until a test calls `run_queue`, as Neovim's event loop would on its next turn.
# Run the cell to write it.

# %%
# %%writefile scratch/fake.lua
-- A stand-in for the parts of Neovim's vim that trim uses.
local function fake_vim(lines)
  local vim = { calls = {}, queue = {}, lines = lines }
  vim.api = {
    nvim_buf_get_lines = function(buf, first, last, strict)
      vim.calls[#vim.calls + 1] = { "get", buf, first, last, strict }
      local copy = {}
      for i, line in ipairs(vim.lines) do copy[i] = line end
      return copy
    end,
    nvim_buf_set_lines = function(buf, first, last, strict, replacement)
      vim.calls[#vim.calls + 1] = { "set", buf, first, last, strict }
      vim.lines = replacement
    end,
  }
  function vim.schedule(fn) vim.queue[#vim.queue + 1] = fn end
  function vim.run_queue()
    local queue = vim.queue
    vim.queue = {}
    for _, fn in ipairs(queue) do fn() end
  end
  return vim
end

return fake_vim

# %% [markdown]
# ### Exercise L14.4 (LO-14.3, LO-14.1, ★★, about 25 minutes)
#
# Write the three functions of `trim.lua`, a plugin that removes the spaces and tabs at the ends of
# a buffer's lines:
#
# - `trim.lines(lines)` returns a new list of the lines, each without its trailing spaces and tabs,
#   and the number of lines that changed. It never touches the host.
# - `trim.buffer(api, buf)` reads every line of buffer `buf` with
#   `api.nvim_buf_get_lines(buf, 0, -1, false)`, trims them, writes them back with
#   `api.nvim_buf_set_lines(buf, 0, -1, false, lines)` only if a line changed, and returns the
#   number that changed.
# - `trim.later(vim, buf)` does what `trim.buffer(vim.api, buf)` does, but on the event loop's next
#   turn, through `vim.schedule`, so it is safe to call from a callback where Neovim forbids
#   changing a buffer.
#
# Neovim runs plugins on LuaJIT, so the check runs your file there, and on Lua 5.4.

# %% tags=["answer-L14.4"]
# %%writefile scratch/trim.lua
-- trim: removes trailing spaces and tabs from the lines of a Neovim buffer.
local trim = {}

function trim.lines(lines)
  -- your code here
end

function trim.buffer(api, buf)
  -- your code here
end

function trim.later(vim, buf)
  -- your code here
end

return trim

# %% tags=["raises-exception"]
check = r'''
local trim = dofile("scratch/trim.lua")
local fake_vim = dofile("scratch/fake.lua")
local out, changed = trim.lines({ "a  ", "b", "\tc\t", "" })
assert(changed == 2, "two of the four lines change")
assert(out[1] == "a" and out[2] == "b" and out[3] == "\tc" and out[4] == "", "keep leading tabs")
local vim = fake_vim({ "x = 1   ", "y = 2" })
assert(trim.buffer(vim.api, 7) == 1, "buffer should return the number of lines that changed")
assert(#vim.calls == 2 and vim.calls[1][1] == "get" and vim.calls[2][1] == "set", "get, then set")
local set = vim.calls[2]
assert(set[2] == 7 and set[3] == 0 and set[4] == -1 and set[5] == false,
  "set every line of buffer 7")
assert(vim.lines[1] == "x = 1" and vim.lines[2] == "y = 2", "the buffer's lines should be trimmed")
local clean = fake_vim({ "ok" })
assert(trim.buffer(clean.api, 0) == 0 and #clean.calls == 1,
  "don't write a buffer that didn't change")
local later = fake_vim({ "late  " })
trim.later(later, 3)
assert(#later.calls == 0, "later should change nothing until the event loop runs it")
later.run_queue()
assert(later.lines[1] == "late", "the queued function should trim the buffer")
print(_VERSION .. (jit and " (LuaJIT)" or "") .. ": passed")
'''
for version in ("luajit", "5.4"):
    try:
        lualab.run(check, version)
    except lualab.LuaError as error:
        raise AssertionError(f"on Lua {version}: {error}") from None

# %% [markdown]
# ## Summary
#
# - One file ran on four Luas by detecting each feature: `table.unpack or unpack`, `//` compiled
#   from a string, `setfenv` where `load` takes no environment, and a byte check where `loadstring`
#   takes binary chunks.
# - The sandbox stopped endless loops, loops that catch its errors, and memory growth, once its hook
#   raised an error at every instruction and its `pcall` let no limit or stack overflow through.
# - It couldn't stop work inside one C call, or compiled LuaJIT code; an allocator limit, and a
#   separate process for time, cover what Lua can't.
# - The plugin's logic needed no host at all, and a stand-in that records calls tested the thin
#   layer and the event loop's timing, on the Lua that Neovim runs.
#
# Next, do the [Module 14 practice](practice.md), and finish the final project.
