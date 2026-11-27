# Capstone: An evaluated prompt package

Build a reusable offline prompt package for a task worth verifying. You can route shop
tickets, answer employee handbook questions with citations, or check a proposed change to
a small program. Choose a narrow task with a stable input and a result that a collaborator
can check. Plan about 20 hours across the proposal, milestone, and final version, at your
own pace.

The course [policies](../../README.md#policies) apply. Keep any published sample data
fictional or your own. Run the evaluation with a scripted stand-in and label every
hand-written reply. Ask a collaborator to follow your run instructions from a fresh clone
or copy, or do the replay yourself in a new directory.

(proposal)=
## Proposal after Module 9

**Objectives** LO-2.2, LO-3.1, LO-7.1, LO-9.3.

Write a one-page proposal. Include the audience and purpose, the input and output contract,
the measurable success criteria, and a rough token and cost budget using a dated price.
Explain why you chose a single request, workflow, or bounded agent. List where untrusted
text enters, what actions the host permits, and which results need human review. Include
one example that should succeed and one that should abstain or fail.

(milestone)=
## Milestone after Module 11

**Objectives** LO-4.2, LO-6.3, LO-7.1, LO-7.2, LO-7.3, LO-7.4, LO-8.1, LO-11.3.

1. Write at least 30 labeled cases with stable IDs. Tag typical, edge, and adversarial
   cases and lock a development and held-out split by case. Related paraphrases should
   stay in one split.
2. Define a code grader for structure and a task grader for result quality. Write a
   judge prompt with rubric examples. Calibrate the grading criteria with at least 20
   hand-written good and flawed responses and independently record your labels before
   applying the graders. Record disagreements and one change inspired by them.
3. Add synthetic trust-boundary fixtures and benign controls. Capture defended and
   baseline outcomes using an inert policy in code. Record what the gate permits and
   what requires trusted approval.
4. Show one result per stage of your pipeline, including an incomplete response or
   validation failure, and demonstrate how the evaluator records it.

(final-version)=
## Final version after Module 13

**Objectives** LO-2.2, LO-3.1, LO-4.2, LO-4.3, LO-6.3, LO-7.1, LO-7.2, LO-7.3, LO-7.4,
LO-8.1, LO-9.3, LO-10.4, LO-11.2, LO-11.3, LO-12.1, LO-12.2, LO-12.3, LO-13.1,
LO-13.2, LO-13.3.

Deliver one repository or folder with the following pieces.

| Piece | What to include |
| :- | :- |
| README and run command | Setup, exact offline run command, expected files or output, assumptions, and tools used |
| Prompt files | Three versions with a change rationale and a case that explains each revision |
| Data | At least 30 labeled cases with split metadata and at least 20 labeled sample responses |
| Evaluation | Code graders, a judge prompt, schema, replay fixture setup, and a reproducible report |
| Cost | A dated per-request and batch estimate with uncached and cached scenarios |
| Policy | Allowlist, approval boundary, and positive and negative fixture checks |
| Agent configuration | CLAUDE.md, one path-scoped rule, one skill, and a deny-only hook with piped JSON tests |
| Review | Two coding-agent task prompts, one annotated diff, and the offline checks you ran |

Use the development cases to compare versions and choose one. Make a single held-out
report using the chosen version and a fixed baseline. Give denominators, uncertainty
measures that match the sample unit, and at least one worked failure. Describe which
properties you measured on fixtures and which require an evaluation with model outputs.
Include a method to trace each stage and a stable record of the versions and costs.
Paper designs for future live adapters can share the stand-in's request interface.

## Self-assessment rubric

Score each row 0, 1, or 2, for a total of 14. Before considering a package complete,
rerun any check with a missing result. Use the direct evidence in the two-point column
when deciding whether to award full credit.

| Criterion | 0 | 1 | 2 |
| :- | :- | :- | :- |
| Task and control flow | No measurable outcome | Contract or control flow is underspecified | Observable outcome, bounded flow, and evidence for the design choice |
| Versioned prompts | One prompt or no stable files | Versions exist with little rationale | Three versions with meaningful diffs, structure checks, and case-linked reasoning |
| Cases and graders | Unlabeled or missing tests | Partial case coverage or uncalibrated grader | Required labeled cases and replies, separate holdout, and checked grading criteria |
| Evaluation replay | Cannot run | Runs with incomplete reporting | One offline command reproduces case counts, comparison, failures, and uncertainty |
| Cost | Absent | Estimate without units, dates, or cache assumptions | Dated input and output rates, cache assumptions, and comparable batch costs |
| Policy and defenses | No trust boundary | A boundary is stated without both control types | Least privilege, host approval, and measured outcomes for negative and positive fixtures |
| Configuration and review | No usable configuration | Partial config or check record | Instructions, scoped rule, skill, verified hook, two task prompts, and annotated diff |

Write your score with one evidence pointer per row. End the capstone README with the
academic-integrity note described in the syllabus.
