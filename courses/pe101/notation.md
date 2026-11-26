# Notation and conventions

This page lists the conventions that the course's readings, labs, and self-tests share. The course
has no LaTeX documents, so its symbols have no LaTeX macros: every page writes them out in full.

## Prompts, requests, and responses

- Code, names, file names, and values are in code font: `max_tokens`, `stop_reason`,
  `"end_turn"`.
- A prompt or a model's reply appears in a fenced block tagged `text`, exactly as the model would
  read or write it.
- A request or a response is a Python dictionary in the shape of the Claude Messages API's JSON.
  The SDKs wrap the same fields in objects, so `response["stop_reason"]` in a lab is
  `response.stop_reason` with the Python SDK.
- A reply labeled **illustrative** was written for this course. It isn't the output of any model,
  and the course never presents it as one.
- **The model**, in a lab, is a stand-in from `promptlab` that answers from a script. The lab says
  so where one first appears.
- Exercise 3.4 is the fourth exercise in Module 3's practice, and Exercise L3.4 is the fourth in
  Lab 3. Neither number ever changes once published.

## Money and tokens

- Prices are in US dollars per million tokens, as Anthropic's pricing page gives them, and each
  table of prices says the date it was taken. Amounts of money are in code font, such as `$4` per
  million input tokens, because a bare dollar sign starts mathematics in Markdown.
- "1M" means one million and "1K" one thousand, as the documentation writes context windows and
  output limits.

## Symbols

| Symbol | Meaning | First used |
| :- | :- | :- |
| $P(w \mid c)$ | The probability that the next token is $w$, given the context $c$ before it | Module 1 |
| $T$ | Temperature: how much sampling flattens ($T > 1$) or sharpens ($T < 1$) the probabilities | Module 1 |
| $p$ | In top-p sampling, the share of probability that the kept tokens must reach | Module 1 |
| $C$ | The cost of a request or a batch, in US dollars | Module 2 |
| $n$ | The number of test cases, or of runs, behind a measurement | Module 7 |
| $\hat{p}$ | A measured pass rate: the share of $n$ graded outputs that passed | Module 7 |
| $z$ | The number of standard errors that sets an interval's confidence: 1.96 for 95% | Module 7 |
| $\kappa$ | Cohen's kappa: agreement between two graders, corrected for chance | Module 7 |
| $k$ | In retrieval, how many passages are kept for each question | Module 10 |
| $k_1$, $b$ | BM25's two settings: how fast repeated terms stop adding score, and how much document length counts | Module 10 |

The letter $p$ means two things, in two modules: the top-p threshold in Module 1, and a pass rate
in Module 7, where it always wears a hat ($\hat{p}$) when it is measured. Each module defines the
symbols it uses when they first appear.
