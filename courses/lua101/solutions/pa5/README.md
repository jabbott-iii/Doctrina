# PA5 answer key and grading notes

Students receive `assignments/pa5/`: the handout, stubs of `src/csvstats.lua` and `bin/csvstats`,
two example tests, a sample CSV file, and the project's `.luacheckrc`, `stylua.toml`, and
`.luacov`. They write the rockspec. This folder holds the model project and what grades it:

| File | What it is |
| :- | :- |
| `csvstats-1.0-1.rockspec`, `src/csvstats.lua`, `bin/csvstats` | The model project, with its tool settings |
| `hidden_spec.lua` | The hidden tests: 22 tests in five blocks, worth 70 points |
| `spec/csvstats_spec.lua` | A model student test suite, which catches all 10 broken versions with 100% coverage |
| `grading.json` | The settings for `tools/grade_project.py`, with `tooling` turned on |

## Grading a submission

From the repository's root, with the notebook environment active, run the grader on the
submission's project folder:

```bash
python courses/lua101/tools/grade_project.py courses/lua101/solutions/pa5 path/to/submission
```

It prints three parts. The hidden tests and the broken versions work as in PA3 and PA4. The third
part, **Tooling**, copies the whole submission and reports whether `luarocks lint` accepts the
rockspec, whether `luarocks --tree lua_modules make` builds it, whether luacheck, `stylua --check`,
and lua-language-server report anything, and the coverage the submission's own tests reach on
`src/csvstats.lua`. The rubric's **Tests** and **Package and tools** criteria follow from that
output; read the code for annotations on every public function, for silenced warnings, and for
**Design and style**.

The self-test should give 70.00 of 70 points, catch all 10 broken versions, pass every tool, and
show 100.00% coverage:

```bash
python courses/lua101/tools/grade_project.py courses/lua101/solutions/pa5 --self-test
```

The hidden tests of the command run `lua bin/csvstats` through the shell, with `LUA_PATH` set to
`./src/?.lua`, so the grader needs the course's standalone `lua` on its `PATH`; the script adds
`.venv/lua/bin` itself. They need Linux or macOS.

## Reasoning and common mistakes

- **`read`'s line numbers** count every line, empty ones included, so the counter goes up before
  the test for an empty line. Counting only the lines that aren't empty is one of the broken
  versions.
- **Missing values:** the empty string must be counted before anything else. A `Column:add` that
  passes `""` to `tonumber` gets `nil`, and then treats the field as text, which makes every column
  with a missing value a text column.
- **A number column needs every value to be a number.** The model keeps the texts and the numbers
  in two lists and compares their lengths; a column with `"1"` and `"x"` is text.
- **Ties for `top`:** `pairs` visits the values in no fixed order, so the comparison must break
  ties alphabetically on its own, as the model's `text < top` does.
- **The command's streams and status:** errors go to standard error and exit with 1; the usage
  message exits with 2. Printing errors with `print` passes a test that only checks the status, so
  the hidden tests check both streams.
- **LuaCATS and `io.open`:** lua-language-server types `io.open`'s message as `string?`, so a
  `---@return` that promises a string makes it report `return-type-mismatch` on
  `return nil, err`. The model writes `err or (path .. ": cannot open")`; changing the annotation
  to `string?` is equally correct.
- **StyLua and `<close>`:** a StyLua built without its `lua54` feature can't parse `<close>`, and
  fails with an "unexpected token" error at the `<`. The starter's `stylua.toml` sets
  `syntax = "Lua54"`, and `setup.md` installs StyLua with that feature; a student whose StyLua still
  fails needs to reinstall it, not to remove `<close>`.
