# Module 10 practice

Use these exercises after the [reading](index.md) and [lab](lab10.ipynb). Write each answer before opening its check.

## Worked example

For one labeled section and k=3, recall is 1 if the section occurs among the three, and 0 if it does not. On a two-section case with one section in the results, recall is 0.5 and coverage fails.

## Exercises

### Exercise P10.1 (LO-10.1, ★, about 10 minutes)

Draft the shape of a prompt from H03 and H09 about returns.

<details>
<summary>Hint</summary>

Name the sources distinctly.

</details>

<details>
<summary>Answer</summary>

Put two ID-marked documents first, ask for an exact quote and ID or abstention, then ask about the return window.

</details>

### Exercise P10.2 (LO-10.2, ★★, about 15 minutes)

Relevant IDs are A and C. Ranked IDs are D, C, A. Find recall at 1, 2, and 3.

<details>
<summary>Hint</summary>

Use the denominator two each time.

</details>

<details>
<summary>Answer</summary>

0, 0.5, 1.

</details>

### Exercise P10.3 (LO-10.3, ★★, about 15 minutes)

A response cites an actual H04 sentence about the return time for a question about how many bicycles are available. How do you score it?

<details>
<summary>Hint</summary>

Check exact match and answer support independently.

</details>

<details>
<summary>Answer</summary>

The quote exists. It neither states nor supports the number, so the answer fails the support criterion.

</details>

### Exercise P10.4 (LO-10.4, ★★★, about 25 minutes)

A 10,000-token prefix at $4 per million gets written at $5 and read at $0.20. Ignore the suffix. When do the costs cross?

<details>
<summary>Hint</summary>

Compare one request and then two.

</details>

<details>
<summary>Answer</summary>

One request costs $0.04 uncached and $0.05 cached. Two cost $0.08 uncached and $0.052 with one hit. Eligibility and a hit are assumptions.

</details>
