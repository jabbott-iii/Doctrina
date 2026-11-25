---
paths:
  - "**/*.ipynb"
  - "**/*.tex"
  - "**/*.bib"
  - "**/*.sty"
  - "**/*.cls"
  - "**/_toc.yml"
  - "**/myst.yml"
  - "**/_quarto.yml"
  - "courses/**"
  - "workbooks/**"
  - "articles/**"
---

# Teaching materials standards

These rules cover materials written to educate readers: courses, workbooks, and formal articles for
journals and informational series. They describe how a university professor designs and writes them,
and which of Markdown, Jupyter notebooks, and LaTeX to use for each piece. The text follows
`writing.md` in this folder.

Apply them to materials you write or edit. Don't restructure published material only to make it
conform; bring a section into shape when you are already changing it.

## Project details

A repository fills in this section when it adopts the rule, and the rest of the rule refers to
each value by its bold name. If a value still reads `[FILL IN: …]`, the rule isn't set up here
yet. Work out that value from the repository itself, and tell the user which values are missing
so they can fill them in.

- **Materials:** courses in `courses/<code>/`, workbooks in `workbooks/<name>/`, and articles in
  `articles/<slug>/`. None exists yet; the first course, workbook, or article creates its folder.
- **Audience:** set by each piece of material: a course in its syllabus
  (`courses/<code>/README.md`, under "Prerequisites"), and a workbook or article in its
  introduction.
- **Course structure:** set by each course's syllabus, which gives the term's length, or the
  suggested pace of a self-paced course, and its modules. Every module follows the shape under
  "Modules" in this rule.
- **Learning objectives:** listed in each course's syllabus, with IDs of the form
  `LO-<module>.<n>`, such as `LO-3.2`.
- **Build tool:** Jupyter Book, the user's choice on 2026-11-22, for the Markdown and notebooks,
  and `latexmk` for standalone LaTeX documents. The first course adds the book's configuration,
  and its build command to this value.
- **Notebook environment:** Python 3.12, with packages pinned in `requirements.txt` at the
  repository root, which the first notebook adds. Notebooks are paired with `py:percent` files
  through Jupytext, and outputs are cleared unless they are part of the lesson. Graded work uses
  nbgrader.
- **LaTeX setup:** LuaLaTeX, built with `latexmk -lualatex`, and biblatex with biber. Each course
  keeps its shared preamble in `courses/<code>/latex/preamble.sty`, which its first LaTeX
  document adds.
- **Venue:** "none" yet. Before an article is written, its folder's `README.md` names its venue,
  template, style guide, and length limits.
- **Citation style:** biblatex's `authoryear` style for course materials, with each course's
  `references.bib`, and the venue's style for articles.
- **Notation:** each course's `notation.md`, with its LaTeX macros in
  `courses/<code>/latex/macros.tex` and the same macros in the book's math configuration.
- **Assessment:** each course's syllabus gives its grading scheme. Answer keys, rubrics with
  model answers, and nbgrader source notebooks may be committed here, the user's choice on
  2026-11-22, even though this repository is public. Keep them apart from the coursework, in
  `courses/<code>/solutions/`, and never link to them from the coursework or include them in the
  built book.
- **License:** text and figures under the Creative Commons Attribution 4.0 International license
  (CC BY 4.0), the user's choice on 2026-11-22, and code under the MIT License in `LICENSE`. Mark
  third-party material with its own license and credit.
- **Accessibility standard:** WCAG 2.1 Level AA, the user's choice on 2026-11-22. Check PDFs with
  a PDF accessibility checker, such as veraPDF.
- **Check commands:** `pytest --nbmake` on changed notebooks, `latexmk -lualatex` on changed
  LaTeX documents, and the Jupyter Book build once the first course adds it.
- **Errata:** each course's `ERRATA.md`, with editions named by term, such as "Spring 2027", or,
  for a self-paced course, by release date, such as "the 2026-11-25 edition".

## Decisions that are the user's

Stop and ask the user before you:

- add, remove, or reword a learning objective;
- change grading weights, a rubric, a deadline, or a course policy;
- put a solution or an answer key anywhere students can see it;
- renumber or remove a published module, exercise, or equation that readers may cite;
- change the format of existing material (for example, from Markdown to LaTeX);
- add a package to the **Notebook environment** or the **LaTeX setup**;
- use a figure, text, or data set that someone else owns;
- change the **License**;
- or submit, share, or publish anything outside the repository.

## Making a change

- **Read what comes before.** Read the **Learning objectives**, the module or chapter around the
  change, the **Notation**, and the materials that come before it, so a new piece builds on what
  readers have already learned. Check the **Materials** to find where new material belongs.
- **Never invent a source.** Cite only works you have confirmed exist and say what you cite them
  for. Never make up a citation, a DOI, a quotation, or a statistic. If you can't confirm one, mark
  the place `[citation needed: …]` and say so in your report.
- **Check every answer yourself.** Work each new exercise, run each code example, and recompute each
  number before you report it done. An error in a key teaches the error.

## Choose the format

Start from what the reader must do with the material, and choose the lightest format that lets
them do it.

| Material | Format | Why |
| --- | --- | --- |
| The course hub: syllabus, schedule, policies, and reading list | Markdown | Read on screen and edited every term; renders on GitHub and in site builders; reviews as plain text |
| Lecture notes and readings | Markdown, with math in `$…$` | Prose comes first, and Markdown renders LaTeX math |
| Labs, demonstrations, and workbooks where readers run code | Jupyter notebook | Readers run the code, change it, and see the result beside the explanation |
| Assignments where the output is the lesson (data analysis, plots, simulations) | Jupyter notebook | The tables and figures come from code the reader can rerun |
| Problem sets and exams with substantial math, printed or handed in as PDF | LaTeX | Exact math typesetting, and one source for the student and answer-key versions |
| Formal articles, technical reports, course readers, and textbooks | LaTeX | The venue's template, numbered cross-references, a bibliography, and consistent typography across a long document |
| Slides with mathematics | LaTeX (the Beamer class) | The same notation and macros as the notes and the exams |

- **Default to Markdown.** It opens anywhere, diffs cleanly, and is the easiest to review and
  correct.
- **Use a notebook only when the reader must run code.** A notebook that shows code nobody runs
  is Markdown with extra weight: its JSON is hard to review, and its outputs can go stale.
- **Use LaTeX when the typesetting matters:** heavy mathematics, long documents with numbered
  cross-references and a bibliography, printed or PDF delivery, or a venue that requires its
  template.
- **Keep one source for each piece of content.** Produce other formats from it with the
  **Build tool** (for example, a PDF of the notes, or a web page of a notebook), and never keep
  hand-made copies in two formats that can drift apart.
- **Write math in LaTeX syntax everywhere.** Markdown and notebooks render it too, so the
  notation in a lab matches the notes and the exam. Keep the symbols in the **Notation**.

## Designing a course

### Start from what students will be able to do

- Write the **Learning objectives** first, then the assessments that show each one was met, and
  only then the instruction that prepares students for those assessments. Every module,
  exercise, and exam question names the objectives it serves.
- Write objectives as observable actions, with a verb a grader can check: "derive", "compute",
  "implement", "compare", "justify". Not "understand", "know", or "appreciate", which no one can
  observe.
- Give every objective an ID in the format the **Learning objectives** use, and never reuse an
  ID once a term has started.

### The course hub

Keep the syllabus in Markdown, in this shape:

```markdown
# <Course code>: <Course title>

<One paragraph: what the course is about, who it is for, and what students will be able to do.>

## Learning objectives
- **LO-1:** <An observable action, with the conditions and standard where they matter.>

## Prerequisites
<What students must already know, with the course or the self-check that shows it.>

## Schedule
| Week | Topic | Reading | Due |
| :- | :- | :- | :- |
| 1 | <Topic> | <Reading, linked> | <Assignment> |

## Assessment
| Component | Weight | Objectives |
| :- | :- | :- |
| <Problem sets> | <30%> | <LO-1, LO-2> |

## Policies
<Late work, collaboration and academic integrity, the use of generative AI tools, and
accommodations for disability, each stated plainly.>
```

- State the course's policy on generative AI tools explicitly: what is allowed, what must be
  disclosed, and what isn't allowed. Students can't follow a policy they have to guess.
- Keep personal details (office hours, phone numbers) in the place the institution requires,
  such as the learning management system, not in a public repository.

### Modules

Give each module the same shape, from the template in the **Course structure**:

1. Its objectives, by ID, and its prerequisites, by module.
2. An estimate of the time it takes.
3. The content, one idea at a time: the concept, a worked example, then practice.
4. A short summary of what the module established.
5. Self-check questions with answers students can see, to practice retrieving what they learned.
6. Further reading, each with a sentence on why it is worth reading.

### Teaching that works

- **Introduce one idea at a time,** and build on what came before. Name the prerequisite when a
  module depends on one.
- **Show, then fade, then ask.** Give a fully worked example, then a partly worked one for the
  student to finish, then a problem to solve alone.
- **Name the common misconceptions** and show why each is wrong, with an example that breaks it.
- **Make abstract ideas concrete first:** a small example with numbers before the general
  statement, and the general statement before the proof.
- **Space and mix practice.** Revisit earlier objectives in later problem sets, and mix problem
  types, so students practice choosing a method, not only applying the one they learned last.
- **Offer more than one way in:** text with a figure, an equation with a worked example, code
  with a plain-language explanation.

## Workbooks and assessment

### Exercises

Give every exercise a stable ID, the objectives it serves, its difficulty, and an estimate of its
time:

```markdown
### Exercise 3.4 (LO-3.2, ★★, about 20 minutes)

<The problem, stated so it has one reading. Give every quantity with its units, and say what
form the answer takes.>

<details>
<summary>Hint</summary>
<A hint that points to the method without giving away the answer.>
</details>
```

- Never renumber a published exercise: students, solutions, and grade records refer to it by
  number. Add a new exercise with the next free number, and mark a withdrawn one as withdrawn.
- Mix kinds of problem: conceptual questions that check understanding, computations that build
  fluency, and transfer problems that apply an idea somewhere new.
- Put a worked example before the first exercise of each new kind.
- Order hints from gentle to specific, so a student takes only the help they need.

### Answer keys and rubrics

- Keep answer keys where the **Assessment** says, and never in student-facing files or published
  output.
- Explain the reasoning in each solution, not only the final answer, and note the mistakes
  students commonly make.
- Write a rubric for every assessment that isn't graded automatically: the criteria, what each
  level of performance looks like, and the points for each.
- Keep the student and key versions in one source where the format allows it, such as LaTeX's
  `exam` class or nbgrader, so a correction reaches both.

## Markdown

- Write GitHub-flavored Markdown, one file for each module or lecture, with one `#` title and
  sections that start at `##`, as `writing.md` describes.
- Write inline math as `$…$` and display math as `$$…$$`, or in a fenced block tagged `math`;
  GitHub renders all three. Keep a `$` that isn't math inside code formatting.
- Give every image alternative text that says what it shows and why it matters, and a caption
  when the text refers to it.
- Link the course hub's pages with relative links, so the course works wherever the repository
  is served.

## Jupyter notebooks

### Structure

Build every notebook in this order:

1. A Markdown cell with the title (`#`), the objectives by ID, the prerequisites, and the time it
   takes.
2. A setup cell: every import, the random seed, and a printout of the versions that matter.
3. Sections that alternate a Markdown cell of explanation with short code cells, each doing one
   thing.
4. Exercises under their own headings (`### Exercise 2.3`), each followed by a cell that checks
   the answer with `assert` and a message that says what went wrong.
5. A summary cell of what the notebook showed.

### Running and storing notebooks

- A notebook must run from top to bottom in a fresh kernel, with no hidden state. Before you
  report one done, restart the kernel and run every cell, or run it from the command line with
  `jupyter nbconvert --to notebook --execute`.
- Store notebooks as the **Notebook environment** says. Clear outputs, unless an output is part
  of the lesson (a plot students discuss); then rerun the whole notebook before saving, so every
  output matches its code.
- Pair notebooks with a text format where the **Notebook environment** uses Jupytext
  (`jupytext --set-formats ipynb,py:percent notebook.ipynb`), so reviews read as ordinary diffs.
- Pin the environment in the file the **Notebook environment** names, and add a package only
  after the user agrees.
- Make every run repeatable: set random seeds, bundle small data sets, and fetch larger ones from
  a stable address with a checksum. Say how long any slow cell takes, and offer a smaller
  default.
- Never put a secret, an API key, or a student's data in a notebook, its outputs included.

### Graded notebooks

- With nbgrader, mark the solution in each graded cell with `### BEGIN SOLUTION` and
  `### END SOLUTION`, and hidden tests with `### BEGIN HIDDEN TESTS` and `### END HIDDEN TESTS`,
  so one notebook produces both the student version and the key.
- Test that every notebook runs, in the **Check commands**, for example with
  `pytest --nbmake`. `pytest --nbval` also compares stored outputs, and `--nbval-lax` compares
  only the cells marked `#NBVAL_CHECK_OUTPUT`.

### Accessibility in notebooks

- Use Markdown headings in order, so a screen reader can move through the notebook by heading.
- Give every figure labeled axes with units, a title, and a palette that people with color
  vision deficiencies can tell apart, and say in the text what the reader should notice.
- Give images alternative text, as in Markdown.

## LaTeX

### Building

- Build with the command in the **LaTeX setup**, usually `latexmk`, which reruns LaTeX and the
  bibliography tool until the cross-references settle.
- Commit the sources, not the build files (`.aux`, `.log`, `.bbl`, and the rest). Commit a PDF
  only where the **Build tool** publishes it.
- Never compile a document from an untrusted source with `-shell-escape`; it lets the document
  run commands on the machine. minted 3 doesn't need it on TeX Live 2024 or later.

### Structure

- Keep one main file per document, with a file for each chapter or section, brought in with
  `\input` or `\include`, and the shared preamble in the file the **LaTeX setup** names.
- Define notation as semantic macros in the **Notation** file (`\newcommand{\vect}[1]{…}`), so a
  change of notation is made in one place.
- Use the standard packages for each job:

  | Job | Package |
  | --- | --- |
  | Mathematics, theorems, and proofs | `amsmath`, `amssymb`, `amsthm`, `mathtools` |
  | Numbers with units | `siunitx` |
  | Tables | `booktabs` |
  | Figures and plots drawn in LaTeX | `graphicx`, `tikz`, `pgfplots` |
  | Links and cross-references | `hyperref`, then `cleveref` after it |
  | Bibliographies | `biblatex` with `biber`, unless the **Venue** requires BibTeX |
  | Code listings | `listings`, or `minted` for richer highlighting |
  | Exams with answer keys | the `exam` class |
  | Slides | the `beamer` class |

### Mathematics, figures, and tables

- Define every symbol the first time it appears, and keep it in the **Notation**.
- Number only the equations the text refers to, and use `align` rather than `eqnarray`. Punctuate
  displayed equations as part of the sentence.
- Refer to figures, tables, sections, and equations by `\label` and `\cref`, never by a typed
  number, and put each `\label` after its `\caption`.
- Make figures vector graphics (PDF from the plotting code, or TikZ), keep the code that drew
  them, and refer to each figure in the text before it appears. Write captions that say what to
  notice.
- Lay out tables with `booktabs` (`\toprule`, `\midrule`, `\bottomrule`). Its guidance is to
  never use vertical rules or double rules. Put units in the column headers.
- Typeset quantities with `siunitx` (`\qty{9.81}{\metre\per\second\squared}`), so numbers and
  units are spaced consistently.

### Exams

- Write exams with the `exam` class, and put each solution in a `solution` environment. The
  `answers` class option, or `\printanswers`, prints the solutions, so one source produces the
  exam and its key.
- Build the answer-key PDF only where the **Assessment** says keys go, and never publish it with
  the student version.

### Accessible PDFs

- A PDF from LaTeX isn't accessible to screen readers unless it is tagged. When the
  **Accessibility standard** requires accessible documents, either produce a tagged PDF or
  publish an accessible HTML or Markdown version alongside it.
- To tag a PDF, put `\DocumentMetadata{tagging=on}` before `\documentclass`, with a recent LaTeX
  release, and give every graphic alternative text with the `alt` key
  (`\includegraphics[alt={…}]{…}`). The tagging code is still under active development.
- Check how well every class and package supports tagging with
  `\DocumentMetadata{tagging=on, check-tagging-status}`, which writes a report at the end of the
  log, or with the LaTeX Project's tagging status list. In November 2026 the report listed the
  `exam` class and `minted` as currently incompatible, and `amsmath`, `mathtools`, `siunitx`,
  `tikz`, `biblatex`, `hyperref`, and `cleveref` as partially compatible.
- Don't trust a PDF's claim to be tagged. An exam built with the incompatible `exam` class still
  reports "Tagged: yes". Check each PDF that must meet the **Accessibility standard** with a PDF
  accessibility checker, such as veraPDF for PDF/UA, and publish an accessible HTML or Markdown
  version of anything that fails, exams included.

## Formal articles

Write articles for journals and informational series in LaTeX, from the **Venue**'s template.
Follow its style guide and length limits, and where they differ from this rule, follow the venue.

### Structure

```text
Title, authors, and affiliations
Abstract: the problem, the approach, the main result, and why it matters, in the venue's limit
Keywords
1. Introduction: the problem, why it matters, what this article contributes, and its outline
2. Background: what readers need, and the work it builds on, with citations
3. The body: the method and results for research, or the exposition for an informational article
4. Discussion: what the results mean, their limits, and the questions they leave open
5. Conclusion
Acknowledgments, the data and code availability statement, and references
Appendices: proofs, derivations, and details that would interrupt the main text
```

### Writing

- Use a formal register: no contractions, and add articles and exams to the formal documents that
  `writing.md` names. Use "we" where the field's style allows it.
- State the contribution in the introduction, plainly enough to check against the results.
- State the limitations in the discussion. Never claim more than the evidence shows.
- Define every term and symbol at first use, even ones the field takes for granted; the reader
  may come from another field.

### Citations

- Cite in the style the **Citation style** names, from its bibliography file. Give every entry
  its complete fields and a DOI where one exists.
- Cite a source for every claim that isn't common knowledge in the field or shown in the article.
  Prefer primary sources to summaries of them.
- Cite only what you have confirmed, as "Making a change" says. Quote rarely, briefly, and with
  attribution; paraphrase in your own words otherwise.
- Get permission for every figure, table, or long quotation from someone else's work, unless its
  license allows the use, and credit it as the license requires.
- When an article draws on code or data, publish them, or say where readers can get them, in the
  availability statement. A notebook that reproduces the results makes a good supplement.

## Accuracy, integrity, and privacy

- Check every fact, number, and code example against its source or by running it, before it
  reaches students.
- Log every correction to published material in the **Errata**, with the date and what changed,
  so students who used the old version can tell.
- Release materials under the **License**, and mark third-party material with its own license and
  credit.
- Never put students' names, grades, submissions, or other records in course materials,
  notebooks, or examples. Privacy laws such as FERPA in the United States protect them.
- Use examples, names, and contexts that students from different backgrounds can follow, and
  avoid ones that need a narrow cultural reference to make sense.

## Before finishing

1. Run every **Check commands** command and read its output.
2. Run every changed notebook from a fresh kernel, top to bottom, and fix any cell that fails or
   depends on state from an earlier run.
3. Compile every changed LaTeX document, and fix every undefined reference or citation and every
   error. Read the remaining warnings, and fix overfull lines that show in the output.
4. Build the published output with the **Build tool**, and read it as readers will see it.
5. Work every new exercise and compare your answer with the key, and confirm that every new
   exercise names its objectives.
6. Check accessibility against the **Accessibility standard**: alternative text on every image,
   headings in order, readable figures, and an accessible version of any PDF that needs one.
7. Confirm every citation you added, and list any you couldn't confirm.
8. Do the two-reader check from `writing.md`, reading as a student at the level the **Audience**
   describes and as a colleague in the field.
9. Review your changes as a reviewer would, then report what you checked, what you didn't, and what
   remains.
