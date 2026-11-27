# Module 11 practice

Use these exercises after the [reading](index.md) and [lab](lab11.ipynb). Write each answer before opening its check.

## Worked example

If three out of ten unapproved fictional state changes reach accepted, the unauthorized acceptance fraction is 0.3. A usable gate must also accept a host-approved change that the policy permits.

## Exercises

### Exercise P11.1 (LO-11.1, ★, about 10 minutes)

One fixture arrives as a user turn and one arrives as a handbook note. Classify the two.

<details>
<summary>Hint</summary>

Look at the route into context.

</details>

<details>
<summary>Answer</summary>

The user turn is direct and the handbook is indirect.

</details>

### Exercise P11.2 (LO-11.2, ★★, about 15 minutes)

A fixture proposes a label change and carries a flag that says approved. The host's approval store has no record. What does the policy return?

<details>
<summary>Hint</summary>

Approval belongs to the host.

</details>

<details>
<summary>Answer</summary>

Needs_review if the action is permitted in principle. Denied if the allowlist omits it.

</details>

### Exercise P11.3 (LO-11.3, ★★, about 15 minutes)

The unguarded policy accepts 8 of 10 unauthorized proposals. The guarded policy accepts one. Report both rates and the change.

<details>
<summary>Hint</summary>

Use the same denominator.

</details>

<details>
<summary>Answer</summary>

80% and 10%. The decline is 70 percentage points for this fixed set.

</details>

### Exercise P11.4 (LO-11.2, LO-11.3, ★★★, about 25 minutes)

Write two policy test cases that keep an overly restrictive defense from passing review unnoticed.

<details>
<summary>Hint</summary>

Include one read and one approved change.

</details>

<details>
<summary>Answer</summary>

Allow an ordinary known read and an allowed change with an approval matching its exact target.

</details>
