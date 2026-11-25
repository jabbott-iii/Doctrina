# Setting up your environment

You need two things for this course: a Python environment that runs the lab notebooks, and a
standalone Lua 5.4 interpreter with LuaRocks, Lua's package manager, for scripts and projects. Set
up both before you start Module 1. The commands below are for Linux and macOS; on Windows, run them
inside the Windows Subsystem for Linux (WSL).

Run every command from the root folder of the repository that holds the course, the folder with
`requirements.txt` in it.

## The notebook environment

The labs are Jupyter notebooks. Their `%%lua` cells run Lua 5.4.8 through lupa, a Python package
that has the Lua interpreter built in, so the notebooks need no separate Lua.

1. Install Python 3.12 and [uv](https://docs.astral.sh/uv/), a Python package installer.
2. Create the environment and install the course's packages:

   ```bash
   uv venv .venv --python 3.12
   ```

   ```bash
   VIRTUAL_ENV=.venv uv pip install -r requirements.txt
   ```

   The second command ends by listing the packages it installed.
3. Start JupyterLab:

   ```bash
   .venv/bin/jupyter lab
   ```

   JupyterLab opens in your browser.
4. Open a lab notebook, for example `courses/lua101/modules/01-first-steps/lab01.ipynb`, and run
   its first two cells. The second prints `Lua 5.4`.

## Standalone Lua and LuaRocks

From module 1 you also run Lua scripts with the `lua` command, and from module 6 you install test
tools with LuaRocks. hererocks, which the notebook environment installed, builds both into a
folder of their own. It needs a C compiler: `gcc` or `clang` on Linux, and the Xcode Command Line
Tools on macOS (`xcode-select --install`).

1. Build Lua 5.4.8 and LuaRocks 3.13.0 into `.venv/lua`:

   ```bash
   .venv/bin/hererocks .venv/lua -l "https://github.com/lua/lua@v5.4.8" -r "https://github.com/luarocks/luarocks@v3.13.0"
   ```

   hererocks downloads both from GitHub, builds them, and ends with `Done.` The command names the
   releases from GitHub because hererocks' own list of Lua versions stops at 5.4.4. Version 5.4.8
   matches the Lua in the notebooks, so a script behaves the same in both.
2. Put the new `lua` and `luarocks` commands first on your `PATH` for this terminal:

   ```bash
   source .venv/lua/bin/activate
   ```

   Run this again in each new terminal, or add the folder `.venv/lua/bin` to your `PATH` for
   good.
3. Check the interpreter:

   ```bash
   lua -v
   ```

   It prints:

   ```text
   Lua 5.4.8  Copyright (C) 1994-2025 Lua.org, PUC-Rio
   ```

Any Lua 5.4 release works for the course, so a `lua5.4` package from your operating system's
package manager is fine too. The course's examples were checked on 5.4.8.

## Tools for later modules

Install these when the module that uses them begins:

| Tool | Module | Install |
| :- | :- | :- |
| LPeg, the parsing library | 4 | `luarocks install lpeg`, which compiles it with the C compiler from step 1 |
| busted, the test framework | 6 | `luarocks install busted` |
| luacheck, the linter, and LuaCov, the coverage tool | 11 | `luarocks install luacheck` and `luarocks install luacov` |
| StyLua, the formatter | 11 | `cargo install stylua --locked --features lua54`, or a release from [StyLua's GitHub page](https://github.com/JohnnyMorganz/StyLua); a build without `lua54` can't read `<close>` |
| lua-language-server, the type checker | 11 | A release from [lua-language-server's site](https://luals.github.io/) |
| A C compiler and the Lua headers | 13 | The compiler from step 1 above; hererocks already installed the headers in `.venv/lua/include` |

The course's examples were checked with LPeg 1.1.0, busted 2.3.0, luacheck 1.2.0, LuaCov 0.17.0,
StyLua 2.6.0, and lua-language-server 3.19.2.
