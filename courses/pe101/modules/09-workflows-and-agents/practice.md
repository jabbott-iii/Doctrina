# Module 9 practice

Use these exercises after the [reading](index.md) and [lab](lab09.ipynb). Write each answer before opening its check.

## Worked example

A budget of 5 and a reserve of 3 allow one call. If it spends 2, the remaining 3 cover a second call. A spend of 2 on that call leaves 1, so a third call would wait for a new budget.

## Exercises

### Exercise P9.1 (LO-9.1, ★, about 10 minutes)

The planner asks for labor, parts, labor. The contracts prohibit duplicates. How many workers run?

<details>
<summary>Hint</summary>

Validate the full plan first.

</details>

<details>
<summary>Answer</summary>

Zero. Reject the plan before starting any worker.

</details>

### Exercise P9.2 (LO-9.2, ★★, about 15 minutes)

A budget is 8, reserve is 4, turn cap is 4, and two consecutive tool calls spend 3 each. Why does the run stop?

<details>
<summary>Hint</summary>

Compare the next reservation with the remainder.

</details>

<details>
<summary>Answer</summary>

Only 2 remain, so the cost limit stops the third call.

</details>

### Exercise P9.3 (LO-9.3, ★★, about 15 minutes)

Compare a route to two known queues with deciding several service reads for a mixed request.

<details>
<summary>Hint</summary>

Ask who should choose the next step.

</details>

<details>
<summary>Answer</summary>

Use fixed routing for one known branch. A planner or agent may help with task-dependent reads if quality gains justify the extra steps.

</details>

### Exercise P9.4 (LO-9.1, LO-9.2, ★★★, about 25 minutes)

A judge never passes a draft and the optimizer allows three drafts. What is the maximum number of stage calls?

<details>
<summary>Hint</summary>

Each attempt calls both stages.

</details>

<details>
<summary>Answer</summary>

Six. Return a failed result when all three checks fail.

</details>
