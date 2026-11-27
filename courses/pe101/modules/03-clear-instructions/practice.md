# Module 3 practice

Use these exercises after the [reading](index.md) and [lab](lab03.ipynb). Write each answer before opening its check.

## Worked example

A customer asks for the receipt for a brake repair. A queue contract that prioritizes the
active request gives `Label: billing`. Your parser should recognize the shape of
`Label: repair` too. The labeled ticket is how you decide which one is correct.

## Exercises

### Exercise P3.1 (LO-3.1, ★, about 10 minutes)

Rewrite “Check this” for a clerk who needs to find duplicate charges on an invoice. Name the evidence that counts.

<details>
<summary>Hint</summary>

Specify two charges with the same reference, rather than two products with the same price.

</details>

<details>
<summary>Answer</summary>

Ask for pairs of lines with the same charge reference and amount. Return the references, or “none” if no pair qualifies.

</details>

### Exercise P3.2 (LO-3.2, ★★, about 15 minutes)

A queue manager changes the policy for every ticket. A dispatcher sends a new ticket. Where does each text go?

<details>
<summary>Hint</summary>

Consider how frequently each changes.

</details>

<details>
<summary>Answer</summary>

Keep the revised policy in the system field and put the ticket in the user turn.

</details>

### Exercise P3.3 (LO-3.3, ★★, about 15 minutes)

Construct a valid but wrong output and an invalid but semantically right one for T10, a request about a charge for a returned part.

<details>
<summary>Hint</summary>

T10 belongs to billing.

</details>

<details>
<summary>Answer</summary>

Valid but wrong: `Label: repair`. Right label, wrong format: `The answer is billing.`

</details>

### Exercise P3.4 (LO-3.1, LO-3.3, ★★★, about 25 minutes)

Write a two-sentence policy for a ticket that asks about two active issues. Design a visible check of your choice.

<details>
<summary>Hint</summary>

Choose one priority rule or an explicit fallback.

</details>

<details>
<summary>Answer</summary>

One policy chooses the first explicit request. A ticket asking first about a receipt and then a flat tire should yield exactly `Label: billing`.

</details>
