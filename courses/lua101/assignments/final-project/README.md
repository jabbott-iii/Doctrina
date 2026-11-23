# The final project

**Objectives:** LO-6.1–6.3, LO-11.1, LO-11.2, LO-11.4, LO-12.1, LO-12.3, and the objectives of
the track you choose: LO-13.2–13.4 (C), LO-14.2 and LO-10.3 (sandbox), or LO-14.3 (host)\
**Due:** a proposal in week 11, a milestone in week 13, and the finished project in week 15, as the
[schedule](../../README.md#schedule) gives them\
**Weight:** 20% of the course grade: the proposal 10% of that, the milestone 30%, and the finished
project 60%\
**Time:** about 25 hours, over weeks 11 to 15

The final project is a Lua program of your own design, built the way the course has taught: a rock
with tests, lint, formatting, type annotations, and coverage, and one part of it made measurably
faster. You choose one of three tracks, each of which takes one of the last modules further.

## What every project includes

- **A rock.** A rockspec that `luarocks lint` accepts and `luarocks --tree lua_modules make` builds,
  with modules in `src/` and any commands in `bin/`.
- **Tests.** busted specs in `spec/` that test every public function, its edges, and its failures,
  with a LuaCov report. Every line the report marks as never run is either tested, or explained in
  your `README.md`.
- **Clean tooling.** luacheck, `stylua --check`, and lua-language-server report nothing, and every
  public function and class carries LuaCATS annotations. Silence a finding only on its line, with
  the warning's code and a comment saying why.
- **A measured speed-up** of one hot path, in `PERFORMANCE.md`: what you measured, on what
  hardware, operating system, and Lua build, how (the number of runs, and the minimum and median),
  the change you made and why it should help, and the times before and after.
- **A `README.md`** that says what the project does, how to build, run, and test it, which track
  it follows, and which tools you used and how (see "Policies").

Run the course's checker before each submission. It builds a copy of your project and runs every
tool, as the graders will:

```bash
python courses/lua101/tools/check_project.py path/to/your/project --lpath='./src/?.lua'
```

## The tracks

### C

Extend Lua with C, or embed it (module 13). Build either:

- a **C module** that `require` loads, which exposes a C data structure as full userdata with a
  metatable: a constructor, at least three methods, `__tostring`, and `__gc`, which frees what the
  C code allocated; every function checks its arguments with `luaL_check…` and raises errors that
  name the argument; or
- a **C program that Lua scripts**, which loads a script, calls functions in it with `lua_pcall`,
  exposes at least three C functions to it, and reports a failing script without stopping.

Build the C code through the rockspec's `builtin` build. Test the Lua side with busted, and say in
your `README.md` how you checked the C side for leaks and stack balance.

### Sandbox

Run untrusted Lua, such as plugins or user scripts, inside your program (module 14). The sandbox
loads code in text mode with an environment built from an allowlist, limits instructions with a
hook and memory with a check of `collectgarbage("count")`, and gives each plugin its settings from
a data file that it parses without running it (module 10). Include a `THREATS.md` that lists the
attacks you tested, each with the test that shows it fails, and the attacks your sandbox can't stop.

### Host

Write Lua for a program that embeds it: a Neovim plugin, a LÖVE game, or a Pandoc filter (module
14). Keep the logic in modules that don't touch the host, and the host's API in a thin layer, so
that busted can test the logic with the host replaced by a stand-in table that records calls. Say
in your `README.md` which version of the host, and which Lua version or LuaJIT, the project runs
on, and what that changes in your code.

## Milestones

| Milestone | Week | What you hand in | Share of the 20% |
| :- | :- | :- | :- |
| Proposal | 11 | `PROPOSAL.md`, one page | 10% |
| Milestone | 13 | The project so far | 30% |
| Final | 15 | The finished project, and a five-minute demonstration in class | 60% |

### The proposal

One page, `PROPOSAL.md`, with these sections:

1. **What it does,** in two or three sentences, and the track.
2. **Its interface:** the modules and functions, or the commands, with one example of use each.
3. **How you will test it,** including the failures you will test.
4. **The hot path** you expect to measure, and why you expect it to matter.
5. **Risks:** what you don't know yet how to do, and your fallback if it doesn't work.

### The milestone

The project builds as a rock; its core, the part every other part depends on, works and is tested;
the tooling reports nothing; and `PERFORMANCE.md` holds a first measurement of the hot path, before
any change.

### The final project

Everything in "What every project includes", and the track's requirements. In week 15 you show it
to the class for five minutes: what it does, one test, and the speed-up.

## Rubrics

### The proposal (10 points)

| Criterion | Full marks | Partial | Little or none |
| :- | :- | :- | :- |
| **Scope** (4) | Fits the time, with the track's requirements covered: 4 points | Too large or too small, but adjustable: 2 points | Doesn't meet the track's requirements: 0 points |
| **Interface and tests** (4) | Every public function or command named, with an example, and a test plan that includes failures: 4 points | Vague in places: 2 points | Missing: 0 points |
| **Hot path and risks** (2) | A plausible hot path, and a fallback for each risk: 2 points | One of the two: 1 point | Neither: 0 points |

### The milestone (30 points)

| Criterion | Full marks | Partial | Little or none |
| :- | :- | :- | :- |
| **Builds** (6) | `luarocks lint` and `make` succeed: 6 points | Builds with a warning, or only by hand: 3 points | Doesn't build: 0 points |
| **Core works and is tested** (12) | The core does what the proposal says, and its tests pass and include failures: 12 points | Works, with thin tests: 6–9 points | Little works: 0–4 points |
| **Tooling** (6) | luacheck, StyLua, and lua-language-server report nothing: 6 points | 2 points off for each tool that reports something | — |
| **First measurement** (6) | `PERFORMANCE.md` reports a method and a baseline, with its conditions: 6 points | A number without its conditions: 3 points | Missing: 0 points |

### The final project (100 points, scaled to its 60%)

| Criterion | Full marks | Partial | Little or none |
| :- | :- | :- | :- |
| **Function and track** (30) | Does what the proposal promised, or what an agreed change promised, and meets every requirement of its track: 30 points | One requirement missing or broken: 20 points | Several missing: 10 points or fewer |
| **Tests and coverage** (20) | Tests for every public function, edge, and failure; every line never run is tested or explained: 20 points | Gaps in the failures or the edges: 10–15 points | Few tests: 5 points or fewer |
| **Package and tooling** (15) | Builds as a rock, and every tool reports nothing: 15 points | 3 points off for each tool that reports something | Doesn't build: 5 points or fewer |
| **Performance** (15) | A measured hot path, a change justified by how Lua works, and times before and after, with conditions and runs: 15 points | A speed-up without a method, or a method without a speed-up: 8 points | Missing: 0 points |
| **Design and documentation** (15) | Clear modules with one job each, LuaCATS on every public function, and a `README.md` a classmate could follow: 15 points | Works, but hard to follow or under-documented: 8–10 points | — |
| **Demonstration** (5) | Shows the program, a test, and the speed-up in five minutes: 5 points | Runs long, or skips one part: 3 points | Missing: 0 points |

## Policies

The course's [policies](../../README.md#policies) apply, with two differences that the syllabus
gives. Generative AI tools are allowed in the final project, with disclosure: your `README.md` must
say which tools you used, for which parts, and how you checked what they produced. And the final
milestone accepts no late work, except through accommodations; the proposal and the milestone use
your grace days as other assignments do. Write your own project, and cite any code you adapted, with
its license.
