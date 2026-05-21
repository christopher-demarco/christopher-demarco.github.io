---
permalink: /zk/Lightweight%20UIDs%20for%20linking%20into%20ZK.md
UID: Z202507132346000
public: true
---
If I ever do need to link into ZK, I should simply use this type of UID:
`ZYYYYMMDDHHMMnnn`. This is [easy to implement](templates/UID.md), sorts correctly for an _ad hoc_ timeline, and it should be easy enough to dereference (via MCP or similar) with whatever AI tooling I'm using, because [ZK in Markdown is accessible to LLMs](ZK%20in%20Markdown%20is%20accessible%20to%20LLMs.md)!

Ooh! And because I have ZK in Git, I can easily derive a UID post hoc, from its creation date (hence `nnn`, to avoid collisions).

See  [Public ZK](Public%20ZK.md)--For public web links, the UID should be the canonical route key, e.g. `/z/Z202507132346000/`. Publication must still fail closed: a UID makes a note addressable, but not publishable. Only notes with explicit `public: true` frontmatter should appear in the public build.
