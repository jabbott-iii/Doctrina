# PE101 plan

**Status:** draft for the instructor's approval, 2026-11-25. Nothing in this plan is built yet.

This is the instructor's blueprint and build checklist for PE101. It stays out of the published
course: `myst.yml` excludes it.

## Decisions so far

The instructor decided these on 2026-11-25:

- **Scope:** both kinds of "LLM coding", API first. Six modules teach prompting through the Claude
  API from Python, and the last two teach prompting and configuring a coding agent, Claude Code.
- **Audience:** programmers who have finished one programming course in any language and are new
  to building with large language models. The labs are in Python, and a primer covers the Python
  they use.
- **Length and delivery:** self-paced, in eight modules and a capstone project. No deadlines and
  no exams.
- **Model:** the labs call Claude Opus 5.5 (`claude-opus-5-5`) by default.
- **Folder:** `courses/pe101/`, following the repository's `courses/<code>/` convention.

Still to decide: everything else in this plan, and the questions in section 13.

## 1. The course

**PE101: Prompt Engineering from First Prompt to Coding Agents**

Large language models (LLMs) now run inside many programs and write much of the code in others.
This course teaches prompt engineering: writing the instructions, examples, and context that get a
model to do a task reliably, and measuring whether it does. It is for programmers who have finished
one programming course and haven't built with an LLM before. Students start with one call to the
Claude API from Python. They work up to programs that return structured data, use tools, answer
from documents, and resist prompt injection, and they measure every change with evaluations they
build themselves. The last two modules turn to coding agents: students prompt Claude Code to change
a repository, configure it with project instructions, rules, and skills, and check its work before
they accept it. The course is self-paced, in eight modules and a capstone project.

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
4. Run a program from a terminal with an environment variable set for it.
5. Clone a Git repository, change a file, and commit the change.

## 3. Learning objectives

### Course objectives

By the end of the course, students can:

- **LO-1:** Call an LLM through the Claude API from Python, and account for its cost, its
  variability, and the limits of what it remembers.
- **LO-2:** Write prompts that state the task, its context, the output's format, and what success
  looks like, using system prompts, XML tags, templates, examples, reasoning, and chains of
  prompts.
- **LO-3:** Measure a prompt with an evaluation: test cases, graders, repeated runs, and a held-out
  test set, and decide between two prompts on that evidence.
- **LO-4:** Get structured output and act through tools, building workflows and agents, and choose
  the simplest design that meets a task's needs.
- **LO-5:** Ground answers in outside documents, and defend a model's tools and outputs against
  prompt injection, stating what each defense can't stop.
- **LO-6:** Direct a coding agent with task prompts and project configuration, and verify its work
  before accepting it.

### Module objectives

Each module objective serves the course objective in brackets.

**Module 1: First calls to the API** [LO-1]

- **LO-1.1:** Send a request to the Messages API from Python, and read the response's text, stop
  reason, and token usage.
- **LO-1.2:** Compute a request's cost from its token usage and the model's prices, and estimate
  the cost of a batch of requests before running it.
- **LO-1.3:** Explain what tokens and the context window are and why one prompt can give different
  outputs, and show the variation by running a prompt several times.
- **LO-1.4:** Hold a multi-turn conversation by resending its history, and explain what the model
  can and can't remember between requests.

**Module 2: Clear instructions** [LO-2]

- **LO-2.1:** Rewrite a vague prompt so it states the task, the audience, the context and its
  purpose, and what a good answer looks like, and show the improvement on test inputs.
- **LO-2.2:** Separate instructions from data with XML tags, and build prompt templates that insert
  variables without breaking the prompt's structure.
- **LO-2.3:** Decide what belongs in the system prompt and what belongs in the user's turn, and
  justify the choice.
- **LO-2.4:** Specify the output's format and length, and check in code that responses follow it.

**Module 3: Examples, reasoning, and chains** [LO-2]

- **LO-3.1:** Write few-shot examples that cover the range of inputs, and detect when the model
  copies an example's surface features instead of its pattern.
- **LO-3.2:** Set the effort level of the model's thinking, and measure its effect on accuracy,
  latency, and cost for a task.
- **LO-3.3:** Split a complex task into a chain of prompts that pass results forward, and compare
  the chain with a single prompt.

**Module 4: Evaluating prompts** [LO-3]

- **LO-4.1:** Write measurable success criteria for a task, and build a test set with typical,
  edge, and adversarial cases.
- **LO-4.2:** Grade outputs with code-based checks, and with a model-based grader whose agreement
  with human labels has been measured.
- **LO-4.3:** Compare two prompts by pass rate over repeated runs, report the uncertainty, and keep
  a held-out test set so that tuning doesn't bias the comparison.

**Module 5: Structured output, tools, and agents** [LO-4]

- **LO-5.1:** Get responses that match a JSON schema with structured outputs, and validate them
  with Pydantic.
- **LO-5.2:** Define tools whose names, descriptions, and input schemas tell the model when and how
  to use each one.
- **LO-5.3:** Implement the tool-use loop (run each call, return its result or error, and stop on
  the right stop reason), and test the loop with a scripted stand-in for the model.
- **LO-5.4:** Choose among one call, a fixed workflow, and an agent for a task, and justify the
  choice by the task's complexity, its value, the model's ability at it, and the cost of errors.

**Module 6: Documents, retrieval, and prompt injection** [LO-5]

- **LO-6.1:** Structure a long-context prompt with tagged documents placed before the question, and
  ground answers in quotations or citations.
- **LO-6.2:** Build a retrieval step that selects passages for a prompt, and measure how retrieval
  recall limits answer accuracy.
- **LO-6.3:** Reduce unsupported answers by allowing "I don't know" and requiring evidence, and
  measure the effect with an evaluation.
- **LO-6.4:** Cache a stable prompt prefix, and verify the savings from the response's usage
  fields.
- **LO-6.5:** Demonstrate an indirect prompt injection against a tool-using assistant, reduce its
  harm with least privilege, marked untrusted content, and human approval of risky actions, and
  state what each defense can't stop.

**Module 7: Prompting a coding agent** [LO-6]

- **LO-7.1:** Trace a coding agent's session as a loop of model turns and tool calls, and identify
  where the context behind each decision came from.
- **LO-7.2:** Write a task prompt for a coding agent that states the goal, the relevant files, the
  constraints, and how to verify the result, and compare its outcome with a vague prompt's on the
  same task.
- **LO-7.3:** Give an agent a way to check its own work (tests, a type checker, or a script), and
  review its changes against the task before accepting them.

**Module 8: Configuring a coding agent** [LO-6]

- **LO-8.1:** Write project instructions, in a `CLAUDE.md` file and in rules scoped to paths, that
  change an agent's behavior in a way you can check.
- **LO-8.2:** Package a repeatable workflow as a skill, and delegate a self-contained task to a
  subagent.
- **LO-8.3:** Set an agent's permissions so that it can do its task and no more, and explain what a
  permission rule or a hook can and can't prevent.

## 4. Modules

Every module has the same four pieces:

| Piece | File | Format | Why this format |
| :- | :- | :- | :- |
| Reading | `modules/NN-<slug>/index.md` | Markdown | Prose with short prompts and Python examples; nothing to run in the page |
| Lab | `labNN.ipynb`, paired with `labNN.py`, and its recorded responses in `labNN.cassette.json` | Jupyter notebook | Students run, change, and rerun prompts, and see each response beside the explanation; `assert` checks each answer |
| Practice | `practice.md` | Markdown | Exercises with collapsed hints and visible answers, for retrieval practice; most need no API key |
| Figures | drawn by code in the labs | PNG from matplotlib | Pass rates with their uncertainty, and accuracy against cost; each has alternative text |

| # | Module | Objectives | Depends on | Hours | Lab's main activity |
| :- | :- | :- | :- | :- | :- |
| 1 | First calls to the API | LO-1.1–1.4 | none | 6 | Read a response's usage and price it; run one prompt five times and compare; a conversation with and without its history; hit `max_tokens` on purpose |
| 2 | Clear instructions | LO-2.1–2.4 | 1 | 8.5 | Rewrite a vague prompt and score both on 10 inputs; wrap a document that contains instructions in tags; check format in code |
| 3 | Examples, reasoning, and chains | LO-3.1–3.3 | 2 | 6 | Classify 20 labeled inputs with 0, 1, and 3 examples, similar and varied; a table of effort against accuracy, time, and cost; a three-step chain against one prompt |
| 4 | Evaluating prompts | LO-4.1–4.3 | 3 | 8.5 | Build an evaluation: a test set, code graders, a model grader checked against 20 human labels, and a comparison of two prompts with intervals, then Opus 5.5 against Haiku 5.5 |
| 5 | Structured output, tools, and agents | LO-5.1–5.4 | 4 | 8.5 | Extract records with `messages.parse`; write the tool loop by hand and test it with a scripted model; an agent with three tools and limits on turns and cost |
| 6 | Documents, retrieval, and prompt injection | LO-6.1–6.5 | 4, 5 | 8.5 | Answer from a bundled handbook; retrieval in plain Python and its recall against answer accuracy; measure a cache hit; attack a tool-using assistant with a planted document, then defend it |
| 7 | Prompting a coding agent | LO-7.1–7.3 | 5 | 7 | Drive Claude Code from Python on a small repository: a vague and a specific task prompt, three runs each, scored by the repository's tests; read a session's tool calls |
| 8 | Configuring a coding agent | LO-8.1–8.3 | 7 | 7 | The same repository with a `CLAUDE.md`, a path-scoped rule, and a skill, each checked by a script; deny a tool and watch what the agent does |

The hours cover the reading, the lab, the practice, and the graded notebook that follows the
module: about 2 hours of reading, 2.5 of lab, 1 of practice, and 2.5 for a graded notebook. The
capstone project takes about 16 hours more, so the course takes about 76 hours in all.

### Data and examples

Every data set is written for this course and bundled with it: support tickets for a fictional
company, a short employee handbook, product reviews, and the small repository that Labs 7 and 8
change. None contains a real person's data.

### What the course teaches about current models

Many prompt-engineering guides were written for older models, and some of their techniques now
fail on the current API. The course teaches the current behavior, confirmed against the API
documentation for each module as it is built:

- Claude Opus 5.5 always thinks before it answers. Its `effort` setting (`low` to `max`, default
  `medium`) controls how much, and setting thinking off returns an error.
- Sampling settings such as `temperature` return an error on current models, so the course controls
  variation with the prompt and measures it with repeated runs.
- Prefilling the start of the model's answer returns an error on current models. Module 2 controls
  format with instructions, and Module 5 with structured outputs.
- Forcing a particular tool with `tool_choice` returns an error on Opus 5.5. Module 5 steers tool
  use with descriptions and instructions.
- A response can stop with `stop_reason` `"refusal"`. Every lab checks the stop reason before it
  reads the text, and Module 5 teaches refusal handling, including the API's optional `fallbacks`
  parameter, which reruns a refused request on another model. I propose the labs leave `fallbacks`
  out before Module 5, to keep early code short, and use it from Module 5 on.

## 5. Assessment

The course has no exams. Self-paced students use every piece as feedback. When an instructor
offers the course for credit, these weights apply:

| Component | Weight | Objectives | Graded by |
| :- | :- | :- | :- |
| Labs 1–8 | 10% | Each module's own | Completion: every visible check in the notebook passes |
| PA1–PA4: graded notebooks | 40% (10% each) | See below | nbgrader: tests of the code parts, and an evaluation of the prompts on hidden test cases |
| Capstone project | 50% (proposal 5%, milestone 15%, final 30%) | See below | A rubric, at three checkpoints |

- **PA1: A prompt that holds up** (after Module 2): a cost estimator, a function that keeps a
  conversation's history, a prompt template that tags its data and splits it between the system
  prompt and the user's turn, and a rewrite of a vague prompt that must pass hidden test inputs
  over repeated runs, with a count of how often its outputs differ. LO-1.1–1.4, 2.1–2.4.
- **PA2: An evaluated classifier** (after Module 4): a support-ticket router with few-shot examples
  and a chosen effort level, its own test set and graders, and a pass rate on held-out cases with
  an interval. LO-3.1, 3.2, 4.1–4.3, and revisits LO-1.3, 2.4.
- **PA3: A tool-using assistant** (after Module 5): structured extraction, three tools, and a tool
  loop that hidden tests drive with a scripted model, so it is graded without API calls; then a
  fixed workflow and an agent compared on five tasks. LO-5.1–5.4, 3.3.
- **PA4: Answers from documents** (after Module 6): retrieval graded by its recall on labeled
  questions, answers with quotations and "I don't know", a verified cache hit, and hidden
  documents that carry injections. LO-6.1–6.5, and revisits LO-2.2, 4.3, 5.1.
- **Capstone project** (proposal after Module 6, milestone after Module 7, final after Module 8):
  each student builds one LLM feature of their own choosing, or one from a list, in a repository
  configured for Claude Code. The proposal states the task, its success criteria, its risks
  (including where untrusted text enters), and a cost estimate. The milestone is an evaluation of
  at least 30 cases, split into development and held-out sets, with its graders and a baseline
  prompt's measured pass rate. The final version shows at least three measured prompt versions, a
  held-out result with its uncertainty, one technique from Modules 3, 5, or 6 justified by
  measurement, the results of injection tests, and the cost per request. It is built with Claude
  Code configured by the student's own `CLAUDE.md`, one path-scoped rule, and one skill, and the
  report quotes two task prompts, traces one session, and describes how the agent's changes were
  reviewed. LO-1.2, 2.1, 3.3, 4.1–4.3, 5.1, 5.4, 6.5, 7.1–7.3, 8.1–8.3.

Graded notebooks mix two kinds of problem. Code problems (a cost function, a grader, a retrieval
step, a tool loop) have exact answers and ordinary tests. Prompt problems have no single answer:
the hidden tests run the student's prompt on hidden cases, three times each, and require a pass
rate that the model solution clears with room to spare and a naive prompt doesn't. I set each
threshold from measurements during the build, and record them in `solutions/`.

Grading the prompt problems calls the API, at roughly $1–3 per student per notebook on Opus 5.5.
I measure the real figure during the build.

**Answer keys** go in `courses/pe101/solutions/`, as the repository's teaching rule already
decided (committed, never linked from coursework, and never built into the website): the nbgrader
sources for PA1–PA4, with their hidden tests and thresholds, lab answer keys, the capstone
rubric's examples, and graders' notes. The capstone rubric's criteria are published with its brief.

## 6. Alignment

Every objective is taught before it is assessed, and assessed at least once beyond its lab.

| Objective | Taught | Assessed |
| :- | :- | :- |
| LO-1.1, LO-1.4 | Module 1 | Lab 1, PA1 |
| LO-1.2 | Module 1 | Lab 1, PA1, capstone |
| LO-1.3 | Module 1 | Lab 1, PA1, PA2 |
| LO-2.1 | Module 2 | Lab 2, PA1, capstone |
| LO-2.2 | Module 2 | Lab 2, PA1, PA4 |
| LO-2.3 | Module 2 | Lab 2, PA1 |
| LO-2.4 | Module 2 | Lab 2, PA1, PA2 |
| LO-3.1, LO-3.2 | Module 3 | Lab 3, PA2 |
| LO-3.3 | Module 3 | Lab 3, PA3, capstone |
| LO-4.1, LO-4.2 | Module 4 | Lab 4, PA2, capstone |
| LO-4.3 | Module 4 | Lab 4, PA2, PA4, capstone |
| LO-5.1 | Module 5 | Lab 5, PA3, PA4, capstone |
| LO-5.2, LO-5.3 | Module 5 | Lab 5, PA3 |
| LO-5.4 | Module 5 | Lab 5, PA3, capstone |
| LO-6.1–LO-6.4 | Module 6 | Lab 6, PA4 |
| LO-6.5 | Module 6 | Lab 6, PA4, capstone |
| LO-7.1–LO-7.3 | Module 7 | Lab 7, capstone |
| LO-8.1–LO-8.3 | Module 8 | Lab 8, capstone |

## 7. Suggested pace

The course is self-paced, so it has no due dates. This pace takes 11 weeks at about 7 hours a week:

| Week | Module | Then |
| :- | :- | :- |
| 1 | 1: First calls to the API | |
| 2 | 2: Clear instructions | PA1 |
| 3 | 3: Examples, reasoning, and chains | |
| 4 | 4: Evaluating prompts | PA2 |
| 5 | 5: Structured output, tools, and agents | PA3 |
| 6 | 6: Documents, retrieval, and prompt injection | PA4 |
| 7 | Capstone proposal | Proposal |
| 8 | 7: Prompting a coding agent | |
| 9 | Capstone evaluation | Milestone |
| 10 | 8: Configuring a coding agent | |
| 11 | Capstone final version | Final version |

## 8. Environment

**Python:** 3.12, in the repository's existing `.venv/`.

Each item needs the instructor's approval before it is installed or added:

| Item | Where | Why |
| :- | :- | :- |
| `anthropic`, the Claude API's Python SDK (2.14.0 on 2026-11-25; needs Python 3.10 or later) | `requirements.txt` | Every lab calls Claude through it; it brings Pydantic, which Module 5 uses |
| `claude-agent-sdk`, which runs Claude Code from Python (0.2.189 on 2026-11-25) | `requirements.txt` | Labs 7 and 8 run Claude Code on a repository from notebook cells, several times per prompt, and score each run. It bundles the Claude Code program, so it needs no separate install and no Node.js |
| `matplotlib` | `requirements.txt` | Plots of pass rates with their intervals, and of accuracy against cost |
| `promptlab`, a small helper written for this course | `courses/pe101/promptlab/`, installed from `requirements.txt` | See below |
| An Anthropic API key for the build | `.env` at the repository root, which `.gitignore` already excludes | Recording every lab's responses and setting the graded notebooks' thresholds; see section 13 |

`promptlab` gives labs an ordinary `anthropic.Anthropic` client with three additions, so the code
students read is the real SDK:

- **Recording and replay.** It records every API response in the lab's cassette file. With no API
  key, a lab runs entirely from its recordings, for free, and a request the cassette doesn't hold
  fails with a message that says a key is needed to run a changed prompt. This makes the labs run
  the same way in the course's checks (`pytest --nbmake`) every time, without a key or any cost.
  Labs 7 and 8 record each agent session's messages and the files it changed.
- **A cost meter.** It prices each response's usage and prints a running total for the notebook.
- **A budget cap.** It refuses a request that would take the notebook past a limit the student
  sets.

No LaTeX: with no exams and little mathematics, every piece is Markdown or a notebook. The course
has no `latex/` folder.

**Cost to students.** Running a lab as written costs nothing, because it replays its recordings.
Changing prompts and running them live costs money. My rough estimate before measuring, for a
student who reruns each lab's live cells about three times: $3–8 for each of Labs 1–6, $10–20
for each of Labs 7 and 8, $3–8 for each graded notebook, and $20–40 for the capstone, so about
$70–160 for the course on Opus 5.5. The build replaces this estimate with measured numbers.

## 9. Sources

Each was fetched and confirmed on 2026-11-25. No textbook is required: the course's own readings
and Anthropic's free documentation cover everything, and the papers are further reading.

**Documentation** (Claude API pages under <https://platform.claude.com/docs/en/>, Claude Code
pages under <https://code.claude.com/docs/en/>):

| Source | Why it is here |
| :- | :- |
| "Prompting best practices", `build-with-claude/prompt-engineering/claude-prompting-best-practices` | Modules 2, 3, and 6: one page that now replaces the older separate pages on clarity, examples, XML tags, roles, long context, thinking, chaining, and moving away from prefill |
| "Using the Messages API", `build-with-claude/working-with-messages` | Module 1, and the source for prefill returning an error on current models |
| "Thinking", `build-with-claude/thinking`, and "Effort", `build-with-claude/effort` | Module 3's thinking and effort levels |
| "Define success criteria and build evaluations", `test-and-evaluate/develop-tests` | Module 4 |
| "Structured outputs", `build-with-claude/structured-outputs`, and "Tool use with Claude", `agents-and-tools/tool-use/overview` | Module 5 |
| "Prompt caching", "Citations", "Reduce hallucinations", and "Mitigate jailbreaks and prompt injections", under `build-with-claude/` and `test-and-evaluate/strengthen-guardrails/` | Module 6 |
| Anthropic, "Building effective agents", by Erik S. and Barry Zhang, December 19, 2024, <https://www.anthropic.com/engineering/building-effective-agents> | Module 5: workflows against agents, and when an agent is worth its cost |
| Claude Code docs: "Overview", "Best practices for Claude Code", "How Claude remembers your project" (`CLAUDE.md` and `.claude/rules/`), "Extend Claude with skills", "Create custom subagents", "Hooks reference" and its guide, "Settings files and precedence", and "Configure permissions" | Modules 7 and 8 |
| "Agent SDK reference - Python", `agent-sdk/python`, and the `claude-agent-sdk` package | Labs 7 and 8, which run Claude Code from notebook cells |
| OWASP Gen AI Security Project, "LLM01:2025 Prompt Injection", <https://genai.owasp.org/llmrisk/llm01-prompt-injection/> | Module 6: the industry's list of direct and indirect injection and their mitigations |

**Papers and books:**

| Source | Why it is here |
| :- | :- |
| Sennrich, Haddow, and Birch, "Neural Machine Translation of Rare Words with Subword Units," ACL 2016, 1715–1725, doi:10.18653/v1/P16-1162 | Module 1: where subword tokens come from |
| Brown et al., "Language Models are Few-Shot Learners," NeurIPS 2020, arXiv:2005.14165 | Module 3: few-shot prompting, named and measured |
| Min et al., "Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?," EMNLP 2022, 11048–11064, doi:10.18653/v1/2022.emnlp-main.759 | Module 3: examples teach format and the range of inputs, not only the labels |
| Zhao, Wallace, Feng, Klein, and Singh, "Calibrate Before Use: Improving Few-Shot Performance of Language Models," ICML 2021, PMLR 139, 12697–12706 | Module 3: how the choice and order of examples bias answers |
| Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," NeurIPS 2022, doi:10.52202/068431-1800 | Module 3: why reasoning before answering helps, the idea behind built-in thinking |
| Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," NeurIPS 2023 Datasets and Benchmarks Track, doi:10.52202/075280-2020 | Module 4: model graders, their agreement with people, and their biases |
| Wilson, "Probable Inference, the Law of Succession, and Statistical Inference," *JASA* 22(158), 1927, 209–212, doi:10.1080/01621459.1927.10502953 | Module 4: the interval the course reports around a pass rate |
| Efron and Tibshirani, *An Introduction to the Bootstrap*, Chapman & Hall, 1993 (ISBN 978-0-412-04231-7) | Module 4: comparing two prompts by resampling test cases |
| Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," ICLR 2023, arXiv:2210.03629 | Module 5: the reason-act-observe loop that agents run |
| Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," NeurIPS 2020, arXiv:2005.11401 | Module 6: retrieval before generation, named |
| Robertson and Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," *Foundations and Trends in Information Retrieval* 3(4), 2009, 333–389, doi:10.1561/1500000019 | Module 6: the BM25 scoring that Lab 6's retrieval implements |
| Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," *TACL* 12, 2024, 157–173, doi:10.1162/tacl_a_00638 | Module 6: where in a long prompt models use information well |
| Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection," AISec '23, ACM, 2023, 79–90, doi:10.1145/3605764.3623985 | Module 6: indirect prompt injection, demonstrated |

Not assigned: Anthropic's interactive prompt engineering tutorial on GitHub. It calls Claude 3
Haiku, which retired on April 20, 2026, and its Chapter 5 teaches prefill, which current models
reject. Anthropic's own overview says to follow "Prompting best practices" where the two differ.

Two details for `references.bib`: the "Building effective agents" byline gives only "Erik S.", so
the entry names its authors as the page does; and Routledge lists *An Introduction to the
Bootstrap* as copyright 1994, a later printing of the 1993 book.

## 10. Policies

Drafts for the instructor to change. The syllabus states them plainly.

- **Pace and late work:** the course is self-paced and has no deadlines. An instructor who offers
  it for credit sets one final date for all work, and late work after it follows the
  institution's rules.
- **Collaboration and academic integrity:** discuss ideas with anyone, but write your own prompts,
  code, and answers. Don't share or look at another student's solution. Name everyone you
  discussed a graded notebook with, and cite any prompt or code you adapted.
- **Generative AI tools:** this course is about using them, so the rules depend on what is being
  practiced. You may use AI tools at any time to explain concepts, error messages, and
  documentation. In labs and graded notebooks, write your own prompts and code, because the prompt
  is what is graded. In Modules 7 and 8 and the capstone, you are expected to use a coding agent:
  keep its session records, and say in your report which parts it wrote. End every submission with
  a short note saying which tools you used and how, or "none".
- **API keys and data:** use your own API key, and set a spending limit for it in the Claude
  Console. Never put a key in a notebook, a file you commit, or a submission. Send the API only
  the course's data and your own text, never another person's personal information.
- **Accommodations:** students with a disability get the accommodations that the institution's
  disability services office approves, such as accessible formats of every material and more time.
  Arrange them through that office and the learning management system.

## 11. Interactivity

I propose static pages: readers download each notebook and run it in their own environment, from
its recordings or live with their own key. In-page execution through Binder (`jupyter: true`)
would need an API key on a public server, which the course should never do, and a Binder session
without a key could only replay recordings. JupyterLite (`lite: true`) runs Python in the browser,
which would expose the student's key to the page.

## 12. Folder layout

The skill's standard layout, adapted to a self-paced course with no exams or LaTeX:

```text
courses/pe101/
├── README.md             the syllabus: the course hub
├── PLAN.md               this plan, not published
├── setup.md              the environment and the API key
├── python-primer.md      Python for the labs
├── notation.md           the few symbols: cost, pass rate, intervals, and retrieval scores
├── references.bib        the confirmed sources, in biblatex's authoryear style
├── ERRATA.md             corrections, by term
├── myst.yml              the website's configuration, for Jupyter Book 2
├── promptlab/            the labs' helper, with its tests
├── modules/NN-<slug>/    index.md, labNN.py, labNN.ipynb, labNN.cassette.json, practice.md
├── assignments/          PA1–PA4 student versions, and the capstone brief
├── tools/                checks for labs and graded notebooks, adapted from LUA101's
└── solutions/            lab keys, nbgrader sources, thresholds, and graders' notes
```

## 13. Questions for the instructor

1. **Approve or change** the objectives, the modules, the weights, the policies, and the
   interactivity choice above.
2. **The packages and the helper** in section 8: `anthropic`, `claude-agent-sdk`, `matplotlib`,
   and `promptlab`.
3. **An API key and a budget for the build.** No key is set up on this machine, so no lab can call
   the model yet. Put a key in `.env` at the repository root, as `ANTHROPIC_API_KEY=…`; I'll never
   print or commit it. I propose a cap of $150 for the whole build. `promptlab`'s meter tracks it,
   and I stop and ask before passing it.
4. **The `fallbacks` parameter** from Module 5 on, as section 4 proposes.

## Build checklist

Tick each line once its piece passes its checks.

- [ ] Environment: packages in `requirements.txt`, `promptlab` with its tests, and the API key
- [ ] Layout: syllabus (`README.md`), `setup.md`, `python-primer.md`, `notation.md`,
  `references.bib`, `ERRATA.md`, `myst.yml`, and the check tools
- [ ] Module 1: reading, lab, and practice
- [ ] Module 2: reading, lab, and practice
- [ ] PA1: graded notebook source, student version, thresholds, and key
- [ ] Module 3: reading, lab, and practice
- [ ] Module 4: reading, lab, and practice
- [ ] PA2: graded notebook source, student version, thresholds, and key
- [ ] Module 5: reading, lab, and practice
- [ ] PA3: graded notebook source, student version, thresholds, and key
- [ ] Module 6: reading, lab, and practice
- [ ] PA4: graded notebook source, student version, thresholds, and key
- [ ] Capstone: brief, checkpoints, and rubric
- [ ] Module 7: reading, lab, practice, and the starter repository
- [ ] Module 8: reading, lab, and practice
- [ ] Whole-course checks: notebooks, website build, leak search, alignment, answers,
  accessibility, links, costs measured, and the rules' checks
