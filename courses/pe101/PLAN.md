# PE101 plan

**Status:** draft for the instructor's approval, 2026-11-26. It replaces the 2026-11-25 draft,
whose labs called the Claude API. Nothing in this plan is built yet.

This is the instructor's blueprint and build checklist for PE101. It stays out of the published
course: `myst.yml` excludes it.

## Decisions so far

The instructor decided these on 2026-11-25, and they still hold:

- **Audience:** programmers who have finished one programming course in any language and are new
  to building with large language models. The labs are in Python, and a primer covers the Python
  they use.
- **Scope:** both kinds of "LLM coding", API first: prompting a model through the Claude API, then
  prompting and configuring a coding agent, Claude Code.
- **Folder:** `courses/pe101/`, following the repository's `courses/<code>/` convention.

The instructor changed these on 2026-11-26:

- **Level and delivery:** self-paced, from beginner to advanced, in three parts: foundations,
  techniques and measurement, and systems and agents. 13 modules and a capstone project replace
  the draft's eight modules.
- **No model calls:** the course is fully offline. No lab, exercise, assignment, self-test, or
  build step calls a model, so the course costs nothing to take or to build, and needs no account
  or API key. This replaces the draft's model choice (Claude Opus 5.5), its recordings of real
  responses, its build budget, and the `anthropic` and `claude-agent-sdk` packages.
- **Coding agents:** kept, offline. Modules 12 and 13 run no agent sessions. Students write
  `CLAUDE.md` files, rules, skills, permission rules, and hook scripts, and check them in code.
- **Grades:** none, as in LUA101's self-paced edition. Every piece checks itself with visible
  tests, answers students can see, or a published rubric. Hidden tests and model answers stay in
  `solutions/`.
- **Packages:** approved (section 9): matplotlib, pinned versions of jsonschema and PyYAML, and a
  course helper, `promptlab`.

Still to decide: everything else in this plan, and the questions in section 14.

## 1. The course

**PE101: Prompt Engineering from First Prompt to Coding Agents**

Large language models (LLMs) now run inside many programs and write much of the code in others.
This course teaches prompt engineering: writing the instructions, examples, and context that get a
model to do a task reliably, and building the code that checks whether it does. It is for
programmers who have finished one programming course and haven't built with an LLM before.
Students start by building a tiny language model to see how a prompt becomes text, then learn to
write clear, structured prompts and to improve them with examples, reasoning, and chains. They
measure prompts with evaluations they build themselves, and work up to structured output, tools,
agents, retrieval from documents, and defenses against prompt injection. The last two modules turn
to coding agents: students write task prompts for Claude Code and configure it with project
instructions, rules, skills, permissions, and hooks. The course calls no model, so it costs nothing
and needs no account. It is self-paced, in 13 modules and a capstone project.

## 2. Prerequisites

Students must have finished one programming course in any language, such as Python, Java,
JavaScript, or C, and have used Git and a terminal. They don't need Python already: the
**Python for the labs** page teaches the Python the labs use (functions, lists, dictionaries,
f-strings, JSON, `assert`, and virtual environments), and Module 1 points to it.

**Self-check.** A student who can do all five, in any language, is ready:

1. Write a function that takes a list of strings and a word, and returns the strings that contain
   the word; then test it with an assertion.
2. Read a JSON file into a dictionary or map, and print one of its fields.
3. Explain the difference between what a function returns and what it prints.
4. Run a program from a terminal with a file path as its argument, and read its error message.
5. Clone a Git repository, change a file, and commit the change.

## 3. Teaching prompt engineering without a model

Prompt engineering is usually learned by trying prompts on a model. This course can't do that, so
it says plainly what it does instead, and what it can't do:

- **What students never see:** a live model's response to a prompt they wrote. Everything a
  student learns about how real models respond comes from the readings, which cite the
  documentation or a paper for every such claim.
- **Writing prompts:** students write many prompts, and score each with the course's prompt
  rubric and against a model answer. Visible tests check only what code can check exactly, such as
  whether the data sits inside its tags and every template variable is filled.
- **Judging responses:** labs bundle sets of responses written for this course, each labeled as
  illustrative and not model output. They show the failure modes the documentation and the papers
  describe (a format that drifts, an example copied too closely, an unsupported answer), so
  students can practice grading, measuring, and comparing. A number computed from them describes
  that data set only, and the labs say so wherever they report one.
- **The software around the model:** tool loops, workflows, agents, and defenses are tested with
  stand-ins, programs that answer in the shape of the Messages API from a script. This is how
  production code tests LLM features without calling a model, and the readings say which behavior
  a stand-in fakes and which it can't.
- **How a model produces text:** Module 1 builds a byte-pair encoding tokenizer and an n-gram
  language model from scratch. They show tokens, next-token probabilities, and sampling at a small
  scale. Real LLMs compute those probabilities with a neural network, the transformer, which the
  reading names and doesn't teach.

The capstone ends with an evaluation ready to run against a real model, and a report that says
what was measured (the graders and the code) and what still needs a model (the prompts' pass
rates).

## 4. Learning objectives

### Course objectives

By the end of the course, students can:

- **LO-1:** Explain how a language model turns a prompt into text (tokens, next-token
  probabilities, sampling, and the context window), and build and price Messages API requests and
  conversations as data.
- **LO-2:** Write prompts that state the task, its context, the output's format, and what success
  looks like, using system prompts, XML tags, and templates that keep instructions apart from data.
- **LO-3:** Improve a prompt with examples, requested reasoning, and chains of prompts, and predict
  what each costs.
- **LO-4:** Measure a prompt with an evaluation (test cases, graders, intervals, and a held-out
  set), and decide between two prompts on that evidence.
- **LO-5:** Specify structured output and tools, build workflows and agents around them, test
  them with stand-ins, and choose the simplest design that meets a task's needs.
- **LO-6:** Ground answers in documents with retrieval, quotations, and caching, and measure how
  retrieval limits the answers.
- **LO-7:** Attack and defend an LLM system against prompt injection, stating what each defense
  can't stop.
- **LO-8:** Direct and configure a coding agent with task prompts, project instructions, skills,
  permissions, and hooks, and verify its work before accepting it.

### Module objectives

Each module objective serves the course objective in brackets.

#### Part 1: Foundations

**Module 1: How language models produce text** [LO-1]

- **LO-1.1:** Train a byte-pair encoding (BPE) tokenizer on a small corpus, and explain why token
  counts differ from word and character counts across prose, code, numbers, and languages.
- **LO-1.2:** Generate text from an n-gram language model by sampling from its next-token
  probabilities, and predict how temperature and top-p (nucleus) sampling change the output's
  variety.
- **LO-1.3:** Explain why one prompt can give different outputs, and how the context window limits
  what a model can use.

**Module 2: The anatomy of a request** [LO-1]

- **LO-2.1:** Build a Messages API request as data (the model, the system prompt, alternating user
  and assistant turns, and `max_tokens`), and read a response's content blocks, stop reason, and
  token usage.
- **LO-2.2:** Compute a request's cost from its token usage and the model's prices, and estimate a
  batch's cost and its context-window use before running it.
- **LO-2.3:** Keep a conversation within a token budget by resending its history, choose what to
  drop or summarize when it overflows, and explain what the model can't remember.
- **LO-2.4:** Handle each stop reason in code, including a truncated answer and a refusal.

**Module 3: Clear instructions** [LO-2]

- **LO-3.1:** Rewrite a vague prompt so it states the task, the audience, the context and its
  purpose, the constraints, and what a good answer looks like, and score both versions with the
  course's prompt rubric.
- **LO-3.2:** Decide what belongs in the system prompt and what belongs in the user's turn, and
  justify the choice.
- **LO-3.3:** Specify an output's format and length, and write code that checks responses against
  the specification.

**Module 4: Structure, data, and templates** [LO-2]

- **LO-4.1:** Separate instructions from data with XML tags, and order a prompt's parts: the
  documents, the instructions, and the question.
- **LO-4.2:** Build a prompt template that inserts variables without breaking the prompt's
  structure, and show a naive template failing on input that contains the template's own markup.
- **LO-4.3:** Keep prompts as versioned files, check that each template's variables are filled,
  and compare two versions with a diff.

#### Part 2: Techniques and measurement

**Module 5: Examples** [LO-3]

- **LO-5.1:** Write few-shot examples that cover the range of inputs and labels, in tags that set
  them apart from the task.
- **LO-5.2:** Detect an example set that invites copying of surface features or has a skewed
  balance of labels, and fix it.
- **LO-5.3:** Select examples for each input from a pool by similarity, and compare the selection
  with a fixed set by how much of the input range each covers.

**Module 6: Reasoning and chains** [LO-3]

- **LO-6.1:** Choose a thinking effort level for a task from measurements of accuracy, latency, and
  cost, and justify the choice.
- **LO-6.2:** Ask for reasoning in tagged sections, and extract the final answer in code, failing
  loudly when it is missing.
- **LO-6.3:** Split a complex task into a chain of prompts that pass results forward, and compute
  how errors compound along the chain and what a check step catches.

**Module 7: Evaluating prompts** [LO-4]

- **LO-7.1:** Write measurable success criteria for a task, and build a test set with typical,
  edge, and adversarial cases.
- **LO-7.2:** Grade outputs with code-based graders, and measure a model-based grader's agreement
  with human labels with percent agreement and Cohen's kappa.
- **LO-7.3:** Report a pass rate over repeated runs with a Wilson interval, and compare two prompts
  with a paired bootstrap over test cases.
- **LO-7.4:** Keep a held-out test set, and explain how tuning a prompt on the test set biases the
  comparison.

**Module 8: Structured output and tools** [LO-5]

- **LO-8.1:** Write a JSON Schema for a structured output, validate responses against it, and
  handle a response that fails validation.
- **LO-8.2:** Define tools whose names, descriptions, and input schemas tell the model when and how
  to use each one.
- **LO-8.3:** Implement the tool-use loop (run each call, return its result or error, and stop on
  the right stop reason), and test it with a scripted stand-in for the model.

#### Part 3: Systems and agents

**Module 9: Workflows and agents** [LO-5]

- **LO-9.1:** Implement four workflow patterns (routing, parallel calls, an orchestrator with
  workers, and an evaluator with an optimizer) with stand-in model calls.
- **LO-9.2:** Build an agent loop with limits on turns and cost, and trace its steps from its log.
- **LO-9.3:** Choose among one call, a fixed workflow, and an agent for a task, and justify the
  choice by the task's complexity, its value, the model's ability at it, and the cost of errors.

**Module 10: Documents, retrieval, and context** [LO-6]

- **LO-10.1:** Structure a long-context prompt with tagged documents placed before the question,
  and ask for answers grounded in quotations.
- **LO-10.2:** Implement BM25 retrieval, measure its recall at k on labeled questions, and explain
  how retrieval recall caps answer accuracy.
- **LO-10.3:** Reduce unsupported answers by allowing "I don't know" and requiring evidence, and
  verify quotations against their sources in code.
- **LO-10.4:** Order a prompt so its stable parts come first, and compute what caching that prefix
  saves.

**Module 11: Prompt injection** [LO-7]

- **LO-11.1:** Demonstrate direct and indirect prompt injection against a tool-using assistant run
  by a deliberately gullible stand-in, and explain why the prompt can't be the only defense.
- **LO-11.2:** Reduce an injection's harm with least privilege, marked untrusted content, and human
  approval of risky actions, and state what each defense can't stop.
- **LO-11.3:** Build an injection test set, and measure a system's attack success rate before and
  after its defenses.

**Module 12: Prompting a coding agent** [LO-8]

- **LO-12.1:** Trace a coding agent's session as a loop of model turns and tool calls, and identify
  where the context behind each decision came from.
- **LO-12.2:** Write a task prompt for a coding agent that states the goal, the relevant files, the
  constraints, and how to verify the result, and score it with the course's rubric.
- **LO-12.3:** Give an agent a way to check its own work (tests, a linter, or a script), and review
  a diff against its task before accepting it.

**Module 13: Configuring a coding agent** [LO-8]

- **LO-13.1:** Write project instructions in a `CLAUDE.md` file and in rules scoped to paths, and
  work out which rules load for a given file.
- **LO-13.2:** Package a repeatable workflow as a skill, and decide what to delegate to a subagent.
- **LO-13.3:** Write permission rules and a hook that blocks a risky command, test the hook by
  piping sample events into it, and explain what permission rules and hooks can and can't prevent.

## 5. Modules

Every module has the same four pieces:

| Piece | File | Format | Why this format |
| :- | :- | :- | :- |
| Reading | `modules/NN-<slug>/index.md` | Markdown | Prose with short prompts and Python examples; nothing to run in the page |
| Lab | `labNN.ipynb`, paired with `labNN.py` | Jupyter notebook | Students run and change code, and see each result beside the explanation; `assert` checks each answer |
| Practice | `practice.md` | Markdown | Exercises with collapsed hints and visible answers, for retrieval practice |
| Figures | drawn by code in the labs | PNG from matplotlib | Sampling distributions, pass rates with their intervals, and recall against k; each has alternative text |

| # | Module | Objectives | Depends on | Hours | Lab's main activity |
| :- | :- | :- | :- | :- | :- |
| 1 | How language models produce text | LO-1.1–1.3 | none | 7 | Train a BPE tokenizer on a bundled corpus and count tokens in prose, code, and two languages; sample from a trigram model at three temperatures and with top-p; overflow a context window |
| 2 | The anatomy of a request | LO-2.1–2.4 | 1 | 6 | Build request bodies as dictionaries; read illustrative responses in the documented shape; price them and a 10,000-request batch; trim a conversation to a token budget; branch on every stop reason |
| 3 | Clear instructions | LO-3.1–3.3 | 2 | 6 | Rewrite three vague prompts and score them with the rubric; split one between system prompt and user turn; write format checkers and run them over 30 illustrative responses |
| 4 | Structure, data, and templates | LO-4.1–4.3 | 3 | 6 | Tag a document that contains instructions; break an f-string template with input that closes its tags, then fix it; store prompts as versioned files and diff them |
| 5 | Examples | LO-5.1–5.3 | 4 | 6 | Measure an example pool's coverage of categories and lengths; find the surface features a bad set shares; choose examples per input by bag-of-words similarity |
| 6 | Reasoning and chains | LO-6.1–6.3 | 5 | 6 | Extract answers from tagged reasoning and catch missing ones; choose an effort level from a table of illustrative measurements; build a three-step chain with stand-ins and compute how errors compound |
| 7 | Evaluating prompts | LO-7.1–7.4 | 6 | 8 | An evaluation of two prompt versions over 40 cases and three runs of illustrative responses: code graders, a model grader's kappa against 30 human labels, Wilson intervals, a paired bootstrap, and a held-out split |
| 8 | Structured output and tools | LO-8.1–8.3 | 7 | 7 | Validate extracted records with jsonschema and handle failures; write three tool definitions; implement the tool loop and test it with a scripted stand-in, including a tool error |
| 9 | Workflows and agents | LO-9.1–9.3 | 8 | 7 | The four workflow patterns with stand-ins; an agent with limits on turns and cost, stopped by each limit; trace a run from its log |
| 10 | Documents, retrieval, and context | LO-10.1–10.4 | 7, 8 | 8 | BM25 over a bundled employee handbook; recall at k on 40 labeled questions, plotted; a quotation checker; the cost of a cached prefix against an uncached one |
| 11 | Prompt injection | LO-11.1–11.3 | 9, 10 | 7 | Plant instructions in a document for a gullible stand-in; add least privilege, marked content, and an approval gate; measure attack success on 25 attacks before and after |
| 12 | Prompting a coding agent | LO-12.1–12.3 | 9 | 6 | Trace an illustrative session log; write task prompts for the starter repository and score them; write a check script; review three illustrative diffs against their tasks |
| 13 | Configuring a coding agent | LO-13.1–13.3 | 12 | 7 | Write a `CLAUDE.md` and a path-scoped rule, and compute which rules match which files; write a skill and check its front matter; write a hook and test it by piping JSON events |

The hours cover the reading (about 2), the lab (about 2.5), and the practice (about 1–1.5).
The assignments add about 3 hours each, the self-tests about 2 each, and the capstone project
about 20, so the course takes about 128 hours in all.

### Data and examples

Every data set is written for this course and kept in `courses/pe101/data/`, and none contains a
real person's data:

- a short corpus of prose, code, and text in two languages, for Lab 1;
- support tickets for a fictional bicycle-repair company, with labels;
- a short employee handbook for the same company, and questions labeled with the sections that
  answer them;
- sets of illustrative responses, each file marked "written for PE101; not model output";
- a table of model prices, dated and taken from Anthropic's pricing page when Module 2 is built;
- illustrative session logs for Module 12, in a simplified format defined by the course, which the
  reading says isn't Claude Code's own;
- 25 injection attempts for Module 11;
- the starter repository for Modules 12 and 13: a small Python package with tests.

### What the course teaches about current models

Many prompt-engineering guides were written for older models, and some of their techniques fail on
the current API. The readings teach the current behavior, each claim cited to the API
documentation. The 2026-11-25 draft confirmed these against the documentation, and each is
confirmed again when its module is built:

- Claude Opus 5.5 always thinks before it answers. Its `effort` setting (`low` to `max`, default
  `medium`) controls how much, and setting thinking off returns an error.
- Sampling settings such as `temperature` return an error on current models. Module 1 teaches
  temperature on the n-gram model, and Module 2 says why the API leaves variation to the prompt.
- Prefilling the start of the model's answer returns an error on current models. Module 3 controls
  format with instructions, and Module 8 with structured outputs.
- Forcing a particular tool with `tool_choice` returns an error on Opus 5.5. Module 8 steers tool
  use with descriptions and instructions.
- A response can stop with `stop_reason` `"refusal"`. Module 2 teaches code to check the stop
  reason before it reads the text.

## 6. Checking work

The course has no grades. Every piece comes with a way to check it:

| Piece | How students check it | Objectives |
| :- | :- | :- |
| Labs 1–13 | Every check cell in the notebook passes | Each lab's module |
| PA1: Requests and costs (notebook, after Module 2) | Its visible tests | LO-2.1–2.4, and revisits LO-1.3 |
| PA2: A prompt library (notebook, after Module 4) | Its visible tests, and the prompt rubric for its prompts | LO-3.1–3.3, LO-4.1–4.3, and revisits LO-2.1 |
| PA3: An evaluated classifier (notebook, after Module 7) | Its visible tests | LO-5.1–5.3, LO-6.2, LO-7.1–7.4, and revisits LO-3.3 |
| PA4: A tool-using assistant (notebook, after Module 9) | Its visible tests, which drive the code with scripted stand-ins | LO-8.1–8.3, LO-9.1–9.3, and revisits LO-2.4, LO-6.3 |
| PA5: Answers from documents, defended (notebook, after Module 11) | Its visible tests | LO-10.1–10.4, LO-11.1–11.3, and revisits LO-4.2, LO-7.3, LO-8.1 |
| Self-test 1, after Module 4 | Answers and scoring notes in the page | Modules 1–4 |
| Self-test 2, after Module 8 | Answers and scoring notes in the page | Modules 1–8, weighted toward 5–8 |
| Self-test 3, after Module 13 | Answers and scoring notes in the page | All modules, weighted toward 9–13 |
| Capstone project: proposal, milestone, and final version | The brief's checklists and its rubric | See below |

- **PA1: Requests and costs:** a request builder, a cost estimator for single requests and
  batches, a function that trims a conversation to a token budget, and a stop-reason handler.
- **PA2: A prompt library:** three vague prompts rewritten and scored with the rubric, one split
  between system prompt and user turn, format checkers, a template that tags and escapes its data,
  and versioned prompt files with a check that every variable is filled.
- **PA3: An evaluated classifier:** a few-shot example set for routing the support tickets, with
  coverage checks; answer extraction; a test set with graders; a model grader's agreement with
  bundled human labels; and a Wilson interval and paired bootstrap over a bundled response set,
  with a held-out split.
- **PA4: A tool-using assistant:** validation of structured output with a retry, three tools, and
  the tool loop, tested with scripted stand-ins; then a router workflow and an agent with limits,
  and a written choice between them.
- **PA5: Answers from documents, defended:** BM25 retrieval with recall at k on labeled questions,
  a grounded-answer prompt, a quotation checker, the savings of a cached prefix, and an injection
  test set run against the gullible stand-in before and after defenses.
- **Capstone project** (proposal after Module 9, milestone after Module 11, final version after
  Module 13): a prompt package for a task of the student's choosing, or one from a list, built to
  show in a portfolio. The proposal states the task, its success criteria, its risks (including
  where untrusted text enters), and a cost estimate. The milestone is a test set of at least 30
  cases, split into development and held-out sets, with code graders and a model-grader prompt, and
  the graders checked against at least 20 responses the student writes and labels by hand, good and
  flawed. The final version has three versioned prompts with a written rationale for each change,
  an evaluation that runs end to end on a stand-in, a cost estimate with and without caching,
  injection tests and defenses, and a Claude Code configuration for its repository (a `CLAUDE.md`,
  one path-scoped rule, one skill, and one hook) checked offline. Its report quotes two task
  prompts and says what was measured and what still needs a model. LO-2.2, LO-3.1, LO-4.2, LO-4.3,
  LO-6.3, LO-7.1–7.4, LO-8.1, LO-9.3, LO-10.4, LO-11.2, LO-11.3, LO-12.1–12.3, LO-13.1–13.3.

Each assignment's hidden tests, and the model answers to its prompt problems, stay in
`courses/pe101/solutions/` (committed, never linked from coursework, and never built into the
website), as the repository's teaching rule decided. So do the lab answer keys, the self-tests'
longer model answers, and the capstone rubric's examples. The capstone rubric's criteria are
published with its brief.

## 7. Alignment

Every objective is taught before it is checked, and checked at least once beyond its lab.

| Objective | Taught | Checked |
| :- | :- | :- |
| LO-1.1, LO-1.2 | Module 1 | Lab 1, Self-test 1 |
| LO-1.3 | Module 1 | Lab 1, PA1, Self-test 1 |
| LO-2.1 | Module 2 | Lab 2, PA1, PA2, Self-test 1 |
| LO-2.2, LO-2.3 | Module 2 | Lab 2, PA1, Self-test 1; LO-2.2 also the capstone |
| LO-2.4 | Module 2 | Lab 2, PA1, PA4, Self-test 1 |
| LO-3.1 | Module 3 | Lab 3, PA2, Self-test 1, capstone |
| LO-3.2 | Module 3 | Lab 3, PA2, Self-test 1 |
| LO-3.3 | Module 3 | Lab 3, PA2, PA3, Self-test 1 |
| LO-4.1 | Module 4 | Lab 4, PA2, Self-test 1 |
| LO-4.2 | Module 4 | Lab 4, PA2, PA5, Self-test 1, capstone |
| LO-4.3 | Module 4 | Lab 4, PA2, capstone |
| LO-5.1–LO-5.3 | Module 5 | Lab 5, PA3, Self-test 2 |
| LO-6.1 | Module 6 | Lab 6, Self-test 2 |
| LO-6.2 | Module 6 | Lab 6, PA3, Self-test 2 |
| LO-6.3 | Module 6 | Lab 6, PA4, Self-test 2, capstone |
| LO-7.1, LO-7.2, LO-7.4 | Module 7 | Lab 7, PA3, Self-test 2, capstone |
| LO-7.3 | Module 7 | Lab 7, PA3, PA5, Self-test 2, capstone |
| LO-8.1 | Module 8 | Lab 8, PA4, PA5, Self-test 2, capstone |
| LO-8.2, LO-8.3 | Module 8 | Lab 8, PA4, Self-test 2 |
| LO-9.1, LO-9.2 | Module 9 | Lab 9, PA4, Self-test 3 |
| LO-9.3 | Module 9 | Lab 9, PA4, Self-test 3, capstone |
| LO-10.1–LO-10.3 | Module 10 | Lab 10, PA5, Self-test 3 |
| LO-10.4 | Module 10 | Lab 10, PA5, Self-test 3, capstone |
| LO-11.1 | Module 11 | Lab 11, PA5, Self-test 3 |
| LO-11.2, LO-11.3 | Module 11 | Lab 11, PA5, Self-test 3, capstone |
| LO-12.1–LO-12.3 | Module 12 | Lab 12, Self-test 3, capstone |
| LO-13.1–LO-13.3 | Module 13 | Lab 13, Self-test 3, capstone |

## 8. Suggested pace

The course is self-paced, so it has no due dates. This pace takes 16 weeks at about 8 hours a
week; weeks with an assignment or a self-test take more.

| Week | Module | Then |
| :- | :- | :- |
| 1 | 1: How language models produce text | |
| 2 | 2: The anatomy of a request | PA1 |
| 3 | 3: Clear instructions | |
| 4 | 4: Structure, data, and templates | PA2, Self-test 1 |
| 5 | 5: Examples | |
| 6 | 6: Reasoning and chains | |
| 7 | 7: Evaluating prompts | PA3 |
| 8 | 8: Structured output and tools | Self-test 2 |
| 9 | 9: Workflows and agents | PA4, capstone proposal |
| 10 | 10: Documents, retrieval, and context | |
| 11 | 11: Prompt injection | PA5, capstone milestone |
| 12 | 12: Prompting a coding agent | |
| 13 | 13: Configuring a coding agent | Self-test 3 |
| 14–16 | The capstone project | Final version |

## 9. Environment

**Python:** 3.12, in the repository's existing `.venv/`. No API key, account, or network access is
needed to take the course.

Approved by the instructor on 2026-11-26:

| Item | Where | Why |
| :- | :- | :- |
| `matplotlib`, pinned to its current release when installed | `requirements.txt` | Figures: sampling distributions, pass rates with intervals, recall against k |
| `jsonschema==4.26.0` | `requirements.txt` | Module 8 validates structured output against JSON Schema; already installed as a dependency of nbformat, and pinned because the labs import it |
| `pyyaml==6.0.4` | `requirements.txt` | Module 13 reads skills' and rules' front matter; already installed, and pinned for the same reason |
| `promptlab`, a small helper written for this course | `courses/pe101/promptlab/`, installed with `-e` from `requirements.txt` | See below |

`promptlab` holds what the labs share, with its own tests:

- **Stand-ins:** `ScriptedModel`, which answers each request from a script in the shape of the
  Messages API's responses and records every request it gets, so tests can check what the code
  sent; and, from Module 11, `GullibleModel`, a caricature that obeys any instruction it finds in
  the text it reads, to show why defenses can't rely on the model.
- **Data:** a loader for the bundled data sets.
- **Later helpers:** reference versions of the Wilson interval, the paired bootstrap, and BM25, for
  labs after the ones where students build them.

The labs use JSON dictionaries in the shape of the HTTP API's requests and responses, and the
reading says that the SDKs wrap the same fields in objects. No LaTeX: with no exams and little
mathematics, every piece is Markdown or a notebook, and the course has no `latex/` folder.

## 10. Sources

Documentation entries were fetched and confirmed for the 2026-11-25 draft, and each page is read
again when its module is built. The four marked "new" were confirmed on 2026-11-26. No textbook is
required: the readings and Anthropic's free documentation cover everything, and the papers are
further reading.

**Documentation** (Claude API pages under <https://platform.claude.com/docs/en/>, Claude Code
pages under <https://code.claude.com/docs/en/>):

| Source | Why it is here |
| :- | :- |
| "Prompting best practices", `build-with-claude/prompt-engineering/claude-prompting-best-practices` | Modules 3–6 and 10: one page that replaces the older pages on clarity, examples, XML tags, roles, long context, thinking, chaining, and moving away from prefill |
| "Using the Messages API", `build-with-claude/working-with-messages` | Module 2, and the source for prefill returning an error on current models |
| "Thinking", `build-with-claude/thinking`, and "Effort", `build-with-claude/effort` | Module 6's thinking and effort levels |
| "Define success criteria and build evaluations", `test-and-evaluate/develop-tests` | Module 7 |
| "Structured outputs", `build-with-claude/structured-outputs`, and "Tool use with Claude", `agents-and-tools/tool-use/overview` | Module 8 |
| "Prompt caching", "Citations", "Reduce hallucinations", and "Mitigate jailbreaks and prompt injections", under `build-with-claude/` and `test-and-evaluate/strengthen-guardrails/` | Modules 10 and 11 |
| Anthropic's pricing page | Module 2's price table; its address and prices are confirmed, and dated, when Module 2 is built |
| Anthropic, "Building effective agents", by Erik S. and Barry Zhang, December 19, 2024, <https://www.anthropic.com/engineering/building-effective-agents> | Module 9: the workflow patterns, and when an agent is worth its cost |
| Claude Code docs: "Overview", "Best practices for Claude Code", "How Claude remembers your project" (`CLAUDE.md` and `.claude/rules/`), "Extend Claude with skills", "Create custom subagents", "Hooks reference" and its guide, "Settings files and precedence", and "Configure permissions" | Modules 12 and 13 |
| OWASP Gen AI Security Project, "LLM01:2025 Prompt Injection", <https://genai.owasp.org/llmrisk/llm01-prompt-injection/> | Module 11: direct and indirect injection and their mitigations |
| New: Simon Willison, "The lethal trifecta for AI agents", June 16, 2025, <https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/> | Module 11: private data, untrusted content, and a way to send data out, and why removing one of the three is the dependable defense |

**Papers and books:**

| Source | Why it is here |
| :- | :- |
| New: Shannon, "A Mathematical Theory of Communication," *Bell System Technical Journal* 27(3), 1948, 379–423, doi:10.1002/j.1538-7305.1948.tb01338.x | Module 1: the n-gram approximations of English that Lab 1 rebuilds |
| Sennrich, Haddow, and Birch, "Neural Machine Translation of Rare Words with Subword Units," ACL 2016, 1715–1725, doi:10.18653/v1/P16-1162 | Module 1: byte-pair encoding, which Lab 1 implements |
| New: Holtzman, Buys, Du, Forbes, and Choi, "The Curious Case of Neural Text Degeneration," ICLR 2020, arXiv:1904.09751 | Module 1: nucleus (top-p) sampling |
| Brown et al., "Language Models are Few-Shot Learners," NeurIPS 2020, arXiv:2005.14165 | Module 5: few-shot prompting, named and measured |
| Min et al., "Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?," EMNLP 2022, 11048–11064, doi:10.18653/v1/2022.emnlp-main.759 | Module 5: examples teach format and the range of inputs, not only the labels |
| Zhao, Wallace, Feng, Klein, and Singh, "Calibrate Before Use: Improving Few-Shot Performance of Language Models," ICML 2021, PMLR 139, 12697–12706 | Module 5: how the choice and order of examples bias answers |
| Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," NeurIPS 2022, doi:10.52202/068431-1800 | Module 6: why reasoning before answering helps, the idea behind built-in thinking |
| Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," NeurIPS 2023 Datasets and Benchmarks Track, doi:10.52202/075280-2020 | Module 7: model graders, their agreement with people, and their biases |
| New: Cohen, "A Coefficient of Agreement for Nominal Scales," *Educational and Psychological Measurement* 20(1), 1960, 37–46, doi:10.1177/001316446002000104 | Module 7: kappa, agreement corrected for chance |
| Wilson, "Probable Inference, the Law of Succession, and Statistical Inference," *JASA* 22(158), 1927, 209–212, doi:10.1080/01621459.1927.10502953 | Module 7: the interval the course reports around a pass rate |
| Efron and Tibshirani, *An Introduction to the Bootstrap*, Chapman & Hall, 1993 (ISBN 978-0-412-04231-7) | Module 7: comparing two prompts by resampling test cases |
| Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," ICLR 2023, arXiv:2210.03629 | Module 9: the reason-act-observe loop that agents run |
| Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," NeurIPS 2020, arXiv:2005.11401 | Module 10: retrieval before generation, named |
| Robertson and Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," *Foundations and Trends in Information Retrieval* 3(4), 2009, 333–389, doi:10.1561/1500000019 | Module 10: the BM25 scoring that Lab 10 implements |
| Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," *TACL* 12, 2024, 157–173, doi:10.1162/tacl_a_00638 | Module 10: where in a long prompt models use information well |
| Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection," AISec '23, ACM, 2023, 79–90, doi:10.1145/3605764.3623985 | Module 11: indirect prompt injection, demonstrated |

Not assigned: Anthropic's interactive prompt engineering tutorial on GitHub. It calls the API,
which this course doesn't; its model, Claude 3 Haiku, retired on April 20, 2026; and its Chapter 5
teaches prefill, which current models reject.

Two details for `references.bib`: the "Building effective agents" byline gives only "Erik S.", so
the entry names its authors as the page does; and Routledge lists *An Introduction to the
Bootstrap* as copyright 1994, a later printing of the 1993 book.

## 11. Policies

Drafts for the instructor to change. The syllabus states them plainly.

- **Pace:** the course is self-paced and has no deadlines. The suggested pace is a guide, not a
  requirement.
- **Cost:** the course costs nothing. It needs no account, API key, or payment, and nothing in it
  sends text to a model.
- **Collaboration and academic integrity:** discuss ideas with anyone, but write your own prompts,
  code, and answers. Don't share or look at another learner's solution. Name everyone you discussed
  an assignment with, and cite any prompt or code you adapted.
- **Generative AI tools:** the course never requires one. You may use one to explain concepts,
  error messages, and documentation. Write your own prompts, code, and answers in the labs, the
  assignments, and the self-tests: writing and judging prompts yourself is the skill the course
  teaches. In the capstone project you may use AI tools, coding agents included, if your report
  says which parts they wrote. End every assignment, and your capstone's `README.md`, with a short
  note saying which tools you used and how, or "none".
- **Data:** use only the course's data and your own text in your prompts and test sets, never
  another person's personal information.
- **Accommodations:** every page of the course is HTML or Markdown, which screen readers can read,
  and nothing is timed except the self-tests' suggested sittings, which you can lengthen as you
  need. If you take the course through an institution, its disability services office arranges any
  other accommodations, through the learning management system.

## 12. Interactivity

I propose static pages, as in LUA101: readers download each notebook and run it in their own
environment. Because the course needs no API key, in-page execution is now possible too: Binder
(`jupyter: true`) would run the notebooks on a public server, and JupyterLite (`lite: true`) in
the browser, which would need `promptlab` built as a wheel. The documentation marks both as beta,
and either can be added later without changing the materials.

## 13. Folder layout

The skill's standard layout, adapted to a self-paced course with no exams or LaTeX:

```text
courses/pe101/
├── README.md             the syllabus: the course hub
├── PLAN.md               this plan, not published
├── setup.md              the environment; no account or key needed
├── python-primer.md      Python for the labs
├── notation.md           the symbols: probability, temperature, cost, pass rate, kappa, BM25
├── references.bib        the confirmed sources, in biblatex's authoryear style
├── ERRATA.md             corrections, by release date
├── myst.yml              the website's configuration, for Jupyter Book 2
├── nbgrader_config.py    settings for the assignments' student versions
├── data/                 the bundled data sets, all written for the course
├── promptlab/            the labs' helper, with its tests
├── modules/NN-<slug>/    index.md, labNN.py, labNN.ipynb, practice.md
├── self-tests/           Self-tests 1–3
├── assignments/          PA1–PA5 student versions, and the capstone brief
├── starter-repo/         the small Python package that Labs 12 and 13 work on
├── tools/                checks for labs and assignments, adapted from LUA101's
└── solutions/            lab keys, nbgrader sources, model answers, and the rubric's examples
```

The build also adds a continuous integration (CI) workflow, `.github/workflows/pe101.yml`, like
LUA101's, which checks every lab with and without its key and builds the website.

## 14. Questions for the instructor

1. **Approve or change** the objectives, the modules, the way work is checked, the policies, and
   the interactivity choice above.
2. **The illustrative responses** in section 3: response sets written for the course, labeled as
   not model output, as the data for grading and evaluation practice.

## Build checklist

Tick each line once its piece passes its checks. Each data set is built with the first piece that
uses it.

- [ ] Environment: packages in `requirements.txt`, and `promptlab` with its tests
- [ ] Layout: syllabus (`README.md`), `setup.md`, `python-primer.md`, `notation.md`,
  `references.bib`, `ERRATA.md`, `myst.yml`, `nbgrader_config.py`, the check tools, and the CI
  workflow
- [ ] Module 1: reading, lab, practice, and the corpus
- [ ] Module 2: reading, lab, practice, and the price table
- [ ] PA1: source, student version, hidden tests, and key
- [ ] Module 3: reading, lab, practice, the prompt rubric, and the tickets
- [ ] Module 4: reading, lab, and practice
- [ ] PA2: source, student version, hidden tests, and model answers
- [ ] Self-test 1
- [ ] Module 5: reading, lab, and practice
- [ ] Module 6: reading, lab, and practice
- [ ] Module 7: reading, lab, and practice
- [ ] PA3: source, student version, hidden tests, and key
- [ ] Module 8: reading, lab, and practice
- [ ] Self-test 2
- [ ] Module 9: reading, lab, and practice
- [ ] PA4: source, student version, hidden tests, and key
- [ ] Capstone: brief, checkpoints, and rubric
- [ ] Module 10: reading, lab, practice, and the handbook
- [ ] Module 11: reading, lab, practice, and the attacks
- [ ] PA5: source, student version, hidden tests, and key
- [ ] Module 12: reading, lab, practice, the starter repository, and the session logs
- [ ] Module 13: reading, lab, and practice
- [ ] Self-test 3
- [ ] Whole-course checks: notebooks, website build, leak search, alignment, answers,
  accessibility, links, and the rules' checks
