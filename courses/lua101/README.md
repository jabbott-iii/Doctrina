# LUA101: Lua from Front to Back

Lua is a small, fast scripting language built to be embedded in other programs: it runs game
logic, editor plugins in Neovim, scripts inside Redis, filters in Pandoc, and web handlers in
OpenResty. This course is for programmers who already know one language and are new to Lua. It
starts at the first Lua program and ends with embedding Lua in C. Along the way you learn the
language's central idea, the table, which serves as array, record, module, object, and class. You
use closures, metatables, and coroutines to build abstractions, and you package, test, lint, and
measure your code with the tools Lua programmers use at work. The last third extends Lua with C,
runs untrusted code in a sandbox, and adapts code to the other Lua versions and hosts you will
meet. The course teaches Lua 5.4. It is self-paced, with no deadlines and no grades: 14 modules,
two self-tests, and a capstone project, a Lua package for your portfolio.

Start with [setting up your environment](setup.md).

## Learning objectives

By the end of the course, you can:

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

Each module's objectives serve the course objective in brackets. Every exercise, lab, and
self-test question names the objectives it tests.

### Module 1: First steps [LO-1]

- **LO-1.1:** Run Lua code three ways (the interactive interpreter, a script file, and a notebook
  `%%lua` cell), and use a runtime error message to find the failing line.
- **LO-1.2:** Predict the type and value of expressions over `nil`, booleans, numbers, and
  strings, including the integer or float result of `/`, `//`, and `%`.
- **LO-1.3:** Declare variables with `local`, and explain the bug that a missing `local` causes.
- **LO-1.4:** Apply Lua's rule that only `nil` and `false` are false to predict conditions and the
  results of `and` and `or`.

### Module 2: Control flow and functions [LO-1]

- **LO-2.1:** Write loops with `while`, `repeat`, the numeric `for`, and the generic `for`, choose
  among them, and predict each loop's bounds and the scope of its variables.
- **LO-2.2:** Write functions that take varargs and return several results, and predict how Lua
  adjusts those results in assignments, calls, and table constructors.
- **LO-2.3:** Write recursive functions, and identify which calls are proper tail calls.
- **LO-2.4:** Design a function that takes a table of named options with defaults, and explain
  when `x or default` gives the wrong result.

### Module 3: Tables [LO-2]

- **LO-3.1:** Build and traverse sequences, records, and nested tables with constructors,
  `ipairs`, `pairs`, and the `table` library.
- **LO-3.2:** Predict the length operator `#` on a sequence, explain why it is unreliable on a
  table with holes, and keep an explicit count instead.
- **LO-3.3:** Predict the effects of assigning and passing tables, which are references, and write
  a shallow and a deep copy.
- **LO-3.4:** Implement a stack, a queue, a set, and a matrix with tables, and compare the cost of
  their operations.

### Module 4: Strings and patterns [LO-2]

- **LO-4.1:** Transform text with the string library, including negative indices,
  `string.format`, and method-call syntax on strings.
- **LO-4.2:** Write Lua patterns with character classes, quantifiers, anchors, captures, `%b`, and
  `%f`, and use them with `find`, `match`, `gmatch`, and `gsub`.
- **LO-4.3:** Explain how Lua patterns differ from regular expressions, and rewrite a regular
  expression that uses alternation as Lua code.
- **LO-4.4:** Build long strings with `table.concat`, and count and walk UTF-8 text with the
  `utf8` library.

### Module 5: Closures and iterators [LO-3]

- **LO-5.1:** Predict the output of closures that capture and share local variables, including
  loop variables.
- **LO-5.2:** Implement higher-order functions (map, filter, reduce, compose) and memoization with
  closures.
- **LO-5.3:** Write stateful and stateless iterators for the generic `for`, and explain the four
  values the generic `for` keeps: the iterator function, the state, the control value, and the
  closing value.

### Module 6: Errors, modules, and tests [LO-4]

- **LO-6.1:** Signal failures with `error` and `assert`, catch them with `pcall` and `xpcall`, and
  choose between raising an error and returning `nil, message`.
- **LO-6.2:** Write a module as a table it returns, load it with `require`, and explain the roles
  of `package.path` and `package.loaded`.
- **LO-6.3:** Write busted tests that check a module's results and its failure paths.

### Module 7: Metatables [LO-3]

- **LO-7.1:** Give tables new behavior with arithmetic, comparison, concatenation, `__tostring`,
  `__len`, and `__call` metamethods.
- **LO-7.2:** Use `__index` and `__newindex`, as tables and as functions, for default values,
  proxies, and read-only tables, with `rawget` and `rawset` where the metamethod must be bypassed.
- **LO-7.3:** Use a weak table (`__mode`) for a cache that doesn't keep its keys alive, and
  explain when the collector clears an entry.

### Module 8: Objects and classes [LO-3]

- **LO-8.1:** Implement a class whose metatable's `__index` is the class, with a constructor and
  methods called with `:`.
- **LO-8.2:** Implement single inheritance, compare it with composition, and defend one of them
  for a given design.
- **LO-8.3:** Hide an object's state in closures, and compare closure-based objects with
  metatable-based ones in memory use and flexibility.

### Module 9: Coroutines [LO-5]

- **LO-9.1:** Trace a coroutine's status and the values passed through `resume` and `yield`.
- **LO-9.2:** Implement generators and producer–consumer pipelines with coroutines.
- **LO-9.3:** Build a cooperative scheduler for tasks that wait on timers, and explain why one
  task that never yields stops all of them.

### Module 10: Files, the operating system, and data [LO-4]

- **LO-10.1:** Read and write files with the `io` library, and close them on every path with
  `<close>` variables.
- **LO-10.2:** Use the `os` library for times, dates, environment variables, and files, and
  explain why passing outside input to `os.execute` is dangerous.
- **LO-10.3:** Parse and write a data format (CSV, and Lua values written with `%q`) without
  running data as code.

### Module 11: Packages and tooling [LO-6]

- **LO-11.1:** Set up a project with LuaRocks: write a rockspec, install dependencies into a
  project tree, and build the rock.
- **LO-11.2:** Lint and format code with luacheck and StyLua, and fix each finding instead of
  suppressing it.
- **LO-11.3:** Document an API with LuaCATS annotations, and check it with lua-language-server.
- **LO-11.4:** Measure test coverage with LuaCov, and add tests for the lines it reports as never
  run.

### Module 12: Performance and memory [LO-6]

- **LO-12.1:** Measure running time and memory with `os.clock` and `collectgarbage("count")` over
  repeated runs, and report the results with the hardware and Lua version.
- **LO-12.2:** Explain how Lua stores tables (an array part and a hash part) and strings, and
  predict the relative cost of common operations.
- **LO-12.3:** Speed up a measured hot path, and justify each change with a measurement.

### Module 13: Lua and C [LO-7]

- **LO-13.1:** Trace the Lua C API's stack through a sequence of push, read, and call operations.
- **LO-13.2:** Write a C function that Lua can call, which checks its arguments and returns
  results, and build it as a C module that `require` loads.
- **LO-13.3:** Embed Lua in a C program that runs a script and calls its functions with
  `lua_pcall`, handling errors without aborting.
- **LO-13.4:** Expose a C struct to Lua as full userdata with a metatable and a `__gc`
  metamethod.

### Module 14: Versions, sandboxes, and hosts [LO-8]

- **LO-14.1:** Port code among Lua 5.4, Lua 5.1, LuaJIT, and Lua 5.5, detecting features instead
  of assuming them.
- **LO-14.2:** Run untrusted Lua in a sandbox built from an allowlist environment, `load` in text
  mode, and an instruction-count hook, and name what the sandbox can't stop.
- **LO-14.3:** Write Lua against a host's API, test it with the host replaced by a stand-in, and
  explain how the host's Lua version, globals, and event loop shape the code.

## Prerequisites

You need one finished programming course in any language, such as Python, Java, JavaScript, or C,
and some practice with Git and a terminal. Module 13 asks you to read and write short C functions;
its reading explains the C it uses.

**Self-check.** If you can do all five of these, in any language, you are ready:

1. Write a function that returns the largest number in a list, and a test that calls it.
2. Explain what happens to a list passed to a function that appends to it.
3. Write a recursive function, and say what happens when it recurses too deeply.
4. Run a program from a terminal with a file path as its argument, and read its error message.
5. Clone a Git repository, change a file, and commit the change.

## Suggested pace

The course is self-paced, so it has no deadlines: take as long as you need. This pace takes 15
weeks at about 9 hours a week. Most modules take about 9 hours: about 2.5 for the reading, 2 for
the lab, 1.5 for the practice, and 3 for the assignment or self-test that follows, as each module's
reading says. Modules 7 and 8 take less, and Modules 4 and 14 take about 10.

| Week | Topic | Reading | Then |
| :- | :- | :- | :- |
| 1 | First steps | [Module 1](modules/01-first-steps/index.md) | |
| 2 | Control flow and functions | [Module 2](modules/02-control-flow-and-functions/index.md) | [PA1](assignments/pa1/pa1.ipynb) |
| 3 | Tables | [Module 3](modules/03-tables/index.md) | |
| 4 | Strings and patterns | [Module 4](modules/04-strings-and-patterns/index.md) | [PA2](assignments/pa2/pa2.ipynb) |
| 5 | Closures and iterators | [Module 5](modules/05-closures-and-iterators/index.md) | |
| 6 | Errors, modules, and tests | [Module 6](modules/06-errors-modules-and-tests/index.md) | [PA3](assignments/pa3/README.md) |
| 7 | Metatables | [Module 7](modules/07-metatables/index.md) | [Self-test 1](self-tests/self-test-1.md), on modules 1–7 |
| 8 | Objects and classes | [Module 8](modules/08-objects-and-classes/index.md) | |
| 9 | Coroutines | [Module 9](modules/09-coroutines/index.md) | |
| 10 | Files, the operating system, and data | [Module 10](modules/10-files-os-and-data/index.md) | [PA4](assignments/pa4/README.md) |
| 11 | Packages and tooling | [Module 11](modules/11-packages-and-tooling/index.md) | The [capstone project](assignments/final-project/README.md)'s proposal |
| 12 | Performance and memory | [Module 12](modules/12-performance-and-memory/index.md) | [PA5](assignments/pa5/README.md) |
| 13 | Lua and C | [Module 13](modules/13-lua-and-c/index.md) | The capstone project's milestone |
| 14 | Versions, sandboxes, and hosts | [Module 14](modules/14-versions-sandboxes-and-hosts/index.md) | [Self-test 2](self-tests/self-test-2.md), on all modules |
| 15 | The capstone project | [The brief](assignments/final-project/README.md) | The capstone project's release |

## Checking your work

The course has no grades. Instead, every piece comes with a way to check it, so you can tell what
you have learned and what to review:

| Piece | How you check it | Objectives |
| :- | :- | :- |
| Labs 1–14 | Every check cell in the notebook passes | Each lab's module |
| PA1: Numbers and functions (notebook) | Its visible tests | LO-1.1, LO-1.2, LO-1.4, LO-2.1–2.4 |
| PA2: Tables and text (notebook) | Its visible tests | LO-3.1–3.4, LO-4.1, LO-4.2, LO-4.4, LO-2.2 |
| PA3: An iterator library (Lua project) | Its example tests, your own tests, and its rubric | LO-5.2, LO-5.3, LO-6.1–6.3, LO-3.1, LO-4.2 |
| PA4: A discrete-event simulation (Lua project) | Its example tests, your own tests, and its rubric | LO-7.1, LO-7.2, LO-8.1, LO-8.2, LO-9.2, LO-9.3, LO-5.3, LO-6.3 |
| PA5: A command-line tool (Lua project) | Its example tests, your own tests, its rubric, and the course's project checker | LO-10.1, LO-10.3, LO-11.1–11.4, LO-4.2, LO-6.1, LO-8.1 |
| Self-test 1, after Module 7 | The answers and scoring notes in the page | Modules 1–7 |
| Self-test 2, after Module 14 | The answers and scoring notes in the page | All modules, weighted toward modules 8–14 |
| Capstone project: proposal, milestone, and release | The brief's checklists and rubric, and the course's project checker | LO-6.1–6.3, LO-11.1–11.4, LO-12.1, LO-12.3, and those of the idea you choose |

- **The notebook assignments** (PA1 and PA2) check your answers with visible tests, which you can
  run as often as you like.
- **The Lua projects** (PA3–PA5) each publish example tests and a rubric. Write your own tests for
  every promise in the handout, as each handout asks, and score your work with the rubric.
- **The assignments' hidden tests aren't published.** They stay with the answer keys, for an
  instructor or a mentor who reviews your work, so test the cases each statement describes
  yourself.
- **The self-tests** mix questions from many modules. Take each in one sitting, without notes, then
  open the answers and score yourself.
- **The capstone project** is a LuaRocks package of your own design, of intermediate size, built to
  show in a portfolio: tested, linted, documented, measured, released as version 1.0.0, and
  checked by continuous integration. If you want more, it can grow into C, a sandbox, or a host,
  as Modules 13 and 14 teach.

Later pieces revisit earlier objectives on purpose, so that you keep practicing them.

## Policies

- **Pace:** the course is self-paced and has no deadlines. The suggested pace is a guide, not a
  requirement.
- **Collaboration and academic integrity:** discuss ideas with anyone, but write your own code and
  answers. Don't share or look at another learner's solution. Name everyone you discussed an
  assignment with, and cite any code you adapted.
- **Generative AI tools:** you may use them to explain concepts, error messages, and
  documentation, and in the capstone project with disclosure. Don't use them to write any part of
  a lab, a programming assignment, or a self-test answer: doing that work yourself is how the
  course teaches. End every assignment, and your capstone's `README.md`, with a short note saying
  which tools you used and how, or "none".
- **Accommodations:** every page of the course is HTML or Markdown, which screen readers can read,
  and nothing is timed except the self-tests' suggested sittings, which you can lengthen as you
  need. If you take the course through an institution, its disability services office arranges
  any other accommodations, through the learning management system.

## Course materials

- [Notation and conventions](notation.md)
- [Errata](ERRATA.md): corrections to published material, by edition
- Text and figures are under the Creative Commons Attribution 4.0 International license (CC BY
  4.0), and code is under the MIT License in the repository's `LICENSE` file.
