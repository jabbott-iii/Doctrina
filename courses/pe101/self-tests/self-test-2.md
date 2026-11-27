# Self-test 2: Techniques and measurement


This self-test covers Modules 1–8. Set aside about two hours. Use paper or a local text
editor and close the notes for your first attempt. Try every question before opening the
answers. Give yourself 2 points for a complete, justified answer, 1 for a correct start
with a material omission, and 0 for an incorrect or missing answer. The total is
22 points for your own review.


## Question S2.1 (LO-2.2, LO-3.3)

A label reply contains a second line of explanation. Why could that increase cost and fail even if the label is right?

<details>
<summary>Answer and scoring notes</summary>

Extra tokens increase output cost. The one-line format and the label require separate checks.

</details>

## Question S2.2 (LO-4.2, LO-5.1)

Draft two examples with the word 'brake' and different labels. Where do they go?

<details>
<summary>Answer and scoring notes</summary>

A brake fault is repair and a brake receipt is billing. Put both in tagged demonstrations separate from the current input.

</details>

## Question S2.3 (LO-5.2, LO-5.3)

The query has terms {chain, price}. Compare candidates {chain, price, tax} and {chain, skips}. Which ranks first under Jaccard? Which test detects a shortcut on the word chain?

<details>
<summary>Answer and scoring notes</summary>

The scores are 2/3 and 1/3. Add a chain fault and a chain receipt to check whether the model relies on a shared word instead of the request.

</details>

## Question S2.4 (LO-6.1)

Three effort levels reach accuracy 85%, 92%, and 94% at median 1.2, 2.0, and 3.4 seconds. Which levels qualify for at least 90% in at most 2.5 seconds?

<details>
<summary>Answer and scoring notes</summary>

Only the second level.

</details>

## Question S2.5 (LO-6.2, LO-6.3)

A two-stage chain has conditional success 0.9 and 0.8. A validator observes two answer tags. Calculate all-correct probability and say how the validator handles that output.

<details>
<summary>Answer and scoring notes</summary>

0.72. The validator reports an ambiguous answer and refuses to silently use either tag.

</details>

## Question S2.6 (LO-7.1, LO-7.4)

Write one typical and one misleading ticket with an expected label. Which split can drive a template change?

<details>
<summary>Answer and scoring notes</summary>

A flat tire routes to repair. A brake repair receipt routes to billing. Use development cases to revise and reserve holdout.

</details>

## Question S2.7 (LO-7.2)

Two annotators agree on 9 of 10 items. Their pass shares are 0.8 and 0.7. Find chance agreement and kappa.

<details>
<summary>Answer and scoring notes</summary>

Chance is 0.8 × 0.7 + 0.2 × 0.3 = 0.62. Kappa is 0.28/0.38, about 0.737.

</details>

## Question S2.8 (LO-7.3)

A case score is 1/3 for A and 2/3 for B. What difference enters the paired bootstrap? When can you use a Wilson interval?

<details>
<summary>Answer and scoring notes</summary>

The difference is +1/3. Use Wilson for independent binary indicators, such as one designated run per independently sampled case.

</details>

## Question S2.9 (LO-8.1, LO-8.2)

A JSON object contains queue=shipping and summary='Flat tire'. What should a schema check? Define a read-only tool to find service availability.

<details>
<summary>Answer and scoring notes</summary>

The queue enum should reject shipping. Define a named availability tool with a required service string and explicit error behavior.

</details>

## Question S2.10 (LO-8.3)

The tool call for price fails and the one for hours succeeds. What goes back in the next turn?

<details>
<summary>Answer and scoring notes</summary>

A user turn with both tool results, including the price error flag and the original proposal IDs.

</details>

## Question S2.11 (LO-1.2, LO-1.3)

A context window clips a routing example. How can that change a comparison of two prompts? Why can repeated sampling still vary?

<details>
<summary>Answer and scoring notes</summary>

Check that both prompts still receive the same intended instructions and demonstrations after trimming. A next-token sampler can choose different tokens from the same distribution.

</details>

## Decide what to review

Revisit every module where you lost a point. Redo one lab check and one practice exercise
with a changed input, then explain why the expected result changes. A missing unit,
unstated assumption, or skipped validation condition is worth correcting in your notes.
