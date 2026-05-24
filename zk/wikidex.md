---
UID: Z202605121716001
public: true
---
# Wikidex: a thin meta-index for agent-discoverable wikis

A lightweight, harness-portable convention for pointing AI agents at on-disk wikis. Inspired by [skills-should-be-thin](skills-should-be-thin.html) — the index is the routing, the wiki is the content.

## Goal

Two components:

- **(a) Bootstrap** — tell the agent where the meta-index lives and how to add `topic → path` entries.
- **(b) Trigger** — get the agent to consult the index when domain context would help, without per-harness skill machinery.

Must replicate trivially across Claude Code, Codex, Gemini, Cursor, and non-coding agents.

## Prior art

- **[llms.txt](https://llmstxt.org/)** — proposed standard: a small markdown file at a well-known root path listing curated links to documentation pages. The index is small enough to load upfront; agents fetch linked pages selectively. Adopted by Anthropic, Vercel, Stripe, Cloudflare, Cursor.
- **[AGENTS.md](https://benjamincrozat.com/agents-md)** — Linux-Foundation-stewarded convention auto-loaded by Codex, Cursor, and Gemini at repo root. Claude Code reads `CLAUDE.md`; the standard workaround is `ln -s AGENTS.md CLAUDE.md` (issue [#34235](https://github.com/anthropics/claude-code/issues/34235) tracks native support).

Wikidex sits between these: llms.txt's *shape* (tiny markdown index of links + hooks), AGENTS.md's *carrier* (auto-loaded root context file).

## Design

### (a) Bootstrap

Either:
1. Inline a `## Wikis` section directly inside `AGENTS.md`, or
2. Add one line to `AGENTS.md`: `When you need domain knowledge, read ./WIKIDEX.md first.`

To add an entry, append one line:

```markdown
- [topic](path/to/wiki.html) — specific one-line hook
```

That is the entire skill. Adding entries needs no tooling.

### (b) Trigger

Don't make "should I enter the wikidex?" a decision the agent has to reason about. Keep the index small enough (≤30–50 short lines) to live in always-on context via AGENTS.md/CLAUDE.md. The agent's normal relevance-matching fires when a topic hook resonates with the user's request. The only lever is **hook quality**.

- Bad: `kubernetes.md — k8s stuff`
- Good: `wikis/k8s/logging.md — Splunk field schema for K8s ingress + nginx labels, status_code buckets`

This is the same authoring discipline as a good CLAUDE.md ([HumanLayer's guide](https://www.humanlayer.dev/blog/writing-a-good-claude-md)).

### Link format: markdown, not @-mentions or k:v

- **`@path` auto-expands** in Claude Code, Cursor, and Codex when it appears in always-on context. Using `@` in the index would inline every wiki and rebuild llms-full.txt by accident — opposite of the goal.
- **`topic: path` k:v** drops the hook. Without the one-line description the agent has to open files speculatively.
- **Markdown `- [topic](path) — hook`** matches the llms.txt convention agents have already been trained on. Free behavioral prior.

## Tradeoffs

- **Hook drift is the real cost.** Format is trivial; keeping hooks specific and current is the ongoing investment.
- **Size cliff.** Codex truncates past `project_doc_max_bytes`; ≥500-line context files lose instruction-following. If wikidex outgrows that, shard recursively (top-level index → domain sub-indices), mirroring llms.txt → llms-full.txt.
- **Cross-harness portability is mostly free** if AGENTS.md is the carrier and a `CLAUDE.md → AGENTS.md` symlink covers Claude Code until native support ships.
- **Non-coding agents** that don't auto-load AGENTS.md need one bootstrap line in their system prompt: "consult `~/path/to/WIKIDEX.md` when domain context might help." Irreducible per-harness cost.

## Minimum viable shipment

1. `WIKIDEX.md` at a well-known path with a handful of `- [topic](path) — hook` entries.
2. One pointer line in `AGENTS.md`.
3. A one-sentence skill: "to add an entry, append `- [topic](path) — specific hook` to WIKIDEX.md."

Skill stays thin; hooks are the product.

## See also

- [Wikidex shadow indexing](Wikidex%20shadow%20indexing.html) — the pattern for routing into a wiki you don't control
- [MCP and the wikidex stack](MCP%20and%20the%20wikidex%20stack.html) — how MCP fits as the typed-action layer alongside wikidex
