---
UID: Z202605240001000
public: true
---
# Public ZK script extraction

Move the public-ZK generator logic out of the GitHub Actions YAML and into a small script.

Goal: the workflow should orchestrate checkout/build/deploy, while the script owns:

- Selecting notes with `public: true`.
- Copying public notes into `zk/`.
- Rewriting generated `.md` links to `.html` for Jekyll.
- Emitting `/zk/<UID>/index.html` redirect pages.

Keep it boring and locally runnable.
