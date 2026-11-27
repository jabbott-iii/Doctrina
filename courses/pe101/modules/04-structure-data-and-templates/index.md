# Module 4: Structure, data, and templates

**Objectives** LO-4.1, LO-4.2, LO-4.3  
**Prerequisites** Module 3  
**Time** About 6 hours across this reading, [Lab 4](lab04.ipynb),
and [practice](practice.md).

## Make the parts visible

You can put a long document first, mark the start and end of each document, and place the
instructions and final question after the documents. A reader can then tell which text to
interpret as a source and which sentence states the task. Anthropic recommends this order
for long-context prompts. Short requests can often use a few headings instead.

A dispatch prompt might contain `<ticket>`, `<instructions>`, and `<question>` inside a
container named `<dispatch>`. A queue definition belongs under instructions. A line in
the ticket that resembles a queue definition still belongs under ticket. Use the same tag
names across the template, examples, and tests.

## Escape text at the boundary

A literal `&` in a text node can start an entity reference. A literal `<` can start
markup. If you concatenate `<ticket>`, the value `Pads & cables < 20`, and `</ticket>`,
the XML parser raises an error. Encode the value as `Pads &amp; cables &lt; 20` and parse
the resulting element to recover the original text. Escape fields when inserting them.
Escaping the whole template would turn the structural tags into text.

Read an XML template once and declare how its variables work. This course inserts variable
values into **text nodes** only. In an XML attribute, quotes also need handling. Prefer
the serializer for that case. Use `Template.substitute` so that a missing field raises an
error. Passing a dictionary of strings also ensures a literal `$amount` in a field stays
literal because substitution runs once.

## Keep the prompt in a versioned file

Store drafts as text, name each version, and compare the files with a line diff before
updating the version used by an evaluation. Suppose you move queue definitions from a
ticket template to system policy. A diff can tell you exactly which strings moved. Record
why that movement is useful, then rerun the same evaluation cases to see what changed.

## Know what the parser proves

Successful parsing shows that the text conforms to the XML parser's grammar. A fresh
parse plus a field round trip proves that a particular value stays in the intended node.
Neither result establishes how a model interprets the words it receives. Keep permissions
and side-effect checks in the application.

## Summary

Use stable tag names, escape values when inserting them, reject missing variables, and compare changes in versioned text.

## Self-check

**LO-4.1.** Where does the final question go when the prompt contains a long collection of documents?

<details>
<summary>Answer</summary>

After the document collection and the task instructions.

</details>

**LO-4.2.** What should a parser recover after you insert Cables & pads?

<details>
<summary>Answer</summary>

It should recover the original string, including the literal ampersand.

</details>

**LO-4.3.** What should happen when the template needs a question and the values lack it?

<details>
<summary>Answer</summary>

Rendering should fail so the caller can supply the required field.

</details>

## Further reading

- [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) explains XML tags and long-context ordering.

Next, open [Lab 4](lab04.ipynb) and then [practice](practice.md).
