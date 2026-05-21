---
UID: Z202512280001000
repo: git@github.com:christopher-demarco/daneel.git
public: true
---
# Daneel

## 1. Vision

This is an attempt to do Scrum with an AI advisor/co-founder/scrummaster.

Transform a passive Zettelkasten into an active "Control Plane" that bridges the gap between high-energy ideation and low-energy execution. The system must act as a **Producer**, handling the cognitive load of "what's next" so the user (**Talent**) only has to focus on "doing."

The name comes from [Asimov](https://en.wikipedia.org/wiki/R._Daneel_Olivaw).

## 2. Information Architecture

- **The Hub:** [`PROJECTS.md`](PROJECTS.html) — A high-level dashboard with state tracking (status, focus, priority).

- **The Spoke:** `Foo_Project.md`, `Bar_Project.md`, et al. — Single documents (index in [PROJECTS](PROJECTS.html)) containing both the **Design** (Spec/Vision) and the **Plan** (tasks/milestones). Projects with code repos include `repo: git@...` in YAML frontmatter.

- **The Control Plane:** [`AGENTS.md`](AGENTS.html) — Instructions for the Daneel persona. (linked from [CLAUDE](CLAUDE.html) and [GEMINI](GEMINI.html))

- **The Bridge:** [`/sync-projects` skill](https://github.com/christopher-demarco/zettelkasten/tree/main/.claude/skills/sync-projects) — Bidirectional sync between ZK project docs and repo `PLAN.md`, using a cached last-clean base per project plus a deterministic 3-way merge to keep concurrent producer/vibe-coder edits in sync. [ref](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

- **The Tooling:** `daneel` repo (separate from ZK) — Infrastructure, GH Actions, automation scripts. ZK stays pure notes + state + session skills; Daneel repo holds read-only observers and infra.

## 3. Interaction Loops

1. **Strategic Loop (Daneel):** Brainstorm, refine vision, break down tasks → Update project Zettels → Run `/sync-projects` to push context to repos.

2. **Tactical Loop (Vibe-coder):** Clone project repo (has `PLAN.md`, referenced from `CLAUDE.md`) → Execute tasks → Commit progress and findings.

3. **Persistence Loop (GHA):** Daily 19:00 parse of the "Pulse" → Push notification to user.
    

## Sync Architecture (ZK ↔ repo PLAN.md)

- Goal: Concurrent producer/vibe-coder edits without stomping. Artifacts are the ZK project doc and the repo `PLAN.md` (referenced from repo `CLAUDE.md`).
- Base cache: After every clean sync, persist the merged content to `.daneel/sync-state/<project>.md` (local cache; should be gitignored) and use it as the next merge base.
- Merge strategy: Deterministic 3-way merge (ZK current, repo current, cached base). On conflict, stop and surface markers—no heuristics. If the cache is missing, fall back to merging current ZK vs repo HEAD (or a one-sided update if only one changed) rather than spelunking history.
- Modes: Push-only/pull-only still update the cache after a clean one-sided sync so the next run has a base.
- Implementation note: Rewrite the `/sync-projects` skill in Python to make base/cache handling, temp dirs, and error reporting safer than the current Bash script.

## Last Session Summary

- Documented the cached-base sync architecture and corrected PLAN.md references in `Daneel.md`.
- Replaced the `/sync-projects` implementation with Python and updated docs + `.gitignore` for sync state.

---

# PLAN: Meta-Project Dogfooding (Sprint 0)

## Phase 1: The Skeleton (Manual Setup)

- DONE Create `AGENTS.md` & link `CLAUDE.md` there
- DONE Create `PROJECTS.md`

## Phase 2: The Producer Interface

- DONE Initialize first "Active" Project: Use Claude Code to move [Daneel](Daneel.html) from backlog to active.
- DONE Configure iOS Claude Code: Point at the ZK repo. Can it read/write [PROJECTS](PROJECTS.html) and [Daneel](Daneel.html)?
- DONE ~~Open question: Sprint task encoding?~~ **Decision**: Keep tasks in project files, mark with `[sprint:: YYYY-Www]`. No duplication.
- DONE ~~Open question: Vibe-coder visibility?~~ **Decision**: Run `/sync-projects` to keep project docs in sync with repo `PLAN.md`. Project repo's `CLAUDE.md` includes `@PLAN.md`.
- DONE Implement `/sync-projects` skill: `.claude/skills/sync-projects/`
- DONE Make `/sync-projects` bidirectional with stateful 3-way merge (cached base per project)

## Phase 3: The Nudge (Infrastructure)

### Sprint 2025-W52
- DONE Define notification channel → **SMS** (goal), email (interim) [status:: done]
  - SMS requires toll-free number; pending carrier verification
  - **Workaround:** Ship with email-via-SNS to unblock
  - Phase complete when SMS is working
- DONE Define message format [status:: done]
  - Single next action + count of remaining
  - Streak/stall callout based on git log (no task metadata needed)
- DONE Choose SMS provider → **AWS SNS** [status:: done]
  - One-way sufficient (real interaction in Claude Code or SPA)
- DONE Create `daneel` repo with infra + GH Actions structure [status:: done]
- DONE Set up SNS infra (CloudFormation + OIDC) [status:: done]
- DONE Write pulse generator script (parse tasks, check git activity) [status:: done]
- DONE Draft GH Action workflow (19:00 trigger) [status:: done]
- DONE **SHIP: Daily motivator live (email)** [status:: done]
- BLOCKED Enable SMS when toll-free number is active
- DONE Update pulse script: parse `^- TODO ` instead of `[status:: ready]`
  - Backlog uses `SOMEDAY` keyword — pulse ignores these
  - Simpler grep, clearer semantics for humans and LLMs

## Phase 4: Expansion
- SOMEDAY Evaluate [OpenClaw](https://clawdbot.com)
	- wtwomey: "Self-host synapse (matrix) maybe? That's what I'm rocking for comms. Openclaw lives in it's own vlan, and the matrix server just has a hole poked through to my reverse nginx proxy for SSL"

---

## Pulse Generator Design

**Purpose**: Daily 19:00 nudge — reads ZK repo, surfaces next action, motivates via streak/stall feedback.

### Inputs
- `ZK_REPO` — GitHub repo (e.g., `owner/zettelkasten`)
- `DANEEL_SNS_TOPIC_ARN` — From CloudFormation stack
- GH PAT with read access to ZK repo

### Task Parsing
1. Clone ZK repo
2. Parse `PROJECTS.md` → find active projects
3. Parse project files → first `^- TODO ` line = "Next"
4. Count remaining `TODO` items
5. Priority = document order (first TODO wins)

**Keywords:**
- `TODO` — Sprint item, ready to work
- `BLOCKED` — Sprint item, waiting on external
- `SOMEDAY` — Backlog (pulse ignores)

### Streak/Stall Logic
- Walk git log day-by-day counting consecutive days with commits
- ≥1 commit today → "🔥 N-day streak!"
- 0 commits today but yesterday had one → no callout
- ≥2 days silent → "⚠️ N days quiet" + coaching prompt

### Coaching Prompt Bank
Randomly selected when stall ≥2 days:
- "What's making this feel heavy?"
- "Is this task too big to start?"
- "What's the smallest possible next step?"
- "What would need to be true for this to feel worth doing?"

### Message Format
```
[streak/stall line - if applicable]
Next: [task name]
(+N more ready)

[coaching prompt - only if stall ≥2 days]
```

### Edge Cases
- No `TODO` items → "Nothing ready — time to groom the backlog?"
- No active projects → "All quiet. What's next?"

### Implementation
- Script: `scripts/pulse.sh` (or `.py`)
- Local testing: `./scripts/pulse.sh --local /path/to/zk --dry-run`
- GH Action: `.github/workflows/pulse.yaml`
  - Trigger: `cron: '0 0 * * *'` (19:00 EST = 00:00 UTC) + `workflow_dispatch`
  - Uses OIDC for AWS (no stored creds)

### Backlog (Pulse-specific)
- SOMEDAY LLM-powered contextual coaching (if static prompts feel stale)

---

## Phase 5: Public Portfolio View

**Strategic insight:** The portfolio play isn't "build a website and write content for it." It's: make Daneel's existing output externally renderable. The pulse, the project status, the architecture — it's already being generated. The work is adding a public read-only view, not creating new content.

**Why this beats LinkedIn drip:**
- LI drip requires sustained cadence → spiky motivation means the account goes silent → silence becomes the message
- A live system requires sustained *system*, not sustained *attention* → spikiness becomes visible intensity on whatever's hot that week
- "I built this and you're looking at it" is stronger than "I built this, here's a post about it"

**What gets surfaced:**
- Project dashboard (live render from PROJECTS.md — curated subset)
- Architecture: live code, interactive visualizations, architecture diagrams — *showing* how Daneel works, not describing it
- ZK notes tagged `#public` — rendered as portfolio content
- Live pulse status (what Daneel is nudging about today)

**What stays private:** Everything by default. Career strategy, org names, review notes, anything without an explicit `#public` tag.

**The LI post is dead, not repurposed.** The [narrative draft](I%20built%20an%20AI%20co-founder%20and%20scrummaster.html) was written to *describe* Daneel for LinkedIn. The portfolio site doesn't describe Daneel — it *is* Daneel rendered. LI becomes an amplification channel (share links when something's worth sharing), not the primary venue.

**Open questions:**
- Tech stack for the public view? Static site generator? Live render from ZK? SPA? See [Public ZK](Public%20ZK.html) for the publishing substrate.
- Does christopherdemarco.com host this, or is it a separate domain?
- What's the smallest version that's shippable? (Live project dashboard + one architecture visualization?)
- What interactive visualizations best demonstrate the system? (Sync flow? Pulse logic? Project graph?)

TODO Scope the smallest shippable portfolio view — live dashboard + one architecture visualization
- SOMEDAY Full web UI with rendered #public notes

---

## Backlog

- SOMEDAY Lower friction for adding items to triage
  - Quick capture from mobile, CLI, or conversation
  - Inbox that doesn't require context-switching into ZK
- SOMEDAY Build triage process
  - Regular cadence to process inbox → projects
  - Decision framework: kill, backlog, or sprint
- SOMEDAY PR/branch merge tooling for iOS agent sessions
  - iOS Claude Code commits to feature branches by design (safety guardrail)
  - Manual workaround: `git fetch --all && git branch -r | grep claude | xargs -I{} git merge {}`
  - Future: `/merge-agent-branches` skill to review and merge
- DONE Spike: Explore org-mode for task management
  - **Decision:** Adopted org-mode keywords (TODO/BLOCKED/SOMEDAY) for task state
  - Keeps Markdown structure, adds semantic clarity for humans + LLMs + scripts
- SOMEDAY Sync agent config files across managed projects
  - **Decision:** AGENTS.md is canonical; CLAUDE.md and GEMINI.md are thin pointers (`@AGENTS.md`)
  - AGENTS.md contains `@PLAN.md` plus project-specific guidance
  - Could extend `/sync-projects` or be a separate skill
  - Consider: ZK-global defaults vs per-project overrides

---

### Implementation Note: Task Keywords

Use **org-mode keywords** for task state — readable by humans, LLMs, and scripts alike:

```markdown
## Sprint
- <TODO keyword> Task ready to work
- <BLOCKED keyword> Task waiting on external dependency
- <DONE keyword> Completed task

## Backlog
- <SOMEDAY keyword> Future idea (pulse ignores)
```

(Keywords do not actually include `keyword` or angle brackets! The above example uses that representation to prevent them from showing up as actual to-do items.

---

### Open Question: Git Worktrees

When using git worktrees for parallel development, synced `PLAN.md` updates land on `origin/main`. **SOP when visiting a worktree**: merge `origin/main` to pick up any Daneel syncs before starting work.

TODO: Consider whether `/sync-projects` should push to a dedicated branch, or if there's a cleaner worktree-aware flow.
