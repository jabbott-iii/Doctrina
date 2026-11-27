# Self-test 1: Foundations


This self-test covers Modules 1–4. Set aside about two hours. Use paper or a local text
editor and close the notes for your first attempt. Try every question before opening the
answers. Give yourself 2 points for a complete, justified answer, 1 for a correct start
with a material omission, and 0 for an incorrect or missing answer. The total is
16 points for your own review.


## Question S1.1 (LO-1.1)

A tokenizer sees `p a d` three times and `p a` once. Which adjacent pair appears most often? Why might a different corpus choose another first merge?

<details>
<summary>Answer and scoring notes</summary>

The pair p a has four counts and a d has three. A different corpus changes the pair counts.

</details>

## Question S1.2 (LO-1.2, LO-1.3)

A next-token distribution gives A probability 0.8 and B 0.2. With top-p 0.75, which survives? What happens to the larger mass when temperature falls below one?

<details>
<summary>Answer and scoring notes</summary>

Only A survives the nucleus cutoff. Lower temperature makes the distribution more concentrated on A.

</details>

## Question S1.3 (LO-1.3, LO-2.3)

A 100-token context has 20 system tokens, needs 25 answer tokens, and has 70 user and history tokens. How many user and history tokens must you remove?

<details>
<summary>Answer and scoring notes</summary>

At least 15. That leaves 55 user and history tokens. Keep the current question and summarize relevant older turns.

</details>

## Question S1.4 (LO-2.1, LO-2.2)

Give the roles in a request with one previous exchange and a new question. Input costs $4 and output $20 per million. Compute the charge for 500 input and 50 output tokens.

<details>
<summary>Answer and scoring notes</summary>

user, assistant, user. The system field is separate. The cost is $0.002 + $0.001 = $0.003.

</details>

## Question S1.5 (LO-2.4)

A reply stops at max_tokens and its first line has the correct label. How should the consumer report it?

<details>
<summary>Answer and scoring notes</summary>

As incomplete. Parse and validate only under an accepted terminal status.

</details>

## Question S1.6 (LO-3.1, LO-3.2, LO-3.3)

A dispatcher gets “Sort it.” Rewrite the prompt for a repair receipt and name one success check. Identify what changes between requests.

<details>
<summary>Answer and scoring notes</summary>

Set queue definitions and exact one-line format as system policy. Pass the ticket as user data. Check that the receipt yields exactly Label: billing.

</details>

## Question S1.7 (LO-4.1, LO-4.2)

In a tagged dispatch prompt, the ticket is `Brakes & pads < $20`. Write the encoded value and name how you test it.

<details>
<summary>Answer and scoring notes</summary>

Use `Brakes &amp; pads &lt; $20`. Parse the prompt and verify that the ticket node contains the original value.

</details>

## Question S1.8 (LO-4.3)

A revised template adds a required field named audience. Design one check on the renderer and one on the version history.

<details>
<summary>Answer and scoring notes</summary>

Check missing audience raises an error. Review a diff showing the added field and record the reason for that version.

</details>

## Decide what to review

Revisit every module where you lost a point. Redo one lab check and one practice exercise
with a changed input, then explain why the expected result changes. A missing unit,
unstated assumption, or skipped validation condition is worth correcting in your notes.
