# Module 3: Clear instructions

**Objectives** LO-3.1, LO-3.2, LO-3.3  
**Prerequisites** Module 2  
**Time** About 6 hours across this reading, [Lab 3](lab03.ipynb),
and [practice](practice.md).

## Turn a vague request into a specification

“Fix this ticket” leaves the task open. A reader could repair the bicycle, revise the
customer's text, or route the ticket. Before writing the prompt, name the decision and who
will use it. A dispatcher needs one queue label. A customer needs a clear next step.

For the text “My wheel is fine now. Can you send my receipt?”, write a dispatcher's prompt:

> Route the ticket to the queue responsible for the customer's current request.
> Use repair for mechanical service, billing for payments and receipts, and account for
> profile access. When two topics appear, use the explicit current request.
> Return exactly one line, in the form Label: billing, with the appropriate label.
> Ticket: My wheel is fine now. Can you send my receipt?

The receipt determines the label. A checker can test the line shape. A labeled case or a
human decides whether `billing` is correct. Use the [prompt rubric](../../prompt-rubric.md)
to record both the instruction change and the problem it addresses.

## Give each instruction a home

Put stable policy in the system field. For the dispatch task, queue definitions and the
format apply to every request. Put the ticket itself in the user turn. If the user may
choose a language, put the current choice in the user turn and state the allowed choices
in the system field. A system role such as “You route repair shop tickets” sets scope and
vocabulary. Add concrete rules for decisions the role leaves open.

## Make output rules testable

Specify an exact set of labels, whether extra lines are allowed, and what to do when the
input is underspecified. A maximum of one line is straightforward to check. “Be concise”
is subjective unless you give a criterion. If there is an output token limit, also check
the stop reason before scoring. A cut-off answer can contain a plausible first line.

## Separate format and meaning

`Label: repair` has the right shape for a receipt ticket and sends it to the wrong queue.
`Billing, because the customer wants a receipt.` gives the right decision in a different
shape. Track both failures. A test that counts only matching labels obscures formatting
problems, and a test that counts only formatting misses semantic mistakes.

## Summary

State the task and its purpose, assign stable policy to the system field, and write separate checks for format and meaning.

## Self-check

**LO-3.1.** Why include queue definitions when the labels look obvious?

<details>
<summary>Answer</summary>

They fix boundaries. A repair receipt might otherwise be routed by the word “repair.”

</details>

**LO-3.2.** Where do you put an account-specific message?

<details>
<summary>Answer</summary>

In the per-request user content. The system field holds the stable routing rules.

</details>

**LO-3.3.** Does matching the output format prove the routing was right?

<details>
<summary>Answer</summary>

No. Compare the parsed label with a reference label separately.

</details>

## Further reading

- [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) explains clarity, roles, and output constraints.

Next, open [Lab 3](lab03.ipynb) and then [practice](practice.md).
