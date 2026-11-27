# Module 6: Reasoning and chains

**Objectives** LO-6.1, LO-6.2, LO-6.3  
**Prerequisites** Module 5  
**Time** About 6 hours across this reading, [Lab 6](lab06.ipynb),
and [practice](practice.md).

## Choose what thinking is for

A routine routing task and a ticket that combines several financial constraints require
different amounts of work. Thinking effort is a model setting. It differs from asking the
model to put a short justification in its final response. Opus 5.5 uses adaptive thinking
and defaults to medium effort. Requests that disable thinking on Opus 5.5 return an HTTP 400
error. The model's migration guide suggests lower effort when the goal is to reduce thinking
token use. Consult the model-specific references before reusing a setting with another model.

Start from a requirement. Here, support needs at least 90% accuracy, median latency at
most 2.5 seconds, and the least cost among the levels that qualify. In the illustrative
table in Lab 6, low costs 4 units and reaches 85%. Medium costs 7 and reaches 92% in
2.0 seconds. High costs 12 and reaches 94% in 3.4 seconds. Medium satisfies both
constraints. The table is practice data. Repeat this type of comparison on labeled
cases and independent runs to select a setting for a deployed task.

## Ask for checkable evidence and an answer

A short explanation can make the answer easier to review. Ask for the evidence that
settles the decision and a separate `<answer>` section with the result. For a receipt
request, the evidence can quote “send the receipt,” and the answer can be billing.
Requesting a public justification differs from reading the model's private reasoning.

Reject a missing, empty, or repeated answer section. Extracting a section only checks
shape. The content still needs validation. For fixed output contracts, a structured
schema can replace this text parsing step in Module 8.

## Chain separate tasks

Suppose the shop wants to classify a ticket, write a response, and check the response.
Send the first stage's label along with the ticket to the draft stage. Send the draft
and the constraints to the review stage. Keep the original ticket available so an
incorrect label cannot silently become the only context the check sees.

When each of three stages succeeds in 90% of the cases that reach it with all previous
stages correct, the all-correct rate is 0.9 × 0.9 × 0.9, or 72.9%. Conditional stage
rates matter. Multiplying marginal rates requires independence. A check that finds
half the failures and rejects them lowers the chance of accepting a bad result. It
does not magically turn those failures into correct results.

## Summary

Set effort from measured constraints, validate the final answer section, and trace errors through each stage.

## Self-check

**LO-6.1.** What would rule out the high level in the worked example?

<details>
<summary>Answer</summary>

Its median latency exceeds the specified 2.5-second ceiling.

</details>

**LO-6.2.** What if there are two final answer tags?

<details>
<summary>Answer</summary>

Reject the result as ambiguous.

</details>

**LO-6.3.** If a two-stage chain has conditional success rates 0.9 and 0.8, what is its all-correct rate?

<details>
<summary>Answer</summary>

0.72.

</details>

## Further reading

- [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) contrasts thinking configurations.
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) lists model-specific settings.
- [Opus 5.5 migration guide](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide) explains how the model handles requests that disable thinking.
- [Wei et al. (2022)](https://arxiv.org/abs/2201.11903) reports results for reasoning demonstrations on studied tasks.

Next, open [Lab 6](lab06.ipynb) and then [practice](practice.md).
