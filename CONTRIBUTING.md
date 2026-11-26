# Contributing to Doctrina

Doctrina welcomes corrections and improvements to its rules, skills, and course materials, and
proposals for new ones. For anything larger than a small fix, open an issue first, so the change
can be agreed on before you write it.

## How the repository works

[`AGENTS.md`](AGENTS.md) explains the layout, and it applies to people as much as to coding agents.
In short:

- `rules/` and `skills/` hold the portable library. Their **Project details** values stay
  `[FILL IN: …]` placeholders, because other repositories copy the files as they are.
- `.claude/rules/` and `.claude/skills/` hold the copies that Doctrina follows itself. A change to
  a rule or a skill goes into both, in the same commit.
- `courses/`, `workbooks/`, and `articles/` hold the course materials, which follow
  [`.claude/rules/teaching-materials.md`](.claude/rules/teaching-materials.md). Answer keys live in
  each course's `solutions/` folder, and the coursework never links to them.

## Set up

Rules and skills need nothing but a text editor and Git. Course materials need the notebook
environment, a Python 3.12 virtual environment that [uv](https://docs.astral.sh/uv/) creates:

```bash
uv venv .venv --python 3.12
```

```bash
VIRTUAL_ENV=.venv uv pip install -r requirements.txt
```

LaTeX documents also need TeX Live with LuaLaTeX, `latexmk`, and biber. A course's own setup guide
lists anything else it needs, such as [LUA101's `setup.md`](courses/lua101/setup.md).

## Check your change

Before you open a pull request, run the checks for what you changed:

- **Any text:** the "Before finishing" steps in
  [`.claude/rules/writing.md`](.claude/rules/writing.md).
- **A rule or a skill:** the commands in "Keep each copy in sync with its source" in
  [`AGENTS.md`](AGENTS.md), which print `<file> matches` for each copy, and the placeholder check
  in [`README.md`](README.md), run on `.claude/rules/*.md`, which prints nothing.
- **A notebook:** run it from top to bottom. Each notebook passes when the command prints a line
  ending in `passed`:

  ```bash
  .venv/bin/pytest --nbmake courses/lua101/modules/01-first-steps/lab01.ipynb
  ```

- **A LaTeX document:** build it with `latexmk -lualatex`, from the folder its README names.
- **A course's website:** build it from the course's folder, and check that it finishes without
  errors:

  ```bash
  ../../.venv/bin/jupyter book build --html
  ```

GitHub Actions runs checks on every pull request to `main`:

- **Copies** runs the copy checks and the placeholder check, on every change.
- **LUA101** runs when a change touches `courses/lua101/` or `requirements.txt`. It checks each lab
  as students get it and with its answer key (`courses/lua101/tools/check_lab.py`), runs the
  graded notebooks' sources, has nbgrader pass each source and fail each student version, checks
  that the student versions match their sources, runs the project graders' self-tests, and builds
  the website. The [workflow](.github/workflows/lua101.yml) shows each command.
- **PE101** runs when a change touches `courses/pe101/` or `requirements.txt`. It runs
  `promptlab`'s tests, checks each lab as students get it and with its answer key
  (`courses/pe101/tools/check_lab.py`), runs the graded notebooks' sources, has nbgrader pass each
  source and fail each student version, checks that the student versions match their sources, and
  builds the website. The course calls no model, so the
  checks need no API key. The [workflow](.github/workflows/pe101.yml) shows each command.

None of these workflows builds LaTeX documents, so build any you add yourself.

## Commit

Doctrina uses [Conventional Commits](https://www.conventionalcommits.org/), as
[`.claude/rules/commits.md`](.claude/rules/commits.md) describes: a type such as `feat`, `fix`, or
`docs`, an optional scope such as `writing` or `lua101`, and a summary in the imperative mood.
Make each commit one change. A new rule or skill and its entry in `README.md` share a commit, and
so do a change to a rule or skill and the same change to its copy.

## Open a pull request

The pull request template asks what changed and why, how you checked it, and what is left for
later. The maintainer, whom [`CODEOWNERS`](.github/CODEOWNERS) names, reviews every pull request.

## Report a problem

- **A bug, a request, or an error in course materials:** open an issue and choose the form that
  fits. Course corrections are recorded in each course's `ERRATA.md`.
- **A question:** ask in [Discussions](https://github.com/jabbott-iii/Doctrina/discussions).
- **A security vulnerability:** follow [`SECURITY.md`](SECURITY.md), and never open a public issue
  for it.

## Licenses

By contributing, you agree that your contribution is licensed under the licenses that already
cover the files you change: the MIT License in [`LICENSE`](LICENSE), and, for course materials,
the Creative Commons Attribution 4.0 International license (CC BY 4.0) for text and figures, as each
course states.

## Coding agents

Agents follow [`AGENTS.md`](AGENTS.md) and every rule in `.claude/rules/`. Claude Code loads the
rules on its own.
