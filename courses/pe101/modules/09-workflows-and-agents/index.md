# Module 9: Workflows and agents

**Objectives** LO-9.1, LO-9.2, LO-9.3  
**Prerequisites** Module 8  
**Time** About 7 hours across this reading, [Lab 9](lab09.ipynb),
and [practice](practice.md).

## Pick a control structure

A single call suits a narrowly specified task. A workflow is application code that
chooses the sequence of steps. An agent lets a model choose some next steps, often
through tool proposals, inside an application loop. Compare the expected gain with
latency, cost, and the impact of a wrong action. In this module all actions read
fictional shop fixtures.

## Four workflow patterns

| Pattern | Who decides the next step | Bicycle-shop example | What to check |
| :- | :- | :- | :- |
| Routing | A routing decision picks a known branch | Send a receipt to the billing writer | Unknown routes fail explicitly |
| Parallel calls | The application schedules independent tasks | Price parts and estimate labor | Results retain the job keys |
| Orchestrator and workers | A planner proposes subtasks | Pick known tasks for a mixed repair ticket | Reject unknown jobs before calling workers |
| Evaluator and optimizer | A check accepts or gives revision feedback | Ask for a clearer receipt reply | Cap the number of drafts |

For parts and labor, keep the two results keyed by job. The notebook uses an isolated
one-item script for each branch. Submitting those independent jobs to two workers
allows overlap. A fixed sequence gives the same data flow if there is no need for overlap.

In an orchestrator, the planner returns a list of job IDs. Parse and check that list
before creating work. In an evaluator loop, pass the review to the next draft and stop
when the review says pass. Repeated retries can amplify a bad grader's decisions, so
budget revisions and spot-check approvals.

## Bound and inspect steps

Reserve a known upper bound before a model call and record actual usage after it. In
this lab one credit equals one output token and the budget excludes input. A real cost
cap must also reserve input and other billed components. If 3 credits remain and the
next call might use 4, stop before calling it. The separate turn cap bounds a loop that
uses few credits each turn.

Log the turn, selected tool names, stop reason, and actual charges. A log that records
“tool_use, end_turn” tells you the exchange took two turns. It does not establish that
the answer or tool selection was right. Test the decisions and the failure transitions.

## Summary

Prefer the smallest sufficient design and bound both the number and the cost of delegated steps.

## Self-check

**LO-9.1.** Which pattern suits independent price and labor lookups?

<details>
<summary>Answer</summary>

Parallel calls or sequential execution of independent branches, keyed by lookup.

</details>

**LO-9.2.** What happens when spend is 4, reserve is 3, and the total budget is 6?

<details>
<summary>Answer</summary>

The next call would exceed the remaining budget, so it is skipped.

</details>

**LO-9.3.** Would you give a model control over queue routing for three well-defined labels and no tools?

<details>
<summary>Answer</summary>

One classified call or deterministic code can handle this scope. A loop adds cost and more failure states.

</details>

## Further reading

- [Building effective agents](https://www.anthropic.com/research/building-effective-agents) distinguishes workflows from agents and describes each pattern.
- [Yao et al. (2023)](https://arxiv.org/abs/2210.03629) studies alternating reasoning and actions.

Next, open [Lab 9](lab09.ipynb) and then [practice](practice.md).
