#!/usr/bin/env python3
"""Generate the public ZK projection for christopherdemarco.com."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlparse


LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class Note:
    path: Path
    rel_path: str
    uid: str
    title: str
    output_name: str
    output_html: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="_zk_source", type=Path)
    parser.add_argument("--out", default="zk", type=Path)
    return parser.parse_args()


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text

    frontmatter: dict[str, object] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        raw = value.strip()
        if raw == "true":
            parsed: object = True
        elif raw == "false":
            parsed = False
        else:
            parsed = raw.strip("\"'")
        frontmatter[key.strip()] = parsed

    body_start = end + len("\n---")
    if text[body_start : body_start + 1] == "\n":
        body_start += 1
    return frontmatter, text[body_start:]


def title_for(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def iter_markdown_files(source: Path):
    ignored = {".git", ".obsidian", ".daneel"}
    for path in source.rglob("*.md"):
        if any(part in ignored for part in path.relative_to(source).parts):
            continue
        yield path


def load_public_notes(source: Path) -> list[Note]:
    notes: list[Note] = []
    seen_uids: dict[str, str] = {}
    seen_names: dict[str, str] = {}

    for path in iter_markdown_files(source):
        text = path.read_text(encoding="utf-8")
        frontmatter, body = split_frontmatter(text)
        if frontmatter.get("public") is not True:
            continue

        uid = frontmatter.get("UID")
        if not uid:
            raise SystemExit(f"public note missing UID: {path.relative_to(source)}")
        uid = str(uid)

        output_name = path.name
        if uid in seen_uids:
            raise SystemExit(f"duplicate UID {uid}: {seen_uids[uid]} and {path}")
        if output_name in seen_names:
            raise SystemExit(f"duplicate public note filename {output_name}: {seen_names[output_name]} and {path}")

        seen_uids[uid] = str(path)
        seen_names[output_name] = str(path)
        notes.append(
            Note(
                path=path,
                rel_path=path.relative_to(source).as_posix(),
                uid=uid,
                title=title_for(path, body),
                output_name=output_name,
                output_html=f"{output_name.removesuffix('.md')}.html",
            )
        )

    return sorted(notes, key=lambda note: note.title.lower())


def rewrite_markdown_links(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        href = match.group(1)
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc or parsed.path.startswith("#"):
            return match.group(0)
        if not parsed.path.endswith(".md"):
            return match.group(0)
        rewritten = href.replace(".md", ".html", 1)
        return match.group(0).replace(href, rewritten)

    return LINK_RE.sub(replace, text)


def write_redirect(note: Note, out: Path) -> None:
    redirect_dir = out / note.uid
    redirect_dir.mkdir(parents=True)
    target = quote(note.output_html)
    body = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=../{target}">
  <link rel="canonical" href="../{target}">
  <title>Redirecting...</title>
</head>
<body>
  <p>Redirecting to <a href="../{target}">{html.escape(note.output_html)}</a>.</p>
  <script>window.location.replace("../{target}");</script>
</body>
</html>
"""
    (redirect_dir / "index.html").write_text(body, encoding="utf-8")


def resolve_link(source: Note, href: str, notes_by_source_rel: dict[str, Note]) -> Note | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or parsed.path.startswith("#"):
        return None
    if not parsed.path:
        return None

    link_path = unquote(parsed.path)
    candidate = (Path(source.rel_path).parent / link_path).as_posix()
    candidates = [candidate]
    if not candidate.endswith(".md"):
        candidates.append(f"{candidate}.md")

    for rel_path in candidates:
        note = notes_by_source_rel.get(Path(rel_path).as_posix())
        if note:
            return note
    return None


def graph_for(notes: list[Note]) -> dict[str, object]:
    notes_by_source_rel = {note.rel_path: note for note in notes}
    links: set[tuple[str, str]] = set()

    for note in notes:
        text = note.path.read_text(encoding="utf-8")
        for href in LINK_RE.findall(text):
            target = resolve_link(note, href, notes_by_source_rel)
            if target:
                links.add((note.uid, target.uid))

    return {
        "nodes": [
            {"id": note.uid, "title": note.title, "url": f"/zk/{note.uid}/"}
            for note in notes
        ],
        "links": [
            {"source": source, "target": target}
            for source, target in sorted(links)
        ],
    }


def write_graph_page(out: Path) -> None:
    (out / "graph.html").write_text(
        """---
layout: page
title: Public ZK Graph
---

<style>
  #zk-graph {
    border: 1px solid #ddd;
    height: 70vh;
    min-height: 32rem;
  }
</style>

<div id="zk-graph"></div>

<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<script>
fetch("/zk/graph.json")
  .then((response) => response.json())
  .then((graph) => {
    const nodes = new vis.DataSet(graph.nodes.map((node) => ({
      id: node.id,
      label: node.title,
      url: node.url,
    })));
    const edges = new vis.DataSet(graph.links.map((edge) => ({
      from: edge.source,
      to: edge.target,
    })));
    const network = new vis.Network(
      document.getElementById("zk-graph"),
      { nodes, edges },
      {
        nodes: { shape: "dot", size: 12, font: { size: 15 } },
        edges: { color: "#999", smooth: false },
        physics: { stabilization: true },
        interaction: { hover: true },
      }
    );
    network.on("doubleClick", (event) => {
      if (event.nodes.length) {
        const node = nodes.get(event.nodes[0]);
        if (node.url) window.location.href = node.url;
      }
    });
  });
</script>
""",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    out = args.out

    notes = load_public_notes(source)

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    for note in notes:
        text = note.path.read_text(encoding="utf-8")
        (out / note.output_name).write_text(rewrite_markdown_links(text), encoding="utf-8")
        write_redirect(note, out)

    (out / "graph.json").write_text(
        json.dumps(graph_for(notes), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_graph_page(out)

    print(f"Generated {len(notes)} public ZK notes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
