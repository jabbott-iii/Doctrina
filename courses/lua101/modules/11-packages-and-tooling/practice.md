# Module 11 practice

These exercises practice the [Module 11 reading](index.md). They aren't graded. Answer each one
yourself before you open its answer, and then confirm it with the tools, from a terminal where
`source .venv/lua/bin/activate` has run.

## Worked example: one command that checks everything

A project should be checked the same way on every machine and in continuous integration. Write a
script, `check.sh`, that runs the formatter's check, the linter, the type checker, and the tests
with coverage, and stops at the first that fails.

1. **Stop on failure.** `set -e` makes a shell script exit as soon as a command fails, and each tool
   exits with a nonzero status when it finds a problem.
2. **Check, don't change.** In a script that verifies, StyLua runs with `--check`; reformatting
   belongs on the developer's machine.
3. **Order by speed.** The formatter and the linter take a fraction of a second, so they run first,
   and a typo stops the script before the slower steps.

```bash
#!/bin/sh
set -e
stylua --check src spec
luacheck src spec
lua-language-server --check=src --checklevel=Warning
busted --coverage
luacov
```

The script ends after `luacov` writes `luacov.report.out`. It doesn't fail on low coverage; a
project that wants a minimum must check the report's last line itself.

### Exercise 11.1 (LO-11.1, ★, about 10 minutes)

Find three problems in this rockspec, which `luarocks lint` or `luarocks make` would reject.

```lua
package = "csvtool"
version = "1.0"
source = { url = "git+https://example.org/csvtool.git" }
description = { summary = "Prints statistics for the columns of a CSV file." }
dependencies = { "lua >= 5.4" }
build = { type = "builtin", modules = { csvtool = "csvtool.lua" } }
```

The module's source is `src/csvtool.lua`.

<details>
<summary>Answer</summary>

1. The version needs a rockspec revision, `"1.0-1"`, which matches the file name
   `csvtool-1.0-1.rockspec`.
2. `description.license` is missing, which `luarocks lint` rejects.
3. The module maps to `csvtool.lua`, but the file is `src/csvtool.lua`, so the build can't find it.
</details>

### Exercise 11.2 (LO-11.2, ★★, about 15 minutes)

For each luacheck finding, say whether it is most likely a bug or dead code, and how to fix it.

1. `unused variable 'result'`, for a line `local result = parse(line)` followed by `return true`.
2. `setting non-standard global variable 'count'`, inside a function.
3. `unused argument 'opts'`, in `function M.render(text, opts)`.
4. `shadowing upvalue 'err'`, for `local ok, err = pcall(f)` inside a function that already has an
   `err`.

<details>
<summary>Answer</summary>

1. Probably a bug: the function parses the line and ignores the result. Return or use `result`;
   if the call is there only for its error, write `parse(line)` without the variable.
2. A bug: a missing `local`. Declare `local count` in the function.
3. Either dead code or an unfinished feature. If `opts` is part of a public interface that a later
   version will use, keep it and silence only that warning on that line, with a comment saying
   why; otherwise remove the parameter.
4. A likely bug: the inner `err` hides the outer one, so code after the block may read the wrong
   one. Rename the inner variable.
</details>

### Exercise 11.3 (LO-11.2, ★★, about 10 minutes)

A teammate's pull request changes 300 lines, but only five do anything; the rest is indentation
their editor changed. What would have prevented that, and what does the project need?

<details>
<summary>Answer</summary>

A formatter that every contributor runs, with its settings in the project: a `stylua.toml`, and
`stylua --check` in continuous integration, which fails the pull request until the code matches the
agreed layout. Then layout changes never appear in a diff, and the reviewer sees only the five
lines that matter.
</details>

### Exercise 11.4 (LO-11.3, ★★, about 15 minutes)

Annotate this function with LuaCATS. `name` is a string; `greeting` is an optional string; the
result is a string.

```lua
function M.greet(name, greeting)
  return (greeting or "Hello") .. ", " .. name
end
```

<details>
<summary>Answer</summary>

```lua
---Returns a greeting for `name`.
---@param name string
---@param greeting? string    The word to greet with; "Hello" if absent.
---@return string
function M.greet(name, greeting)
  return (greeting or "Hello") .. ", " .. name
end
```

The `?` after the parameter's name marks it optional, so `M.greet("Ada")` passes the check, and
`M.greet(42)` fails it with `param-type-mismatch`.
</details>

### Exercise 11.5 (LO-11.4, ★★, about 10 minutes)

A module's coverage report shows 100%, yet this function's error has never been tested. How can
both be true, and how would you make the report show it?

```lua
function M.parse(text) if text == "" then error("empty input", 2) end return text:upper() end
```

<details>
<summary>Answer</summary>

LuaCov counts lines, and the whole function, `if` and `error` included, is one line, which counts
as covered whenever any test calls `parse`. Let StyLua lay it out, which puts the `error` on a line
of its own; the report then marks that line `*0` until a test calls `parse("")` and checks the
error.
</details>
