# Module 7 practice

Use these exercises after the [reading](index.md) and [lab](lab07.ipynb). Write each answer before opening its check.

## Worked example

If A passes two of three runs on a case and B passes all three, that case contributes +1/3 to the paired comparison. Keep all six results together when resampling.

## Exercises

### Exercise P7.1 (LO-7.1, ★, about 10 minutes)

Write a measurable pass criterion for a one-line routing answer that can abstain.

<details>
<summary>Hint</summary>

Specify allowed labels and the condition for abstention.

</details>

<details>
<summary>Answer</summary>

Require one exact line. For an ambiguous ticket, require Label: unknown. For a clear ticket, require the annotated queue.

</details>

### Exercise P7.2 (LO-7.2, ★★, about 15 minutes)

You agree on 8 of 10 items and each grader passes exactly 5. What is kappa?

<details>
<summary>Hint</summary>

Chance agreement is 0.5 × 0.5 plus 0.5 × 0.5.

</details>

<details>
<summary>Answer</summary>

Observed 0.8, chance 0.5, kappa (0.8 − 0.5) / 0.5 = 0.6.

</details>

### Exercise P7.3 (LO-7.3, ★★, about 15 minutes)

You see a difference of +0.03 with interval −0.04 to +0.10. What can you conclude?

<details>
<summary>Hint</summary>

The interval crosses zero.

</details>

<details>
<summary>Answer</summary>

The point estimate favors B. The interval includes both an improvement and a loss, so the comparison is inconclusive.

</details>

### Exercise P7.4 (LO-7.4, ★★★, about 25 minutes)

You inspect holdout errors, add matching examples, and rerun the same split. How should you report it?

<details>
<summary>Hint</summary>

Ask which data influenced selection.

</details>

<details>
<summary>Answer</summary>

Treat that split as development and disclose the reuse. Gather fresh held-out cases.

</details>
