# Final project: grading notes

The brief and its rubrics are published in `assignments/final-project/README.md`. These notes are
for the people who grade it: how to run the checks, what to look for in each track, and the
attacks to try on a sandbox. The split of the project's 20% among the milestones (10%, 30%, 60%)
and the rubrics' points are drafts in the brief; change them there if the instructor decides
otherwise.

## Running the checks

From the repository's root, with the notebook environment active:

```bash
python courses/lua101/tools/check_project.py path/to/project --lpath='./src/?.lua'
```

It copies the project, and reports the rockspec's lint and build, luacheck, `stylua --check`,
lua-language-server, the tests' result, each file's coverage, and the number of lines the tests
never ran. Its results feed **Builds** and **Tooling** at the milestone, and **Package and
tooling** and part of **Tests and coverage** in the final project. Read `README.md` for the
explanation of every line never run.

A project that uses another `--lpath`, or C code that needs a compiler flag, may need its own
options; the student's `README.md` says how to build and test it, and is part of the documentation
criterion.

## What to look for in each track

### C

- **The stack stays balanced.** Every C function that Lua calls returns the number of results it
  pushed, and pops what it pushed for its own work. Ask the student to show the test they used,
  such as `lua_gettop` before and after a call in a debug build.
- **Arguments are checked** with `luaL_checkinteger`, `luaL_checkudata`, and the like, so a wrong
  argument raises `bad argument #n to 'name'` rather than crashing.
- **`__gc` frees what C allocated, once.** A userdata whose `__gc` frees a pointer must set it to
  `NULL`, because `__gc` can be called on an object that a `__close` or an explicit `close` method
  already released.
- **Errors in an embedding host** are caught with `lua_pcall`, and the program reports the message
  and carries on, or exits with a status, without `abort`.
- If the student ran Valgrind or AddressSanitizer (`-fsanitize=address`), the report belongs in the
  `README.md`; credit it under documentation.

### Sandbox

Try each attack on the student's sandbox with a plugin of your own. Each must fail with an error
the host catches, or be listed in `THREATS.md` as something the sandbox doesn't stop:

| Attack | Plugin code | Why it matters |
| :- | :- | :- |
| An endless loop | `while true do end` | Needs an instruction-count hook |
| An endless loop in a coroutine | `coroutine.wrap(function() while true do end end)()` | A hook set with `debug.sethook` from Lua fires only in the coroutine it was set on; a new coroutine has none, so this loop runs forever unless the sandbox sets the hook in every coroutine it lets a plugin create |
| Filling memory | `local s = ("x"):rep(1e9)` | String methods are reachable through every string's metatable, even with an empty environment |
| Reaching the real globals through `load` | `load("return os")()` | `load` without an environment argument uses the real global table; tested, it returned the host's `os` |
| Changing the host's string library | `getmetatable("").__index.upper = …` | Every string shares one metatable, whose `__index` is the real `string` table; tested, the host's `upper` changed |
| A binary chunk | Precompiled code passed to the sandbox's loader | Must be refused by loading in text mode |
| Reading files | `io.open("/etc/passwd")` | `io` must not be in the allowlist |

A sandbox that offers `coroutine`, `load`, or `getmetatable` to plugins must wrap them: set the hook
in each coroutine it creates (`debug.sethook(co, hook, "", count)`), pass the sandbox's environment
to every `load`, and offer a `getmetatable` that refuses strings. Grade **Function and track** on
the attacks it stops, and credit a `THREATS.md` that names honestly the ones it doesn't.

### Host

- **The logic doesn't touch the host.** Modules in `src/` that `require` `vim`, `love`, or
  `pandoc`, or read those globals, can't be tested without the host; the brief asks for a thin
  layer that does.
- **The stand-in records calls.** A good test replaces the host's API with a table whose functions
  record their arguments, and checks those records, for example that a Neovim plugin called
  `vim.api.nvim_buf_set_lines` with the right lines.
- **Versions are named.** Neovim's Lua interface is Lua 5.1, and its documentation recommends
  building it with LuaJIT; Pandoc embeds Lua 5.4. LÖVE's Lua
  [citation needed: the Lua implementation LÖVE embeds; love2d.org refused automated reads on
  2026-11-23]. Code that uses `//`, integers, or `<close>`, none of which Lua 5.1 or LuaJIT has,
  must say how it handles the difference, as module 14 teaches.

## Proposals that work, and proposals that don't

A good proposal names a small core, such as a CSV-to-JSON converter, a rate limiter for plugin
calls, or a Pandoc filter that numbers figures, and grows from it. Steer students away from
proposals whose core depends on something the course didn't cover, such as a network protocol or a
GUI framework, and from proposals with no plausible hot path: the performance criterion needs a
loop that runs often enough to measure.
