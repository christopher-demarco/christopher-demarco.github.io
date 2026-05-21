---
UID: Z202605071430000
public: true
---
# Wikidex shadow indexing

A pattern for routing agents into a wiki you don't control: build the index in your *own* notes and link out.

## Context

[Skills Should Be Thin; the Wiki Should Be Fat](skills-should-be-thin.html) argues that organizational knowledge belongs in the wiki, not inlined into agent skills. [Wikidex](wikidex.html) describes the routing layer that makes thin skills viable: a small markdown index of `- [topic](path) — specific hook` entries, loaded into always-on context via `AGENTS.md` / `CLAUDE.md`, that triggers the agent's relevance-matching when a request shape resonates with a hook.

Together they imply a three-layer architecture:

1. **Wiki** — declarative truth (Diátaxis-shaped).
2. **Index hooks** — procedural retrieval; specificity is the entire lever.
3. **Skill** — cognitive rails (operational stance, hypothesis discipline), *not* how-to recipes.

## The shadow-index problem

Both source notes assume you can edit the wiki. What if you can't?

The DRW team wiki (`updocs`) is a VuePress site whose navigation is a clickable gutter tree. There is no markdown index file with hooks suitable for agent retrieval. Adding one would require team buy-in *and* customer-UX consideration, since customers read the same wiki. The social cost of fixing the upstream index is non-trivial; the personal cost of unreliable retrieval is paid every session.

## The pattern

Build the index in a venue you fully control — a personal ZK collection — and have it point into the upstream wiki.

- The index lives in your own notes (e.g. `drw-index.md` in the work ZK).
- Entries point at upstream paths using a stable, repo-relative form (`updocs/path/to/page.md`), so the index is portable if it ever migrates.
- A distinct section header (`## Team wiki (updocs)`) marks provenance — so it's visually obvious which entries point into someone else's content tree vs. native ZK notes.
- Don't bulk-shadow. Index a doc only when a real retrieval needs it. Hooks earn their place by firing.

## The covert-standard upside

A shadow index is not just a workaround. If your agent sessions outperform teammates' because the index routes you reliably into the wiki, the index itself becomes the artifact teammates ask about. Wikidex enters the team via demonstrated value rather than RFC. The migration moment arrives when someone says "can I have a copy of that?" — at which point the upstream-UX conversation finally gets a concrete proposal to react to.

## See also

- [skills-should-be-thin](skills-should-be-thin.html)
- [wikidex](wikidex.html)
- [Thin harness, Fat Skills](Thin%20harness,%20Fat%20Skills.html)
- [MCP and the wikidex stack](MCP%20and%20the%20wikidex%20stack.html)
