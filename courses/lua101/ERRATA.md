# Errata

Corrections to published LUA101 material, newest first, grouped by the edition they correct, which
is named by its release date. Each entry gives the date, the file, and what changed, so you can tell
whether the version you used had the error.

## The 2026-11-25 edition

- **2026-11-25, [`setup.md`](setup.md) and the
  [final project](assignments/final-project/README.md):** building Lua with hererocks on Linux
  stopped with `readline/readline.h: No such file or directory` when the GNU Readline headers
  weren't installed, because hererocks builds Lua with readline unless told not to. `setup.md`
  now lists the headers, with the command that installs them, and says how to build without
  them. The final project's GitHub Actions workflow now passes `--no-readline`, because GitHub's
  `ubuntu-latest` machines don't have the headers.
