# Module 11: Packages and tooling

**Objectives:** LO-11.1, LO-11.2, LO-11.3, LO-11.4\
**Prerequisites:** [Module 6](../06-errors-modules-and-tests/index.md)\
**Time:** about 9 hours: 2.5 for this reading, 2 for [Lab 11](lab11.ipynb), 1.5 for the
[practice](practice.md), and 3 to start PA5, which is due in week 12

So far your code has been a file or two that you ran by hand. Code that other people install,
review, and maintain needs more: a package that says what it contains and what it depends on, and
tools that catch mistakes before anyone runs the code. This module covers the tools the Lua
community uses for each job: LuaRocks for packages, luacheck for lint, StyLua for formatting,
LuaCATS annotations with lua-language-server for types, and LuaCov for test coverage. Each one
answers a question that tests alone don't, and PA5 asks for all of them.

| Tool | Answers | Run it as |
| :- | :- | :- |
| LuaRocks | What does this package contain and need, and how is it installed? | `luarocks make`, `luarocks install` |
| luacheck | Does the code use undefined globals, or leave variables unused? | `luacheck src spec` |
| StyLua | Is the code laid out the way the project agreed? | `stylua --check src spec` |
| lua-language-server | Do the calls match the types the functions document? | `lua-language-server --check=src` |
| LuaCov | Which lines did the tests never run? | `busted --coverage`, then `luacov` |

## Packages with LuaRocks

A **rock** is a Lua package. A **rockspec**, a file of Lua assignments, describes it: its name and
version, where its source comes from, what it depends on, and how to build it. Here is the
rockspec for a module that counts words, which depends on another rock, `textutil`:

```lua
-- wordfreq-0.1-1.rockspec
package = "wordfreq"
version = "0.1-1"
source = {
  url = "git+https://github.com/example/wordfreq.git",
  tag = "v0.1",
}
description = {
  summary = "Counts the words in a text.",
  license = "MIT",
}
dependencies = {
  "lua >= 5.4",
  "textutil >= 0.1",
}
build = {
  type = "builtin",
  modules = {
    wordfreq = "src/wordfreq.lua",
  },
}
```

- **`version`** has two parts: `0.1` is the version of the code, and `-1` the revision of the
  rockspec, which goes up when only the rockspec changes. The file name repeats both.
- **`source.url`** says where `luarocks` fetches the code when someone installs the rock from a
  server. For a rock you build from its own folder, it isn't used.
- **`dependencies`** lists rocks with version constraints. LuaRocks installs any that are missing
  before it builds the rock.
- **`build.modules`** maps each module name that `require` will use to its source file. The type
  `builtin` means LuaRocks needs no makefile: it copies Lua files, and compiles any C files listed
  the same way, which module 13 uses.

`luarocks lint wordfreq-0.1-1.rockspec` checks the rockspec, and fails, for example, when
`description.license` is missing.

### A tree for each project

By default, `luarocks install` puts rocks in one place shared by every project on the machine,
where two projects that need different versions of a rock collide. Pass a **tree**, a folder of
the project's own, to every command instead:

```bash
luarocks --tree lua_modules install busted     # a dependency from luarocks.org
luarocks --tree lua_modules make               # build and install this folder's rock
eval "$(luarocks path --tree lua_modules)"     # point Lua at the tree, in this shell
```

`luarocks make` reads the rockspec in the current folder, installs its missing dependencies into
the tree, and installs the rock itself. `luarocks path` prints shell commands that set
`LUA_PATH`, `LUA_CPATH`, and `PATH` so that `lua` and `require` find what the tree holds. Keep
`lua_modules` out of Git, as you would any build output: a fresh checkout recreates it with the
same commands.

## Lint with luacheck

**Lint** is a check of the source for mistakes that are legal Lua but almost never intended.
luacheck reads code without running it, and reports, among others:

```text
src/messy.lua:2:7: unused variable 'unused'
src/messy.lua:4:3: setting non-standard global variable 'sum'
src/messy.lua:5:7: unused loop variable 'i'
src/messy.lua:5:37: accessing undefined variable 'sum'
```

The second line is module 1's missing `local`, found before the program runs. luacheck exits with
a nonzero status when it reports anything, so a script or a continuous-integration job can stop
on it. A `.luacheckrc` file in the project's folder, itself a file of Lua assignments, sets the
options, for example the Lua version, and busted's globals for the specs:

```lua
std = "lua54"
files["spec"] = { std = "+busted" }
```

**Fix each finding rather than silencing it.** An unused variable is either a bug, where a name
was misspelled or a result ignored, or dead code to delete. A finding that is correct but
intended, such as the unused `self` of a method that a subclass overrides in PA4, can be
silenced on its line with a comment that names the warning, `-- luacheck: ignore 212/self`, where
212 is luacheck's code for an unused argument. Silencing everything with a broad `ignore` hides
the next real bug along with the false alarm.

## Formatting with StyLua

A **formatter** rewrites code into one layout: indentation, spaces, line breaks, and quotes. With
every file in the same layout, reviews show only the changes that matter, and nobody argues
about style. A `stylua.toml` file sets the few choices StyLua leaves open:

```toml
syntax = "Lua54"
indent_type = "Spaces"
indent_width = 2
column_width = 100
```

`syntax = "Lua54"` lets StyLua read Lua 5.4's `<close>` and `<const>`, and needs a StyLua built
with Lua 5.4 support, as [setting up](../../setup.md) describes. `stylua --check src spec` prints
the changes it would make and exits with a nonzero status if
there are any; `stylua src spec` makes them. Run the formatter before you commit, and check it in
continuous integration.

## Types with LuaCATS and lua-language-server

Lua doesn't check types until the program runs, and only on the paths it runs. **LuaCATS**
annotations, comments that start with three dashes, describe the types of parameters, results,
and fields, and **lua-language-server** checks the code against them without running it. Editors
such as VS Code and Neovim use the same server to underline mistakes as you type.

```lua
---Counts how many times each word occurs in `text`.
---@param text string
---@return table<string, integer> counts
function M.counts(text)
  -- ...
end

---@class Account
---@field balance number
---The ? after a type means the field may be nil.
---@field owner string?
```

With these annotations, `M.counts(42)` gets a warning from the checker:

```text
src/typed.lua:16:22 [Warning] Cannot assign `integer` to parameter `string`.
- `integer` cannot match `string`
- Type `integer` cannot match `string`
- Type `number` cannot match `string` (param-type-mismatch)
```

`lua-language-server --check=src --checklevel=Warning` checks a folder from the command line, and
exits with a nonzero status when it finds a problem. Annotations are only comments: Lua itself
ignores them, so they catch mistakes in code the checker can see, and a wrong value that arrives at
run time, from a file or a user, still needs a check in the code.

## Coverage with LuaCov

**Test coverage** measures which lines of a module the tests ran. `busted --coverage` records it
in `luacov.stats.out`, and `luacov` writes a report, `luacov.report.out`, that shows how many
times each line ran, and marks the lines that never ran with `*0`; when other lines ran ten times
or more, the marker grows to fill the column, as `**0`. A `.luacov` file limits the report to the
project's own modules:
`return { include = { "src/wordfreq" } }`.

```text
 1   if n < 0 then
*0     error("n must not be negative", 2)
     end
```

A line marked `*0` is a line no test exercised, so a bug there would pass every test. Add a test
that runs it; here, one that calls with a negative `n` and expects the error. Two limits keep the
number honest:

- **Coverage counts lines, not branches.** Written on one line,
  `if n < 0 then error("…", 2) end` counts as covered whenever the `if` runs, even if no test ever
  makes the condition true. Putting each branch on a line of its own, as StyLua's layout often does,
  makes the report more useful.
- **A line that ran isn't a line that was checked.** A test can run every line and assert nothing.
  Module 6's method, breaking the code on purpose and seeing whether a test fails, measures what
  coverage can't.

## Common misconceptions

| Belief | What the tool does | Example that breaks it |
| :- | :- | :- |
| `luarocks install` puts a rock in this project | Without `--tree`, it installs for the whole machine | Two projects that need different versions collide |
| A rockspec's `source.url` is used by `luarocks make` | `make` builds from the current folder | The url matters when the rock is installed from a server |
| luacheck findings are style opinions | Most are bugs: undefined globals, ignored results | `setting non-standard global variable 'sum'` is a missing `local` |
| Silencing a warning fixes it | It hides it, and the next one like it | Name the warning and the line, and only when the code is right |
| LuaCATS annotations are checked when the program runs | They are comments that only the checker reads | A number read from a file still reaches a `string` parameter |
| 100% coverage means the tests are complete | It means every line ran | `if n < 0 then error(…) end` counts as covered without a negative `n` |

## Summary

- A rockspec names a rock and its version, lists its dependencies, and maps module names to
  files; `luarocks lint` checks it, and `luarocks --tree lua_modules make` builds it into a tree of
  the project's own.
- luacheck finds legal code that is almost certainly wrong; fix each finding, and silence only a
  named warning on a single line, for a reason.
- StyLua gives every file one layout, set in `stylua.toml`; `--check` makes it a test.
- LuaCATS annotations document types, and lua-language-server checks calls against them without
  running anything.
- LuaCov shows which lines the tests never ran; it counts lines, not branches, and ran isn't the
  same as checked.

## Self-check

1. What do the two parts of the version `2.3-1` mean, and when would the second change?

   <details>
   <summary>Answer</summary>

   `2.3` is the version of the code and `1` the revision of the rockspec. The revision goes up
   when only the rockspec changes, for example to fix a dependency's version constraint.
   </details>

2. luacheck reports `accessing undefined variable 'totl'` in a function that runs fine in your
   tests. Should you silence it?

   <details>
   <summary>Answer</summary>

   No. The function reads a global that nobody sets, which is almost certainly a misspelling of a
   local, such as `total`. The tests pass only because they never reach that line, or never check
   its result.
   </details>

3. Why run `stylua --check` in continuous integration rather than only `stylua` on your machine?

   <details>
   <summary>Answer</summary>

   `--check` fails the build when any file isn't formatted, so every contributor's code stays in
   the same layout, not only yours. It changes nothing, so it can't make a commit by surprise.
   </details>

4. A function is annotated `---@param n integer`, and a caller passes a value it read from a file.
   Does the annotation protect the function?

   <details>
   <summary>Answer</summary>

   Only from mistakes the checker can see in the source. The value from the file is known only at
   run time, so the function must still check it, for example with `math.type(n) == "integer"`,
   if a wrong type would cause harm.
   </details>

5. The coverage report shows 100% for a module, and a bug is later found in its error handling.
   How is that possible?

   <details>
   <summary>Answer</summary>

   The error branch may sit on the same line as its `if`, which counts as covered whenever the
   `if` runs. Or the tests ran the line but never checked what it did. Coverage shows what never
   ran, not what works.
   </details>

## Further reading

- The [LuaRocks rockspec format](https://github.com/luarocks/luarocks/blob/main/docs/rockspec_format.md),
  for every field of a rockspec, including `install.bin`, which PA5 uses to install a command.
- The [luacheck documentation](https://luacheck.readthedocs.io/en/stable/), for the list of
  warnings and their codes, and the options of `.luacheckrc`.
- [StyLua's README](https://github.com/JohnnyMorganz/StyLua), for the options of `stylua.toml`.
- The [LuaCATS annotations](https://luals.github.io/wiki/annotations/) in lua-language-server's
  wiki, for every annotation, from `@param` to generics.
- The [LuaCov documentation](https://lunarmodules.github.io/luacov/), for the options of
  `.luacov`.
