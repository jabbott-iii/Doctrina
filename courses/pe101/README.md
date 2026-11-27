# PE101: Prompt Engineering from First Prompt to Coding Agents

Large language models (LLMs) now run inside many programs and write much of the code in others.
This course teaches prompt engineering: writing the instructions, examples, and context that get
a model to do a task reliably, and building the code that checks whether it does. It is for
programmers who have finished one programming course and haven't built with an LLM before. You
start by building a tiny language model, to see how a prompt becomes text. Then you learn to write
clear, structured prompts, improve them with examples, reasoning, and chains of prompts, and
measure them with evaluations you build yourself. From there you work up to structured output,
tools, agents, answers drawn from documents, and defenses against prompt injection. The last two
modules turn to coding agents: you write task prompts for Claude Code and configure it with
project instructions, rules, skills, permissions, and hooks. The course is self-paced, with no
deadlines and no grades: 13 modules in three parts, five assignments, three self-tests, and a
capstone project for your portfolio.

**The course calls no model.** It needs no account, no API key, and no payment. Its labs build
requests, read responses, and test the code around a model with stand-ins, programs that answer
in the shape of a real model's responses from a script. [How the course teaches without a
model](#how-the-course-teaches-without-a-model) explains what that covers and what it can't.

Start with [setting up your environment](setup.md). If you are new to Python, read
[Python for the labs](python-primer.md) too.

This edition is being published one module at a time. A module without a link in the
[suggested pace](#suggested-pace) isn't published yet.

## Learning objectives

By the end of the course, you can:

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

Each module's objectives serve the course objective in brackets. Every exercise, lab, and
self-test question names the objectives it tests.

### Part 1: Foundations

#### Module 1: How language models produce text [LO-1]

- **LO-1.1:** Train a byte-pair encoding (BPE) tokenizer on a small corpus, and explain why token
  counts differ from word and character counts across prose, code, numbers, and languages.
- **LO-1.2:** Generate text from an n-gram language model by sampling from its next-token
  probabilities, and predict how temperature and top-p (nucleus) sampling change the output's
  variety.
- **LO-1.3:** Explain why one prompt can give different outputs, and how the context window limits
  what a model can use.

#### Module 2: The anatomy of a request [LO-1]

- **LO-2.1:** Build a Messages API request as data (the model, the system prompt, alternating user
  and assistant turns, and `max_tokens`), and read a response's content blocks, stop reason, and
  token usage.
- **LO-2.2:** Compute a request's cost from its token usage and the model's prices, and estimate a
  batch's cost and its context-window use before running it.
- **LO-2.3:** Keep a conversation within a token budget by resending its history, choose what to
  drop or summarize when it overflows, and explain what the model can't remember.
- **LO-2.4:** Handle each stop reason in code, including a truncated answer and a refusal.

#### Module 3: Clear instructions [LO-2]

- **LO-3.1:** Rewrite a vague prompt so it states the task, the audience, the context and its
  purpose, the constraints, and what a good answer looks like, and score both versions with the
  course's prompt rubric.
- **LO-3.2:** Decide what belongs in the system prompt and what belongs in the user's turn, and
  justify the choice.
- **LO-3.3:** Specify an output's format and length, and write code that checks responses against
  the specification.

#### Module 4: Structure, data, and templates [LO-2]

- **LO-4.1:** Separate instructions from data with XML tags, and order a prompt's parts: the
  documents, the instructions, and the question.
- **LO-4.2:** Build a prompt template that inserts variables without breaking the prompt's
  structure, and show a naive template failing on input that contains the template's own markup.
- **LO-4.3:** Keep prompts as versioned files, check that each template's variables are filled,
  and compare two versions with a diff.

### Part 2: Techniques and measurement

#### Module 5: Examples [LO-3]

- **LO-5.1:** Write few-shot examples that cover the range of inputs and labels, in tags that set
  them apart from the task.
- **LO-5.2:** Detect an example set that invites copying of surface features or has a skewed
  balance of labels, and fix it.
- **LO-5.3:** Select examples for each input from a pool by similarity, and compare the selection
  with a fixed set by how much of the input range each covers.

#### Module 6: Reasoning and chains [LO-3]

- **LO-6.1:** Choose a thinking effort level for a task from measurements of accuracy, latency, and
  cost, and justify the choice.
- **LO-6.2:** Ask for reasoning in tagged sections, and extract the final answer in code, failing
  loudly when it is missing.
- **LO-6.3:** Split a complex task into a chain of prompts that pass results forward, and compute
  how errors compound along the chain and what a check step catches.

#### Module 7: Evaluating prompts [LO-4]

- **LO-7.1:** Write measurable success criteria for a task, and build a test set with typical,
  edge, and adversarial cases.
- **LO-7.2:** Grade outputs with code-based graders, and measure a model-based grader's agreement
  with human labels with percent agreement and Cohen's kappa.
- **LO-7.3:** Report a pass rate over repeated runs with a Wilson interval, and compare two prompts
  with a paired bootstrap over test cases.
- **LO-7.4:** Keep a held-out test set, and explain how tuning a prompt on the test set biases the
  comparison.

#### Module 8: Structured output and tools [LO-5]

- **LO-8.1:** Write a JSON Schema for a structured output, validate responses against it, and
  handle a response that fails validation.
- **LO-8.2:** Define tools whose names, descriptions, and input schemas tell the model when and how
  to use each one.
- **LO-8.3:** Implement the tool-use loop (run each call, return its result or error, and stop on
  the right stop reason), and test it with a scripted stand-in for the model.

### Part 3: Systems and agents

#### Module 9: Workflows and agents [LO-5]

- **LO-9.1:** Implement four workflow patterns (routing, parallel calls, an orchestrator with
  workers, and an evaluator with an optimizer) with stand-in model calls.
- **LO-9.2:** Build an agent loop with limits on turns and cost, and trace its steps from its log.
- **LO-9.3:** Choose among one call, a fixed workflow, and an agent for a task, and justify the
  choice by the task's complexity, its value, the model's ability at it, and the cost of errors.

#### Module 10: Documents, retrieval, and context [LO-6]

- **LO-10.1:** Structure a long-context prompt with tagged documents placed before the question,
  and ask for answers grounded in quotations.
- **LO-10.2:** Implement BM25 retrieval, measure its recall at k on labeled questions, and explain
  how retrieval recall caps answer accuracy.
- **LO-10.3:** Reduce unsupported answers by allowing "I don't know" and requiring evidence, and
  verify quotations against their sources in code.
- **LO-10.4:** Order a prompt so its stable parts come first, and compute what caching that prefix
  saves.

#### Module 11: Prompt injection [LO-7]

- **LO-11.1:** Demonstrate direct and indirect prompt injection against a tool-using assistant run
  by a deliberately gullible stand-in, and explain why the prompt can't be the only defense.
- **LO-11.2:** Reduce an injection's harm with least privilege, marked untrusted content, and human
  approval of risky actions, and state what each defense can't stop.
- **LO-11.3:** Build an injection test set, and measure a system's attack success rate before and
  after its defenses.

#### Module 12: Prompting a coding agent [LO-8]

- **LO-12.1:** Trace a coding agent's session as a loop of model turns and tool calls, and identify
  where the context behind each decision came from.
- **LO-12.2:** Write a task prompt for a coding agent that states the goal, the relevant files, the
  constraints, and how to verify the result, and score it with the course's rubric.
- **LO-12.3:** Give an agent a way to check its own work (tests, a linter, or a script), and review
  a diff against its task before accepting it.

#### Module 13: Configuring a coding agent [LO-8]

- **LO-13.1:** Write project instructions in a `CLAUDE.md` file and in rules scoped to paths, and
  work out which rules load for a given file.
- **LO-13.2:** Package a repeatable workflow as a skill, and decide what to delegate to a subagent.
- **LO-13.3:** Write permission rules and a hook that blocks a risky command, test the hook by
  piping sample events into it, and explain what permission rules and hooks can and can't prevent.

## Prerequisites

You need one finished programming course in any language, such as Python, Java, JavaScript, or C,
and some practice with Git and a terminal. You don't need Python already: the labs are in Python,
and [Python for the labs](python-primer.md) teaches the Python they use. You don't need any
experience with language models.

**Self-check.** If you can do all five of these, in any language, you are ready:

1. Write a function that takes a list of strings and a word, and returns the strings that contain
   the word; then test it with an assertion.
2. Read a JSON file into a dictionary or map, and print one of its fields.
3. Explain the difference between what a function returns and what it prints.
4. Run a program from a terminal with a file path as its argument, and read its error message.
5. Clone a Git repository, change a file, and commit the change.

(how-the-course-teaches-without-a-model)=
## How the course teaches without a model

Prompt engineering is usually learned by trying prompts on a model, which costs money for every
request. This course calls no model, so it costs nothing, and it is plain about what it does
instead:

- **What you never see:** a live model's response to a prompt you wrote. What you learn about how
  real models respond comes from the readings, which cite the documentation or a paper for every
  such claim.
- **Writing prompts:** you write many prompts, and score each with the course's prompt rubric and
  against a model answer. The labs' checks test only what code can check exactly, such as whether
  the data sits inside its tags and every template variable is filled.
- **Judging responses:** the labs bundle sets of responses written for this course, each labeled
  as illustrative and not model output. They show the failure modes that the documentation and
  the research describe, such as a format that drifts or an answer the documents don't support,
  so you can practice grading, measuring, and comparing. A number computed from them describes
  that data set only.
- **The software around the model:** you test tool loops, workflows, agents, and defenses with
  stand-ins, the way production code tests features built on a model without calling one. The
  readings say which behavior a stand-in fakes and which it can't.
- **How a model produces text:** Module 1 builds a tokenizer and a small language model from
  scratch. They show tokens, next-token probabilities, and sampling at a small scale. Real LLMs
  compute those probabilities with a neural network, the transformer, which the course names but
  doesn't teach.

Your capstone project ends with an evaluation that is ready to run against a real model, and a
report that says what you measured and what still needs a model.

(suggested-pace)=
## Suggested pace

The course is self-paced, so it has no deadlines: take as long as you need. This pace takes 16
weeks at about 8 hours a week. A module takes 6–8 hours: about 2 for the reading, 2.5 for the lab,
and 1–1.5 for the practice, as each module's reading says. An assignment adds about 3 hours, a
self-test about 2, and the capstone project about 20.

| Week | Topic | Reading | Then |
| :- | :- | :- | :- |
| 1 | How language models produce text | [Module 1](modules/01-how-models-produce-text/index.md) | |
| 2 | The anatomy of a request | [Module 2](modules/02-anatomy-of-a-request/index.md) | [PA1](assignments/pa1/pa1.ipynb) |
| 3 | Clear instructions | [Module 3](modules/03-clear-instructions/index.md) | |
| 4 | Structure, data, and templates | [Module 4](modules/04-structure-data-and-templates/index.md) | [PA2](assignments/pa2/pa2.ipynb), [Self-test 1](self-tests/self-test-1.md) |
| 5 | Examples | [Module 5](modules/05-examples/index.md) | |
| 6 | Reasoning and chains | [Module 6](modules/06-reasoning-and-chains/index.md) | |
| 7 | Evaluating prompts | [Module 7](modules/07-evaluating-prompts/index.md) | [PA3](assignments/pa3/pa3.ipynb) |
| 8 | Structured output and tools | [Module 8](modules/08-structured-output-and-tools/index.md) | [Self-test 2](self-tests/self-test-2.md) |
| 9 | Workflows and agents | [Module 9](modules/09-workflows-and-agents/index.md) | [PA4](assignments/pa4/pa4.ipynb), [capstone proposal](assignments/final-project/README.md#proposal) |
| 10 | Documents, retrieval, and context | [Module 10](modules/10-documents-retrieval-and-context/index.md) | |
| 11 | Prompt injection | [Module 11](modules/11-prompt-injection/index.md) | [PA5](assignments/pa5/pa5.ipynb), [capstone milestone](assignments/final-project/README.md#milestone) |
| 12 | Prompting a coding agent | [Module 12](modules/12-prompting-a-coding-agent/index.md) | |
| 13 | Configuring a coding agent | [Module 13](modules/13-configuring-a-coding-agent/index.md) | [Self-test 3](self-tests/self-test-3.md) |
| 14–16 | The capstone project | [The capstone brief](assignments/final-project/README.md) | [Final version](assignments/final-project/README.md#final-version) |

## Checking your work

The course has no grades. Instead, every piece comes with a way to check it, so you can tell what
you have learned and what to review:

| Piece | How you check it | Objectives |
| :- | :- | :- |
| Labs 1–13 | Every check cell in the notebook passes | Each lab's module |
| PA1: Requests and costs (notebook) | Its visible tests | LO-2.1–2.4, LO-1.3 |
| PA2: A prompt library (notebook) | Its visible tests, and the prompt rubric for its prompts | LO-3.1–3.3, LO-4.1–4.3, LO-2.1 |
| PA3: An evaluated classifier (notebook) | Its visible tests | LO-5.1–5.3, LO-6.2, LO-7.1–7.4, LO-3.3 |
| PA4: A tool-using assistant (notebook) | Its visible tests, which drive your code with scripted stand-ins | LO-8.1–8.3, LO-9.1–9.3, LO-2.4, LO-6.3 |
| PA5: Answers from documents, defended (notebook) | Its visible tests | LO-10.1–10.4, LO-11.1–11.3, LO-4.2, LO-7.3, LO-8.1 |
| Self-test 1, after Module 4 | The answers and scoring notes in the page | Modules 1–4 |
| Self-test 2, after Module 8 | The answers and scoring notes in the page | Modules 1–8, weighted toward 5–8 |
| Self-test 3, after Module 13 | The answers and scoring notes in the page | All modules, weighted toward 9–13 |
| Capstone project: proposal, milestone, and final version | The brief's checklists and rubric | LO-2.2, LO-3.1, LO-4.2, LO-4.3, LO-6.3, LO-7.1–7.4, LO-8.1, LO-9.3, LO-10.4, LO-11.2, LO-11.3, LO-12.1–12.3, LO-13.1–13.3 |

- **The assignments** check your code with visible tests, which you can run as often as you like.
  Their hidden tests aren't published: they stay with the answer keys, for an instructor or a
  mentor who reviews your work, so test the cases each statement describes yourself.
- **The prompts you write** have no single right answer. Score each with the prompt rubric that
  Module 3 introduces, and compare it with the worked examples in the readings.
- **The self-tests** mix questions from many modules. Take each in one sitting, without notes,
  then open the answers and score yourself.
- **The capstone project** is a prompt package for a task you choose: versioned prompts, a test
  set with graders checked against labels you write, an evaluation that runs end to end on a
  stand-in, a cost estimate, injection tests, and a Claude Code configuration for its repository.

Later pieces revisit earlier objectives on purpose, so that you keep practicing them.

(policies)=
## Policies

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

## Course materials

- [Setting up your environment](setup.md)
- [Python for the labs](python-primer.md)
- [Prompt rubric](prompt-rubric.md)
- [Notation and conventions](notation.md)
- [Errata](ERRATA.md): corrections to published material, by edition
- Text and figures are under the Creative Commons Attribution 4.0 International license (CC BY
  4.0), and code is under the MIT License in the repository's `LICENSE` file.
