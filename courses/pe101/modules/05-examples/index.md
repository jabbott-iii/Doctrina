# Module 5: Examples

**Objectives** LO-5.1, LO-5.2, LO-5.3  
**Prerequisites** Module 4  
**Time** About 6 hours across this reading, [Lab 5](lab05.ipynb),
and [practice](practice.md).

## Teach a contract with demonstrations

In few-shot prompting, a request includes examples of an input and its desired output.
A zero-shot request supplies instructions without demonstrations. Brown and colleagues
use the terms to distinguish how much task-specific example information is in context.

A useful pair for routing is `My brake pulls left → Label: repair` and
`I need the brake repair receipt → Label: billing`. Both contain “brake.” The second one
teaches the boundary between a repair and a receipt better than an unrelated payment
example. Put each pair in its own example block with separate input and output tags.
Reserve a distinct input block for the actual ticket.

## Check coverage before adding volume

A pool of twenty examples can still omit account cases or requests with two topics.
Count labels and measure an input property such as word count. Then inspect coverage
at the decision boundary. A pool containing “please” only in billing examples may
suggest an accidental rule. Replace or supplement those cases with matched contrasts
from more than one queue.

Min and colleagues showed that demonstration format and input distribution mattered
in the tasks they studied. Zhao and colleagues observed sensitivity to example choice
and order. Their findings motivate checks for transfer to new wording and for the
effect of rotating example order while holding the set fixed.

## Choose examples per request

A fixed set is easy to review and keeps the prompt prefix stable. A dynamic set can
include an example close to a rare input. Start with words as sets. Jaccard similarity
is the number of words the two sets share divided by the number in their union.
For “repair chain” and “chain skips,” the shared set has one word and the union has
three. The similarity is one third. Sort by decreasing similarity, and break ties by
a stable identifier so that replay picks the same examples.

A nearest-neighbor policy can return only one queue. Inspect how much of the label
space your choices cover and try a policy that reserves slots for contrast cases.
Token costs rise as you add examples. Evaluate choices on cases held apart from the pool.

## Summary

Write contrastive demonstrations, measure their coverage, and choose between a fixed set and similarity-based selection.

## Self-check

**LO-5.1.** What makes a brake receipt a useful example?

<details>
<summary>Answer</summary>

It shares repair vocabulary while requesting a billing action.

</details>

**LO-5.2.** Every account example begins with “Hi.” How do you test a shortcut based on the greeting?

<details>
<summary>Answer</summary>

Try account tickets without that greeting and repair and billing tickets with it.

</details>

**LO-5.3.** What is the Jaccard score for two identical nonempty word sets?

<details>
<summary>Answer</summary>

One. Their intersection equals their union.

</details>

## Further reading

- [Brown et al. (2020)](https://arxiv.org/abs/2005.14165) defines zero-shot and few-shot settings.
- [Min et al. (2022)](https://aclanthology.org/2022.emnlp-main.759/) analyzes input distributions and demonstration format.
- [Zhao et al. (2021)](https://proceedings.mlr.press/v139/zhao21c.html) measures sensitivity to demonstration choice and order.

Next, open [Lab 5](lab05.ipynb) and then [practice](practice.md).
