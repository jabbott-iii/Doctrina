# Module 6 practice

Use these exercises after the [reading](index.md) and [lab](lab06.ipynb). Write each answer before opening its check.

## Worked example

With two stages at conditional success rates 0.8 and 0.75, the all-correct rate is 0.60. If a check catches 3/4 of incorrect results, 0.10 of all runs still accept an incorrect result.

## Exercises

### Exercise P6.1 (LO-6.1, ★, about 10 minutes)

Change the lab's median latency limit to 1.5 seconds while keeping 90% accuracy. Which effort qualifies?

<details>
<summary>Hint</summary>

Check the thresholds before ordering by cost.

</details>

<details>
<summary>Answer</summary>

None. Low is fast enough but misses accuracy. The two other levels are too slow.

</details>

### Exercise P6.2 (LO-6.2, ★★, about 15 minutes)

Write two distinct responses that a tag extractor should reject.

<details>
<summary>Hint</summary>

Try a well-formed empty answer.

</details>

<details>
<summary>Answer</summary>

`<answer> </answer>` and `<evidence>receipt</evidence>` should both fail.

</details>

### Exercise P6.3 (LO-6.3, ★★, about 15 minutes)

A chain returns correct answers half the time. Its check catches four in five incorrect answers and no correct ones. How often do incorrect answers get through?

<details>
<summary>Hint</summary>

The denominator is all runs.

</details>

<details>
<summary>Answer</summary>

0.5 × 0.2 = 0.10 of all runs.

</details>

### Exercise P6.4 (LO-6.3, ★★★, about 25 minutes)

A one-step assistant has weak invoices but good receipts. Design a three-step alternative and say how to compare it.

<details>
<summary>Hint</summary>

Keep the original request available for checking.

</details>

<details>
<summary>Answer</summary>

Extract task and references, draft a response, then verify it against the original. Compare accuracy by request type, cost, and latency on the same cases.

</details>
