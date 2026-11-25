# LUA101 plan

**Status:** approved by the instructor on 2026-11-23, as written, and changed to a self-paced
edition on 2026-11-25.

This is the instructor's blueprint and build checklist for LUA101. It stays out of the published
course: `myst.yml` excludes it.

## Decisions so far

The instructor decided these on 2026-11-23:

- **Audience:** programmers new to Lua, who have finished one programming course in any language.
- **Length:** a 15-week term of 14 modules, about 9 hours a week, in a classroom or online.
- **Labs:** Python 3.12 notebooks whose `%%lua` cells run Lua 5.4 through the lupa package.
- **Folder:** `courses/lua101/`, following the repository's `courses/<code>/` convention.
- **Blueprint:** approved as written, including the objectives, the grading weights, the
  schedule, and the policies in section 10.
- **Installs:** all of section 8 approved. The instructor installs TeX Live.
- **Interactivity:** static pages; readers run notebooks locally (section 11).
- **Exam accessibility:** the accommodations route in section 12.

The instructor changed these on 2026-11-25, for a self-paced edition:

- **Delivery:** self-paced, with no deadlines. A suggested pace of 15 weeks at about 9 hours a week
  replaces the schedule, and each assignment follows the modules it covers.
- **Grades:** none. Every piece is checked by its published tests, rubric, or answers, and the
  grading weights are gone.
- **Exams:** the midterm and the final exam became two ungraded self-tests, published in Markdown
  with their answers in collapsed blocks: Self-test 1 after Module 7, and Self-test 2 after Module
  14. The Markdown replaced the LaTeX sources, so each has one source.
- **Final project:** replaced by a capstone project of intermediate difficulty, a Lua package that
  a student can add to a portfolio. The C, sandbox, and host tracks became optional extensions.

## 1. The course

**LUA101: Lua from Front to Back**

Lua is a small, fast scripting language built to be embedded in other programs. It runs game
logic, editor plugins in Neovim, scripts inside Redis, filters in Pandoc, and web handlers in
OpenResty. This course takes programmers who already know one language from their first Lua
program to embedding Lua in C. Students write Lua 5.4 in notebooks and in real projects, and learn
the language's central idea, the table, which serves as array, record, module, object, and class.
They then use closures, metatables, and coroutines to build abstractions, and package, test, lint,
and measure their code with the community's standard tools. The last third extends Lua with C,
embeds it in a C program, runs untrusted code in a sandbox, and adapts code to the other Lua
versions and hosts students will meet at work.

## 2. Prerequisites

Students must have finished one programming course in any language, such as Python, Java,
JavaScript, or C, and have used Git and a terminal. Module 13 asks students to read and write short
C functions; its reading explains the C it uses.

**Self-check.** A student who can do all five, in any language, is ready:

1. Write a function that returns the largest number in a list, and a test that calls it.
2. Explain what happens to a list passed to a function that appends to it.
3. Write a recursive function, and say what happens when it recurses too deeply.
4. Run a program from a terminal with a file path as its argument, and read its error message.
5. Clone a Git repository, change a file, and commit the change.

## 3. Learning objectives

### Course objectives

By the end of the course, students can:

- **LO-1:** Write, run, and debug Lua 5.4 programs, predicting how Lua's types, operators, control
  flow, and functions behave.
- **LO-2:** Represent data with tables, and process text with the string library and Lua
  patterns.
- **LO-3:** Build abstractions with closures, iterators, metatables, and classes, and justify
  which one a design calls for.
- **LO-4:** Structure programs as tested modules that report failures by Lua's conventions, and
  handle files, the operating system, and outside data safely.
- **LO-5:** Implement cooperative concurrency with coroutines.
- **LO-6:** Package, lint, document, test, and measure Lua code with the community's standard
  tools, and speed up a hot path on the evidence of measurements.
- **LO-7:** Extend Lua with C, and embed Lua in a C program, keeping the stack balanced and errors
  contained.
- **LO-8:** Adapt code to the Lua version and host it runs in, and run untrusted code in a
  sandbox, stating what the sandbox can't stop.

### Module objectives

Each module objective serves the course objective in brackets.

**Module 1: First steps** [LO-1]

- **LO-1.1:** Run Lua code three ways (the interactive interpreter, a script file, and a notebook
  `%%lua` cell), and use a runtime error message to find the failing line.
- **LO-1.2:** Predict the type and value of expressions over `nil`, booleans, numbers, and
  strings, including the integer or float result of `/`, `//`, and `%`.
- **LO-1.3:** Declare variables with `local`, and explain the bug that a missing `local` causes.
- **LO-1.4:** Apply Lua's rule that only `nil` and `false` are false to predict conditions and the
  results of `and` and `or`.

**Module 2: Control flow and functions** [LO-1]

- **LO-2.1:** Write loops with `while`, `repeat`, the numeric `for`, and the generic `for`, choose
  among them, and predict each loop's bounds and the scope of its variables.
- **LO-2.2:** Write functions that take varargs and return several results, and predict how Lua
  adjusts those results in assignments, calls, and table constructors.
- **LO-2.3:** Write recursive functions, and identify which calls are proper tail calls.
- **LO-2.4:** Design a function that takes a table of named options with defaults, and explain
  when `x or default` gives the wrong result.

**Module 3: Tables** [LO-2]

- **LO-3.1:** Build and traverse sequences, records, and nested tables with constructors,
  `ipairs`, `pairs`, and the `table` library.
- **LO-3.2:** Predict the length operator `#` on a sequence, explain why it is unreliable on a
  table with holes, and keep an explicit count instead.
- **LO-3.3:** Predict the effects of assigning and passing tables, which are references, and write
  a shallow and a deep copy.
- **LO-3.4:** Implement a stack, a queue, a set, and a matrix with tables, and compare the cost of
  their operations.

**Module 4: Strings and patterns** [LO-2]

- **LO-4.1:** Transform text with the string library, including negative indices,
  `string.format`, and method-call syntax on strings.
- **LO-4.2:** Write Lua patterns with character classes, quantifiers, anchors, captures, `%b`, and
  `%f`, and use them with `find`, `match`, `gmatch`, and `gsub`.
- **LO-4.3:** Explain how Lua patterns differ from regular expressions, and rewrite a regular
  expression that uses alternation as Lua code.
- **LO-4.4:** Build long strings with `table.concat`, and count and walk UTF-8 text with the
  `utf8` library.

**Module 5: Closures and iterators** [LO-3]

- **LO-5.1:** Predict the output of closures that capture and share local variables, including
  loop variables.
- **LO-5.2:** Implement higher-order functions (map, filter, reduce, compose) and memoization with
  closures.
- **LO-5.3:** Write stateful and stateless iterators for the generic `for`, and explain the four
  values the generic `for` keeps: the iterator function, the state, the control value, and the
  closing value.

**Module 6: Errors, modules, and tests** [LO-4]

- **LO-6.1:** Signal failures with `error` and `assert`, catch them with `pcall` and `xpcall`, and
  choose between raising an error and returning `nil, message`.
- **LO-6.2:** Write a module as a table it returns, load it with `require`, and explain the roles
  of `package.path` and `package.loaded`.
- **LO-6.3:** Write busted tests that check a module's results and its failure paths.

**Module 7: Metatables** [LO-3]

- **LO-7.1:** Give tables new behavior with arithmetic, comparison, concatenation, `__tostring`,
  `__len`, and `__call` metamethods.
- **LO-7.2:** Use `__index` and `__newindex`, as tables and as functions, for default values,
  proxies, and read-only tables, with `rawget` and `rawset` where the metamethod must be bypassed.
- **LO-7.3:** Use a weak table (`__mode`) for a cache that doesn't keep its keys alive, and
  explain when the collector clears an entry.

**Module 8: Objects and classes** [LO-3]

- **LO-8.1:** Implement a class whose metatable's `__index` is the class, with a constructor and
  methods called with `:`.
- **LO-8.2:** Implement single inheritance, compare it with composition, and defend one of them
  for a given design.
- **LO-8.3:** Hide an object's state in closures, and compare closure-based objects with
  metatable-based ones in memory use and flexibility.

**Module 9: Coroutines** [LO-5]

- **LO-9.1:** Trace a coroutine's status and the values passed through `resume` and `yield`.
- **LO-9.2:** Implement generators and producer–consumer pipelines with coroutines.
- **LO-9.3:** Build a cooperative scheduler for tasks that wait on timers, and explain why one
  task that never yields stops all of them.

**Module 10: Files, the operating system, and data** [LO-4]

- **LO-10.1:** Read and write files with the `io` library, and close them on every path with
  `<close>` variables.
- **LO-10.2:** Use the `os` library for times, dates, environment variables, and files, and
  explain why passing outside input to `os.execute` is dangerous.
- **LO-10.3:** Parse and write a data format (CSV, and Lua values written with `%q`) without
  running data as code.

**Module 11: Packages and tooling** [LO-6]

- **LO-11.1:** Set up a project with LuaRocks: write a rockspec, install dependencies into a
  project tree, and build the rock.
- **LO-11.2:** Lint and format code with luacheck and StyLua, and fix each finding instead of
  suppressing it.
- **LO-11.3:** Document an API with LuaCATS annotations, and check it with lua-language-server.
- **LO-11.4:** Measure test coverage with LuaCov, and add tests for the lines it reports as never
  run.

**Module 12: Performance and memory** [LO-6]

- **LO-12.1:** Measure running time and memory with `os.clock` and `collectgarbage("count")` over
  repeated runs, and report the results with the hardware and Lua version.
- **LO-12.2:** Explain how Lua stores tables (an array part and a hash part) and strings, and
  predict the relative cost of common operations.
- **LO-12.3:** Speed up a measured hot path, and justify each change with a measurement.

**Module 13: Lua and C** [LO-7]

- **LO-13.1:** Trace the Lua C API's stack through a sequence of push, read, and call operations.
- **LO-13.2:** Write a C function that Lua can call, which checks its arguments and returns
  results, and build it as a C module that `require` loads.
- **LO-13.3:** Embed Lua in a C program that runs a script and calls its functions with
  `lua_pcall`, handling errors without aborting.
- **LO-13.4:** Expose a C struct to Lua as full userdata with a metatable and a `__gc`
  metamethod.

**Module 14: Versions, sandboxes, and hosts** [LO-8]

- **LO-14.1:** Port code among Lua 5.4, Lua 5.1, LuaJIT, and Lua 5.5, detecting features instead
  of assuming them.
- **LO-14.2:** Run untrusted Lua in a sandbox built from an allowlist environment, `load` in text
  mode, and an instruction-count hook, and name what the sandbox can't stop.
- **LO-14.3:** Write Lua against a host's API, test it with the host replaced by a stand-in, and
  explain how the host's Lua version, globals, and event loop shape the code.

## 4. Modules

Most modules take about 9 hours: about 2.5 for the reading, 2 for the lab, 1.5 for the practice,
and 3 for the assignment or self-test that follows. Module 7 takes 8, with 2 for Self-test 1, and
Module 8 takes 6. Every module has the same four pieces:

| Piece | File | Format | Why this format |
| :- | :- | :- | :- |
| Reading | `modules/NN-<slug>/index.md` | Markdown | Prose with short Lua examples; nothing to run in the page |
| Lab | `labNN.ipynb`, paired with `labNN.py` | Jupyter notebook | Students run, change, and rerun Lua in `%%lua` cells, and `assert` checks each answer |
| Practice | `practice.md` | Markdown | Exercises with collapsed hints and visible answers, for retrieval practice |
| Figures | drawn by code in the course | SVG or PNG from code | Only where a figure teaches something; each has alternative text |

| # | Module | Objectives | Depends on | Hours | Lab's main activity |
| :- | :- | :- | :- | :- | :- |
| 1 | First steps | LO-1.1–1.4 | none | 9 | Predict, then run, the type and value of 20 expressions; fix a missing `local` |
| 2 | Control flow and functions | LO-2.1–2.4 | 1 | 9 | Varargs and multiple results; measure recursion depth with and without tail calls |
| 3 | Tables | LO-3.1–3.4 | 2 | 9 | Watch `#` change as holes appear; build a queue and time it against `table.remove(t, 1)` |
| 4 | Strings and patterns | LO-4.1–4.4 | 3 | 9 | Parse a log file with patterns; time `..` in a loop against `table.concat` |
| 5 | Closures and iterators | LO-5.1–5.3 | 2, 3 | 9 | Build counters, memoize Fibonacci and count calls, write a range iterator |
| 6 | Errors, modules, and tests | LO-6.1–6.3 | 5 | 9 | Turn a script into a module, then catch and classify its errors |
| 7 | Metatables | LO-7.1–7.3 | 3, 5 | 9 | A vector type with operators; a read-only proxy; watch a weak cache empty after collection |
| 8 | Objects and classes | LO-8.1–8.3 | 7 | 9 | A class, a subclass, and the same design by composition, compared |
| 9 | Coroutines | LO-9.1–9.3 | 5, 6 | 9 | Generators, a pipeline of filters, and a scheduler with timers |
| 10 | Files, the OS, and data | LO-10.1–10.3 | 6 | 9 | Read and write CSV with `<close>`; serialize a table with `%q` and read it back safely |
| 11 | Packages and tooling | LO-11.1–11.4 | 6 | 9 | Shell cells that create a rock, then lint, format, annotate, and measure coverage |
| 12 | Performance and memory | LO-12.1–12.3 | 3, 4, 7 | 9 | Benchmark table growth, string building, and local caching; read collector statistics |
| 13 | Lua and C | LO-13.1–13.4 | 6, 7 | 9 | Shell cells that compile a C module and a C host program against Lua 5.4 |
| 14 | Versions, sandboxes, and hosts | LO-14.1–14.3 | 6, 9, 10 | 9 | Run one file on lupa's Lua 5.1, 5.4, 5.5, and LuaJIT; build and attack a sandbox |

Modules 11 and 13 need the standalone Lua 5.4, LuaRocks, and a C compiler, because their tools
work on files and programs outside a notebook. Their labs run those tools from Python cells.

## 5. Assessment

The self-paced edition has no grades. Every piece comes with a way to check it:

| Piece | Objectives | Checked by |
| :- | :- | :- |
| Labs 1–14 | Each module's own | Every visible check in the notebook passes |
| PA1–PA2: notebook assignments | PA1: LO-1.1, 1.2, 1.4, 2.1–2.4. PA2: LO-3.1–3.4, 4.1, 4.2, 4.4, 2.2 | Visible tests in `%%lua` cells. The hidden tests stay in `solutions/`, for a reviewer |
| PA3–PA5: Lua projects | See below | Published example tests and rubrics. The hidden busted tests and the broken versions stay in `solutions/`, for a reviewer |
| Self-test 1, after Module 7 | LO-1.1–7.2 | 14 questions, 75 points, 75 minutes, no computer; answers and scoring notes in the page |
| Self-test 2, after Module 14 | All modules, weighted toward 8–14 | 20 questions, 105 points, 125 minutes, no computer; answers and scoring notes in the page |
| Capstone project | LO-6.1–6.3, LO-11.1–11.4, LO-12.1, LO-12.3, and its idea's objectives | Checklists at the proposal and the milestone, a three-level rubric at the release, and `tools/check_project.py` |

- **PA1: Numbers and functions** (notebook, after Module 2): Collatz step counts,
  integer-or-float formatting, a recursive digit sum, a tail-recursive greatest common divisor,
  and a function with named options.
- **PA2: Tables and text** (notebook, after Module 4): word frequencies, a set type built on
  tables, run-length encoding, and a UTF-8-aware reverse.
- **PA3: An iterator library** (Lua project, after Module 6; LO-5.2, 5.3, 6.1–6.3, revisits
  LO-3.1, 4.2): a module of lazy iterators (`map`, `filter`, `take`, `zip`) and `memoize`, with
  the student's own busted tests.
- **PA4: A discrete-event simulation** (Lua project, after Module 10; LO-7.1, 7.2, 8.1, 8.2, 9.2,
  9.3, revisits LO-5.3, 6.3): classes for customers and servers, and a coroutine scheduler that
  runs a queue simulation with a fixed random seed, so the output can be checked exactly.
- **PA5: A command-line tool** (Lua project, after Module 12; LO-10.1, 10.3, 11.1–11.4, revisits
  LO-4.2, 6.1, 8.1): a rock that prints statistics for each column of a CSV file, with a
  rockspec, no luacheck findings, StyLua formatting, LuaCATS annotations, and coverage measured.
- **Capstone project** (proposal after Module 11, milestone after Module 13, release after Module
  14): a Lua package of the student's design, from five ideas in the brief or one of their own,
  released as version 1.0.0 for a portfolio. Every project is a rock with busted tests, coverage,
  clean tooling, LuaCATS annotations, and a measured speed-up of one hot path (LO-12.1, 12.3),
  plus a `README.md` written for a stranger, a license, a changelog, a tag, and a GitHub Actions
  workflow. The C, sandbox, and host tracks of the old final project are optional extensions.

Later pieces revisit earlier objectives, and Self-test 2 mixes question types from every module,
so students practice choosing a method as well as applying one.

**Answer keys** go in `courses/lua101/solutions/`, as the repository's teaching rule already
decided (committed, never linked from coursework, and never built into the website): nbgrader
sources for PA1 and PA2, model solutions and hidden tests for PA3–PA5, rubrics with model
answers, and the capstone's reviewers' notes. The self-tests publish their own answers, so they
have no separate key. The rubrics' criteria are published with each assignment.

## 6. Alignment

Every objective is taught before it is assessed, and assessed at least once beyond its lab.

| Objective | Taught | Assessed |
| :- | :- | :- |
| LO-1.1, LO-1.2, LO-1.4 | Module 1 | Lab 1, PA1, Self-test 1 |
| LO-1.3 | Module 1 | Lab 1, Self-test 1 |
| LO-2.1, LO-2.3 | Module 2 | Lab 2, PA1, Self-test 1 |
| LO-2.2 | Module 2 | Lab 2, PA1, PA2, Self-test 1 |
| LO-2.4 | Module 2 | Lab 2, PA1 |
| LO-3.1 | Module 3 | Lab 3, PA2, PA3, Self-test 1 |
| LO-3.2 | Module 3 | Lab 3, PA2, Self-test 1 |
| LO-3.3 | Module 3 | Lab 3, PA2, Self-test 1, Self-test 2 |
| LO-3.4 | Module 3 | Lab 3, PA2 |
| LO-4.1 | Module 4 | Lab 4, PA2 |
| LO-4.2 | Module 4 | Lab 4, PA2, PA3, PA5, Self-test 1 |
| LO-4.3 | Module 4 | Lab 4, Self-test 1 |
| LO-4.4 | Module 4 | Lab 4, PA2, Self-test 2 |
| LO-5.1 | Module 5 | Lab 5, Self-test 1, Self-test 2 |
| LO-5.2 | Module 5 | Lab 5, PA3 |
| LO-5.3 | Module 5 | Lab 5, PA3, PA4 |
| LO-6.1 | Module 6 | Lab 6, PA3, PA5, Self-test 1, capstone |
| LO-6.2 | Module 6 | Lab 6, PA3, capstone |
| LO-6.3 | Module 6 | Lab 6, PA3, PA4, PA5, capstone |
| LO-7.1, LO-7.2 | Module 7 | Lab 7, PA4, Self-test 1 |
| LO-7.3 | Module 7 | Lab 7, Self-test 2 |
| LO-8.1 | Module 8 | Lab 8, PA4, PA5, Self-test 2 |
| LO-8.2 | Module 8 | Lab 8, PA4, Self-test 2 |
| LO-8.3 | Module 8 | Lab 8, Self-test 2 |
| LO-9.1 | Module 9 | Lab 9, Self-test 2 |
| LO-9.2, LO-9.3 | Module 9 | Lab 9, PA4, Self-test 2 |
| LO-10.1 | Module 10 | Lab 10, PA5 |
| LO-10.2 | Module 10 | Lab 10, Self-test 2 |
| LO-10.3 | Module 10 | Lab 10, PA5, Self-test 2 |
| LO-11.1–LO-11.4 | Module 11 | Lab 11, PA5, capstone |
| LO-12.1, LO-12.3 | Module 12 | Lab 12, capstone, Self-test 2 |
| LO-12.2 | Module 12 | Lab 12, Self-test 2 |
| LO-13.1, LO-13.4 | Module 13 | Lab 13, Self-test 2 |
| LO-13.2, LO-13.3 | Module 13 | Lab 13, Self-test 2, capstone (C extension) |
| LO-14.1 | Module 14 | Lab 14, Self-test 2 |
| LO-14.2 | Module 14 | Lab 14, Self-test 2, capstone (sandbox extension) |
| LO-14.3 | Module 14 | Lab 14, Self-test 2, capstone (host extension) |

Self-test 1 follows Module 7, so it covers modules 1–7. The capstone's ideas add objectives of
their own, which its brief lists.

## 7. Suggested pace

The self-paced edition has no deadlines. This pace takes 15 weeks at about 9 hours a week:

| Week | Module | Then |
| :- | :- | :- |
| 1 | 1: First steps | |
| 2 | 2: Control flow and functions | PA1 |
| 3 | 3: Tables | |
| 4 | 4: Strings and patterns | PA2 |
| 5 | 5: Closures and iterators | |
| 6 | 6: Errors, modules, and tests | PA3 |
| 7 | 7: Metatables | Self-test 1 (modules 1–7) |
| 8 | 8: Objects and classes | |
| 9 | 9: Coroutines | |
| 10 | 10: Files, the OS, and data | PA4 |
| 11 | 11: Packages and tooling | Capstone proposal |
| 12 | 12: Performance and memory | PA5 |
| 13 | 13: Lua and C | Capstone milestone |
| 14 | 14: Versions, sandboxes, and hosts | Self-test 2 (all modules) |
| 15 | The capstone project | Capstone release |

## 8. Environment

**Lua version:** Lua 5.4 throughout, with Lua 5.1, LuaJIT 2.1, and Lua 5.5 compared in module 14.

Each item needs the instructor's approval before it is installed or added:

| Item | Where | Why |
| :- | :- | :- |
| `requirements.txt` at the repository root, pinning `jupyterlab`, `ipykernel`, `jupytext`, `nbgrader`, `nbmake`, `pytest`, `lupa`, `jupyter-book`, and `hererocks` | `.venv/`, created with `uv` | The labs, their checks, the graded notebooks, and the website |
| `lualab`, a small helper written for this course that adds the `%%lua` cell magic | `courses/lua101/lualab/`, installed from `requirements.txt` | Runs each cell in one Lua 5.4 state that persists between cells, prints to the notebook, and turns Lua errors into failed cells; `%%lua --version 5.1` runs a cell on lupa's other runtimes |
| Lua 5.4 and LuaRocks, built by hererocks | `.venv/lua/` (ignored by Git) | Modules 6 and 11–13, the Lua projects, and checking every example outside the notebooks |
| The rocks busted, luacheck, and luacov | LuaRocks, into `.venv/lua/` | Tests, lints, and coverage for modules 6 and 11 and the projects |
| The rock lpeg 1.1.0-2, added on 2026-11-25 | LuaRocks, into `.venv/lua/` | Module 4's LPeg section; `setup.md` installs it with the other tools |
| StyLua and lua-language-server | `cargo install stylua`, and the lua-language-server release from GitHub | Module 11's formatting and type checks |
| TeX Live with LuaLaTeX, `latexmk`, `chktex`, and the `exam` class | You run `sudo apt install texlive-luatex texlive-latex-extra latexmk chktex`, which needs your password | The two exams and their keys; no longer needed since the self-paced edition of 2026-11-25, which has no LaTeX documents |

Until 2026-11-25, LaTeX packages beyond the preamble: `listings` for Lua code (it knows Lua up to
5.3, which covers everything the exams show), `fontspec`, `xcolor`, and `hyperref`. All four ship
with TeX Live.

## 9. Sources

Confirmed on 2026-11-23:

| Source | Why it is here |
| :- | :- |
| Ierusalimschy, de Figueiredo, and Celes, *Lua 5.4 Reference Manual*, <https://www.lua.org/manual/5.4/> | The definition of the language; every module links its sections |
| Ierusalimschy, *Programming in Lua*, 4th edition, Lua.org, 2016 (ISBN 978-85-903798-6-7) | The standard textbook, written for Lua 5.3; recommended, not required, because it costs money |
| Ierusalimschy, de Figueiredo, and Celes, *Lua 5.5 Reference Manual*, <https://www.lua.org/manual/5.5/> | Module 14's comparison of versions |
| Ierusalimschy, de Figueiredo, and Celes, "The Evolution of Lua," HOPL III, 2007, doi:10.1145/1238844.1238846 | Module 1: why Lua is small and built around tables |
| Ierusalimschy, de Figueiredo, and Celes, "A Look at the Design of Lua," *Communications of the ACM* 61(11), 2018, doi:10.1145/3186277 | Modules 1 and 7: the mechanisms Lua offers instead of features |
| de Moura and Ierusalimschy, "Revisiting Coroutines," *ACM TOPLAS* 31(2), 2009, doi:10.1145/1462166.1462167 | Module 9: asymmetric coroutines and what they can express |
| Ierusalimschy, de Figueiredo, and Celes, "Passing a Language through the Eye of a Needle," *Communications of the ACM* 54(7), 2011, doi:10.1145/1965724.1965739 | Module 13: why the C API is built around a stack |
| Ierusalimschy, de Figueiredo, and Celes, "The Implementation of Lua 5.0," *Journal of Universal Computer Science* 11(7), 2005, 1159–1176, <https://www.lua.org/doc/jucs05.pdf> | Module 12: the array and hash parts of tables, and the register-based virtual machine |
| Ierusalimschy, "Lua Performance Tips," chapter 2 of *Lua Programming Gems*, Lua.org, 2008, <https://www.lua.org/gems/sample.pdf> | Module 12: measured advice on tables, strings, and locals |
| Ierusalimschy, "A Text Pattern-Matching Tool Based on Parsing Expression Grammars," *Software: Practice and Experience* 39(3), 2009, doi:10.1002/spe.892 | Module 4: LPeg, the next step when Lua patterns aren't enough |
| The documentation of LuaRocks, busted, luacheck, StyLua, lua-language-server, LuaCov, LuaJIT and its FFI, lupa, Neovim's Lua guide, and Redis's Lua scripting | The tools and hosts each module uses |

The first edition of *Programming in Lua* is free at <https://www.lua.org/pil/>, but it describes
Lua 5.0, so the course doesn't assign it.

## 10. Policies

Approved as drafted on 2026-11-23, and revised for the self-paced edition on 2026-11-25. The
syllabus states them plainly.

- **Pace:** the course is self-paced and has no deadlines; the suggested pace is a guide. This
  replaces the late-work policy of grace days and daily penalties.
- **Collaboration and academic integrity:** discuss ideas with anyone, but write your own code and
  answers. Don't share or look at another learner's solution. Name everyone you discussed an
  assignment with, and cite any code you adapted.
- **Generative AI tools:** allowed for explaining concepts, error messages, and documentation, and
  in the capstone project with disclosure. Not for writing any part of a lab, programming
  assignment, or self-test answer. Every assignment, and the capstone's `README.md`, ends with a
  short note saying which tools were used and how, or "none".
- **Accommodations:** every page is HTML or Markdown, which screen readers can read, and nothing is
  timed except the self-tests' suggested sittings, which a learner can lengthen. A learner who
  takes the course through an institution arranges any other accommodations through its disability
  services office. This wording is a draft for the instructor to confirm.

## 11. Interactivity

Decided on 2026-11-23: the published pages don't run code. Students download each notebook and run
it in their own environment. In-page execution through Binder (`jupyter: true`) is possible, because
lupa installs from `requirements.txt`, but it depends on a public Binder service and on where the
course is hosted. JupyterLite (`lite: true`) can't run these labs, because lupa is a compiled Python
extension that JupyterLite's browser-based Python can't load.

## 12. Exam accessibility

Decided on 2026-11-23: the exams weren't published on the website, and an accessible version went
to each student who needed one through the accommodations process. Resolved on 2026-11-25: the
self-tests that replaced the exams are Markdown pages, which screen readers can read, so no PDF
needs tagging.

## Build notes

Choices made while building, on 2026-11-23, within the approved plan:

- **Lua releases:** the standalone interpreter is Lua 5.4.8 with LuaRocks 3.13.0, built by
  hererocks from the GitHub tags, because hererocks' own list stops at Lua 5.4.4. Lua 5.4.8 is
  also the release lupa 2.8 bundles, so notebooks and scripts behave alike. lupa's other
  runtimes are Lua 5.1.5, 5.5.1, and LuaJIT 2.1.
- **`lualab`:** captures standard output and standard error at the file-descriptor level while a
  cell runs, so `print`, `io.write`, and `io.stdout:write` behave as in `lua`. A cell that is one
  expression shows its values, as `lua -i` does. It disables `os.exit`, which would end the
  kernel. Its tests are in `lualab/test_lualab.py`.
- **Lab answer keys:** each lab's answer cells carry an `answer-<id>` tag, and the key in
  `solutions/labs/labNN_answers.py` holds a cell with the same tag. `tools/check_lab.py` runs the
  lab as students get it (only cells tagged `raises-exception` may fail) and again with the key
  (no cell may fail).
- **Exercise IDs:** practice exercises are numbered `Exercise 1.4`, and lab exercises
  `Exercise L1.4`, so the two never collide.
- **Exam sources:** each exam's LaTeX source holds its key in `solution` environments, so the
  sources live in `solutions/exams/`, not in `exams/`. Superseded on 2026-11-25: the self-tests
  replaced them.
- **Website URLs:** `site.options.folders` is on, so pages keep their folders in their URLs
  (MyST drops the number prefix): `modules/first-steps/practice`.
- **Further reading:** DOI links go to the publisher's page (`dl.acm.org/doi/…`), because MyST
  turns `doi.org` links into automatic citations that repeat the reference.
- **Graded notebooks:** the source in `solutions/paN/` holds the solutions and hidden tests,
  and `tools/student_version.py` writes the student version to `assignments/paN/`. The source
  must pass `nbgrader validate`; the student version must fail it on every graded cell, which
  shows that no problem passes untouched. `pytest --nbmake` runs the sources, not the student
  versions, which fail at their first stub by design. A problem that asks students to debug code
  shows the broken code in a locked cell tagged `raises-exception`, because nbgrader replaces
  every solution region with a stub.
- **Assignments on the website:** each student version is in the `toc`, so students can read
  and download it there.
- **Figures:** the notebook environment has no plotting package, so labs show results as
  printed tables. Adding matplotlib needs the instructor's approval.
- **Timed checks:** Lab 3, Lab 4, and PA2's hidden tests time a function on a large input, to
  tell an $O(n)$ solution from an $O(n^2)$ one. Each limit is at least 11 times what the model
  solution took on an Intel Core i7-11800H with lupa 2.8, and well under what the slow solution
  took; `solutions/pa2/README.md` lists the measurements.
- **Lua projects:** each project's handout, starter module, and example tests are in
  `assignments/paN/`, and the website publishes the handout with the starter files as downloads.
  `solutions/paN/` holds the model solution, the hidden busted tests in blocks that name their
  points, a model student test suite, and `grading.json`, which names the module and lists broken
  versions of the model. `tools/grade_project.py` runs the hidden tests one block at a time, and
  runs the student's tests against the broken versions, for the rubric's Tests criterion; its
  `--self-test` checks the grader and the model together.
- **StyLua with Lua 5.4:** `cargo install stylua` without `--features lua54` builds a StyLua that
  can't parse `<close>` or `<const>`. The course's StyLua was rebuilt with the feature on
  2026-11-23, `setup.md` installs it that way, and every `stylua.toml` sets `syntax = "Lua54"`.
- **PA5's tooling:** `grading.json` can list several files (PA5's module and command), extra busted
  options, and `"tooling": true`, which makes `tools/grade_project.py` also run luarocks, luacheck,
  StyLua, lua-language-server, and LuaCov on the whole submission. PA5's rubric replaces Design,
  Tests, and Style with Tests, Package and tools, and Design and style, each 10 points, so that the
  tools of LO-11.1 to LO-11.4 count; the instructor may change that split.
- **Links to files on the website:** Markdown links to starter files with ordinary extensions
  (`.lua`, `.csv`, `.toml`) become downloads. A link to a dotfile such as `.luacheckrc` crashed the
  HTML export, and every later build failed until `_build/site` and `_build/cache` were deleted; so
  handouts name dotfiles and extensionless scripts without linking them.
- **Final project** (superseded on 2026-11-25 by the capstone project, below): the brief is
  `assignments/final-project/README.md`, with its rubrics, and
  `solutions/final-project/README.md` holds the graders' notes and the sandbox attacks to try. The
  split of the project's 20% (proposal 10%, milestone 30%, final 60%), the rubrics' points, and
  letting the proposal and the milestone use grace days are drafts for the instructor to confirm.
  `tools/check_project.py` runs the tooling checks on any project, for students and graders.
- **Rubric split:** PA3's 30 rubric points are split equally among Tests, Design, and Style, 10
  each. The approved plan gives only the 70/30 split, so the instructor may change this one.
- **LO-5.3's wording:** the objective says the generic `for` keeps three values, but Lua 5.4
  keeps four: the iterator function, the state, the control value, and a closing value. Module 5
  teaches all four, the three that drive the loop first; the objective's wording is the
  instructor's to change. Resolved on 2026-11-25: the instructor approved naming all four.
- **Two builds of Lua 5.4:** hererocks builds the standalone `lua` with `LUA_COMPAT_5_3`, as the
  makefile in Lua's own source release does (checked in 5.4.4), so it has `math.pow` and derives
  `<=` from `__lt`; lupa's Lua has neither. The standalone `lua` also starts its garbage collector
  in generational mode, and lupa in incremental mode. The materials rely on neither difference:
  Module 7 tells students to define `__le`, and every lab that depends on garbage collection
  controls it with `collectgarbage`. Module 12 should explain both. lupa's Lua also lacks
  `io.popen` (`'popen' not supported`), and its `os.execute` returns the raw wait status, 768 for
  `exit 3`; Module 10 says so, and Lab 10 uses `os.execute` with output to a file instead.
- **Exams** (superseded on 2026-11-25 by the self-tests, below): each exam's LaTeX source, with
  its key, is in `solutions/exams/`, with a
  `latexmkrc` that builds with LuaLaTeX and finds the shared preamble. The preamble's `\code`
  reads its code verbatim, as `\code|…|`, so Lua's `%` and `#` need no escapes. In the `exam`
  class, a question whose parts have points must not have points of its own, or they are counted
  twice.
- **Two interpreters, two speeds:** an early measurement found the standalone `lua` three times
  slower than lupa's Lua at `table.remove` (1.25 s against 0.39 s). Repeated later, with the
  machine's load average near 15 on 16 hardware threads, the gap ranged from none to about two
  times, and most of Module 12's benchmarks ran equally fast in both. The standalone `lua` is
  statically linked and compiled with `-O2`; the cause of the early gap wasn't found, and load is
  the likeliest. Module 12 says so, and compares numbers only within one interpreter.
- **C in Lab 13:** lupa's Lua can't load a C module (`undefined symbol: lua_settop`), because it
  lives inside a Python extension that doesn't export Lua's functions. Lab 13 therefore compiles
  with the system's `cc` and runs the standalone `lua`, which exports them; hosts link
  `.venv/lua/lib/liblua54.a`. Linking that library into a module fails (`recompile with -fPIC`).
  The lab's macOS flags (`-bundle -undefined dynamic_lookup`) follow the reading but weren't tested
  here; the lab ran on Linux with gcc 13.3.0. Measured facts the module uses: a host that never pops
  a result fails only after 999,996 passes, at `LUAI_MAXSTACK`; and with 169 MB of Lua tables,
  20,000 dropped bit sets holding 125 KB each were all still alive, because the collector doesn't
  see memory C allocated.
- **Sandboxes in Lab 14:** each attack runs in a new standalone `lua` process with a time limit,
  because a plugin the sandbox fails to stop would otherwise freeze the kernel. Measured: a plugin
  that recurses through `pcall` to the C stack's limit (197 levels) leaves no room to call a Lua
  hook, and a sandbox without a guarded `pcall` didn't stop it in 10 s; finalizers run with hooks
  off; a plugin's own coroutine ran 10 million iterations unhooked; with LuaJIT's compiler on, the
  count hook never stopped an endless loop (5 s), and after `jit.off()` it did in 2 ms. Lua 5.5
  printed floats with 17 digits where 14 don't read back (`0.1 + 0.2` as `0.30000000000000004`),
  which the manual doesn't list. LÖVE's Lua is unconfirmed (love2d.org refused automated reads),
  so the reading doesn't state it, and the project's grading notes mark it `[citation needed]`.
- **Final exam** (superseded on 2026-11-25 by Self-test 2): `solutions/exams/final.tex`, 19
  questions, 100 points, 120 minutes, with 81
  points on modules 8–14 and one question for each objective the alignment table sends to the
  final exam. Its grade table runs down the page (`\gradetable[v][pages]`), because 14 pages
  across overflowed the line. Every Lua answer was run on Lua 5.4.8, the porting answer on all four
  Luas, and the C answers compiled with gcc 13.3.0. chktex reports only warnings caused by the Lua
  and shell code in listings, as for the midterm. Whether it is closed book is still open, as for
  the midterm.

## Build notes for the self-paced edition

Choices made on 2026-11-25, within the instructor's decisions above:

- **Self-tests:** `self-tests/self-test-1.md` and `self-test-2.md`, converted from the exams'
  LaTeX by a script for the `exam` class's commands, then proofread. Every inline code span and
  listing carried over: 170 and 9 in Self-test 1, 198 and 24 in Self-test 2. Each question keeps
  its number, objectives, and points, which the page says are for scoring oneself. The website
  lists each self-test after the module it follows.
- **Question 20 of Self-test 2** is new, for LO-14.3, which only the old final project's host
  track had assessed beyond Lab 14. Its answer's busted test passed with busted 2.3.0 on Lua 5.4.8,
  and failed on a broken version; lupa's LuaJIT 2.1 confirmed that `//` and `<const>` don't
  compile there and that `utf8` and `math.type` are `nil`.
- **Removed:** `solutions/exams/` and `latex/preamble.sty`, which only the exams used.
  `latex/macros.tex` stays, because the teaching rule keeps the notation's macros there.
- **Where each piece falls:** after the module whose reading already gave it time: PA1 after
  Module 2, PA2 after 4, PA3 after 6, PA4 after 10, PA5 after 12, Self-test 1 after 7, and
  Self-test 2 after 14. The capstone's proposal comes after Module 11, its milestone after 13, and
  its release after 14. Modules 7 and 8 lost the midterm's hours: Module 7 now takes 8 hours, with
  2 for Self-test 1, and Module 8 takes 6.
- **Hidden tests stay private.** The handouts of PA1–PA5 now say the course has no grades, that
  the hidden tests aren't published, and that a reviewer can run them. Publishing them, for
  learners working alone, is the instructor's decision; PA3–PA5's broken versions are edits of the
  model solutions, so they can't be published without the keys.
- **Capstone project:** the brief keeps its path, `assignments/final-project/README.md`, so links to
  it keep working. Its continuous integration workflow copies its steps from
  `.github/workflows/lua101.yml`; the YAML parses, and its luacheck and busted commands passed on a
  sample project, but the workflow hasn't run on GitHub. `solutions/final-project/README.md`
  became reviewers' notes, with the sandbox attacks kept for the optional sandbox extension.
- **Errata and the teaching rule:** `ERRATA.md` now groups corrections by edition, named by release
  date. The **Course structure** and **Errata** values in `.claude/rules/teaching-materials.md`
  now allow a self-paced course.
- **Checks on 2026-11-25:** Labs 1 and 7 ran as students get them and with their keys; PA1's and
  PA2's sources ran under `pytest --nbmake` and passed `nbgrader validate`, their regenerated
  student versions failed it on every graded cell and matched the committed ones; PA3–PA5's
  graders passed their self-tests, each catching 10 of 10 broken versions; and the website built 54
  pages. The built site holds no nbgrader markers, no text from this plan or the reviewers' notes,
  and no model-solution code; its only lines shared with the hidden tests are in the published
  example specs.

## Gaps closed on 2026-11-25

A review on 2026-11-25 found topics that an advanced Lua course should teach and LUA101 didn't. The
instructor approved closing them. Each fits an existing objective, so no objective was added:

- **`_ENV`** (LO-14.2), at the start of Module 14's "The environment": globals as fields of
  `_ENV`, `local _ENV` for a block, and `load`'s environment argument as the chunk's `_ENV`. Lua
  5.1 and LuaJIT have no `_ENV`; with lupa's runtimes, `local _ENV = {}` left their globals
  unchanged. Exercise 14.8, and two rows in the versions table.
- **LuaJIT's FFI** (LO-14.1), a section of Module 14 after "Detect features, not versions":
  `ffi.cdef`, `ffi.C`, `ffi.new`, 0-based arrays, and detection with `pcall(require, "ffi")`. On
  lupa's LuaJIT 2.1, `strlen` came back as `5ULL`, a read past an array's end raised no error, and
  `#` and `ipairs` on a C array raised errors. Two claims cite LuaJIT's documentation, confirmed on
  2026-11-25: FFI calls can be inlined in compiled code, unlike C API calls (`ext_ffi.html`), and
  the FFI allows out-of-bounds access (`ext_ffi_semantics.html`). Exercise 14.7. Module 14 now
  takes about 10 hours.
- **`package.searchers`** (LO-6.2), in Module 6 after "How `require` finds and keeps modules": the
  four searchers, the loader's second argument (`:preload:` for `package.preload`), and a searcher
  of one's own. Exercise 6.8.
- **`string.pack` and `string.unpack`** (LO-10.3), in Module 10's "Data formats". Lua 5.1 and
  LuaJIT lack them; `i16` is the widest integer code. Exercise 10.7.
- **LO-5.3** now names all four values the generic `for` keeps.
- **LPeg** (LO-4.3), a section of Module 4 after "Patterns are not regular expressions": building
  patterns with `P`, `R`, `S`, and operators, captures with `/` and `Ct`, a grammar for two kinds
  of nested brackets, ordered choice, and the `re` module. Exercise 4.8, a misconception row, and
  a row in `setup.md`'s table of tools. Module 4 now takes about 10 hours.
- **How LPeg was checked:** its rockspec downloads the source from LPeg's home server, which refused
  connections on 2026-11-25, and LuaRocks.org showed a notice of a security incident in September
  2026. With the instructor's approval, `luarocks download --source` fetched `lpeg-1.1.0-2.src.rock`
  (78,933 bytes, dated 2024-09-13) from LuaRocks.org instead. Its tarball's MD5 matched the
  rockspec's, its files were LPeg's C sources, `re.lua`, and its manuals, and the rockspec's build
  only compiles those sources. It was built into a scratch tree, not `.venv/lua/`; installing by
  name, as `setup.md` tells students, also fetched that source rock. Every example ran on LPeg
  1.1.0 with Lua 5.4.8. The notebooks can't load LPeg, so the section's examples run as scripts.

Every new example and answer ran on Lua 5.4.8 or lupa's LuaJIT 2.1, and printed what the text
says. The labs are unchanged.

## Build checklist

Tick each line once its piece passes its checks.

- [x] Environment: `requirements.txt`, `.venv/`, `lualab`, standalone Lua 5.4, rocks, and tools
- [x] Layout: syllabus (`README.md`), `notation.md`, `references.bib`, `ERRATA.md`, `myst.yml`,
  `latex/preamble.sty`, `latex/macros.tex`, and `.gitignore` entries
- [x] Module 1: reading, lab, and practice
- [x] Module 2: reading, lab, and practice
- [x] PA1: graded notebook source, student version, and key
- [x] Module 3: reading, lab, and practice
- [x] Module 4: reading, lab, and practice
- [x] PA2: graded notebook source, student version, and key
- [x] Module 5: reading, lab, and practice
- [x] Module 6: reading, lab, and practice
- [x] PA3: handout, starter code, hidden tests, model solution, and rubric
- [x] Module 7: reading, lab, and practice
- [x] Midterm exam and key (replaced by Self-test 1 on 2026-11-25)
- [x] Module 8: reading, lab, and practice
- [x] Module 9: reading, lab, and practice
- [x] PA4: handout, starter code, hidden tests, model solution, and rubric
- [x] Module 10: reading, lab, and practice
- [x] Module 11: reading, lab, and practice
- [x] PA5: handout, starter code, hidden tests, model solution, and rubric
- [x] Module 12: reading, lab, and practice
- [x] Final project: brief, milestones, and rubric (replaced by the capstone on 2026-11-25)
- [x] Module 13: reading, lab, and practice
- [x] Module 14: reading, lab, and practice
- [x] Final exam and key (replaced by Self-test 2 on 2026-11-25)
- [x] Whole-course checks: notebooks, LaTeX, website build, leak search, alignment, answers,
  accessibility, links, and the rules' checks
- [x] Self-paced edition: syllabus, suggested pace, policies, module times, and handouts
- [x] Self-test 1 and Self-test 2, from the exams, with Question 20 added
- [x] Capstone project: brief, checkpoints, rubric, and reviewers' notes
- [x] Self-paced edition: whole-course checks
- [x] Gaps: `_ENV` and LuaJIT's FFI (Module 14), `package.searchers` (Module 6), `string.pack`
  (Module 10), and LO-5.3's wording
- [x] Gap: LPeg in Module 4
