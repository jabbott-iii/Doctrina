# Doctrina

Doctrina holds Claude Code rules and skills that are shared across repositories. None names a
particular project. The details that differ between repositories go in a **Project details**
section at the top of each rule, which each repository fills in when it adopts the rule. A skill
has no details of its own: it uses the values of the rules it relies on.

## Rules

- [`rules/writing.md`](rules/writing.md): spelling, grammar, numbers and units, technical writing
  for an audience from students to senior engineers, and a check to run before finishing. It
  covers all prose in a repository, including code comments and commit messages.
- [`rules/web-front-end.md`](rules/web-front-end.md): how to build a website or web app as a
  senior front-end developer and work with the user as a pair, covering semantic HTML, CSS that
  meets the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA, progressively enhanced
  JavaScript, security and privacy, performance budgets, hosting limits, and the checks to run in
  the browser. It relies on `writing.md` for page text and YAML checks, so adopt both.
- [`rules/commits.md`](rules/commits.md): copy-ready commit messages, how much Git Claude may run,
  one change per commit, the Conventional Commits format, and pull request descriptions, with no
  attribution lines. It relies on `writing.md` for the text of each message, so adopt both.
- [`rules/rust.md`](rules/rust.md): how to write Rust as a senior engineer and work with the user
  as a pair, covering type design, ownership, errors, hostile input, concurrency, `unsafe`,
  public APIs, tests, lints, and dependencies. Its documentation section covers doc comments and
  crate docs for docs.rs, a tested README for each crate on crates.io, and the docs.rs and
  crates.io metadata. It relies on `writing.md` for doc comments and error messages, so adopt
  both.
- [`rules/kotlin.md`](rules/kotlin.md): how to write Kotlin as a senior engineer and work with
  the user as a pair, covering type design, null safety, errors, coroutines and Flow, hostile
  input, Java and platform interop, binary compatibility, KDoc and Dokka docs, module READMEs,
  tests, lints, and Gradle builds. It relies on `writing.md` for KDoc and error messages, so
  adopt both.
- [`rules/android.md`](rules/android.md): how to build Android apps with Jetpack Compose as a
  senior mobile developer and work with the user as a pair, covering app architecture, Compose
  state and performance, adaptive layouts, accessibility, translations, lifecycle and process
  death, background work, Room migrations, security and privacy, tests, and release builds. It
  relies on `kotlin.md` for the language and on `writing.md` for strings, so adopt all three.
- [`rules/kotlin-multiplatform.md`](rules/kotlin-multiplatform.md): how to share Kotlin code
  between Android and iOS as a senior mobile developer and work with the user as a pair,
  covering what to share, source sets and targets, common-code limits, platform APIs, the API
  that Swift sees, coroutines across platforms, the Xcode toolchain, and tests on every target.
  Its Compose Multiplatform section covers shared UI: setup and entry points, shared resources,
  iOS behavior and look, native views, accessibility, iOS performance, previews, and UI tests.
  It relies on `kotlin.md`, `android.md`, `swift.md`, and `writing.md`, so adopt all five.
- [`rules/swift.md`](rules/swift.md): how to write Swift and SwiftUI as a senior mobile developer
  and work with the user as a pair, covering type design, optionals and errors, memory, strict
  concurrency, SwiftUI state and identity, layout, accessibility, localization, persistence,
  security and privacy, Kotlin Multiplatform interop, tests, and release. It relies on
  `writing.md` for doc comments and strings, so adopt both.
- [`rules/flutter.md`](rules/flutter.md): how to build cross-platform mobile apps with Dart and
  Flutter as a senior mobile developer and work with the user as a pair, covering Dart types,
  errors, and isolates, widgets and `build`, layout and performance, state management,
  navigation, platform adaptation, accessibility, localization, platform channels, data and
  security, tests, and release. It relies on `writing.md`, and on `android.md`, `kotlin.md`, and
  `swift.md` for native code, so adopt those that apply.
- [`rules/roadmap-and-docs.md`](rules/roadmap-and-docs.md): how to plan and document a project
  in the style of Nadir's `docs/` folder, covering the numbered core documents, a roadmap of
  milestones and checkable tasks with a backlog of triggers, append-only decision records,
  specs for each part of the system, a feature list tied to the roadmap, and where status is
  reported. It includes a template for each document, and relies on `writing.md` for the text,
  so adopt both.
- [`rules/teaching-materials.md`](rules/teaching-materials.md): how to write courses, workbooks,
  and formal articles that educate readers, as a university professor working with the user as
  a pair. It covers when to use Markdown, Jupyter notebooks, or LaTeX; objectives-first course
  design; exercises, answer keys, and rubrics; each format's practices; accessible PDFs;
  citations; and integrity and student privacy. It relies on `writing.md`, so adopt both.

## Skills

- [`skills/next-task/`](skills/next-task/SKILL.md): `/next-task [task-id]` works through the
  roadmap one task at a time. It picks the next unblocked task (or the one named), asks the
  questions and checks the decisions the task depends on, makes the smallest complete change,
  runs the task's checks, ticks the box only when they pass, updates the documents, and reports
  what ran and what didn't. It relies on `roadmap-and-docs.md`, `commits.md`, and `writing.md`,
  so adopt those first.
- [`skills/fix-doc-drift/`](skills/fix-doc-drift/SKILL.md): `/fix-doc-drift [scope]` finds
  statements in the documentation that no longer match the code, the tools, or the project's
  records, and corrects them. The scope is a path, an area, a Git range, or, when empty, every
  document. It decides which side is wrong before it edits, asks wherever a spec or decision may
  be right and the code wrong, leaves the records of the past alone, and suggests checks that
  would catch the same drift next time. It relies on `writing.md` and `commits.md`, and uses
  `roadmap-and-docs.md` where it is adopted.
- [`skills/draw-diagrams/`](skills/draw-diagrams/SKILL.md): `/draw-diagrams [file or view]`
  draws formal architecture diagrams of the project as Mermaid in Markdown, in `diagram/` or the
  folder `roadmap-and-docs.md` names: C4 views, UML class, component, and sequence diagrams,
  data-flow, state, data-model, and deployment diagrams. Built parts are solid and planned ones
  dashed with their task, and every file records the commit it was drawn from, so later runs
  rebuild only the diagrams whose sources changed. It relies on `roadmap-and-docs.md`,
  `commits.md`, and `writing.md`.
- [`skills/phase-gates/`](skills/phase-gates/SKILL.md): `/phase-gates [plan | phase ID]`
  clusters the roadmap's tasks into phases by dependency, risk, and deliverable, and gives each
  phase a gate of checkable criteria: integration, budgets, the full check, open work,
  decisions, documents, and risks. Given a phase, it evaluates that gate with evidence gathered
  in this session and records the result, and you confirm a pass. Empty, it shows every gate's
  state. It relies on `roadmap-and-docs.md`, `commits.md`, and `writing.md`.

## Adopt a rule in a repository

These steps use `writing.md`; replace it with the rule you are adopting.

1. Create the repository's rules folder if it doesn't exist yet:

   ```bash
   mkdir -p path/to/repository/.claude/rules
   ```

2. Copy the rule into it:

   ```bash
   cp rules/writing.md path/to/repository/.claude/rules/writing.md
   ```

3. Open the copy and replace every `[FILL IN: …]` value under **Project details**.
4. Check that none are left. This command searches only the value lines, because the section's
   introduction mentions the placeholder too:

   ```bash
   grep -n '^- \*\*.*\[FILL IN' path/to/repository/.claude/rules/writing.md
   ```

   The command prints nothing when every value is filled in.

Claude Code reads the files in `.claude/rules/` on its own, starting with the next session:

- A rule without `paths` front matter, such as `writing.md`, applies to every session in that
  repository.
- A rule with `paths` front matter, such as `web-front-end.md` or `rust.md`, applies only when
  Claude works on files that match one of its patterns. Edit the list to fit the repository:
  add template files such as `**/*.liquid` or `**/*.njk`, and remove file types the repository
  doesn't use.

If a copy still has unfilled values, the rule tells Claude to infer them from the repository and
to tell you which ones are missing.

## Adopt a skill in a repository

These steps use `next-task`; replace it with the skill you are adopting. Adopt the rules the
skill relies on first.

1. Create the repository's skills folder if it doesn't exist yet:

   ```bash
   mkdir -p path/to/repository/.claude/skills
   ```

2. Copy the skill's folder into it:

   ```bash
   cp -r skills/next-task path/to/repository/.claude/skills/
   ```

Start the skill by typing `/next-task`, with a task ID if you want a particular task. Its front
matter sets `disable-model-invocation: true`, so Claude never starts it on its own.
