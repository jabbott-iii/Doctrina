# Module 13: Configuring a coding agent

**Objectives** LO-13.1, LO-13.2, LO-13.3  
**Prerequisites** Module 12  
**Time** About 7 hours across this reading, [Lab 13](lab13.ipynb),
and [practice](practice.md).

## Put guidance where it applies

Claude Code reads project instructions from `CLAUDE.md` and supports Markdown rules
under `.claude/rules/`. A rule with a `paths` list is scoped to the files it covers.
Use the main file for facts every task needs, for example that the shop uses integer
cents and has an offline test suite. Use a scoped rule for narrower conventions,
such as a reminder about fixture IDs when working in `data/`. Avoid turning instructions
into an unenforced security boundary.

A minimal scoped rule has YAML front matter with `paths: ["data/**"]` followed by its
Markdown guidance. The lab implements exact path and directory-prefix checks for this
subset. Full Claude Code path matching has additional cases. Test scope examples
against the configuration you intend to maintain.

## Package repeated work

A project skill lives in a folder under `.claude/skills/` and has a `SKILL.md` with
name and description in YAML front matter. Give it a trigger and a clear workflow.
For comparing service-label diffs, give it three checks for scope, regression, and
evidence. Delegate a bounded review of test coverage to a subagent if isolated
context is helpful. Keep product decisions and integration with the main task.

## Use permissions and hooks for enforceable conditions

Permissions can allow, ask about, or deny specified tool operations. A hook is trusted
code triggered by a configured event. A `PreToolUse` hook can examine the JSON
describing a proposal and emit a structured deny decision before a tool runs. This
lab's skill and rules teach expected behavior. A deny-only hook enforces a narrow
local command policy without issuing approvals.

Review hooks before enabling them because a command hook executes code at its configured
event. Here the hook reads standard input and emits a deny decision for anything except
the exact test command. For the expected command it prints nothing, deferring to the
normal permissions and other controls. Its return is neither a security sandbox nor
evidence that a command has run. An incorrect matcher, a different tool, or an inactive
configuration can leave a condition unchecked. Test handler behavior with input events
and verify the effective settings separately.

## Summary

Use scoped guidance, make repeated work a skill, and verify enforceable restrictions with offline events.

## Self-check

**LO-13.1.** Where should the integer-cents convention apply?

<details>
<summary>Answer</summary>

Put it in CLAUDE.md if all changes must follow it. Put fine-grained fixture conventions in a rule scoped to the relevant paths.

</details>

**LO-13.2.** Which part of the diff review is a bounded subagent task?

<details>
<summary>Answer</summary>

Review whether a named diff covers the specified test cases. Keep acceptance with the main task.

</details>

**LO-13.3.** Does an empty hook result authorize a command?

<details>
<summary>Answer</summary>

No. It gives no decision, so the permissions layer and other controls still apply.

</details>

## Further reading

- [How Claude remembers your project](https://code.claude.com/docs/en/memory) explains instruction files and path-scoped rules.
- [Skills](https://code.claude.com/docs/en/skills) covers skill folders and front matter.
- [Subagents](https://code.claude.com/docs/en/sub-agents) describes delegation and separate context.
- [Permissions](https://code.claude.com/docs/en/permissions) and [hooks](https://code.claude.com/docs/en/hooks) describe action decisions and event input.
- [Settings](https://code.claude.com/docs/en/settings) lists where configuration is read and how layers interact.

Next, open [Lab 13](lab13.ipynb) and then [practice](practice.md).
