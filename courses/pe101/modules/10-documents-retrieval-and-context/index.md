# Module 10: Documents, retrieval, and context

**Objectives** LO-10.1, LO-10.2, LO-10.3, LO-10.4  
**Prerequisites** Module 7 and 8  
**Time** About 8 hours across this reading, [Lab 10](lab10.ipynb),
and [practice](practice.md).

## Start from evidence

A grounded answer is supported by the supplied sources. Give each section a stable ID.
Place the document blocks before the task and the question. Ask for the section ID and a
verbatim quotation supporting the answer. Allow “I don't know” when the supplied sources
cannot answer. Anthropic documents built-in citations for supported document inputs. The
course uses a simpler local quotation checker to make the evidence boundary visible.

For “How many loan bicycles are available?”, cite H04 and quote “The shop has two loan
bicycles.” Check that the quoted text occurs in the retrieved H04 section. A real quote
from H04 about the loan form still fails to support the answer about the number. Exact
match verifies provenance. A separate judgment checks whether the quote supports the claim.

## Retrieve with BM25

Search ranks documents for the question before composing an answer. BM25 gives more
weight to words that occur in fewer documents, limits the benefit of repetition, and
adjusts for document length. Here $N$ is the number of documents, $df$ is the number
containing a query term, $tf$ is its count in one document, and $L/\bar L$ is document
length divided by average length. Count each distinct query word once.

For a term, multiply its inverse document frequency
$\log(1 + (N-df+0.5)/(df+0.5))$ by
$tf(k_1+1)/(tf + k_1(1-b+bL/\bar L))$. Sum over terms present in the document.
The lab uses $k_1=1.2$ and $b=0.75$. For $N=10$, $df=1$, $tf=1$, and an average-length
section, the frequency factor is one and the term adds about 1.99. Break ties by ID.

## Measure retrieval before answers

Recall at k is the share of labeled relevant sections in the first k results. If a
question needs H03 and H04 and the first two results contain only H04, recall at 2 is 0.5.
The mean of these fractions describes the labeled questions. Separately report the share
with every required section retrieved. With a system that must quote all required evidence,
that full-coverage share is an upper bound on correct fully supported answers. Mean recall
alone does not establish answer accuracy. A retrieved section can also distract the reader.

## Price repeated context

Keep stable policy and documents ahead of per-request text. A cache hit requires a
matching prefix and an eligible cache window. The dated price fixture distinguishes the
input rate, a five-minute cache write rate, and a cache read rate. For $n$ identical
prefix uses, budget one write and $n-1$ reads in the all-hit scenario. Charge the
uncached suffix each time. Compare a second scenario with misses if requests are spread
out or the document changes. Check model-specific minimum cache sizes before relying
on the savings outside the lab.

## Summary

Retrieve relevant sections, track evidence coverage, verify quotations, and compute caching scenarios.

## Self-check

**LO-10.1.** Where does the final question go?

<details>
<summary>Answer</summary>

After the tagged documents and instructions.

</details>

**LO-10.2.** Two sections are required. Only one is in the first four. What is recall at 4?

<details>
<summary>Answer</summary>

0.5. Full coverage for that question is zero.

</details>

**LO-10.3.** A quote exists in the section. Does that establish the claim?

<details>
<summary>Answer</summary>

No. Check whether the quote supports the claim and whether required evidence was omitted.

</details>

**LO-10.4.** What gets charged on a cache hit?

<details>
<summary>Answer</summary>

The matching prefix at the cache read rate and the rest at its applicable rate.

</details>

## Further reading

- [Robertson and Zaragoza (2009)](https://doi.org/10.1561/1500000019) develops BM25.
- [Liu et al. (2024)](https://aclanthology.org/2024.tacl-1.9/) measures position effects in long contexts.
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) describes the cache boundary and costs.
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations) shows the API's citation format.
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) discusses quotations and abstention.

Next, open [Lab 10](lab10.ipynb) and then [practice](practice.md).
