# Module 4 practice

Use these exercises after the [reading](index.md) and [lab](lab04.ipynb). Write each answer before opening its check.

## Worked example

The phrase `Chain & brakes < $30` becomes `Chain &amp; brakes &lt; $30` inside a text node. The parser reads it back as `Chain & brakes < $30`.

## Exercises

### Exercise P4.1 (LO-4.1, ★, about 10 minutes)

You have two manual sections and a question about a tire. Lay out your tags.

<details>
<summary>Hint</summary>

Group sources before instructions.

</details>

<details>
<summary>Answer</summary>

Put both sections in documents, followed by instructions and the question.

</details>

### Exercise P4.2 (LO-4.2, ★★, about 15 minutes)

Finish `<ticket>TODO</ticket>` for the value `Cables < $12 & grips`.

<details>
<summary>Hint</summary>

Preserve the literal dollar sign.

</details>

<details>
<summary>Answer</summary>

`<ticket>Cables &lt; $12 &amp; grips</ticket>`.

</details>

### Exercise P4.3 (LO-4.3, ★★, about 15 minutes)

A diff deletes “briefly” and adds “one line, at most 12 words.” Write a test and a rationale.

<details>
<summary>Hint</summary>

Count words and lines independently.

</details>

<details>
<summary>Answer</summary>

Reject a 13-word line and two 5-word lines. The rule trades open-ended brevity for an observable limit.

</details>

### Exercise P4.4 (LO-4.2, LO-4.3, ★★★, about 25 minutes)

Should a blank ticket count as a missing variable? State a policy and design cases for it.

<details>
<summary>Hint</summary>

The distinction can belong in different layers.

</details>

<details>
<summary>Answer</summary>

Require the key in the renderer. Validate nonempty tickets before rendering, so no field and blank field get distinct messages.

</details>
