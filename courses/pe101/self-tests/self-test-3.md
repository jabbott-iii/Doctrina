# Self-test 3: Systems and agents


This self-test covers all modules, especially Modules 9–13. Set aside about two hours. Use paper or a local text
editor and close the notes for your first attempt. Try every question before opening the
answers. Give yourself 2 points for a complete, justified answer, 1 for a correct start
with a material omission, and 0 for an incorrect or missing answer. The total is
24 points for your own review.


## Question S3.1 (LO-3.3, LO-7.1)

Supply a pass criterion for a help-desk reply that can abstain.

<details>
<summary>Answer and scoring notes</summary>

Require one valid record with a supported reply or an abstention token. Annotate which cases should abstain and why.

</details>

## Question S3.2 (LO-8.3, LO-9.1)

Two independent fixture reads must be paired with a ticket. What workflow fits and what preserves identity?

<details>
<summary>Answer and scoring notes</summary>

Use parallel branches. Keep results keyed by job and correlate tool results to the proposal IDs.

</details>

## Question S3.3 (LO-9.2, LO-9.3)

Three turns cost 2 credits each. The next call reserves 3, and the starting budget is 8. Why stop before the fourth call? When can you remove the agent loop?

<details>
<summary>Answer and scoring notes</summary>

Two credits remain, so the fourth call cannot be reserved. Use a single call or direct lookup when no dynamic decisions are needed.

</details>

## Question S3.4 (LO-10.1, LO-10.2, LO-10.3)

The prompt contains H04 and H02. The answer needs H04 and H09. Find recall, say whether full coverage passed, and give a grounding rule.

<details>
<summary>Answer and scoring notes</summary>

Recall is 0.5 and full coverage fails. Put identified sources first, then instructions and question. Require exact evidence or abstention.

</details>

## Question S3.5 (LO-2.2, LO-10.4)

A prefix of 1,000 tokens is billed at $4 input, $5 write, or $0.20 read per million tokens. Compare four uncached requests with one write and three hits. Ignore suffix and output.

<details>
<summary>Answer and scoring notes</summary>

Uncached input costs $0.016. With hits it costs $0.0056.

</details>

## Question S3.6 (LO-11.1, LO-11.2, LO-11.3)

A fictional proposal arrives via a retrieved document. The unguarded policy accepts 25 cases, and the guarded policy accepts none. Report the rates and name a positive control.

<details>
<summary>Answer and scoring notes</summary>

Indirect. Report 25/25 and 0/25 in this exercise. Test a host-approved label change permitted by the allowlist.

</details>

## Question S3.7 (LO-12.1, LO-12.2)

A trace claims all tests passed. Where can you find evidence? Add verification text to a task that changes service label formatting.

<details>
<summary>Answer and scoring notes</summary>

Look for the test tool's output. Ask to preserve both separators, run the stated test command, and report its result.

</details>

## Question S3.8 (LO-12.3)

A proposed edit changes the invoice calculation alongside the requested label change. What do you check before accepting it?

<details>
<summary>Answer and scoring notes</summary>

Check each changed line against task scope and run independent invoice and label regression tests. Request a scoped revision.

</details>

## Question S3.9 (LO-13.1, LO-13.2)

You need fixture rules and a repeated test review. Where does each go and what could a subagent do?

<details>
<summary>Answer and scoring notes</summary>

Put fixture rules under a path scope and package the review as a skill. Delegate a bounded coverage review without delegating integration.

</details>

## Question S3.10 (LO-13.3)

Why should a deny-only PreToolUse hook print nothing for the exact test command? Give two test events it should deny.

<details>
<summary>Answer and scoring notes</summary>

No decision lets the normal permission layer apply. Test an unknown proposed command and invalid JSON.

</details>

## Question S3.11 (LO-1.1, LO-1.3, LO-4.2)

A long manual contains literal ampersands and many part numbers. Explain how to put it in a tagged template and how to decide which sections fit the context.

<details>
<summary>Answer and scoring notes</summary>

Escape the text at insertion and confirm an exact XML round trip. Count tokens with the relevant tokenizer or document the uncertainty of an estimate. Reserve room for the instructions, question, and response before admitting sections.

</details>

## Question S3.12 (LO-5.2, LO-5.3, LO-6.3)

A receipt mentions the same brake phrase as five repair examples. Propose a less skewed set and show how to test a classify-then-draft chain.

<details>
<summary>Answer and scoring notes</summary>

Keep a receipt contrast with the same phrase and select examples across relevant labels. Measure correct routing, conditional drafting success when routing is correct, and pipeline success. Keep the original receipt request available to the checking stage.

</details>

## Decide what to review

Revisit every module where you lost a point. Redo one lab check and one practice exercise
with a changed input, then explain why the expected result changes. A missing unit,
unstated assumption, or skipped validation condition is worth correcting in your notes.
