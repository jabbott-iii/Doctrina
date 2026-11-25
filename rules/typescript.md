---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.mts"
  - "**/*.cts"
  - "**/*.js"
  - "**/*.jsx"
  - "**/*.mjs"
  - "**/*.cjs"
  - "**/package.json"
  - "package-lock.json"
  - "pnpm-lock.yaml"
  - "yarn.lock"
  - "bun.lock"
  - "**/tsconfig*.json"
  - "eslint.config.*"
  - "prettier.config.*"
  - ".prettierrc*"
  - "biome.json"
  - "biome.jsonc"
  - "vitest.config.*"
  - ".nvmrc"
  - ".node-version"
  - ".npmrc"
---

# TypeScript and JavaScript standards

These rules cover the TypeScript and JavaScript in this repository: libraries, servers, command-line
tools, scripts, tests, and the configuration files around them, whether they run on Node.js, in a
browser, or both. They describe how a senior engineer writes TypeScript, and they apply to plain
JavaScript too, except where a point needs types. Code that runs in web pages also follows
`web-front-end.md` in this folder, which covers the page, the Document Object Model (DOM), and
accessibility; this rule covers the language. Doc comments, error messages, and other text follow
`writing.md`.

Apply them to code you write or edit. Don't rewrite existing code only to make it conform; fix a
passage when you are already changing it, and mention anything else you notice.

## Project details

A repository fills in this section when it adopts the rule, and the rest of the rule refers to
each value by its bold name. If a value still reads `[FILL IN: …]`, the rule isn't set up here
yet. Work out that value from the repository itself, and tell the user which values are missing
so they can fill them in.

- **Packages:** [FILL IN: the packages and what each is for, and where they live, for example
  `packages/<name>/` in an npm workspace, or a single package with its entry point in `src/index.ts`
  and its command-line tool in `src/cli.ts`]
- **Runtimes:** [FILL IN: every runtime and version the code must run on, and where that is stated,
  for example Node.js 24 and 26, in `engines` in `package.json` and in `.nvmrc`, and the browsers in
  the **Browser support** of `web-front-end.md`]
- **Toolchain:** [FILL IN: the TypeScript version and how code is built and run, for example
  TypeScript 7.0 with `tsc` writing `dist/`, a bundler such as Vite with `tsc --noEmit` checking the
  types, or Node.js running `.ts` files directly]
- **Package manager:** [FILL IN: the package manager, its lock file, and the install command for
  continuous integration (CI), for example npm with `package-lock.json` and `npm ci`, or pnpm with
  `pnpm-lock.yaml` and `pnpm install --frozen-lockfile`]
- **Check commands:** [FILL IN: the commands that must pass before you report done, for example
  `npx prettier --check .`, `npx eslint . --max-warnings 0`, `npx tsc --noEmit`, and `npm test`]
- **Compiler options:** [FILL IN: where the `tsconfig.json` files are and how strict they are, for
  example a `tsconfig.base.json` that each package extends, with `strict`,
  `noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes` on]
- **Lint configuration:** [FILL IN: the formatter and linter and where they are set, for example
  Prettier in `.prettierrc.json` and ESLint in `eslint.config.js` with typescript-eslint's
  `strictTypeChecked` config, or Biome in `biome.json`]
- **Dependency policy:** [FILL IN: "none" if no third-party packages are allowed, or how a package
  gets approved and where approved packages are listed, for example `docs/dependency-policy.md`]
- **Errors:** [FILL IN: the error design, for example error classes that extend one `AppError` with
  a `code` field, in `src/errors.ts`, mapped to HTTP status codes in `src/server/errors.ts`]
- **Logging:** [FILL IN: how code reports diagnostics, for example the project's logger in
  `src/log.ts`, which writes one JSON object per line, and which modules may write to the console]
- **Languages:** [FILL IN: the languages users see the program's text in, which are right to left,
  where that text lives, for example International Components for Unicode (ICU) messages in
  `locales/<tag>.json`, and who reviews translations, or "English only"]
- **Untrusted input:** [FILL IN: the modules that read data from outside the program (requests,
  files, messages, users), and where their limits are defined, or "none"]
- **Concurrency:** [FILL IN: how work runs at the same time, for example one Node.js process per
  container, with worker threads for CPU-bound work in `src/workers/`, or "none"]
- **Native code:** [FILL IN: code that leaves JavaScript, for example Node-API addons or WebAssembly
  modules, and what approval new native code needs, or "none"]
- **Public API:** [FILL IN: the packages and modules that other code imports, and how breaking
  changes are caught, for example an API Extractor report in `etc/<package>.api.md`, or "none"]
- **Published packages:** [FILL IN: the packages published to the npm registry, each of which needs
  its own README and `package.json` metadata, or "none"]
- **API docs:** [FILL IN: how the API reference is built from doc comments, for example TypeDoc with
  `npx typedoc --treatWarningsAsErrors`, or "doc comments only"]
- **Design docs:** [FILL IN: where each package's design is written up, for example
  `docs/packages/<package>.md`, or "none"]
- **Test layout:** [FILL IN: the test framework, folders, and naming, and the runtimes the tests run
  on, for example Vitest with `*.test.ts` files beside the code and Playwright tests in `e2e/`, run
  on every version in the **Runtimes** in CI]

## Decisions that are the user's

Stop and ask the user before you:

- add a dependency, including a development tool, a type package such as `@types/<name>`, or a
  plugin for the linter or the bundler;
- change a public API, a request or response format, a stored data format, or a database schema;
- change the **Runtimes**, the **Toolchain**, the module system, or the **Package manager**;
- add native code, or a script that runs when the package is installed;
- run code the program didn't ship, with `eval`, `new Function`, `node:vm`, or a plugin loader;
- or weaken the **Compiler options**, a lint rule, a test, or a check.

## Making a change

- **Read first.** Read the code around a change and the tests that cover it. Check the **Packages**
  to find where new code belongs, and check the platform before you write a helper or add a package:
  `structuredClone`, `Object.groupBy`, `Array.prototype.toSorted`, `AbortSignal.timeout`, `fetch`,
  `Intl`, and `node:test` do what many small packages once did.
- **Check each step.** After each step, run `tsc --noEmit` and the tests for the file you changed,
  such as `npx vitest run src/parse.test.ts`. Bundlers such as esbuild and Vite, and Node.js itself,
  remove types without checking them, so only `tsc` finds type errors.
- **Fix the cause, not the symptom.** For a bug, first write a test that fails, then fix the bug and
  show the test passing. Don't add a `?.`, a `?? []`, or an `if (!value) return` that quietly skips
  a value that should never be missing; find out why it is missing.
- **Don't silence the compiler.** Never add `any`, an `as` cast, a `!` (the non-null assertion),
  `// @ts-ignore`, `// @ts-expect-error`, an `eslint-disable` comment, or an empty `catch` only to
  make an error go away. Work out what it is saying, then fix the types or the design.

## Know your runtime and modules

- Write code that runs on every runtime in the **Runtimes**. Before you use a newer API, check its
  support on MDN's compatibility tables. Node.js 26 has, for example, `Temporal`, `using`
  declarations, iterator helpers such as `.map` on an iterator, the `Set` methods `union` and
  `intersection`, `Promise.try`, and `RegExp.escape`, but older Node.js versions and some browsers
  lack some of them.
- Set `target` and `lib` in the **Compiler options** to match the oldest runtime, so the compiler
  rejects an API that runtime lacks. Since TypeScript 6.0, `types` is empty unless you list packages
  in it: add `"node"` (from `@types/node`) for code that runs on Node.js.
- Write ES modules (`import` and `export`), and set `"type": "module"` in `package.json`. Keep
  CommonJS (`require`) only where an ES module can't run. Node.js 20.19, 22.12, and later can
  `require()` an ES module that has no top-level `await`, so a library can publish ES modules alone.
- Set `module` to `nodenext` for code that Node.js runs. Relative imports then name the file Node.js
  will load, with its extension: `import { parse } from "./parse.js"`, even in `parse.ts`. For code
  that a bundler builds, use `module: "preserve"` with `moduleResolution: "bundler"`.
- Node.js runs `.ts` files directly by removing their types (type stripping, on by default since
  22.18 and 23.6, and stable since 24.12 and 25.2). It doesn't check the types, and it rejects
  TypeScript syntax that would need generated code: `enum`, a `namespace` that holds code, parameter
  properties (`constructor(private x: number)`), and `import x = …` aliases. Turn on
  `erasableSyntaxOnly`, so `tsc` reports the same syntax.
- TypeScript 7.0 turned the options that 6.0 deprecated into errors: `baseUrl`,
  `moduleResolution: "node"` (also called `node10`), `target: "es5"`, and the `amd`, `umd`, and
  `system` module formats. It also no longer lets `esModuleInterop` be set to `false`. Use `paths`,
  which resolve from the `tsconfig.json`'s folder, in place of `baseUrl`.

## Compiler options

- Keep `strict` on; it is the default since TypeScript 6.0. Among other checks, it makes
  `catch (err)` give `err` the type `unknown`, so code must check what was thrown before it reads
  `.message`.
- Turn on the checks `strict` leaves out, as `tsc --init` in TypeScript 7 does for the first two:
  - `noUncheckedIndexedAccess`, so `list[0]` has the type `T | undefined` and the code must handle
    an empty list;
  - `exactOptionalPropertyTypes`, so an optional property can be left out but not set to `undefined`
    unless its type says so;
  - `noImplicitOverride`, so a method that replaces a base class's method must say `override`;
  - and `noFallthroughCasesInSwitch`, so a `case` can't run on into the next one without a
    `break` or a `return`.
- Turn on `verbatimModuleSyntax`, so an import used only for types is written `import type` and
  disappears from the output, and `isolatedModules`, so each file compiles on its own, as bundlers
  and type stripping compile it.
- Check plain JavaScript too, with `checkJs` or a `// @ts-check` comment at the top of the file, and
  write its types in JSDoc comments (`/** @param {string} name */`). That gives a script with no
  build step the same checks.

## Design with types

- Never use `any`. Use `unknown` for a value of unknown type, and narrow it with `typeof`,
  `instanceof`, `in`, or a type guard (a function that returns `value is T`) before you use it.
- Make invalid states unrepresentable. Use a discriminated union, a union of object types that each
  have a literal `kind` field, instead of one type whose optional fields are set only in some
  states: `{ kind: "loaded"; data: Data } | { kind: "failed"; error: Error }`.
- Handle every member of a union. End a `switch` on `kind` with `default: state satisfies never;`,
  so adding a member makes the compiler name it in every `switch` that misses it.
- Give IDs and units their own types with a brand, so the compiler rejects a `UserId` passed where
  an `OrderId` belongs: `type UserId = string & { readonly __brand: "UserId" }`.
- Parse at the boundary. Check outside data (a request body, a file, a message) once, where it
  enters the program, and turn it into typed values, with a schema library if the
  **Dependency policy** allows one or a type guard if not. Never write `JSON.parse(text) as User`:
  the cast checks nothing.
- Use a union of string literals (`type Mode = "read" | "write"`) or an object declared `as const`,
  not an `enum`, which type stripping rejects and which generates code.
- Mark what a function doesn't change as `readonly`: `readonly string[]` parameters, `Readonly<T>`
  objects, and `readonly` fields. Use `satisfies` to check a value against a type without widening
  the value's own type.
- Pass options in an object, not as `boolean` arguments: `save(path, { overwrite: true })` says what
  `save(path, true)` hides.
- Annotate the return type of every exported function, so a change inside the function can't change
  the API by accident.
- Organize modules by what they do (`parser`, `cache`), not by kind (`utils`, `helpers`). Avoid
  index files that only re-export a folder, except for a package's entry point: importing one name
  through such a file loads every module it re-exports.

## Values and common traps

- Compare with `===` and `!==`, never `==`, which converts types first: `0 == ""` is `true`.
- `sort()` without a compare function sorts as strings: `[10, 9, 1].sort()` is `[1, 10, 9]`. Pass a
  compare function, such as `(a, b) => a - b`, and use `toSorted`, which returns a new array instead
  of changing the old one.
- Every `number` is a 64-bit float, which holds integers exactly only up to
  `Number.MAX_SAFE_INTEGER`, 2^53 − 1: `Number.MAX_SAFE_INTEGER + 2` is 9007199254740992. Use
  `bigint` for larger integers, and keep 64-bit IDs from JSON as strings.
- `0.1 + 0.2` is 0.30000000000000004. Keep money in integers of the smallest unit, or in a decimal
  library the **Dependency policy** allows.
- Converting text to numbers is loose: `Number("")` and `Number(" ")` are 0, and `parseInt("1e3")`
  is 1. Check the text against a pattern first, then check the result with `Number.isFinite`.
- `NaN` never equals itself; test it with `Number.isNaN`. `typeof null` is `"object"`.
- Use `??` for defaults, not `||`: `count || 10` replaces a count of 0, and `count ?? 10` replaces
  only `null` and `undefined`.
- Spread (`{ ...obj }`) and `Object.assign` copy only the top level. Use `structuredClone` to copy
  nested data.
- Use a `Map` for a lookup keyed by outside data, not a plain object, whose inherited keys, such as
  `constructor` and `__proto__`, look like entries.
- `Date` parses inconsistently: `new Date("2026-11-25")` is midnight UTC, but
  `new Date("2026-11-25T00:00")` is midnight in the machine's time zone, and `new Date(2026, 0, 15)`
  is January, because months count from 0. Use `Temporal` where every runtime in the **Runtimes**
  has it; otherwise store instants as ISO 8601 strings with an offset, or as milliseconds since
  1970, and pass the time zone explicitly when you format them.

## Errors

- Follow the **Errors** design.
- Throw only `Error` objects and their subclasses, never strings or plain objects, so every error
  has a stack trace. Set `name` in each subclass, and give the errors that callers branch on a
  stable `code`, so they never match on message text.
- Keep the cause: `throw new ParseError("bad header", { cause: err })`. Add context where an error
  crosses a layer, such as the path, the operation, or the position in the input.
- Catch only what you can handle, and never leave a `catch` block empty. Catch everything only at
  the top of a request, a job, or the program, to log the error and respond or exit.
- Await every promise, return it, or give it a `.catch`. Node.js ends the process with exit code 1
  on a rejection that nothing handles. typescript-eslint's `no-floating-promises` and
  `no-misused-promises` rules find the promises that are missed.
- `forEach` doesn't wait for an `async` callback, so code after it runs before the work finishes.
  Use a `for (const item of items)` loop with `await`, or `await Promise.all(items.map(…))`.
- `Promise.all` rejects at the first failure, while the other promises keep running. Use
  `Promise.allSettled` when you need every result, or cancel the rest with an `AbortSignal`.

## Logging and output

- Follow the **Logging** setup. Library code never writes to the console: it throws errors, and
  logs through the logger the **Logging** value names or one its caller passes in.
- Only the program's entry point decides where logs go and how much they say.
- Log a fixed message, with the values in separate fields, so tools that group log messages see one
  message instead of thousands.
- Never log secrets, tokens, or personal data, and never log a whole request or response object,
  which holds cookies and authorization headers.
- In a command-line tool, write diagnostics to standard error with `console.error`, and keep
  standard output for the tool's results, so other programs can read them.

## Async code and concurrency

- Follow the **Concurrency** model. Don't add worker threads, processes, or queues it doesn't
  include.
- Never block the event loop in a server: no synchronous file or crypto calls such as `readFileSync`
  or `pbkdf2Sync` while handling a request, and no long computation. Move CPU-bound work to a worker
  thread (`node:worker_threads`). Synchronous calls are fine at startup and in short scripts.
- Make long-running async functions cancelable. Accept a `signal` option, and pass it on to `fetch`,
  timers, and streams. Time work out with `AbortSignal.timeout(ms)`, and combine signals with
  `AbortSignal.any`.
- Bound concurrency. Don't start thousands of requests at once with `Promise.all`; work through them
  in batches, or with a limit on how many run at a time.
- Start independent work together, with `Promise.all`, instead of awaiting each step in turn when
  the order doesn't matter.
- Release resources in `finally`, or with `using` and `await using` where every runtime in the
  **Runtimes** supports them, so they are released when an error is thrown.
- Connect streams with `pipeline` from `node:stream/promises`, which passes errors along and closes
  every stream, instead of `.pipe`, which does neither.

## Text for users and languages

This section covers the text a program shows people: its output, its help, and its errors as the
user sees them. With "English only" as the **Languages** value, the first two points still apply, so
the program can be translated later. Text in web pages also follows "Languages" in
`web-front-end.md`.

- Keep user-facing text in the **Languages** location, and refer to it by an ID. Logs and the
  messages of errors a library throws are for developers: keep them in English and out of the
  translations.
- Never build a sentence from pieces, and never choose a word form with `n === 1`. Write messages
  with plural selection, such as the ICU message `{count, plural, one {# file} other {# files}}`, or
  choose the form with `Intl.PluralRules`. Arabic has six plural categories (`zero`, `one`, `two`,
  `few`, `many`, and `other`), and Chinese has one.
- Format numbers, dates, and lists for the user's locale with `Intl.NumberFormat`,
  `Intl.DateTimeFormat`, and `Intl.ListFormat`: German writes 1234.5 as `1.234,5`. `toFixed` and
  `toString` are for text that programs read.
- `.length` counts UTF-16 code units, not characters: the family emoji 👨‍👩‍👧 has a `.length` of 8
  and is one character on screen. Count and cut text with `Intl.Segmenter` and
  `granularity: "grapheme"`.
- Sort text people read with `Intl.Collator` or `localeCompare`, and compare it after
  `normalize("NFC")`.
- When you insert a name or a number into a sentence in a right-to-left language, wrap it in the
  invisible isolation marks FSI and PDI (U+2068 and U+2069), so it doesn't reorder the text around
  it.
- Treat translations you write as drafts, and list their IDs in your report for a native speaker to
  review.

## Untrusted input

Treat every byte from outside the program as possibly malformed or hostile, especially in the
**Untrusted input** modules.

- Never run outside data as code: no `eval`, `new Function`, or string passed to `setTimeout`.
  Node.js's `node:vm` module isn't a sandbox; its documentation says it "is not a security
  mechanism".
- Parse JSON into `unknown`, and check it before you use it (see "Design with types").
- Don't merge parsed objects into others with `Object.assign` or a deep-merge function. `JSON.parse`
  turns a `"__proto__"` key into an ordinary property, and `Object.assign` then sets the target's
  prototype from it, so `Object.assign({}, JSON.parse('{"__proto__": {"isAdmin": true}}')).isAdmin`
  is `true` (prototype pollution). Copy only the fields you expect, and reject `__proto__`,
  `constructor`, and `prototype` keys in any merge.
- Run other programs with `execFile` or `spawn` and an array of arguments, never with `exec` or
  `shell: true` and a string built from input.
- Pass values to a database as query parameters, never in a string you build.
- Treat paths from input as hostile. Resolve them with `path.resolve(root, name)`, and check that
  the result starts with `root` plus `path.sep` before you open it.
- Limit sizes before you read or allocate: the body of each request, each file, and each array a
  client sends. Don't run a regular expression with nested repetition, such as `(a+)+`, over outside
  text, because some inputs take exponential time; limit the text's length first.
- Use `crypto.randomUUID()` and `crypto.getRandomValues()` for IDs and tokens, never
  `Math.random()`. Compare secrets with `crypto.timingSafeEqual`, whose timing doesn't reveal where
  two values differ. Hash passwords with `crypto.scrypt`, or a library the **Dependency policy**
  allows.
- Keep certificate checks on. Never set `NODE_TLS_REJECT_UNAUTHORIZED=0` or
  `rejectUnauthorized: false` to get past an error.
- Fetch a URL that input chose only after you check its host against an allowlist, so a request
  can't reach internal addresses (server-side request forgery).

## Native code

- Follow the **Native code** value. Prefer the platform, or WebAssembly, to a native addon: an addon
  needs a compiler or a prebuilt binary for every platform, and runs with the full rights of the
  process.
- Write addons against Node-API, whose interface stays the same across Node.js versions, so an addon
  doesn't need a new build for each one.

## Public APIs

- Keep every API small. List each entry point in the `exports` field of `package.json`; Node.js
  refuses an import of any other file in the package (`ERR_PACKAGE_PATH_NOT_EXPORTED`), so files
  outside `exports` stay private.
- Ship the types. Turn on `declaration`, and put the `types` condition first in each `exports`
  entry, so TypeScript finds the declarations before the JavaScript.
- Mark what is going away with a `@deprecated` tag in its doc comment, which editors show as struck
  through, and keep it for at least one release before you remove it.
- In the **Public API** packages, each of these breaks callers: removing or renaming an export or an
  `exports` entry; making an optional parameter or property required; narrowing a parameter's type
  or widening a return type; adding a required member to an interface that callers implement;
  changing the errors a function throws or their codes; and moving from CommonJS to ES modules. Ask
  before you make one, and mark it as `commits.md` requires.

## Documentation

Three kinds of docs describe a package, and each has its own reader:

- Doc comments (`/** … */`), which editors show when a reader hovers over a name.
- The API reference, which the **API docs** build from the doc comments.
- The README, which is the package's page on npm and in the repository.

Keep all three true. A change to behavior, a signature, an error, or an option updates every one of
them that describes it, in the same change.

### Doc comments

- Give every exported function, class, type, and constant a doc comment. Start with a one-sentence
  summary, because editors and the API reference show that sentence alone in lists.
- Don't repeat the types that the signature gives. Use `@param` to say what each parameter means,
  `@returns` for what comes back, `@throws` for each error and when, and `@example` for typical use.
- Give each module a comment at the top that says what it holds and why it is a module of its own.
  In a package's entry point, also say where the package fits, and link to its write-up in the
  **Design docs**, if there is one.
- State only what the code does. A claim about cost, ordering, or a limit must match the code, so
  check it there or in a test before you write it. Describe planned behavior as planned, never in
  the present tense.
- Copy each `@example` from a test, or keep it in a file the tests run, so it can't stop working
  without anyone noticing.
- Write code comments that explain why, not what, and keep them true when the code changes. Delete
  commented-out code instead of leaving it.

### Package READMEs

Give each of the **Published packages** a `README.md` in its folder. Its npm page is often the first
thing a new user reads, so write it for someone deciding whether to use the package, in this shape:

1. `# <package-name>`, then one short paragraph on what the package is and does.
2. `## Installation`: the install command, and the **Runtimes** it supports.
3. `## Usage`: a short example that runs, then what a user must know to avoid errors.
4. `## Status`: the version and how stable the API is. Then, kept apart, what is built today, what
   is left out by design, and what is planned.
5. `## Documentation`: links to the API reference, the package's write-up in the **Design docs**,
   and the project.
6. `## License`: the license, with a link to the license file.

- Use absolute URLs for links and images, so they work wherever the README is shown.
- Reread the README whenever the package's behavior or API changes. A test catches an example that
  stops working, but nothing catches a sentence that stops being true.

### Package metadata

For each of the **Published packages**, fill in `package.json`:

- `name`, `version`, and `description`, which is one plain-text sentence that npm's search results
  show.
- `license`, as a Software Package Data Exchange (SPDX) expression such as `"MIT"`, and
  `repository`, `homepage`, and `bugs`.
- `type`, `exports`, and `engines`, matching the **Runtimes**.
- `files`, which lists what the package includes, so nothing else is published by accident.
- `sideEffects: false`, when importing the package's modules does nothing but define them, so
  bundlers can drop the modules an app doesn't use.

Set `"private": true` in every `package.json` that must never be published, so `npm publish` refuses
it. Publish from CI with npm's trusted publishing, which uploads without a long-lived token and
attaches provenance: a signed record of the repository and workflow that built the package.

## Tests

- Follow the **Test layout**. Where `testing.md` is adopted, it sets how strict and complete the
  tests must be.
- Give every behavior change a test. Start every bug fix with a test that fails before the fix.
- Name each test for the behavior it checks: `it("rejects a length past the end of the input")`, not
  `it("works")`.
- Keep tests deterministic: use fake timers (`vi.useFakeTimers()`, or `mock.timers` in `node:test`),
  seed every random number generator, give each test its own temporary folder, and replace `fetch`
  at the boundary instead of reaching the network.
- Use strict comparisons: `node:assert/strict`, whose `deepEqual` rejects `1` where `"1"` was
  expected, and `toStrictEqual` in Vitest and Jest, which also checks for properties set to
  `undefined` and for the class of each object.
- Await every assertion on a promise: `await expect(load()).rejects.toThrow(ParseError)`. Without
  the `await`, the test ends before the promise settles, and passes whatever happens.
- Test the types of a public API too, with Vitest's `expectTypeOf`, or with `// @ts-expect-error`
  lines in a test file that `tsc` checks. `tsc` reports an `@ts-expect-error` that no longer has an
  error to expect, so a type that becomes too loose fails the check.
- Test the edges: empty, one, the maximum, one past the maximum, and malformed. For a parser,
  include truncated and oversized input.
- Keep snapshots small, and read a changed snapshot's diff before you accept it.
- Never leave `.only` in a test, or a `.skip` without a comment that says why. Run the tests on
  every version in the **Runtimes**.

## Style, lints, and the toolchain

- Format with the formatter in the **Lint configuration**, and don't hand-format against it.
- Lint with type information. With ESLint, use typescript-eslint's `strictTypeChecked` and
  `stylisticTypeChecked` configs with `parserOptions.projectService: true`, which lets the linter
  ask the compiler about types. Run it with `--max-warnings 0`, so a warning fails the check.
- When a type error or a lint rule is wrong in one place, silence it on that line alone, and say
  why: `// @ts-expect-error -- <reason>`, never `// @ts-ignore`, which keeps hiding the line after
  the error is gone, and `// eslint-disable-next-line <rule> -- <reason>`, never a comment that
  turns off every rule. Make ESLint report disable comments that no longer suppress anything, with
  `linterOptions.reportUnusedDisableDirectives: "error"`.
- Don't leave `console.log` calls used for debugging, or `debugger` statements, behind.
- Pin the TypeScript version exactly. TypeScript doesn't follow semantic versioning, so a minor
  release can add errors.
- Keep the **Runtimes** and the **Toolchain**. Don't raise `engines`, change the Node.js version in
  `.nvmrc`, or upgrade TypeScript as a side effect of another task; each is a change of its own.

## Dependencies and packages

- Follow the **Dependency policy**. Never add a package without asking. When you propose one, say
  what it does that the platform or existing code can't, and give its license, how well it is
  maintained, how many packages it brings in (from `npm ls --all`), whether it runs scripts when it
  is installed, and whether it ships its own types.
- Put what the code needs at run time in `dependencies`, build and test tools in `devDependencies`,
  and a framework the user's app must provide, such as the host of a plugin, in `peerDependencies`.
- Commit the lock file, update it in the same change as `package.json`, and install in CI with the
  **Package manager**'s command that fails when the two disagree: `npm ci`,
  `pnpm install --frozen-lockfile`, or `yarn install --immutable`.
- Every package in the tree can run code on your machine when it is installed. Install with
  `--ignore-scripts` in CI where the build allows it. pnpm 10 and later run install scripts only for
  the packages you allow.
- Check the signatures and provenance of what you installed with `npm audit signatures`.
- Don't add a package for a few lines the platform already provides.

## Before finishing

1. Run every **Check commands** command and read its output. Fix every warning, not only the errors.
2. Type-check every package, tests included, with `tsc --noEmit` or `tsc --build`, even when the
   build doesn't run `tsc`.
3. Run the tests on each runtime in the **Runtimes** that you can, and say which you couldn't. For
   code that runs in web pages, also do the browser checks in `web-front-end.md`.
4. If you changed exports, doc comments, or a README, build the API reference as the **API docs**
   say, with warnings as errors, and reread the changed prose against the code.
5. If you changed what a published package ships, run `npm pack --dry-run` and read the list of
   files. Check that the README, the license, the built JavaScript, and its `.d.ts` files are there,
   that every path in `exports` exists, and that sources you don't mean to ship, tests, and secrets
   aren't.
6. If you changed dependencies, check that the lock file is in the same change, and that a clean
   install with the **Package manager**'s CI command succeeds.
7. Review your diff as a reviewer would. Look for `any`, `as` casts, `!` assertions, `@ts-ignore`,
   `eslint-disable` comments without a reason, promises nothing awaits, `==`, `console.log`,
   `debugger`, `.only` in tests, a `catch` that hides an error, `Math.random()` used for an ID, and
   missing docs or tests. Then report what you ran, what you didn't, and what remains.
