# Module 12: Prompting a coding agent

**Objectives** LO-12.1, LO-12.2, LO-12.3  
**Prerequisites** Module 9  
**Time** About 6 hours across this reading, [Lab 12](lab12.ipynb),
and [practice](practice.md).

## Read a session as a sequence

A coding agent uses an interaction loop in which a model can propose a tool call and
the host decides whether to run it. The result returns to the conversation as input
to later decisions. In a real project, context can include the current task, project
instructions, files read through tools, earlier messages, and environment details.
In the lab, a simplified session stores an event type, an origin, and a short note.
This format belongs to PE101. Review the sequence as a human decision record.

In the illustrated repair-shop session, the user asks for hyphens in service labels.
The agent reads code and tests, notices the underscore behavior, and tries a new test.
A failing test establishes the current symptom. The later passing result is a report
about what the example ran. Review the change and rerun an appropriate command yourself.

## Specify both the goal and the check

“Make labels nicer” gives almost no boundaries. A better task names the issue and the
working files:

> In repair_shop.py, let service_label turn hyphens into spaces alongside underscores.
> Keep Title Case and preserve existing price and estimate behavior. Add a hyphen case
> to test_repair_shop.py and run python -m unittest discover -v. Report the result and
> changed files.

Score the prompt with the [prompt rubric](../../prompt-rubric.md). Include a concrete
example, such as `"brake-adjustment" → "Brake Adjustment"`, if the output is ambiguous.
When requirements conflict, ask the agent to describe the conflict before editing.

## Review the difference

Review the change file by file. First check that every changed area serves the task.
Then verify behavior and edge cases against independent tests. A narrow change that
adds hyphen support but removes underscore support fails a regression requirement. A
change that also alters invoice totals exceeds the requested scope. Tests and manual
review catch different things. A passing existing suite can still fail to exercise
a new requirement.

Keep validation results distinct from claims in a session transcript. The test output
you produce in the lab concerns a local copy of the starter shop. The example transcript
demonstrates which information you would expect to see in a real run.

## Summary

Read the event sequence, write a verifiable task, and compare the proposed edits with both the requirements and tests.

## Self-check

**LO-12.1.** Where did the agent learn underscore labels already worked?

<details>
<summary>Answer</summary>

From reading the code and tests through a tool.

</details>

**LO-12.2.** What makes the task verifiable?

<details>
<summary>Answer</summary>

A concrete change, the expected example, a regression constraint, and a test command.

</details>

**LO-12.3.** The code handles both separators but also changes prices. Do you accept it?

<details>
<summary>Answer</summary>

Request a revision or isolate the label change. Prices are out of scope.

</details>

## Further reading

- [Claude Code overview](https://code.claude.com/docs/en/overview) describes the coding agent and its context.
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) discusses scoped tasks and giving the agent a way to verify work.

Next, open [Lab 12](lab12.ipynb) and then [practice](practice.md).
