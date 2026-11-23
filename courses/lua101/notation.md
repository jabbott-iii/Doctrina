# Notation and conventions

This page lists the conventions the course's readings, labs, and exams share. Each symbol's LaTeX
macro is in `latex/macros.tex`, and the website defines the same macros in `myst.yml`.

## Code

- Lua code, names, and values are in code font: `local x = 1`, `table.concat`, `nil`.
- A comment that starts with `-->` shows what a line prints or what an expression is:

  ```lua
  print(7 // 2)   --> 3
  print(7 / 2)    --> 3.5
  ```

  When `print` gets several values, it separates them with tabs; a `-->` comment shows them
  separated by spaces.
- Exercise 1.4 is the fourth exercise in module 1's practice, and Exercise L1.4 is the fourth in
  Lab 1. Neither number ever changes once published.
- A line that starts with `>` is typed at the interactive interpreter (`lua -i`), and the lines
  under it are what the interpreter prints.
- "Lua" means Lua 5.4. Other versions are named: Lua 5.1, LuaJIT, Lua 5.5.

## Symbols

| Symbol | Meaning | LaTeX macro |
| :- | :- | :- |
| $n$ | The number of elements in a table or characters in a string | none |
| $O(n)$ | Big-O notation: the cost grows at most in proportion to $n$, for large $n$ | `\bigO{n}` |

The Markdown pages write $O(n)$ out in full, because GitHub's math renderer doesn't know the
course's macros. The LaTeX documents and the website accept either form.
