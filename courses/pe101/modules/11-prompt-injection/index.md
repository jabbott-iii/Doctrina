# Module 11: Prompt injection

**Objectives** LO-11.1, LO-11.2, LO-11.3  
**Prerequisites** Module 9 and 10  
**Time** About 7 hours across this reading, [Lab 11](lab11.ipynb),
and [practice](practice.md).

## Trace the trust boundary

Prompt injection occurs when text arriving as data is treated as authoritative
instructions. Direct injection is delivered in a user turn. Indirect injection can
arrive through content the assistant retrieves, such as a document or a tool result.
The difference is the source. In either case the host application has to authorize
the proposed action from a trusted signal.

The lab uses predeclared records that represent these paths. A fixture says where a
proposal came from and which sample display label it would change. A scripted stand-in
passes that proposal through. The host then decides how to handle it. No input string
generates a proposal, and the fixture has no access to files, commands, secrets, or
messages. The outcome “accepted” records a policy decision on an inert label.

## Use multiple controls

**Mark untrusted content.** Store its source and trust status separately. A tag helps
the model and the reader distinguish data from policy. The serializer can preserve the
boundary in the request. A model can still misinterpret text inside it, so the tag
cannot grant or revoke permission.

**Give least privilege.** Run a reader with an allowlist of read operations. Remove
actions that the task does not need. Deny unknown proposals before handling their
arguments. This prevents disallowed action types. An allowed read could still produce
misleading content, and access to private data deserves its own policy.

**Require approval on a permitted state change.** Bind the decision to the current
action and its arguments, and record it with the actor and time. Keep the approval
source outside the model and document text. A review gate can stop an unapproved
change. A reviewer can still make a mistaken decision, so show the relevant evidence.

## Compare policy outcomes

Define success for an undesired action as host acceptance without authorized approval.
Report the denominator and include control cases with legitimate approvals so that a
policy that denies everything cannot pass unnoticed. When an allowed configuration
changes, rerun the matrix. The rate is specific to the predeclared fixtures and their
policy. It does not measure model robustness or a real system's vulnerability.

## Summary

Track where a proposal came from, separate the decision from the model, and measure the defense on fixtures with controls.

## Self-check

**LO-11.1.** A retrieved schedule is the source of an unauthorized proposal. Which boundary is involved?

<details>
<summary>Answer</summary>

Indirect injection is represented because the proposal originates in retrieved data.

</details>

**LO-11.2.** Can a document label itself approved and authorize a change?

<details>
<summary>Answer</summary>

No. Approval must come from the host's trusted record of authorization.

</details>

**LO-11.3.** A policy rejects 25 invalid proposals and one correct control. Is that enough to accept it?

<details>
<summary>Answer</summary>

It blocks the tested invalid proposals but fails the approved control. Record and diagnose both outcomes.

</details>

## Further reading

- [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) distinguishes direct and indirect injection and surveys defenses.
- [Willison (2025)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) discusses how access, untrusted data, and communication combine.

Next, open [Lab 11](lab11.ipynb) and then [practice](practice.md).
