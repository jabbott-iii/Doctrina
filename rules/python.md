---
paths:
  - "**/*.py"
  - "**/*.pyi"
  - "**/pyproject.toml"
  - "uv.lock"
  - "poetry.lock"
  - "pylock*.toml"
  - "**/requirements*.txt"
  - "**/requirements*.in"
  - "setup.cfg"
  - "tox.ini"
  - "pytest.ini"
  - "mypy.ini"
  - "pyrightconfig.json"
  - "ruff.toml"
  - ".ruff.toml"
  - ".python-version"
---

# Python standards

These rules cover the Python in this repository: packages, scripts, command-line tools, tests, type
stubs, and the project files around them. They describe how a senior engineer writes Python.
Docstrings, error messages, and other text follow `writing.md` in this folder.

Apply them to code you write or edit. Don't rewrite existing code only to make it conform; fix a
passage when you are already changing it, and mention anything else you notice.

## Project details

A repository fills in this section when it adopts the rule, and the rest of the rule refers to
each value by its bold name. If a value still reads `[FILL IN: …]`, the rule isn't set up here
yet. Work out that value from the repository itself, and tell the user which values are missing
so they can fill them in.

- **Packages:** [FILL IN: the import packages and what each is for, and where they live, for example
  `src/<package>/` (the src layout) with `<package>.cli` as the command-line entry point, or where a
  map of them lives]
- **Python versions:** [FILL IN: every Python version and implementation the code must run on, the
  `requires-python` that states them, and the version used for development, for example
  `requires-python = ">=3.12"`, tested on CPython 3.12, 3.13, and 3.14, with 3.14 in
  `.python-version`]
- **Project tool:** [FILL IN: the tool that manages environments, dependencies, and the lock file,
  and the build backend, for example uv with `uv.lock` and the `hatchling` backend, or pip with a
  `requirements.txt` compiled by pip-tools]
- **Check commands:** [FILL IN: the commands that must pass before you report done, for example
  `ruff format --check .`, `ruff check .`, `mypy`, and `pytest`]
- **Lint configuration:** [FILL IN: the formatter and linter, the rules they enforce, and where they
  are set, for example Ruff's formatter and linter in `[tool.ruff]` in `pyproject.toml`]
- **Type checker:** [FILL IN: the type checker, how strict it is, and which code it covers, for
  example mypy with `strict = true` in `[tool.mypy]`, covering `src/` and `tests/`, or "none"]
- **Dependency policy:** [FILL IN: "none" if no third-party packages are allowed, or how a package
  gets approved and where approved packages are listed, for example `docs/dependency-policy.md`]
- **Errors:** [FILL IN: the exception design, for example one base class, `<Package>Error`, in
  `<package>/errors.py`, with a subclass for each kind of failure, mapped to exit codes in the
  command-line tool]
- **Logging:** [FILL IN: how code reports diagnostics, for example the standard `logging` module
  with one logger per module, configured only in `<package>/cli.py`, and which modules may print to
  stdout or stderr]
- **Languages:** [FILL IN: the languages users see the program's text in, which are right to left,
  where that text lives, for example gettext catalogs in
  `src/<package>/locale/<tag>/LC_MESSAGES/<domain>.po`, and who reviews translations, or "English
  only"]
- **Untrusted input:** [FILL IN: the modules that read data from outside the program (files, the
  network, users), and where their limits are defined, or "none"]
- **Concurrency:** [FILL IN: the concurrency model, for example `asyncio` with one event loop
  started by `asyncio.run` in `main`, a thread pool for blocking I/O, processes for CPU-bound work,
  or "none"]
- **Native code:** [FILL IN: code that leaves Python, for example C extensions, Cython, Rust through
  PyO3, or libraries loaded with `ctypes` or `cffi`, and what approval new native code needs, or
  "none"]
- **Public API:** [FILL IN: the packages and modules that other code imports, and how breaking
  changes are caught, for example a test that compares each module's `__all__` with a saved list, or
  "none"]
- **Published packages:** [FILL IN: the distributions published to the Python Package Index (PyPI),
  each of which needs its own README and metadata, or "none"]
- **API docs:** [FILL IN: the docstring style and how the API reference is built, for example Google
  style, built with Sphinx and `sphinx.ext.napoleon` by `sphinx-build -W docs docs/_build`, or
  "docstrings only"]
- **Design docs:** [FILL IN: where each package's design is written up, for example
  `docs/packages/<package>.md`, or "none"]
- **Test layout:** [FILL IN: the test framework, folders, and naming, and the versions the tests run
  on, for example pytest with tests in `tests/` named `test_*.py`, run on every version in the
  **Python versions** in continuous integration (CI)]

## Decisions that are the user's

Stop and ask the user before you:

- add a dependency, including a development tool or a pytest plugin;
- change a public API, a command-line option, a stored or exchanged data format, or a database
  schema;
- change the **Python versions**, the **Project tool**, or the build backend;
- add native code, or load a native library with `ctypes` or `cffi`;
- run code or load objects the program didn't ship, with `eval`, `exec`, `pickle`, or a plugin
  loader;
- or weaken the **Type checker** settings, a lint rule, a test, or a check.

## Making a change

- **Read first.** Read the code around a change and the tests that cover it. Check the **Packages**
  to find where new code belongs, and check the standard library before you write a helper:
  `pathlib`, `itertools`, `functools`, `collections`, and `contextlib` already hold many.
- **Check each step.** After each step, run the tests for the module you changed, such as
  `pytest tests/test_<module>.py`, which is much faster than the whole suite, and run the
  **Type checker**.
- **Fix the cause, not the symptom.** For a bug, first write a test that fails, then fix the bug and
  show the test passing. Don't add an `if x is None: return`, a `getattr(obj, "name", None)`, or a
  `try` that catches everything to skip a value that should never be missing; find out why it is
  missing.
- **Don't silence the checkers.** Never add `# type: ignore`, `# noqa`, `typing.cast`, `Any`, an
  `except Exception: pass`, or a warnings filter only to make an error or a warning go away. Work
  out what it is saying, then fix the types or the design.

## Know which Python you are writing

- Write code that runs on every version in the **Python versions**: use only what the oldest of them
  has. Before you use a feature, check the "What's New" page of the version that added it. For
  example:
  - 3.10 added `match` statements, `X | Y` unions at run time, and `dataclass(slots=True)`.
  - 3.11 added `ExceptionGroup` and `except*`, `asyncio.TaskGroup`, `tomllib`, and `typing.Self`.
  - 3.12 added the `type` statement, generic syntax such as `class Box[T]:`, and `typing.override`.
  - 3.13 added `warnings.deprecated` and `typing.TypeIs`.
  - 3.14 added template strings (`t"…"`), and stopped evaluating annotations until something reads
    them.
  - 3.15 made UTF-8 mode the default, so `open` uses UTF-8 when the code gives no encoding.
- Where versions really differ, check `sys.version_info` against a tuple:
  `if sys.version_info >= (3, 12):`. Type checkers understand that form, and check each branch
  against the version they target.
- Write for every implementation in the **Python versions**, not only CPython. PyPy, for one,
  doesn't free an object as soon as its last reference goes, so a file that the code never closes
  stays open there until the garbage collector runs.

## Design with types

- Annotate every function signature and every public attribute, and keep the **Type checker**
  passing. Annotations are documentation that the checker keeps true.
- Make invalid states unrepresentable:
  - Use an `Enum` instead of string constants, and a `Literal` type for a small fixed set of values
    in a signature.
  - Use a class for each state instead of one class whose fields are set only in some states.
  - Use `typing.NewType` for IDs and units, so the checker rejects a `UserId` passed where an
    `OrderId` belongs.
- Parse at the boundary. Turn raw input (a `dict` from JSON, a database row, command-line arguments)
  into a dataclass or another typed object once, where it enters the program, so code inside never
  checks it again. Use a `TypedDict` only for data that stays a `dict`.
- Use `@dataclass(frozen=True, slots=True)` for plain values. A frozen instance can't change after
  it is made, and `slots` saves memory and rejects a misspelled attribute. Add `kw_only=True` when a
  class has more than a few fields.
- Accept the most general type and return the most specific: take `Iterable[str]` or
  `Mapping[str, int]` from `collections.abc`, and return `list[str]` or `dict[str, int]`.
- Use a `Protocol` to say what a parameter must be able to do, instead of requiring a base class.
- Make `bool` and other option parameters keyword-only, after a `*`: `save(path, overwrite=True)`
  says what `save(path, True)` hides.
- When you `match` on an enum or a union, end with `case _: assert_never(value)`, using
  `typing.assert_never` (3.11). The type checker then reports every `match` that a new member leaves
  unhandled.
- Avoid `Any`. Use `object` for a value of unknown type, and narrow it with `isinstance` before you
  use it.
- Organize modules by what they do (`parser`, `cache`), not by kind (`utils`, `helpers`). Keep
  functions short enough that none needs comments to separate its parts.

## Values, functions, and common traps

- A default argument is evaluated once, when the `def` runs, and every call shares it. Default to
  `None`, and create the list or dict inside the function.
- A closure reads a loop variable when it runs, not when it is made: `[lambda: i for i in range(3)]`
  makes three functions that all return 2. Bind the value with a default argument or
  `functools.partial`.
- Compare with `is` only for `None` and other singletons, and compare values with `==`. Write
  `if x is None:`, not `if not x:`, when `0`, `""`, or an empty list is a valid value.
- `bool("False")` is `True`, because every non-empty string counts as true. Parse flags from text
  explicitly.
- Copies are shallow: `list(a)`, `a[:]`, `dict.copy()`, and `copy.copy` share the objects inside.
  Don't return an internal list or dict from a public method; return a copy or a tuple.
- A `dict` keeps insertion order. A `set` of strings keeps none, and its order changes from one run
  to the next, because Python randomizes string hashes in each process. Sort before the order
  reaches output, files, or test expectations.
- `functools.cache` and `lru_cache` keep every result, and on a method they keep `self` alive too.
  Give the cache a `maxsize`, and cache a module-level function rather than a method.
- Don't use `assert` to check input or anything else that must hold in production: `python -O`
  removes every `assert`.
- Keep a module free of side effects when it is imported: no I/O, network calls, or heavy work at
  the top level. Put a script's work in a `main()` function behind `if __name__ == "__main__":`.

## Errors and exceptions

- Follow the **Errors** design.
- A library raises its own exceptions, all derived from one base class for the package, so a caller
  can catch everything it raises with one `except`, or pick out one kind of failure. Don't let a
  `KeyError` or a `ValueError` from inside the library reach callers.
- Keep the cause: `raise ParseError(...) from err`. Add context where an error crosses a layer, such
  as the path, the operation, or the position in the input. `err.add_note(...)` (3.11) adds a line
  to an exception without replacing it.
- Catch the narrowest exception you can handle, and keep each `try` block to the lines that can
  raise it. Never write a bare `except:`, which also catches `KeyboardInterrupt` and `SystemExit`.
- Catch `Exception` only at the top of a program or a task, to log the error and exit or go on, and
  never let it pass silently. When ignoring an error is correct, use
  `contextlib.suppress(FileNotFoundError)`, with a comment that says why.
- Write messages that say what failed and with which value: `f"unknown color {name!r}"`. The `!r`
  shows the quotes, so an empty string or a trailing space is visible.
- Don't return `None` or a value such as `-1` to report a failure the caller must handle. Raise, or
  return what the **Errors** design says.
- When several tasks fail together, as in an `asyncio.TaskGroup`, Python raises an `ExceptionGroup`.
  Handle it with `except*`, which matches each kind of error inside the group.

## Files and other resources

- Open every file, socket, lock, and connection with `with`, so it is closed even when an exception
  is raised. Use `contextlib.ExitStack` when the number of resources varies.
- Pass `encoding="utf-8"`, or the encoding the format requires, to `open`, `Path.read_text`, and
  `Path.write_text`. Before Python 3.15, the default is the locale's encoding, which differs between
  machines. `python -X warn_default_encoding` prints an `EncodingWarning` for each call that leaves
  it out.
- Use `pathlib.Path` for paths, not string concatenation.
- Make temporary files and folders with `tempfile.NamedTemporaryFile`, `mkstemp`, or
  `TemporaryDirectory`. Never use `tempfile.mktemp`, which returns a name that another process can
  take first.
- To replace a file that must never be left half written, write a temporary file in the same folder,
  then move it into place with `os.replace`. On POSIX systems the move happens in one step.
- Run other programs with `subprocess.run` and a list of arguments, with `check=True` and a
  `timeout`, so a failure raises an exception and a program that hangs can't hang yours.

## Logging and output

- Follow the **Logging** setup. Library code never prints: it raises exceptions, and logs through a
  logger made with `logging.getLogger(__name__)`.
- Only the program's entry point configures logging. A library adds no handler except
  `logging.NullHandler`, and never calls `logging.basicConfig`.
- Pass values to a log call as arguments, not in an f-string:
  `logger.info("loaded %d rows from %s", count, path)`. The message is then formatted only when the
  record is written, and tools that group log messages see one message instead of thousands.
- Log an exception you handle with `logger.exception(...)` inside the `except` block, which adds the
  traceback.
- Never log secrets, tokens, or personal data.
- Warn about deprecated use with `warnings.warn(..., DeprecationWarning, stacklevel=2)`, so the
  warning points at the caller's line, not yours.

## Time, numbers, and money

- Use datetimes that carry a time zone: `datetime.now(UTC)`, never `datetime.utcnow()`, which
  returns a value with no time zone and is deprecated since 3.12. `datetime.UTC` arrived in 3.11;
  use `timezone.utc` on older versions. Store and compare instants in UTC, and convert to a local
  zone with `zoneinfo.ZoneInfo` only to show a time.
- Get the current time from a function or a clock object the code receives, not from
  `datetime.now()` inside the logic, so tests can fix it.
- Measure durations with `time.monotonic()` or `time.perf_counter()`, not `time.time()`, which jumps
  when the system clock is set.
- Floats are binary: `0.1 + 0.2 == 0.3` is `False`. Compare floats with `math.isclose`, and never
  use them for money. Use `decimal.Decimal`, built from a string (`Decimal("0.10")`; `Decimal(0.1)`
  keeps the float's error), or an `int` count of the smallest unit.
- `round()` rounds halves to the even neighbor: `round(2.5)` is 2 and `round(0.5)` is 0. Round money
  with `Decimal.quantize` and the rounding mode the domain requires.
- Integers never overflow, so a size or a count from input can grow until it exhausts memory. Check
  it against a limit before you allocate or loop on it.
- `/` always returns a float; use `//` for integer division. `//` and `%` round toward negative
  infinity: `-7 // 2` is -4.

## Text for users and languages

This section covers the text a program shows people: its output, its help, and its errors as the
user sees them. With "English only" as the **Languages** value, the first two points still apply, so
the program can be translated later.

- Keep user-facing text in the **Languages** catalogs, and mark each string for translation with the
  standard `gettext` module's functions, usually bound to `_`. Logs and the messages of exceptions
  that a library raises are for developers: keep them in English and out of the catalogs, and
  translate an error only where the program shows it to its user.
- Translate the template, then fill it in: `_("Saved {name}").format(name=name)`. Never pass an
  f-string to `_()`. Python fills it in first, so the text it looks up is never in the catalog.
- Never build a sentence from pieces, and never choose a word form with `n == 1`. Use `ngettext`,
  and let each language's catalog state its own plural rule in its `Plural-Forms` header, so Arabic
  gets its six forms and Chinese its one:

  ```python
  print(ngettext("{count} file", "{count} files", count).format(count=count))
  ```

- Load catalogs with `gettext.translation(domain, localedir, fallback=True)`. Without a `languages`
  argument, it reads `LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, and `LANG`, in that order. With
  `fallback=True`, it shows the source text when no catalog matches, instead of raising an
  exception.
- `str.format` and f-strings don't depend on a locale: `f"{x:.2f}"` writes `3.14` everywhere. That
  suits text that programs read. For text people read, format numbers, dates, and currencies for the
  user's locale with Babel, if the **Dependency policy** allows it. The standard `locale` module's
  settings belong to the whole process, so one thread's `setlocale` call changes every other
  thread's output.
- When you insert a name or a number into a sentence in a right-to-left language, wrap it in the
  invisible isolation marks FSI and PDI (U+2068 and U+2069), so it doesn't reorder the text around
  it.
- A string's length isn't its width on screen. `len()` counts code points: a Chinese character takes
  two terminal columns, and combining marks, such as the virama in Hindi, take none. Compare text
  after `unicodedata.normalize("NFC", text)`, and compare it without case with `str.casefold()`, not
  `lower()`: `"Straße".casefold()` equals `"STRASSE".casefold()`.
- Treat translations you write as drafts, and list their message IDs in your report for a native
  speaker to review.

## Untrusted input

Treat every byte from outside the program as possibly malformed or hostile, especially in the
**Untrusted input** modules.

- Never run outside data or rebuild objects from it. `eval`, `exec`, `pickle`, `marshal`, and
  `shelve` can all run arbitrary code. Read data with `json`, `tomllib`, or `csv`. Use
  `ast.literal_eval` only for Python literals, and only with a size limit: its documentation warns
  that large or deeply nested input can exhaust memory or crash the interpreter.
- Never build a command, a query, or a template from outside data:
  - Commands: pass `subprocess.run` a list of arguments, never a string with `shell=True`, and never
    use `os.system`. If a shell can't be avoided, quote each value with `shlex.quote`.
  - SQL: pass values as parameters, as in
    `cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))`, never with an f-string or
    `%`.
  - Templates: never call `.format` on a template from outside the program, because a field such as
    `{0.__class__.__mro__}` reads attributes of the values passed in. Use `string.Template` and its
    `safe_substitute` method.
- Treat paths from input as hostile. Joining an absolute path drops the base:
  `Path("/srv/data") / "/etc/passwd"` is `/etc/passwd`. Resolve the joined path, and check it with
  `is_relative_to(root.resolve())` before you open it.
- Extract tar files with `filter="data"` (3.12 and later, and the default from 3.14), which keeps
  every file inside the target folder and refuses device files and links that point outside it. For
  zip files, check each member's name and size before you extract it.
- Check sizes before you read or allocate. Read at most a limit (`f.read(limit + 1)`, then reject
  anything longer), and compare a claimed length or count with the input that remains.
- Bound nesting. Deeply nested JSON makes `json.loads` raise `RecursionError`, which isn't a
  `ValueError`; catch it, and treat the input as invalid. Give your own recursive code an explicit
  depth limit.
- Since 3.11, `int()` refuses strings of more than 4,300 digits, because the time to convert one
  grows with the square of its length. Don't raise that limit with `sys.set_int_max_str_digits` for
  input.
- Don't run a regular expression with nested repetition, such as `(a+)+`, over outside text, because
  some inputs take exponential time. Limit the text's length, or use possessive quantifiers (`a*+`)
  and atomic groups (`(?>…)`), which are in 3.11 and later.
- Use `secrets` for tokens, passwords, and anything else an attacker must not guess, never `random`.
  Compare secrets with `hmac.compare_digest`, whose timing doesn't reveal where two values differ.
- Store passwords only as a slow, salted hash, such as `hashlib.scrypt` or a library the
  **Dependency policy** allows, never as a plain `hashlib.sha256`.
- Keep certificate checks on. Never pass `verify=False`, or use an unverified `ssl` context, to get
  past an error.

## Concurrency and async

- Follow the **Concurrency** model. Don't add threads, processes, or an event loop it doesn't
  include.
- Choose by the kind of work. Threads and `asyncio` overlap time spent waiting on I/O. On the
  standard build, only one thread runs Python code at a time, because of the global interpreter lock
  (GIL), so run CPU-bound work in processes, with `concurrent.futures.ProcessPoolExecutor`.
- Don't treat the GIL as a lock for your data. `counter += 1` is a read, an add, and a write, and
  another thread can run between them. The free-threaded build, officially supported from 3.14, has
  no GIL at all. Protect shared state with a `threading.Lock`, held with `with`, or pass data
  through a `queue.Queue`.
- Start processes as if they share nothing with the parent. The default start method is `spawn` on
  Windows and macOS, and `forkserver` on other POSIX systems from 3.14, and neither copies the
  parent's memory, so code that relied on `fork` copying it breaks. Keep the program's work behind
  `if __name__ == "__main__":`, and pass only values that `pickle` can copy.
- In `asyncio`:
  - Start the event loop once, with `asyncio.run(main())`, at the entry point.
  - Run tasks in an `asyncio.TaskGroup` (3.11), which waits for all of them and cancels the rest
    when one fails. If you call `asyncio.create_task` instead, keep a reference to the task: the
    event loop keeps only a weak reference, so a task nothing refers to can vanish before it
    finishes.
  - Never block the event loop. Move a blocking call (`time.sleep`, I/O through a blocking library,
    or a long computation) to a thread with `asyncio.to_thread`, and wait with
    `await asyncio.sleep(...)`.
  - Put a timeout on every network wait, with `asyncio.timeout` (3.11) or `asyncio.wait_for`.
  - Let `asyncio.CancelledError` propagate. It derives from `BaseException`, so `except Exception`
    doesn't catch it; if you catch it to clean up, raise it again.
- Bound every queue and every group of tasks: give each `asyncio.Queue` a `maxsize`, and put an
  `asyncio.Semaphore` around work that fans out. An unbounded queue turns a slow consumer into
  unbounded memory use.
- Give every thread, process, and task an owner that waits for it or cancels it, and that handles
  the error it raises. Use executors with `with` and task groups with `async with`.

## Native code

- Follow the **Native code** value. Prefer the standard library or pure Python where it does the
  job: native code needs a compiler on every platform, a wheel (a prebuilt package file) for each
  platform and Python version the project supports, and a review for memory safety.
- Load a library with `ctypes` or `cffi` behind one module of its own. With `ctypes`, set each
  function's `argtypes` and `restype`: without them, `ctypes` treats the return value as a C `int`,
  which keeps only the low 32 bits of a 64-bit pointer.
- Release what native code owns in a `with` block or a `close` method, not in `__del__`, which may
  run late or not at all.

## Public APIs

- Keep every API small. Give everything that isn't part of it a name that starts with an underscore,
  and list each module's public names in `__all__`.
- Make optional parameters keyword-only (after `*`), so you can add and reorder them later without
  breaking callers. Make parameters positional-only (before `/`) when their names aren't part of the
  contract.
- Ship the types. Add an empty `py.typed` file to each typed package, so type checkers read its
  annotations, as PEP 561 describes.
- Deprecate before you remove. Mark the old name with `@warnings.deprecated("use load_all instead")`
  (3.13), or call `warnings.warn(..., DeprecationWarning, stacklevel=2)` on older versions, so
  callers see a warning for at least one release before the name goes.
- In the **Public API** packages, each of these breaks callers: removing or renaming a public name,
  module, or parameter; making an optional parameter required, or moving one that callers may pass
  by position; and changing a return type or the exceptions a function raises. Ask before you make
  one, and mark it as `commits.md` requires.

## Documentation

Three kinds of docs describe a package, and each has its own reader:

- Docstrings, which `help()` and editors show.
- The API reference, which the **API docs** build from the docstrings.
- The README, which is the package's page on PyPI and in the repository.

Keep all three true. A change to behavior, a signature, an exception, or an option updates every one
of them that describes it, in the same change.

### Docstrings

- Give every public module, class, function, and method a docstring in the style the **API docs**
  name. Start with a one-line summary that ends with a period, as PEP 257 describes; listings in the
  API reference and in `help()` show that line alone.
- Say in each module's docstring what the module holds and why it is a module of its own. In a
  package's `__init__.py`, also say where the package fits, and link to its write-up in the
  **Design docs**, if there is one.
- Don't repeat the types that the annotations give. Say what each parameter means, what the function
  returns, each exception it raises and when, and any side effect.
- State only what the code does. A claim about cost, ordering, thread safety, or a limit must match
  the code, so check it there or in a test before you write it. Describe planned behavior as
  planned, never in the present tense.
- Write examples as doctests (lines that start with `>>> `, each followed by its output), and run
  them with the tests, for example with `pytest --doctest-modules`, so they can't go stale.
- Write code comments that explain why, not what, and keep them true when the code changes. Delete
  commented-out code instead of leaving it.

### Package READMEs

Give each of the **Published packages** a README, named with `readme = "README.md"` in `[project]`.
Its PyPI page is often the first thing a new user reads, so write it for someone deciding whether to
use the package, in this shape:

1. `# <package-name>`, then one short paragraph on what the package is and does.
2. `## Installation`: the install command, and the **Python versions** it supports.
3. `## Usage`: a short example that runs, then what a user must know to avoid errors.
4. `## Status`: the version and how stable the API is. Then, kept apart, what is built today, what
   is left out by design, and what is planned.
5. `## Documentation`: links to the API reference, the package's write-up in the **Design docs**,
   and the project.
6. `## License`: the license, with a link to the license file.

- Use absolute URLs for links and images. PyPI shows the README without the repository around it, so
  a relative link breaks there.
- Test the README's examples. Written as `>>>` sessions, they run with
  `python -m doctest README.md`. Leave a blank line between the last output line and the closing
  fence: doctest reads every line up to a blank one as expected output, so it reads the fence as
  part of the output and the example fails.
- Reread the README whenever the package's behavior or API changes. A doctest catches an example
  that stops working, but nothing catches a sentence that stops being true.

### Package metadata

For each of the **Published packages**, fill in the `[project]` table in `pyproject.toml`, which the
Python Packaging User Guide documents:

- `name`, `version`, and `description`, which is one plain-text sentence that PyPI's search results
  show.
- `requires-python`, matching the **Python versions**.
- `license`, as a Software Package Data Exchange (SPDX) expression such as `"MIT"`, and
  `license-files`, as PEP 639 describes.
- `readme`, `authors`, `classifiers` (each supported Python version, and `Typing :: Typed` for a
  typed package), and `[project.urls]`, with links such as `Documentation`, `Source`, and
  `Changelog`.
- `[project.scripts]` for each command the package installs.

Publish from CI with PyPI's trusted publishing, which lets the workflow upload without a long-lived
API token.

## Tests

- Follow the **Test layout**. Where `testing.md` is adopted, it sets how strict and complete the
  tests must be.
- Give every behavior change a test. Start every bug fix with a test that fails before the fix.
- Name each test for the behavior it checks: `test_rejects_length_past_end_of_input`, not `test_3`.
- Use pytest's tools for isolation: `tmp_path` for files, `monkeypatch` for environment variables
  and attributes, and fixtures for shared setup. Use `pytest.mark.parametrize` for cases that differ
  only in their data, and give each case an ID, as in `pytest.param("", id="empty")`.
- Keep tests deterministic: seed every random number generator, pass in a fixed clock, and don't
  depend on the network or on the order of a set.
- Test the edges: empty, one, the maximum, one past the maximum, and malformed. For a parser,
  include truncated and oversized input.
- Check the exception type with `pytest.raises(ParseError)`. Match the message only where the
  message itself is the contract, so rewording it doesn't break a test.
- Make warnings fail the tests, with `filterwarnings = ["error"]` under `[tool.pytest.ini_options]`,
  so a deprecation shows up when it starts, not when the feature disappears.
- Mock only what the test can't control, such as the network or the clock, and never the code under
  test.
- Run the tests on every version in the **Python versions**; code can pass on one and fail on
  another.

## Style, lints, and the toolchain

- Format with the formatter in the **Lint configuration**, and don't hand-format against it. Follow
  the names in PEP 8: `snake_case` for functions, variables, and modules, `PascalCase` for classes,
  and `UPPER_CASE` for constants.
- Set lint rules and type checker options only in the **Lint configuration** and the
  **Type checker** settings, not on the command line or at the top of one file.
- When a lint or a type error is wrong in one place, silence it on that line alone, with its code,
  such as `# noqa: S603` or `# type: ignore[arg-type]`, and say why in a comment on the line above.
  Never use a bare `# noqa` or `# type: ignore`, which hides every error on the line.
- Turn on the checks that report a suppression nothing needs any more, so an exception can't outlive
  its reason: mypy's `warn_unused_ignores` (part of `strict`), Pyright's
  `reportUnnecessaryTypeIgnoreComment`, and Ruff's `RUF100`.
- Don't leave `print` calls used for debugging, `breakpoint()`, or `pdb` imports behind.
- Work in a virtual environment for the project, made by the **Project tool**. Never install
  packages into the system's Python, with `sudo pip` or `--break-system-packages`.
- Keep the **Python versions**. Don't raise `requires-python` or drop a version from CI as a side
  effect of another task; a version change is a change of its own.

## Dependencies and packaging

- Follow the **Dependency policy**. Never add a package, an optional extra, or a development tool
  without asking. When you propose one, say what it does that the standard library or existing code
  can't, and give its license, how well it is maintained, how many packages it brings in, and
  whether it has native code that needs a wheel for each platform.
- Declare the project in `pyproject.toml`: its metadata in `[project]`, its build backend in
  `[build-system]`, and tool settings in `[tool.<name>]` tables. Don't add a `setup.py` unless the
  build has to run code.
- Put development tools, such as the test runner, the linter, and the type checker, in
  `[dependency-groups]` (PEP 735), not in `[project.optional-dependencies]`, which users can install
  as extras.
- In a library, declare each dependency as a range with a tested lower bound, such as
  `"attrs>=23.1"`. Don't cap it (`<24`) unless a known release breaks the code: a cap stops users
  from upgrading even when nothing broke.
- In an application, commit the lock file that the **Project tool** writes, update it in the same
  change as `pyproject.toml`, and install from it in CI and deployment (with `uv sync --locked`, for
  example), so the versions that were tested are the versions that run.
- Install the package you are working on in editable mode, through the **Project tool** or with
  `pip install -e .`, so the environment runs the code in the repository. Import it by its package
  name, and never add to `sys.path` or `PYTHONPATH` to make an import work.

## Before finishing

1. Run every **Check commands** command and read its output. Fix every warning, not only the errors.
2. Run the tests on each version in the **Python versions** that you can, for example with
   `uv run --python 3.12 pytest`, and say which versions you couldn't.
3. If you changed public names, docstrings, or a README:
   1. Build the API reference as the **API docs** say, with warnings as errors, so a broken
      reference fails.
   2. Run the doctests.
   3. Reread the changed prose against the code.
4. If you changed what a published package ships (its modules, metadata, README, or license files),
   build it with the **Project tool**, for example with `uv build`, and list what each file holds:
   `python -m zipfile -l dist/<name>.whl` for the wheel and `tar -tzf dist/<name>.tar.gz` for the
   source distribution. Check that the README, the license files, and `py.typed` are there, and that
   secrets, local settings, and build output aren't.
5. If you changed dependencies, check that the lock file is current, for example with
   `uv lock --check`, and that it is in the same change.
6. Review your diff as a reviewer would. Look for `print` and `breakpoint()` calls, a bare `except:`
   or an `except Exception: pass`, `Any`, a `# type: ignore` or `# noqa` without a code, mutable
   default arguments, datetimes without a time zone, `shell=True`, an `assert` that checks input,
   and missing docs or tests. Then report what you ran, what you didn't, and what remains.
