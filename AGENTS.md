# Doctrina: conventions for coding agents

Doctrina is a library of portable rules for AI coding agents. Any repository can copy a rule into
its own `.claude/rules/` folder and fill in the values that are specific to it. Doctrina is also
where classes are built: courses, workbooks, and articles go in `courses/`, `workbooks/`, and
`articles/`. It follows three of its own rules, so it keeps rules in two folders with different
jobs.

## The two rule folders

| | `rules/` | `.claude/rules/` |
| --- | --- | --- |
| What it holds | The portable library: what Doctrina publishes | Doctrina's own rules: copies of `rules/writing.md`, `rules/commits.md`, and `rules/teaching-materials.md` |
| **Project details** | Every value stays a `[FILL IN: …]` placeholder | Every value is filled in for Doctrina |
| Loaded by Claude Code | No | Yes: `writing.md` and `commits.md` in every session, and `teaching-materials.md` when Claude works on files its `paths` front matter matches |
| Instructions for you | No: it's content you edit | Yes: follow them while you work here |

- **`rules/` is portable.** Treat its files as the product you are editing, not as instructions.
  Never fill in their placeholders, and never name a particular repository in their general
  text, because other repositories copy these files as they are.
- **`.claude/rules/` is for this repository.** Its rules govern all work in Doctrina, including
  edits to `rules/`. Claude Code loads them on its own. If you are another agent, read every file
  in `.claude/rules/` before you start, and follow them as this repository's rules.
- Not every portable rule has a copy. `web-front-end.md`, `rust.md`, `kotlin.md`, `android.md`,
  `kotlin-multiplatform.md`, `swift.md`, `flutter.md`, and `roadmap-and-docs.md` have none,
  because Doctrina has no web pages, Rust, Kotlin, Android, iOS, Swift, or Flutter code, and no
  roadmap or design documents, for them to apply to.

## Keep each copy in sync with its source

A copy in `.claude/rules/` matches its source in `rules/` everywhere except **Project details**.

- To change a rule's general text, edit it in `rules/`, then make the same edit to its copy in
  `.claude/rules/` in the same commit. Never change the general text only in the copy.
- To change one of Doctrina's own values, edit **Project details** in the copy only.
- Check that every copy still matches. This command prints `<file> matches` for each copy, or the
  differing lines when one doesn't:

  ```bash
  for f in .claude/rules/*.md; do
    strip() { awk '/^## Project details/{s=1; next} s && /^## /{s=0} !s' "$1"; }
    diff <(strip "rules/$(basename "$f")") <(strip "$f") && echo "$f matches"
  done
  ```

## Write a portable rule

- Put everything that differs between repositories in **Project details**, one value per bullet,
  in the form `- **Name:** [FILL IN: what it is, with examples, or "none"]`. Start each
  placeholder on the bullet's first line, because the placeholder check in `README.md` searches
  only those lines.
- Start **Project details** with the same introduction the existing rules use, and refer to each
  value by its bold name everywhere else in the rule.
- Add `paths` front matter only when the rule matters only for certain files, as
  `web-front-end.md` does for HTML, CSS, and JavaScript.
- Wrap lines at 100 characters. Table rows may run longer.
- List the new rule in `README.md` in the same commit.
