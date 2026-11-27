# Module 8 practice

Use these exercises after the [reading](index.md) and [lab](lab08.ipynb). Write each answer before opening its check.

## Worked example

A proposal with ID `c1` asks for Friday hours. The next user message contains a `tool_result` with `tool_use_id: c1`. For an unknown day, return an error associated with `c1` so the caller can diagnose it.

## Exercises

### Exercise P8.1 (LO-8.1, ★, about 10 minutes)

Write one record that fails schema and one that passes schema but misroutes a broken brake.

<details>
<summary>Hint</summary>

Use an enum value in the second record.

</details>

<details>
<summary>Answer</summary>

A missing queue fails validation. A record with account and “broken brake” passes the schema but should route to repair.

</details>

### Exercise P8.2 (LO-8.2, ★★, about 15 minutes)

Propose a name and input schema for reading whether a fictional service is offered. What does it return for an unknown service?

<details>
<summary>Hint</summary>

Use a read-only name and a required string.

</details>

<details>
<summary>Answer</summary>

Use service_availability with a required service string. Report an unknown service explicitly.

</details>

### Exercise P8.3 (LO-8.3, ★★, about 15 minutes)

A turn contains IDs p1 and h1. p1 succeeds and h1 fails. Outline the next message.

<details>
<summary>Hint</summary>

Both proposals need a result.

</details>

<details>
<summary>Answer</summary>

Send one user message containing an ordinary result for p1 and an error result for h1.

</details>

### Exercise P8.4 (LO-8.1, LO-8.3, ★★★, about 25 minutes)

A JSON response fails validation twice with a retry limit of one. What happens?

<details>
<summary>Hint</summary>

The initial call is followed by at most one retry.

</details>

<details>
<summary>Answer</summary>

Return an explicit invalid-record failure and let the caller decide the fallback.

</details>
