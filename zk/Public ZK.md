---
UID: Z202605192233000
public: true
---

## Vision

Publish a fail-closed public view of the personal ZK at `christopherdemarco.com/zk`, so individual public notes can be shared by stable links without exposing private material by accident.

The public app should preserve the "ZK DAG" experience: readable notes, traversable links, backlinks where possible, and graph/context affordances. It is not just a blog export; it is a read-only public projection of selected notes.

## Decisions

- Public/private gate: fail closed for the prototype. A note is publishable only when its YAML frontmatter contains an explicit `public: true`.
- Visibility migration path: after the public build proves safe and useful, audit the ZK, mark private notes explicitly with `private: true`, and flip the static-site-generator predicate from allowlist mode to denylist mode. This changes the publication predicate, not the architecture.
- Stable public address: use the existing [Lightweight UIDs for linking into ZK](Lightweight%20UIDs%20for%20linking%20into%20ZK.html) convention as the route key, not filenames.
- Hosting preference: `christopherdemarco.com/zk`, via the existing GitHub Pages site at `~/cmd/src/www/master` (`christopher-demarco/christopher-demarco.github.io`).
- Repo boundary: the ZK repo remains the content source and natural trigger; the public website repo is the publishing host. On ZK pushes, a ZK workflow dispatches a website workflow; the website workflow checks out the ZK repo, regenerates `/zk/`, and deploys GitHub Pages.
- Trigger strategy: dispatch the website build on every Markdown push while prototyping. Do not prematurely gate on `public: true`; deletes, visibility flips, private-link reports, and generator changes can all matter. Later optimization should compare the generated public projection, not infer relevance from raw changed files.
- Work-ZK outbound links: create an Obsidian command that lets me choose a note with Obsidian's familiar file picker, reads the target note's `UID`, and inserts a Markdown link to the public web app.

## Prototype Shape

Build a static site generator pass that:

- Scans Markdown notes.
- Parses YAML frontmatter.
- Includes only notes with `public: true`.
- Requires `UID` for every included note.
- Copies public Markdown notes into the website repo under `/zk/`.
- Generates one static UID redirect page per public note, e.g. `/zk/Z202507132346000/index.html`.
- Relies on Jekyll to render copied Markdown notes and convert relative `.md` links to `.html`.
- Reports or fails on public notes that link to non-public notes, rather than trying to expose or rewrite those links silently.
- Generates graph data only from public-to-public edges.

The rich GUI can then load the generated note JSON and graph JSON client-side. That keeps GitHub Pages viable and keeps the privacy boundary in the build step, not in browser code. The important router trick is that GitHub Pages only serves real files, so every inbound UID route should be generated as an actual static `index.html` file.

The canonical public base URL should be `https://christopherdemarco.com/zk/`. GitHub Pages remains the deployment mechanism, but the user-facing links should prefer the custom domain over the GitHub Pages hostname.

Deployment flow:

- ZK repo workflow triggers on Markdown pushes to `main`.
- ZK workflow sends a `repository_dispatch` event to `christopher-demarco/christopher-demarco.github.io`.
- Website repo workflow handles `repository_dispatch` and `workflow_dispatch`.
- Website workflow checks out both repos, rebuilds `/zk/`, and deploys the GitHub Pages site.

This avoids polling while also avoiding cross-repo content pushes from the ZK workflow. The ZK workflow needs only a fine-scoped token that can dispatch events to the website repo.

Treat visibility as a build configuration with two modes:

- `allowlist`: publish only `public: true`; prototype/default until the safety model is proven.
- `denylist`: publish everything except `private: true`; later steady state after private-note audit.

In both modes, the invariant is the same: the browser app never receives private note content, private route indexes, private search data, or private graph edges.

## Obsidian Outbound Link Command

Yes, this is feasible as a small Obsidian community/private plugin.

Command behavior:

- Invoke command from the work vault via keyboard shortcut.
- Show Obsidian's file autocomplete modal for the personal ZK vault.
- On selection, read the target file's frontmatter `UID`.
- Optionally verify `public: true`; for the prototype, fail closed and refuse to create a public URL without it.
- Insert Markdown at the cursor, e.g. `[Lightweight UIDs for linking into ZK](https://christopherdemarco.com/zk/Z202507132346000/)`.

The main wrinkle is vault access: an Obsidian plugin normally operates inside the current vault. For work-vault linking into the personal vault, the clean prototype is either:

- Run the plugin in the personal vault and copy the link to the clipboard; or
- Configure an absolute path to the personal ZK checkout and have the plugin index that directory itself.

The second option better matches the desired workflow: from the work vault, hit a shortcut, search personal notes, insert a public URL.

## Sprint

- DONE Create static build spike for public notes only [status:: done] [sprint:: 2026-W21]
- DONE Define public frontmatter contract: `public: true`, `UID`, title fallback [status:: done] [sprint:: 2026-W21]
- DONE Manually prove Jekyll renders copied Markdown notes and converts relative `.md` links to `.html` [status:: done] [sprint:: 2026-W21]
- DONE Manually create UID redirect pages in `~/cmd/src/www/master/zk/` for browser testing [status:: done] [sprint:: 2026-W21]
- DONE Generate UID redirect pages automatically for every public note [status:: done] [sprint:: 2026-W21]
- DONE Decide artifact handoff: ZK dispatches, website repo pulls/builds/deploys [status:: done] [sprint:: 2026-W21]
- DONE Add ZK workflow that dispatches website build on Markdown pushes [status:: done] [sprint:: 2026-W21]
- DONE Add website workflow that regenerates `/zk/` from checked-out ZK source [status:: done] [sprint:: 2026-W21]
- DONE Configure required GitHub secrets: `PUBLIC_ZK_DISPATCH_TOKEN` in ZK repo and `ZK_READ_TOKEN` in website repo [status:: done] [sprint:: 2026-W21]
- DONE Test end-to-end dispatch from ZK push to website Pages deploy [status:: done] [sprint:: 2026-W21]
- TODO Move inline website workflow generator into a script [status:: ready] [sprint:: 2026-W21]
- TODO Install/test packaged Obsidian command in work vault [status:: ready] [sprint:: 2026-W21]
- DONE Add Emacs markdown-mode command to insert public ZK links [status:: done] [sprint:: 2026-W21]

## Backlog

- SOMEDAY Add graph visualization over public-to-public links only.
- SOMEDAY Add backlinks computed only from public notes.
- SOMEDAY Support aliases/slugs while keeping UID as canonical route.
- SOMEDAY Add an optional privacy report listing links from public notes to non-public notes. Non-public notes are not exported, so these links are dead rather than content leaks; the remaining concern is metadata leakage through link text or filenames.
- SOMEDAY Integrate with [Daneel](Daneel.html#phase-5-public-portfolio-view) as the content substrate for the public portfolio view.

## Last Session Summary

- Decided that public ZK should fail closed via `public: true` frontmatter and use existing lightweight UIDs as stable web route keys.
- Clarified that fail-closed is a prototype hedge; the intended later steady state is denylist publication after private notes are explicitly marked `private: true`.
- Set the preferred public URL to `https://christopherdemarco.com/zk/`, hosted by the existing GitHub Pages website repo at `~/cmd/src/www/master`.
- Proved with live website test files that Jekyll converts relative `.md` links between copied Markdown pages into `.html` links, so internal link rewriting is not core to the design.
- Chose static per-UID redirect pages as the inbound router: GitHub Pages serves real `/zk/<UID>/index.html` files generated for each public note.
- Chose deployment shape: ZK push dispatches a website repo build; website repo pulls ZK source, regenerates `/zk/`, and deploys. During prototype, dispatch on every Markdown push rather than trying to gate on `public: true`.
- Created manual test UID redirects in `~/cmd/src/www/master/zk/`; next implementation step is a generator that copies public notes and emits these redirect pages automatically.
- Added raw-curl ZK dispatch workflow at `.github/workflows/public-zk-dispatch.yml` and yq-based website receiver workflow at `~/cmd/src/www/master/.github/workflows/public-zk-build.yml`.
- Marked this design note `public: true` as the first seed note; local `yq --front-matter=extract` confirms the workflow commands read both `public` and `UID`.
- Confirmed end-to-end publishing works: ZK dispatch triggers the website workflow, website workflow regenerates `/zk/`, GitHub Pages publishes the branch, UID routes redirect, and generated public copies rewrite `.md` links to `.html` for Jekyll.
- Decided not to block on links from public notes to private notes. Private targets are not exported; a future report may help identify metadata leakage through link text or filenames.
- Packaged the Obsidian command as `tools/obsidian-public-zk-link/public-zk-link/` with a README for copying it into work vaults. The plugin expands `~`, reads public notes from the configured personal ZK checkout, and inserts `https://christopherdemarco.com/zk/<UID>/`.
- Added Doom Emacs markdown command `cmd-markdown-insert-public-zk-link`, bound to `C-c C-z`, using `expand-file-name` for a portable ZK path.
