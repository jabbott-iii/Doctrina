# Module 13 practice

Use these exercises after the [reading](index.md) and [lab](lab13.ipynb). Write each answer before opening its check.

## Worked example

A rule scoped to `data/**` applies to `data/tickets.json` and `data/archives/old.json`. A rule for `repair_shop.py` applies to that file. Keep test instructions in the main file when both scopes share them.

## Exercises

### Exercise P13.1 (LO-13.1, ★, about 10 minutes)

Your instructions for money apply across the project, and ID formatting matters only in fixtures. Write one sentence for each file.

<details>
<summary>Hint</summary>

Place the narrow rule under data/**.

</details>

<details>
<summary>Answer</summary>

Use integer cents in CLAUDE.md. In the data rule, require stable unique fixture IDs.

</details>

### Exercise P13.2 (LO-13.2, ★★, about 15 minutes)

The same test review happens on every label change. Which steps belong in the skill and which can you delegate?

<details>
<summary>Hint</summary>

Give a subagent a bounded question.

</details>

<details>
<summary>Answer</summary>

Put process and output in the skill. Delegate checking coverage for both separators. Keep the decision about accepting the patch with the main task.

</details>

### Exercise P13.3 (LO-13.3, ★★, about 15 minutes)

Name three inputs for a deny-only hook and their expected output.

<details>
<summary>Hint</summary>

Include malformed input.

</details>

<details>
<summary>Answer</summary>

The exact test event gives no decision. An unfamiliar command and malformed JSON each get deny.

</details>

### Exercise P13.4 (LO-13.3, ★★★, about 25 minutes)

A Bash hook is installed. Are all edits to a Markdown file covered?

<details>
<summary>Hint</summary>

Think about which tool triggers the event matcher.

</details>

<details>
<summary>Answer</summary>

The matcher covers Bash. An edit tool has its own permissions. Review both layers and use a dedicated rule where needed.

</details>
