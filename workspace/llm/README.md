# LLM Workspace

This directory is the **agent's sandbox** — a scratch area where AI agents draft, compile, and iterate freely without affecting the curated knowledge layer.

Inspired by [Andrej Karpathy's personal knowledge base pattern](https://x.com/karpathy): raw documents compiled into structured wiki pages, with the LLM owning the files entirely.

## Subfolders

| Folder | Purpose |
|--------|---------|
| `ingest/` | Raw clips, web exports, paper summaries, data dumps |
| `compiled/concepts/` | Auto-generated concept notes, cross-reference wikis |
| `outputs/` | Q&A artifacts, slide drafts, analysis plots |
| `lint/` | Health-check reports, gap analysis, consistency audits |
| `tools/` | Agent-generated scripts, one-off utilities |

## Rules

1. **Default writes go here.** When an agent produces draft content (summaries, compilations, exploratory analysis), it writes to `workspace/llm/` — not to `knowledge/`.
2. **Promotion is explicit.** If content is good enough for the curated layer, the user (or a governed automation) promotes it to `knowledge/`.
3. **Regenerable by design.** Everything in this directory can be deleted and rebuilt by re-running the agents. Do not store canonical data here.
4. **No secrets.** Same rules as the rest of the repo — no API keys, tokens, or credentials.
