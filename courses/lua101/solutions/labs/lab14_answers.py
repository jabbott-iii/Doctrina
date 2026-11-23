# %% [markdown]
# # Lab 14: answer key
#
# Each tagged cell replaces the lab cell with the same tag; `tools/check_lab.py` runs the lab with
# them. The untagged Markdown cells explain the answers and the common mistakes.

# %% [markdown]
# ## Exercise L14.1
#
# Each function detects what it needs. `idiv` compiles a function that uses `//` from a string,
# because the operator in the file itself would stop the file compiling on 5.1 and LuaJIT; there,
# every number is a float, so `math.floor(a / b)` gives the same result. `load_text` probes once
# whether `load` takes a string and an environment, which fails on 5.1 only, and on 5.1 refuses a
# chunk whose first byte is 27 before `loadstring` can run it. `utf8_len` counts the bytes that
# aren't continuation bytes (128 to 191), which is the number of characters in valid UTF-8.
#
# Common mistakes: testing `_VERSION == "Lua 5.1"`, which sends LuaJIT down the 5.1 path for
# `load` (harmless here, but wrong in general); writing `a // b` in the file; using
# `math.floor(a / b)` everywhere, which turns two integers into a float on 5.4 and loses precision
# above $2^{53}$; and calling `setfenv` on a failed load's `nil`.

# %% tags=["answer-L14.1"]
# %%writefile scratch/compat.lua
-- compat: the same four functions on Lua 5.1, LuaJIT, Lua 5.4, and Lua 5.5.
local compat = {}

compat.unpack = table.unpack or unpack

-- Floor division. Where the // operator exists, compile a function that uses it, so integers
-- stay integers; elsewhere, every number is a float, and math.floor gives the same result.
local idiv = (loadstring or load)("return function(a, b) return a // b end")
compat.idiv = idiv and idiv() or function(a, b) return math.floor(a / b) end

-- Loads text only, with env as its globals. Lua 5.1's loadstring takes binary chunks too and
-- has no env argument, so refuse binary chunks by their first byte, and set env with setfenv.
local load_takes_env = pcall(load, "return 1", "=probe", "t", {})
function compat.load_text(code, name, env)
  if load_takes_env then
    return load(code, name, "t", env)
  end
  if code:byte(1) == 27 then
    return nil, "attempt to load a binary chunk"
  end
  local fn, err = loadstring(code, name)
  if fn then setfenv(fn, env) end
  return fn, err
end

-- The number of characters in a UTF-8 string: utf8.len where it exists; elsewhere, count the
-- bytes that start a character, which are all but the continuation bytes 128-191.
function compat.utf8_len(s)
  if utf8 then return utf8.len(s) end
  return select(2, s:gsub("[^\128-\191]", ""))
end

return compat

# %% [markdown]
# ## Exercise L14.2
#
# `env` builds the environment from the allowlist and copies each library, so a plugin that
# changes `string.upper` changes only its copy; the check's `('x'):upper()` still works because
# string methods come from the real `string` table through the string metatable. `run` compiles in
# text mode, runs the plugin in a coroutine of its own, and sets the hook on that coroutine only,
# so the host's code never runs under it. `stop` replaces the hook with one that raises at every
# instruction, so a plugin that catches the first error with `pcall` fails at its next instruction
# outside the `pcall`.
#
# Common mistakes: `env.string = string`, which shares the host's table; setting the hook with
# `debug.sethook(hook, "", 1000)`, without the coroutine, which limits the host instead of the
# plugin; raising the error once, which the `pcall` loop survives; reading `collectgarbage("count")`
# only at the end, too late to stop anything; and returning `results[2]` alone, which loses the
# plugin's other results and its `nil`s.

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
  local env = {}
  for _, name in ipairs(sandbox.SAFE) do
    env[name] = _G[name]
  end
  for _, lib in ipairs(sandbox.LIBRARIES) do
    local copy = {}
    for key, value in pairs(_G[lib]) do
      copy[key] = value
    end
    env[lib] = copy
  end
  env.pcall = guard.wrap(pcall)
  return env
end

-- Runs code as a plugin, with at most limits.instructions instructions (default 1e6) and at
-- most limits.memory_kb more kilobytes of memory in use (default 10240). Returns true and the
-- plugin's results, or false and a message.
function sandbox.run(code, limits)
  limits = limits or {}
  local max_instructions = limits.instructions or 1e6
  local max_kb = limits.memory_kb or 10240
  local fn, err = load(code, "=plugin", "t", sandbox.env())
  if not fn then
    return false, err
  end
  local co = coroutine.create(fn)
  local step, used, base = 1000, 0, collectgarbage("count")
  local function stop(why)
    local message = guard.STOPPED .. ": " .. why
    debug.sethook(co, function() error(message, 0) end, "", 1)
    error(message, 0)
  end
  debug.sethook(co, function()
    used = used + step
    if used > max_instructions then stop("instruction limit") end
    if collectgarbage("count") - base > max_kb then stop("memory limit") end
  end, "", step)
  local results = table.pack(coroutine.resume(co))
  if not results[1] then
    return false, tostring(results[2])
  end
  return true, table.unpack(results, 2, results.n)
end

return sandbox

# %% [markdown]
# ## Exercise L14.3
#
# The wrapper calls the real `pcall`, and when it caught an error that is the sandbox's own or a
# stack overflow, raises it again with level 0, so the message stays unchanged. Stack overflows
# must pass too, because near the C stack's limit the hook can't run at all: the error the plugin
# gets is `C stack overflow`, not the sandbox's message. Every other error, tables included, is
# caught as before, and all results are returned, `nil`s included.
#
# Common mistakes: matching the message with `==`, which misses `plugin:1: C stack overflow`;
# calling `e:find` on an error that is a table; and `error(message)` without level 0, which adds a
# position to the message.

# %% tags=["answer-L14.3"]
# %%writefile scratch/guard.lua
-- guard: the pcall that the sandbox gives plugins.
local guard = {}

-- Every error the sandbox raises to stop a plugin starts with this.
guard.STOPPED = "sandbox: stopped"

-- Errors a plugin must not catch: the sandbox's own, and stack overflows. A stack overflow is
-- also what a plugin gets when the C stack is so deep that Lua can't call the hook at all.
local function fatal(e)
  return type(e) == "string"
    and (e:find(guard.STOPPED, 1, true) or e:find("stack overflow", 1, true)
      or e:find("error in error handling", 1, true)) ~= nil
end

-- Returns the function that plugins get as pcall: real_pcall, except that it passes fatal
-- errors on instead of catching them.
function guard.wrap(real_pcall)
  return function(f, ...)
    local results = table.pack(real_pcall(f, ...))
    if not results[1] and fatal(results[2]) then
      error(results[2], 0)
    end
    return table.unpack(results, 1, results.n)
  end
end

return guard

# %% [markdown]
# ## Exercise L14.4
#
# `lines` keeps the logic free of the host, so it needs no stand-in at all. `buffer` is the thin
# layer: one read, the logic, and a write only when something changed. `later` hands the work to
# `vim.schedule` and does nothing else, so the stand-in shows that nothing changes until the queue
# runs. Everything runs on LuaJIT: `gsub` and `ipairs` are in Lua 5.1.
#
# Common mistakes: the pattern `%s+$`, which also removes a trailing carriage return or form feed;
# counting a line as changed without comparing it with the original; reading the global `vim`
# inside `buffer` instead of using its argument, which the stand-in can't replace; and calling
# `trim.buffer` inside `later` before `vim.schedule`, instead of in the function it schedules.

# %% tags=["answer-L14.4"]
# %%writefile scratch/trim.lua
-- trim: removes trailing spaces and tabs from the lines of a Neovim buffer.
local trim = {}

-- The logic, which never touches the host: returns the trimmed lines and how many changed.
function trim.lines(lines)
  local out, changed = {}, 0
  for i, line in ipairs(lines) do
    out[i] = line:gsub("[ \t]+$", "")
    if out[i] ~= line then changed = changed + 1 end
  end
  return out, changed
end

-- The thin layer: reads the buffer through the host's API, and writes it only if a line changed.
function trim.buffer(api, buf)
  local lines = api.nvim_buf_get_lines(buf, 0, -1, false)
  local out, changed = trim.lines(lines)
  if changed > 0 then
    api.nvim_buf_set_lines(buf, 0, -1, false, out)
  end
  return changed
end

-- For callbacks that may run where the editor can't be changed: trims on the event loop's next turn.
function trim.later(vim, buf)
  vim.schedule(function()
    trim.buffer(vim.api, buf)
  end)
end

return trim
