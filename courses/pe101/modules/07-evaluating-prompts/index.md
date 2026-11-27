# Module 7: Evaluating prompts

**Objectives** LO-7.1, LO-7.2, LO-7.3, LO-7.4  
**Prerequisites** Module 6  
**Time** About 8 hours across this reading, [Lab 7](lab07.ipynb),
and [practice](practice.md).

## Define success in observable terms

For the bicycle dispatcher, a pass requires a single recognized label that matches the
queue defined by the active request. A **test case** contains a ticket, an expected
label, and metadata such as category and split. Include typical requests, edge cases
with two topics, and cases with misleading surface cues. An evaluation runs those
cases and applies a grader to the outputs.

For “My brake repair is complete. Please resend the receipt,” mark billing as the
expected label and store “active request is a receipt” as the annotation rule. A
grader should record a wrong label separately from a missing format. Use a threshold
set before inspecting the final evaluation. Then examine failures by case class.

## Calibrate a grader

A code grader can verify label strings or shapes. For qualities like whether a reply
acknowledges a customer's concern, start with a rubric and human labels. A model-based
grader can apply a similar rubric, though agreement must be measured. Include examples
of each score, blind the grader to which prompt produced the answer, and spot-check
disagreements. A judge that rates longer answers more highly can prefer extra words
over the actual requirement.

For binary pass labels, observed agreement is the share of item pairs that match.
Chance agreement from the graders' margins is $p q + (1-p)(1-q)$, where p and q
are the fractions each grader passes. Cohen's kappa is the observed agreement minus
chance agreement, divided by one minus chance agreement. If everyone gives the same
constant label, the denominator is zero. Report the raw agreement and mark kappa
undefined. Review disagreements even if overall agreement is high.

## Quantify variation

For $s$ passes in $n$ independent binary trials, the observed rate is $s/n$.
The Wilson interval centers on $(s/n + z^2/(2n)) / (1+z^2/n)$ and adds or subtracts
$z\sqrt{(s/n)(1-s/n)/n+z^2/(4n^2)}/(1+z^2/n)$. For 8 of 10, a 95% interval using
$z=1.96$ is about 0.49 to 0.94. A Wilson interval assumes independent Bernoulli
outcomes. If a case has three repeated calls, the responses share the same input.
Show the run-level pass rate and use case-level resampling for comparisons.

Compare A and B on the same cases. Compute each case's average success over its runs
for A and for B. Subtract A from B within each case, then resample those case
differences with replacement. The center of the original differences estimates the
change, and the sorted resamples approximate its uncertainty. Preserve whole cases so
a hard case that affects both prompts stays paired.

## Protect the held-out cases

Pick a development split to study and revise. Keep a held-out split for a final check.
If you change the prompt after seeing a test error, the test set has effectively
become development data. Collect fresh cases before claiming a final comparison.
A large gain on a small hand-written fixture set teaches how a grader responds to
that set. A live evaluation would be needed to estimate model behavior.

## Summary

Define the observable pass condition, calibrate judges, quantify uncertainty, and reserve cases for the final comparison.

## Self-check

**LO-7.1.** What should you store about a two-topic case?

<details>
<summary>Answer</summary>

Store the text, expected label, applicable priority rule, case category, and split.

</details>

**LO-7.2.** What does high observed agreement with both graders always passing say about kappa?

<details>
<summary>Answer</summary>

Kappa is undefined because chance agreement is also one.

</details>

**LO-7.3.** What is the sample unit for the paired bootstrap?

<details>
<summary>Answer</summary>

The test case, including scores for both prompts and all repeated runs.

</details>

**LO-7.4.** When does a held-out case become development data?

<details>
<summary>Answer</summary>

As soon as you use its result to choose or revise the prompt.

</details>

## Further reading

- [Develop tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) describes success criteria and evaluation design.
- [Cohen (1960)](https://journals.sagepub.com/doi/10.1177/001316446002000104) defines kappa.
- [Wilson (1927)](https://www.jstor.org/stable/2276774) derives the score interval.
- [Zheng et al. (2023)](https://arxiv.org/abs/2306.05685) discusses judge agreement and biases.

Next, open [Lab 7](lab07.ipynb) and then [practice](practice.md).
