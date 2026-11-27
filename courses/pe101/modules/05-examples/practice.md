# Module 5 practice

Use these exercises after the [reading](index.md) and [lab](lab05.ipynb). Write each answer before opening its check.

## Worked example

For `{brake, pads}` and `{brake, pads, price}`, Jaccard similarity is 2/3. A higher score is a measure of shared words. The price could still make the intent different.

## Exercises

### Exercise P5.1 (LO-5.1, ★, about 10 minutes)

Supply two labeled examples using the word “chain” that belong in distinct queues.

<details>
<summary>Hint</summary>

Change the customer's request.

</details>

<details>
<summary>Answer</summary>

“The chain skips” is repair. “I was billed twice for a chain” is billing.

</details>

### Exercise P5.2 (LO-5.2, ★★, about 15 minutes)

Every billing prompt contains a dollar amount. Which validation case is missing?

<details>
<summary>Hint</summary>

Try a receipt without a price.

</details>

<details>
<summary>Answer</summary>

Add “Could I get a copy of the receipt?” with label billing, and a repair quote question with a price where the current request is mechanical advice.

</details>

### Exercise P5.3 (LO-5.3, ★★, about 15 minutes)

Rank `{wheel}` and `{wheel, brake, receipt}` for `{wheel, brake}`.

<details>
<summary>Hint</summary>

Divide overlap by union.

</details>

<details>
<summary>Answer</summary>

The scores are 1/2 and 2/3, so the second ranks first.

</details>

### Exercise P5.4 (LO-5.3, ★★★, about 25 minutes)

Design a comparison of fixed and dynamic examples that isolates selection. What might you measure besides label accuracy?

<details>
<summary>Hint</summary>

Keep the template and evaluation cases fixed.

</details>

<details>
<summary>Answer</summary>

Track format compliance, label accuracy, and token use. Keep copies of the selected IDs for each case.

</details>
