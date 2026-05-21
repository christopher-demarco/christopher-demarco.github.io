---
UID: Z202605201531001
public: true
---

# Read-only hooks are the part of a thin skill that must stay fat

[Skills Should Be Thin; the Wiki Should Be Fat](skills-should-be-thin.html) prescribes that a skill keeps three things: trigger conditions, a wiki pointer, and *guardrails*. The first two are markdown. The third is doing more work than the doctrine acknowledges.

## The evidence

`plugins/troubleshooting/k8s-troubleshooter/hooks/k8s-guard.sh` is 57 lines of `bash + grep -E` that block destructive `kubectl` and `argocd` invocations at PreToolUse. It pattern-matches across flag positions, distinguishes pipes from chain operators (so `kubectl get pods | grep delete` is allowed but `kubectl --context ctx delete pod foo` is denied), and emits structured `permissionDecision: deny` JSON. It's not documentation. It's enforcement code.

That code can't migrate to `updocs`. A wiki page can describe the policy ("k8s-troubleshooter is read-only — never `delete`, `apply`, `exec`, `patch`, `scale`"), but the *execution* of that policy must live where the agent's tool calls are intercepted: in the plugin, in a hook script, before the Bash tool fires.

## The doctrine has a slot for this; "guardrails" hides it

[Thin harness, Fat Skills](Thin%20harness,%20Fat%20Skills.html) describes a three-layer architecture: fat skills on top (markdown procedures), a thin CLI harness in the middle, and a **deterministic application layer** at the bottom — same input, same output, every time. `k8s-guard.sh` is a deterministic-layer artifact: regex predicate over tool-call JSON → allow/deny decision.

The thin-skill doctrine packs three architecturally distinct things under the word "skill":

1. **Routing markdown** — declarative.
2. **Wiki pointers** — declarative.
3. **Hook scripts** — deterministic enforcement.

The plugin packaging accidentally bundles a sliver of the deterministic layer into the skill directory. That's a Claude Code design detail, not a skill-design principle.

## Why the distinction matters

If "guardrails" stays a fuzzy bucket alongside trigger conditions, two failure modes follow.

- **Guardrails get written as prose.** "Don't run destructive commands" inside `SKILL.md` is documentation, which the agent may or may not respect. Real read-only enforcement requires a PreToolUse hook with a regex predicate. Calling both "guardrails" smuggles soft policy into a slot that needs hard enforcement.
- **Hooks get under-invested.** If they're the small leftover after the wiki migration, the regex stays at "good enough" — fine until someone discovers a quoting variant that slips through. Hook scripts deserve the same engineering treatment as any deterministic-layer code: tests, code review, version pinning. The repo's `CLAUDE.md` already mandates ShellSpec for shell scripts; the doctrine should make that a first-class expectation, not an afterthought.

## Restated

The thin-skill recipe is three layers, not two-and-a-handwave:

- **Skill** = routing markdown (trigger + wiki pointer).
- **Deterministic enforcement** = hook scripts, packaged alongside the skill but architecturally distinct.
- **Wiki** = the content (Diátaxis-shaped, single source of truth).

Three layers, three failure modes, three sets of authoring conventions. Calling the middle layer "guardrails" is the doctrine's one fuzzy moment.

## See also

- [Skills Should Be Thin; the Wiki Should Be Fat](skills-should-be-thin.html)
- [Thin harness, Fat Skills](Thin%20harness,%20Fat%20Skills.html)
- [k8s-troubleshooter as a worked example of thin skills](k8s-troubleshooter%20as%20a%20worked%20example%20of%20thin%20skills.html)
