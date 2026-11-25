# Capstone project: a Lua package for your portfolio

**Objectives:** LO-6.1–6.3, LO-11.1–11.4, LO-12.1, LO-12.3, and the objectives of the idea you
choose, which the table below lists\
**When:** a proposal after Module 11, a milestone after Module 13, and the release after Module 14,
as the [suggested pace](../../README.md#suggested-pace) places them\
**Checking your work:** the course's project checker, and the checklists and rubric below\
**Time:** about 25 hours: about 2 for the proposal, 10 more by the milestone, and 13 more for the
release

The capstone project is a Lua package that you design, build, and release as version 1.0.0,
finished well enough to show an employer. It is of intermediate size: it uses what Modules 1–12
teach, from tables and patterns to packaging and measuring, and it needs no C. The Lua projects
showed that you can meet a handout's specification. A portfolio project shows how you work: how you
scope a problem, test it, document it, and measure it. So this brief asks for the quality of PA5,
plus what a stranger needs to trust and use your code: a clear `README.md`, a license, a changelog,
a tagged release, and continuous integration (CI), which runs your checks on every change you push.

## Choose an idea

Pick one of these ideas, or propose your own of a similar size. Each lists the objectives it
practices beyond the ones every project does, and a hot path worth measuring.

| Idea | What it does | Objectives it adds | A hot path to measure |
| :- | :- | :- | :- |
| A log analyzer | A command that reads web-server access logs, filters the lines by status, path, or time, and prints the busiest paths and the share of each status code | LO-4.2, LO-10.1, LO-10.2 | Parsing each line |
| A template engine | A module that renders text templates with `{{name}}` fields, sections that repeat for each item of a list, and HTML escaping, without ever running a template as Lua code | LO-4.2, LO-5.2, LO-10.3 | Rendering one template many times, before and after compiling it once into closures |
| A configuration reader | A module that reads INI files into tables, checks them against a schema of types and defaults, and reports every error with its line number | LO-2.4, LO-4.2, LO-6.1, LO-10.3 | Reading a file of many thousands of lines |
| A Markdown-subset converter | A command that turns headings, paragraphs, emphasis, lists, inline code, and links into HTML, and escapes everything else | LO-4.2, LO-4.4, LO-10.1 | Converting a long document, and how the output is built |
| A collections library | A module of data structures built with metatables: a priority queue on a binary heap, a least-recently-used (LRU) cache, and a set with `+`, `-`, and `__tostring` | LO-3.4, LO-7.1, LO-7.2, LO-8.1 | Pushing and popping the heap, against sorting a list after every push |

An idea of your own works if it has a small core you can finish in about 10 hours, that busted can
test, and a loop that runs often enough to measure. Avoid ideas whose core needs something the
course didn't teach, such as a network protocol or a graphical interface.

## What every project includes

- **A rock.** A rockspec, versioned `1.0.0-1` at release, that `luarocks lint` accepts and
  `luarocks --tree lua_modules make` builds, with modules in `src/` and any commands in `bin/`.
- **Tests.** busted specs in `spec/` that test every public function, its edges, and its failures,
  with a LuaCov report. Every line the report marks as never run is either tested, or explained in
  your `README.md`.
- **Clean tooling.** luacheck, `stylua --check`, and lua-language-server report nothing, and every
  public function and class carries LuaCATS annotations. Silence a finding only on its line, with
  the warning's code and a comment saying why.
- **A measured speed-up** of one hot path, in `PERFORMANCE.md`: what you measured, on what
  hardware, operating system, and Lua build, how (the number of runs, and the minimum and median),
  the change you made and why it should help, and the times before and after.
- **A `README.md` written for a stranger.** Its first paragraph says what the package does and who
  it is for. Then come how to install it, one example of use with its real output copied from a
  run, the public functions or the command's options, and how to run the tests and the checks.
  End with design notes (two or three decisions you made, and what each trades away), the
  package's known limitations, and which tools you used and how (see "Policies").
- **A license.** A `LICENSE` file with an open-source license, such as the MIT License, named
  again in the rockspec's `description.license`.
- **A changelog and a release.** A `CHANGELOG.md` whose entry for 1.0.0 says what the release
  does, and a Git tag, `v1.0.0`, on the commit you release.
- **Continuous integration.** A GitHub Actions workflow that runs luacheck and busted on every
  push, and passes on the tagged commit.

## Continuous integration

GitHub Actions runs a workflow, a YAML file in `.github/workflows/`, on GitHub's machines whenever
you push. This one builds the course's Lua 5.4.8 and LuaRocks with hererocks, installs busted and
luacheck, and runs both. Save it as `.github/workflows/check.yml`, and add `bin` to the luacheck
line if your project has commands:

```yaml
# Run the linter and the tests on every push and pull request.
name: "check"

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0 # v7.1.0
        with:
          python-version: "3.12"
      - name: "Build Lua 5.4.8 and LuaRocks 3.13.0"
        run: |
          pip install hererocks==0.25.1
          hererocks .lua -l "https://github.com/lua/lua@v5.4.8" -r "https://github.com/luarocks/luarocks@v3.13.0"
      - name: "Install busted and luacheck"
        run: |
          .lua/bin/luarocks install busted 2.3.0-1
          .lua/bin/luarocks install luacheck 1.2.0-1
      - name: "Lint"
        run: .lua/bin/luacheck src spec
      - name: "Test"
        run: .lua/bin/busted --lpath='./src/?.lua'
```

Each `uses:` line names an action by the hash of one exact commit, with its version in a comment,
so the workflow runs the same code every time. Add `.lua/` to your `.gitignore`, so a local run of
the same commands doesn't commit the built Lua.

## Checking your project

Run the course's checker before each checkpoint. It builds a copy of your project and runs every
tool, as a reviewer would:

```bash
python courses/lua101/tools/check_project.py path/to/your/project --lpath='./src/?.lua'
```

It prints `ok` or `FAIL` for each check: the rockspec's lint and build, luacheck, StyLua,
lua-language-server, the tests, and each file's coverage.

## Checkpoints

| Checkpoint | When | What you have |
| :- | :- | :- |
| Proposal | After Module 11 | `PROPOSAL.md`, one page |
| Milestone | After Module 13 | The core, working, tested, packaged, and checked by CI |
| Release | After Module 14 | Version 1.0.0, tagged, with everything in "What every project includes" |

### The proposal

One page, `PROPOSAL.md`, with these sections:

1. **What it does,** in two or three sentences, who would use it, and which idea it follows.
2. **Its interface:** the modules and functions, or the commands, with one example of use each.
3. **How you will test it,** including the failures you will test.
4. **The hot path** you expect to measure, and why you expect it to matter.
5. **Risks:** what you don't know yet how to do, and your fallback if it doesn't work.

Before you build, check that the core fits in about 10 hours, that every public function or command
has an example, that the test plan includes failures, and that the hot path runs often enough to
measure. If not, cut the core down until it does.

### The milestone

- `luarocks lint` accepts the rockspec, and `luarocks --tree lua_modules make` builds it.
- The core works, and its tests pass, failures included.
- luacheck, StyLua, and lua-language-server report nothing.
- The CI workflow runs on every push, and passes.
- `PERFORMANCE.md` holds a first measurement of the hot path, before any change.

### The release

Everything in "What every project includes", with the tag `v1.0.0` on the commit you release. Then
ask someone who hasn't seen the project to install it and run your `README.md`'s example, using
only the `README.md`. Whatever stops them is the next thing to fix.

## Publishing it

A portfolio project needs a place where others can see it, usually a public repository on GitHub.
Publishing is your choice. Before you make the repository public, check that it holds no secrets,
no one's personal data, and nothing you don't have the right to share, and that every piece of
code you adapted is cited with its license. Point the rockspec's `source.url` at the repository,
and its `source.tag` at `v1.0.0`, as Module 11 shows.

## Going further

These extensions are optional. Each takes one of the last modules further, and makes the project
stand out, but none is needed for a finished capstone.

- **C** (Module 13): move the hot path into a C module that `require` loads, built through the
  rockspec's `builtin` build, with arguments checked by `luaL_check…` functions and errors that
  name the argument. Measure it against the Lua version, and say in your `README.md` how you
  checked the C side for leaks and for a balanced stack.
- **Sandbox** (Module 14): let users supply code, such as template helpers or plugins, and run it
  loaded in text mode, with an environment built from an allowlist and a limit on instructions.
  Add a `THREATS.md` that lists the attacks you tested, each with the test that shows it fails, and
  the attacks your sandbox can't stop.
- **Host** (Module 14): ship a thin layer that runs the package inside a host, such as a Neovim
  plugin or a Pandoc filter, tested with the host replaced by a stand-in. Say which version of the
  host, and which Lua version or LuaJIT, it runs on, and what that changes in your code.

## Rubric

Score your release with this rubric. The course has no grades: the levels show how close each
part is to ready for a portfolio.

| Criterion | Portfolio-ready | Almost there | Not yet |
| :- | :- | :- | :- |
| **Function** | Does what `PROPOSAL.md` promised, or what a change recorded in `CHANGELOG.md` promised | One promise missing or broken | Several missing |
| **Tests and coverage** | Tests for every public function, edge, and failure; every line never run is tested or explained | Gaps in the failures or the edges | Few tests |
| **Package and tooling** | Builds as a rock, and every tool reports nothing | One tool reports something | Doesn't build |
| **Performance** | A measured hot path, a change justified by how Lua works, and times before and after, with conditions and runs | A speed-up without a method, or a method without a speed-up | Missing |
| **Design** | Clear modules with one job each, failures reported by Lua's conventions, and LuaCATS on every public function | Works, but hard to follow in places | Hard to follow throughout |
| **`README.md`** | A stranger can install the package and run its example from the `README.md` alone, and the design notes explain real trade-offs | Complete, but unclear in places | Missing installation, an example, or the design notes |
| **Release** | `LICENSE`, `CHANGELOG.md`, the tag `v1.0.0`, and CI passing on the tagged commit | One of the four missing | Two or more missing |

## Policies

The course's [policies](../../README.md#policies) apply. Generative AI tools are allowed in the
capstone project, with disclosure: your `README.md` must say which tools you used, for which parts,
and how you checked what they produced. A portfolio is a claim about your own work, so be exact
about what you wrote. Write your own project, and cite any code you adapted, with its license.
