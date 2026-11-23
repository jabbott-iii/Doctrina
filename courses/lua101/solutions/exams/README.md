# Exams

Each exam's LaTeX source holds its questions and its key, so the sources live here, with the other
keys, and never in `exams/`. The website doesn't publish exams.

| File | What it is |
| :- | :- |
| `midterm.tex` | The midterm exam, on modules 1–7: 14 questions, 75 points, 75 minutes |
| `final.tex` | The final exam, on all modules, weighted toward modules 8–14: 19 questions, 100 points, 120 minutes |
| `latexmkrc` | Settings for `latexmk`: LuaLaTeX, and the shared preamble in `../../latex/` |

## Building

Run these from this folder. The first command builds the exam that students sit, without
solutions, as `midterm.pdf`; the second builds the key, with every solution and its grading
notes, as `midterm-key.pdf`:

```bash
latexmk -lualatex midterm.tex
```

```bash
latexmk -lualatex -jobname=midterm-key -usepretex='\PassOptionsToClass{answers}{exam}' midterm.tex
```

The final exam builds the same way, with `final` in place of `midterm`:

```bash
latexmk -lualatex final.tex
```

```bash
latexmk -lualatex -jobname=final-key -usepretex='\PassOptionsToClass{answers}{exam}' final.tex
```

Git ignores the PDFs and LaTeX's build files. Print each exam from its student PDF, and keep the
keys' PDFs with the instructor.

## Accessibility

The `exam` class doesn't support PDF tagging yet, so neither PDF meets WCAG 2.1 Level AA for screen
readers. As the plan decided, a student who needs an accessible version gets one through the
disability services office, with the accommodations it approves. Make that version from this
source, so that a correction reaches every version.

## Checks

Before each term: build both versions of each exam and read them; confirm that `midterm.pdf` and
`final.pdf` show no solutions; and work every question again in Lua 5.4, and the final exam's C
questions with a C compiler. Each question names the objectives it
assesses, which the syllabus defines, and the key's notes give the points for each part.
