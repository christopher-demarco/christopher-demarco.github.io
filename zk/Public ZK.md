---
UID: Z202605192233000
public: true
---
Publish a fail-closed public view of the personal ZK at `christopherdemarco.com/zk`, so individual public notes can be shared by stable links without exposing private material by accident.

Preserve the "ZK DAG" experience: readable notes, traversable links, backlinks where possible, and graph/context affordances.

Stable public address: use the existing [Lightweight UIDs for linking into ZK](Lightweight%20UIDs%20for%20linking%20into%20ZK.html) convention as the route key, not filenames.

Work-ZK outbound links: create an Obsidian command that lets me choose a note with Obsidian's familiar file picker, reads the target note's `UID`, and inserts a Markdown link to the public web app. Same for Emacs.
