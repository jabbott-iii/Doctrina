# Module 12 practice

Use these exercises after the [reading](index.md) and [lab](lab12.ipynb). Write each answer before opening its check.

## Worked example

A diff replaces all underscore handling with hyphen handling. It meets the new example but breaks the existing underscore test. Request both separators and an explicit regression case.

## Exercises

### Exercise P12.1 (LO-12.1, ★, about 10 minutes)

Which events in the example are file or test evidence, and which are decisions?

<details>
<summary>Hint</summary>

Use both event and origin.

</details>

<details>
<summary>Answer</summary>

Tool events contain evidence. Model events interpret it. The final model summary is a report.

</details>

### Exercise P12.2 (LO-12.2, ★★, about 15 minutes)

Turn “repair costs look weird” into a task with a clear acceptance criterion.

<details>
<summary>Hint</summary>

Give values and expected total.

</details>

<details>
<summary>Answer</summary>

For repair_total, preserve integer cents and return 1,900 for 1,200 labor plus parts 200 and 500. Add a test and report the suite result.

</details>

### Exercise P12.3 (LO-12.3, ★★, about 15 minutes)

The proposed diff deletes the existing underscore test. What should you check?

<details>
<summary>Hint</summary>

The old behavior is a requirement.

</details>

<details>
<summary>Answer</summary>

Keep the underscore case and add a hyphen case, then run both.

</details>

### Exercise P12.4 (LO-12.2, LO-12.3, ★★★, about 25 minutes)

Write a scope rule for when the agent sees a necessary change in a third file.

<details>
<summary>Hint</summary>

Separate observation from permission to edit.

</details>

<details>
<summary>Answer</summary>

Ask it to describe the dependency and await a decision before editing outside the two named files.

</details>
