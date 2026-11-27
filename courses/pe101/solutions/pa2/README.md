# PA2 answer key

## Model prompt notes

**Routing.** Use one user turn for the ticket. The model version in the notebook's solution
spells out the queue names, the current request rule, and the output form. A prompt that
starts “Sort this” earns 1/10 before context and constraints are added. The revision earns
10/10 on the rubric with “for the dispatcher” as the audience and queue routing as its purpose.

**Receipt reply.** “For a customer who asked about a receipt, acknowledge the request in one
line of at most 20 words. Ask for the invoice reference if it is missing. Avoid promises.”
This states the fallback, format, audience, and scope. Add the original ticket to earn full
context credit.

**Profile change.** “For an account clerk, extract the requested profile field from the
ticket. Return exactly Field: email, Field: address, or Field: unknown. Use unknown for a
missing or ambiguous request.” Save the draft and revision separately and use a line diff
to point to the new fallback.
