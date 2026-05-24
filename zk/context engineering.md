---
UID: Z202507132358000
public: true
---
There's a popular idea right now (Summer 2025) that "context engineering" is an important skill/practice. This is the idea that it's important to manage the context that's given to an LLM/agent/interaction, so that it's maximally-rich yet minimally-massive, so that the AI can get the best results without flooding context unneccessarily.

This is a form of [layered complexity](Abstractions%20AKA%20layered%20complexity.html)! If I've got an AI helping me with some task, and I want to [give it access to e.g. my ZK re: some topic](ZK%20in%20Markdown%20is%20accessible%20to%20LLMs.html), I probably don't want to give it access to the whole thing. Instead, I should (and the context-engineering literature definitely talks about this) [summarize/condense the relevant Zettel](zk-is-a-conversation-it-is-emergent.html), and feed that to the AI instead. Or, maybe it follows [a UID](Lightweight%20UIDs%20for%20linking%20into%20ZK.html).

The first is an example of building a higher-level (== lossy) abstraction; the second of metadata.

[Jeff Bay characterized this well: "waste context on every turn rebuilding . . . world knowledge"](Re-integrating%20context.html)