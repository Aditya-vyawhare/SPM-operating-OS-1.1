# PM Operating System

A lightweight operating system for product managers, built on Cursor IDE. It gives LLMs shared context about your products, strategy, and decisions — so every conversation starts informed.

**Created by [@hardiktiwari](https://github.com/hardiktiwari) and [@Sach1ng](https://github.com/Sach1ng)**

**Blog:** [Part 1 — Giving AI Your Context](https://medium.com/@hardiktiwari) | [Part 2 — Self-Updating Knowledge Base](https://medium.com/@hardiktiwari)

---

## Quick Start

1. **Clone this repo**
   ```bash
   git clone https://github.com/hardiktiwari/PM-operating-OS.git
   cd PM-operating-OS
   ```

2. **Open in Cursor** and say: **"onboard"**

   The onboarding agent asks about your role, products, goals, and tools — then writes the config, creates your product folder, and sets up MCPs.

3. **Restart Cursor** to load rules.

---

## What's Inside

| Folder | Purpose |
|--------|---------|
| `AGENTS.md` | Persistent memory — persona, learned preferences, workspace facts |
| `skills/` | On-demand PM capabilities (PRDs, experiments, launch posts, etc.) |
| `.cursor/agents/` | Onboarding agent |
| `knowledge/products/` | Product dossiers — brief, roadmap, metrics, experiments, releases |
| `workspace/drafts/` | Agent scratch space for drafts and analysis |
| `config/` | Your configuration (written during onboarding) |
| `.cursor/mcp.json` | MCP connections for Figma, Google Drive, Jira |

---

## Skills (included)

| Workflow | Skills |
|----------|--------|
| **Planning** | strategy-connector, working-backwards |
| **Building** | prd-writer, one-pager, experiment-designer |
| **Shipping** | launch-readiness, launch-post |
| **Communicating** | exec-communicator, stakeholder-update |
| **Learning** | experiment-writeup, continual-learning |
| **Operating** | meeting-to-actions, brainstorming, writing-clearly |
| **Decisions** | decision-logger, what-if, knowledge-updater |

---

## Product Dossiers

Each product lives in `knowledge/products/<product-name>/`:

```
knowledge/products/my-product/
├── brief.md           # What it is, problem, hypothesis, scope
├── roadmap.md         # Now / Next / Later + milestones
├── metrics.md         # Dated metric snapshots
├── updates.md         # Status updates (newest first)
├── releases/          # Per-release docs
└── experiments/       # Experiment write-ups
```

Copy `_template/` to create a new product. The agent reads `brief.md` first for any product question.

---

## MCPs (Tool Connections)

Pre-configured in `.cursor/mcp.json` — add your credentials:

| Tool | What you need | Where to get it |
|------|--------------|-----------------|
| **Figma** | Personal Access Token | [figma.com/developers](https://www.figma.com/developers) |
| **Google Drive** | OAuth Client ID + Secret | [Google Cloud Console](https://console.cloud.google.com) |
| **Jira** | API Token + Site URL | [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) |

Or install from the Cursor marketplace: Settings → Plugins → search for Figma, Atlassian, etc.

---

## Memory (auto-updating)

PM-OS maintains persistent memory in `AGENTS.md`:

- **Learned User Preferences** — behavioral corrections you make (e.g., "don't assume numbers")
- **Learned Workspace Facts** — durable truths about your workspace (e.g., file locations, conventions)

Install the **Continual Learning** plugin to keep this updated automatically:

```
/add-plugin continual-learning
```

It runs after every conversation — mines transcripts for corrections and facts, writes them into `AGENTS.md`. No manual upkeep.

---

## Upgrading

Already using PM-OS? See [UPGRADING.md](UPGRADING.md) for how to pull new features. Check [CHANGELOG.md](CHANGELOG.md) for what changed in each release.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Not affiliated with any employer.*
