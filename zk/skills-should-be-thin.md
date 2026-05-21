---
UID: Z202605121716000
public: true
---

# Skills Should Be Thin; the Wiki Should Be Fat

## The problem

Knowledge locked inside a skill is invisible to humans and uncomposable by agents. A human who needs the Splunk field schema for K8s labels must read skill source code. An agent correlating ingress-nginx logs with external-secrets failures cannot combine knowledge from two skills. Each skill is a sealed box. See [Progressive disclosure is related to composability](Progressive%20disclosure%20is%20related%20to%20composability.html).

We maintain the same knowledge in two places. The up-log skill duplicates field schemas belonging in cluster-logging.mdx. The ingress-nginx skill carries 390 lines of Splunk query reference alongside existing ingress documentation. The deploy-app-to-k8s skill embeds 13 deployment guardrails that duplicate the namespace and golden-paths wiki pages — in a format only agents read.

Every published skill is another document to keep current. Field schemas change; CLI flags appear; clusters come and go. Updates must happen in the wiki *and* in every skill that embedded the same information. They will drift. They always do.

## The fix

Shrink skills to thin behavioral wrappers: trigger conditions, a pointer to a wiki index page, and guardrails. Move field schemas, CLI references, investigation workflows, and deployment rules into wiki articles organized along Diataxis lines.

A skill like up-log drops from 180 lines to roughly 20: "When the user asks about application logs, start at the logging index, follow the query-splunk-logs how-to, and never omit `-o json`."

## The effort

Our wiki already has 55+ pages covering Kubernetes, observability, Argo CD, and load balancing. cluster-logging.mdx alone documents Splunk queries for 25+ K8s components. The gaps are small:

- **3–4 CLI reference pages**: up-log flags and time formats, splunk_query.py usage, helper scripts (up-log-fields, up-log-values)
- **2–3 how-to pages**: the six-step Splunk investigation workflow (now in up-log), the ingress troubleshooting decision tree (now in ingress-nginx), the K8s deployment checklist (now in deploy-app-to-k8s)
- **Light enrichment of 3–4 existing pages**: add the K8s label field schema to cluster-logging.mdx; merge deployment guardrails into namespace and golden-paths docs

That totals 5–8 new pages and a few patches to absorb 1,400 lines of skill content from all five marketplace skills.

## The payoff

Agents compose knowledge that skill authors never anticipated combining. Teams update a field schema once instead of patching three skills. Humans and agents read the same source of truth. Helper scripts move to a tools repo where they can be versioned and tested.

Every agent session doubles as a documentation review. End with "any suggestions for improving these docs?" — the agent that just navigated the wiki knows exactly where the gaps are.

Skills are not documentation. They are routing. Build them that way.

-----

See also:
- [Thin harness, Fat Skills](Thin%20harness,%20Fat%20Skills.html)
- [Wikidex](wikidex.html)
- [Wikidex shadow indexing](Wikidex%20shadow%20indexing.html)
- [MCP and the wikidex stack](MCP%20and%20the%20wikidex%20stack.html)

