"""Run Lua in Jupyter notebooks: the ``%%lua`` cell magic for LUA101's labs.

Load it in a notebook with ``%load_ext lualab``. Then a cell that starts with
``%%lua`` runs as Lua 5.4, through the lupa package, which embeds the Lua
interpreter in Python.

Each Lua version keeps one Lua state for the whole notebook, so a variable or
function defined in one cell is still there in the next, as in the standalone
interpreter's interactive mode (``lua -i``). Like that mode, a cell that is a
single expression shows its value.

Output goes where the standalone interpreter would send it: ``print``,
``io.write``, and ``io.stdout:write`` appear below the cell, because lualab
captures the process's standard output and standard error while the cell runs.
A Lua error, including a failed ``assert``, fails the cell, so a notebook's
checks fail the same way a script's would.
"""

from __future__ import annotations

import importlib
import os
import sys
import tempfile
from typing import Any

__all__ = ["DEFAULT_VERSION", "VERSIONS", "LuaError", "load_ipython_extension", "reset", "run"]

#: The Lua versions a cell can ask for, and the lupa module that provides each.
VERSIONS = {
    "5.1": "lua51",
    "5.2": "lua52",
    "5.3": "lua53",
    "5.4": "lua54",
    "5.5": "lua55",
    "luajit": "luajit21",
}

#: The version a cell runs on unless it says otherwise.
DEFAULT_VERSION = "5.4"

# The chunk name Lua puts in error messages: "cell:3: ..." means line 3 of the cell.
CHUNK_NAME = "=cell"

# Runs once in each new Lua state. It is written to the subset of Lua that every
# version above shares, and it keeps its helpers in locals, so it adds no globals.
_PRELUDE = r"""
local type, tostring, getmetatable, select, print, pcall =
  type, tostring, getmetatable, select, print, pcall
local format = string.format
local traceback = debug.traceback
local io_stdout, io_stderr = io.stdout, io.stderr
local pack = table.pack or function(...) return { n = select("#", ...), ... } end
local unpack = table.unpack or unpack

-- lupa adds a global table named `python`; a Lua program shouldn't see it.
python = nil

-- os.exit would end the whole kernel, not only the cell.
os.exit = function()
  error("os.exit would stop the notebook's kernel, so lualab disables it; "
    .. "use it in a script run with lua", 2)
end

local compile
if _VERSION == "Lua 5.1" then
  compile = function(code, name) return loadstring(code, name) end
else
  compile = function(code, name) return load(code, name, "t") end
end

-- Mirrors the message handler of the standalone interpreter (lua.c).
local function handler(message)
  if type(message) ~= "string" then
    local mt = getmetatable(message)
    if type(mt) == "table" and mt.__tostring then
      message = tostring(message)
    else
      message = format("(error object is a %s value)", type(message))
    end
  end
  return traceback(message, 2)
end

local function flush()
  pcall(function() io_stdout:flush() end)
  pcall(function() io_stderr:flush() end)
end

-- Like lua -i: try the cell as an expression first, and print its values.
local function run(code, name)
  local chunk = compile("return " .. code, name)
  local is_expression = chunk ~= nil
  if not chunk then
    local message
    chunk, message = compile(code, name)
    if not chunk then
      return false, message
    end
  end
  local results = pack(xpcall(chunk, handler))
  if not results[1] then
    return false, results[2]
  end
  if is_expression and results.n > 1 then
    print(unpack(results, 2, results.n))
  end
  return true
end

return run, flush
"""


class LuaError(Exception):
    """A Lua error raised while a cell ran, with Lua's message and stack traceback."""


_states: dict[str, tuple[Any, Any, Any]] = {}


def _state(version: str, fresh: bool = False) -> tuple[Any, Any, Any]:
    """Return ``(runtime, run, flush)`` for ``version``, creating the state on first use."""
    if version not in VERSIONS:
        choices = ", ".join(VERSIONS)
        raise ValueError(f"unknown Lua version {version!r}; choose one of {choices}")
    if fresh or version not in _states:
        try:
            module = importlib.import_module("lupa." + VERSIONS[version])
        except ImportError as exc:
            raise ValueError(f"this build of lupa doesn't include Lua {version}") from exc
        runtime = module.LuaRuntime(register_eval=False, register_builtins=False)
        # Lua 5.1's load takes a function, not a string; its loadstring takes a string.
        prelude = runtime.eval("loadstring or load")(_PRELUDE, "=lualab")
        run_cell, flush = prelude()
        _states[version] = (runtime, run_cell, flush)
    return _states[version]


def reset(version: str = DEFAULT_VERSION) -> None:
    """Throw away ``version``'s Lua state, so the next cell starts with a fresh one."""
    _state(version, fresh=True)


def _clean_traceback(message: str) -> str:
    # Drop the frames that belong to lualab rather than to the student's code.
    lines = message.split("\n")
    kept = [
        line
        for line in lines
        if "lualab:" not in line and "in function 'xpcall'" not in line
        and "in function <lualab" not in line
    ]
    while kept and kept[-1].strip() in ("[C]: in ?", "(...tail calls...)"):
        kept.pop()
    if len(kept) >= 2 and kept[-1].strip() == "stack traceback:":
        kept.pop()
    return "\n".join(kept)


def run(code: str, version: str = DEFAULT_VERSION) -> None:
    """Run ``code`` in ``version``'s Lua state, as a ``%%lua`` cell would.

    Lua's output is written to Python's ``sys.stdout`` and ``sys.stderr``.
    Raises ``LuaError`` if the code doesn't compile or raises an error.
    """
    _, run_cell, flush = _state(version)
    sys.stdout.flush()
    sys.stderr.flush()
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        saved_out, saved_err = os.dup(1), os.dup(2)
        os.dup2(out.fileno(), 1)
        os.dup2(err.fileno(), 2)
        try:
            # lupa returns one Lua result as a value, and several as a tuple.
            result = run_cell(code, CHUNK_NAME)
            ok, message = result if isinstance(result, tuple) else (result, None)
        finally:
            flush()
            os.dup2(saved_out, 1)
            os.dup2(saved_err, 2)
            os.close(saved_out)
            os.close(saved_err)
        out.seek(0)
        err.seek(0)
        sys.stdout.write(out.read().decode("utf-8", "replace"))
        sys.stderr.write(err.read().decode("utf-8", "replace"))
    sys.stdout.flush()
    sys.stderr.flush()
    if not ok:
        raise LuaError(_clean_traceback(str(message)))


def _show_lua_error(shell, etype, evalue, tb, tb_offset=None):
    # Show Lua's message alone, without the Python frames that carried it. IPython
    # ignores this handler's return value when the error comes from a cell, so the
    # handler publishes the error itself; that is also what fails the cell in nbmake.
    structured = [f"LuaError: {evalue}"]
    shell._showtraceback(etype, evalue, structured)
    return structured


def load_ipython_extension(ipython) -> None:
    """Register ``%%lua``, ``%lua``, and ``%lua_reset`` (called by ``%load_ext lualab``)."""
    from IPython.core.magic import Magics, line_cell_magic, line_magic, magics_class
    from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

    @magics_class
    class LuaMagics(Magics):
        @magic_arguments()
        @argument(
            "-v",
            "--version",
            default=DEFAULT_VERSION,
            choices=list(VERSIONS),
            help="the Lua version to run the cell on (default: %(default)s)",
        )
        @argument(
            "--reset",
            action="store_true",
            help="start this version's Lua state fresh before running the cell",
        )
        @line_cell_magic
        def lua(self, line, cell=None):
            """Run the cell (``%%lua``) or the rest of the line (``%lua``) as Lua."""
            if cell is None:
                run(line)
                return
            args = parse_argstring(self.lua, line)
            if args.reset:
                reset(args.version)
            run(cell, args.version)

        @line_magic
        def lua_reset(self, line):
            """Start a version's Lua state fresh: ``%lua_reset`` or ``%lua_reset 5.1``."""
            reset(line.strip() or DEFAULT_VERSION)

    ipython.register_magics(LuaMagics)
    ipython.set_custom_exc((LuaError,), _show_lua_error)
