# Prompt rubric

Use this rubric for a first draft, a revision, or a coding-agent task. Score each criterion
independently from 0 to 2. Quote a few words from your prompt as evidence and revise the
lowest-scoring criterion first. The total is out of 10. A high score records a clear
specification. Measuring a live model's performance would require an evaluation.

| Criterion | 0 | 1 | 2 |
| :- | :- | :- | :- |
| Task | The requested action is missing | The action is clear but its scope is implicit | The action and scope are both explicit |
| Audience and purpose | Both are absent | One is present | Both are named and affect the requested answer |
| Context | Critical input is missing | Some inputs are supplied | All necessary inputs and their roles are supplied |
| Constraints | The prompt leaves material choices implicit | It states some boundaries | It covers the important limits and unresolved cases |
| Output and success | The expected result is unclear | The format or a success check is specified | Both are specified and can be checked |

For coding tasks, treat **context** as the relevant files and observed behavior. Under
**output and success**, name a verification command and the expected behavior.
