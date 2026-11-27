# Module 8: Structured output and tools

**Objectives** LO-8.1, LO-8.2, LO-8.3  
**Prerequisites** Module 7  
**Time** About 7 hours across this reading, [Lab 8](lab08.ipynb),
and [practice](practice.md).

## Specify a record with a schema

A JSON parser checks syntax. A JSON Schema validator checks an instance against a declared
structure. A record can parse as JSON and still omit an expected field, supply the wrong
type, or use a value outside an enumerated set.

For a dispatch record, require a queue from the three known labels and a string summary.
Set `additionalProperties` to false to catch unexpected fields. A string that satisfies
the schema can still name the wrong queue or say something unsupported. Check business rules
separately. For example, validate that a summary includes real text after trimming.

Anthropic documents schema-constrained output using `output_config.format` and strict
validation of tool arguments on supported models. The labs validate scripted responses
locally. Handle stop reasons before parsing. A refusal or length cutoff may leave no usable
record. Set a retry budget and preserve the final failure for inspection.

## Design a tool interface

A tool definition supplies a name, description, and input schema. The description tells
the model when to propose the tool. The schema specifies data types and required fields.
`find_service` reads a menu price by service name. `estimate_minutes` reads the workload
for that service. `shop_hours` reads opening hours for a weekday. These tools only read
a local fixture.

Choose names that distinguish the tools and describe what errors mean. An unknown service
is a domain error even if the argument is a valid string. The host validates inputs and
decides whether the proposed action is allowed.

## Trace a client-side tool exchange

1. Send the user message and tool definitions.
2. Check for the `tool_use` stop reason. Keep the assistant's entire content in history.
3. For each tool proposal, validate its inputs, run the known local action, and produce a
   `tool_result` whose `tool_use_id` matches the proposal ID.
4. Send the tool results together in the next user message. Include error results for failed
   calls. Repeat within a turn limit.
5. Return text on `end_turn`. Surface other stop reasons separately.

If the assistant proposes two reads in one turn, return both results before asking it
to continue. Mixing up their IDs associates the price with the wrong proposal. Provider
tool-choice options vary with model and thinking mode. Opus 5.5 returns an HTTP 400 error
for forced tool choice with type `any` or `tool`. Use `auto` and tell the model when
each tool applies. The host still validates each proposal it receives.

## Summary

Validate the result and its meaning separately. Preserve tool proposal IDs, errors, and explicit stop reasons.

## Self-check

**LO-8.1.** JSON parses but queue is missing. Which layer catches it?

<details>
<summary>Answer</summary>

JSON Schema when queue appears in the required list.

</details>

**LO-8.2.** Why do service names need a domain check after schema validation?

<details>
<summary>Answer</summary>

The input schema accepts strings. Only names in the fictional menu are known.

</details>

**LO-8.3.** Where do two results for one assistant turn go?

<details>
<summary>Answer</summary>

Together in the next user message, with each tool_use_id copied from its proposal.

</details>

## Further reading

- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) documents output schemas and strict tool use.
- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) describes the client-side tool exchange.
- [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) explains tool descriptions, schemas, and model-specific tool-choice restrictions.
- [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object) explains required and additional properties.

Next, open [Lab 8](lab08.ipynb) and then [practice](practice.md).
