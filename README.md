# PM Operating System

A PM operating system that **accelerates product work** by giving LLMs **shared context**. It connects to where you work (Slack, Drive, Jira, Figma, Databricks, etc. via MCPs), includes PM skills (PRDs, strategy, launch, exec updates), and maintains a living context of your strategy and decisions — evolving into a **context graph** that compounds over time. Built on Cursor IDE.

**Created by [@Sach1ng](https://github.com/Sach1ng) and [@hardiktiwari](https://github.com/hardiktiwari)**

---

## Quick start (self-serve onboarding)

1. **Clone this repo**
   ```bash
   git clone https://github.com/Sach1ng/PM-operating-OS.git
   cd PM-operating-OS
   ```

2. **Run onboarding** — Open the repo in Cursor, then in chat say: **"onboard"** or **"PM-OS setup"**. Answer the questions; the agent writes config and runs setup automatically. MCPs (tool connections) are the **last step** and **optional** — you can skip and add them later via Cursor Settings → Tools & MCP or the Cursor plugin marketplace.
   - *Or* manually edit `config/pm-os-config.yaml` and run `./scripts/setup.sh --copy`

3. **Restart Cursor** — Rules, skills, and agents will load from `~/.cursor/`.

---

## What's included

| Type | What it is | How it's customized |
|------|------------|---------------------|
| **Rules** | Persistent guidance Cursor applies | Your product, role, org, deprioritization signals |
| **Skills** | On-demand PM capabilities | Goals, VIPs, PRD template, expanded PM workflows |
| **Agents** | Specialized assistants (feedback analysis, planning, strategy review, exec updates, retrospective) | Slack channel, Google docs, goals |
| **Knowledge layer** | Strategy and domain context (personas, metrics, competitive landscape) | Customize in `knowledge/` |
| **Memory** | Trajectory store — accumulated agent outputs, decision traces, knowledge snapshots | Builds automatically as you use agents |

---

## Structure (after onboarding)

| Folder / file | Purpose |
|---------------|---------|
| **AGENTS.md** | Persistent memory — PM Chief of Staff persona + Learned User Preferences + Learned Workspace Facts. Auto-updated by the [Continual Learning plugin](https://cursor.com/marketplace/cursor/continual-learning). |
| **.cursor/commands/** | Slash commands — `/planday`, `/slack-sync`, `/program-update`, `/continual-learning` |
| **.cursor/agent-schedules.json** | IDE-native cron — runs slash commands on a schedule when Cursor is open |
| **.cursor/hooks/state/** | Cooldown files and transcript processing index |
| **config/** | Your answers → `pm-os-config.yaml` + `agent-schedule.md` (cadence map) |
| **templates/** | Jinja2 templates for rules, agents, skills |
| **scripts/** | `setup.sh` / `setup.py` — generates personalized files |
| **scheduler/** | Headless agent scheduler — runs commands via Claude API even when Cursor is closed |
| **skills/** | Source for prd-writer, working-backwards, and expanded PM skills |
| **knowledge/** | Curated layer — strategy, projects (brief + updates + metrics), roadmap |
| **knowledge/projects/** | Project dossiers — one folder per product/initiative |
| **workspace/llm/** | Agent sandbox — drafts, compilations, exploratory work (regenerable) |
| **memory/** | Context graph trajectory store — decision traces, agent outputs, knowledge snapshots |
| **docs/agents.md** | Agent documentation (all agents, trigger phrases, requirements) |

---

## Rules, skills, and agents — what's the difference?

| | What it is | In plain terms |
|---|------------|----------------|
| **Rules** | Persistent guidance Cursor applies | How *you* work: standards, org context, prioritization |
| **Skills** | On-demand "how-to" Cursor uses when the task fits | PM capabilities: PRDs, working backwards, prioritization |
| **Agents** | Specialized assistants Cursor delegates to | Concrete tasks: feedback analysis, daily planning, strategy review |

---

## PM Workflows

| Workflow | Skills |
|----------|--------|
| **Planning** | strategy-connector, working-backwards |
| **Building** | prd-writer, one-pager, experiment-designer |
| **Shipping** | launch-readiness, launch-post |
| **Communicating** | exec-communicator, stakeholder-update |
| **Learning** | experiment-writeup, feedback-analyzer |
| **Operating** | weekly-planner, meeting-to-actions, action-item-prioritizer |
| **Context graph** | decision-logger, what-if, knowledge-updater, retrospective |

---

## Knowledge Layer

The `knowledge/` directory holds strategy and domain context that agents and rules reference:

- **_template/** — Copy this folder and rename it for your domain (e.g., `my-product/`)
- **_template/projects/** — Project dossier pattern: `brief.md` + `updates.md` + `metrics.md` + `experiments/`
- **product/roadmap.md** — Portfolio roadmap template
- **data/experiment-log.md** — Central experiment tracker
- **examples/** — Fully worked-out examples using public investor data from **Spotify, Netflix, Shopify, and Uber** (SEC 10-Ks, earnings calls, investor presentations)

**How to customize:** Edit the markdown files in `knowledge/` to reflect your product, team, and current strategy. Create a folder under `knowledge/projects/` for each product or initiative using the template in `knowledge/_template/projects/`.

---

## Self-Updating Memory

PM OS goes beyond static context — it **updates itself**. Three mechanisms work together to keep the knowledge base current without manual maintenance:

### 1. Continual Learning (automatic)

Install the [Continual Learning plugin](https://cursor.com/marketplace/cursor/continual-learning) from the Cursor marketplace. It runs a `stop` hook after every agent conversation, mines transcripts for corrections and workspace facts, and writes them into `AGENTS.md`. Your agent gets smarter with every session — automatically.

```
You correct the agent → plugin extracts the correction → AGENTS.md updates → next session starts smarter
```

### 2. Scheduled Agents (automatic)

Agent commands run on a schedule via two mechanisms:

| Mechanism | When it runs | Setup |
|-----------|-------------|-------|
| **IDE cron** (`.cursor/agent-schedules.json`) | When Cursor is open | Edit the JSON, adjust times |
| **Headless scheduler** (`scheduler/main.py`) | Always (macOS LaunchAgent) | `bash scheduler/setup.sh` + API keys |

Default schedule:

| Time | Command | What it does |
|------|---------|-------------|
| 8:30 AM (Mon-Fri) | `/planday` | Reads weekly goals + Slack, builds P0/P1/Backlog, sends to Slack DM |
| 4:58 PM (daily) | `/slack-sync` | Syncs strategic Slack content to project knowledge files |
| 5:00 PM (Mon-Fri) | `/program-update` | EOD status across workstreams → Slack + log |

### 3. Two-Layer Architecture

Content is separated into two layers to balance speed with integrity:

| Layer | Path | Who writes | What goes here |
|-------|------|-----------|----------------|
| **Curated** | `knowledge/` | Governed automations + humans | Product truth: briefs, metrics, updates, roadmap |
| **Workspace** | `workspace/llm/` | Agents freely | Drafts, compilations, exploratory analysis |

Governed automations (Slack sync, metrics refresh) write directly to the curated layer — they earn trust through storage bars, dedup checks, and cooldowns. Ad-hoc agent work lands in the workspace. Good outputs get promoted to `knowledge/` by the user.

### A Day in the Life

**6:30 AM** — Agent refreshes customer feedback dashboard from data warehouse.
**8:30 AM** — Planning agent reads weekly goals, Slack, and standup doc → posts today's priorities to Slack DM.
**11:00 AM** — You ask "what's our attach rate?" → agent reads the metrics file it updated at 7 AM.
**2:00 PM** — You design an experiment with the agent → output lands in `workspace/llm/`.
**4:58 PM** — Slack sync agent distills two channels into strategic bullets, files them in project updates.
**5:00 PM** — Program update agent posts EOD status to Slack and appends to log.
**Between sessions** — Continual learning mines today's conversations → updates `AGENTS.md`.

None of the scheduled runs require opening a chat. The knowledge base maintains itself.

```
+-------------------------------------------------------+
|  EXTERNAL SOURCES                                     |
|  Slack  |  Data warehouse  |  Google Docs  |  Jira    |
+----------------------------+--------------------------+
                             |
                             v
+-------------------------------------------------------+
|  SCHEDULED AGENTS (cron)                              |
|                                                       |
|  * Storage bar -- what qualifies for curated layer    |
|  * Dedup check -- skip if already captured            |
|  * Cooldown -- don't re-run within 24h                |
+----------------------------+--------------------------+
                             |
                    +--------+--------+
                    |                 |
                    v                 v
          +-----------------+  +-----------------+
          | CURATED         |  | WORKSPACE       |
          | knowledge/      |  | workspace/llm/  |
          |                 |  |                 |
          | Product truth   |  | Agent sandbox   |
          | (governed)      |  | (draft freely)  |
          +--------+--------+  +--------+--------+
                   |                    |
                   |        +-----------+
                   |        | review + promote
                   |        v
                   |   Human reviews workspace
                   |   output, promotes to knowledge/
                   |
                   v
+-------------------------------------------------------+
|  CONTINUAL LEARNING --> AGENTS.md                     |
|  Mines transcripts --> extracts corrections + facts   |
|  --> updates persistent memory (loaded every turn)    |
+-------------------------------------------------------+
```

---

## Context Graph — Memory Layer

PM OS includes a **memory layer** that turns it from a static configuration system into a context graph where reasoning accumulates over time. Inspired by [context graph infrastructure](https://www.linkedin.com/pulse/how-do-you-build-context-graph-jaya-gupta-xicwe/) — the idea that the next wave of AI won't just store data, it will capture the *reasoning* that connects data to decisions.

### How it works

Every agent **reads from memory before starting** (what happened last time, what trends are emerging) and **writes to memory after completing** (structured summary of findings). This creates three capabilities:

| Capability | What it does | How |
|------------|-------------|-----|
| **Temporal awareness** | Agents know what happened before | Feedback analyzer in March knows what February found; weekly planner knows what got done vs. dropped |
| **Cross-agent context** | Agents read each other's outputs | Exec update pulls from feedback, plans, decisions, and reviews — no manual stitching |
| **Compounding intelligence** | Context gets richer over time | More runs → better trend detection, drift analysis, and simulation grounding |

### Memory structure

```
memory/
├── decisions/            # Decision traces — the "why" behind key calls
├── feedback/             # Feedback analyzer outputs over time
├── weekly-plans/         # Weekly planner outputs
├── strategy-reviews/     # Strategy reviewer scorecards
├── exec-updates/         # Executive status updates
└── knowledge-snapshots/  # Versioned snapshots for drift detection
```

### Context graph skills and agents

| Name | Type | What it does |
|------|------|-------------|
| **decision-logger** | Skill | Captures structured decision traces after key PM moments (PRD approvals, scope changes, launch/kill calls) |
| **what-if** | Skill | Simulates impact of proposed decisions using accumulated context — strategy, past decisions, customer feedback, execution history |
| **knowledge-updater** | Skill | Updates knowledge docs with automatic snapshotting for drift detection |
| **retrospective** | Agent | Reads across all memory to surface patterns, strategy drift, execution velocity, and blind spots |

### Getting started with memory

Memory builds automatically as you use PM OS agents. To accelerate:

1. **Log a few key decisions** — Say *"log this decision"* after your next prioritization call or PRD approval
2. **Run feedback analysis** — Each run saves to memory, building a trend baseline
3. **Plan your week** — Weekly plans accumulate, creating an execution history
4. **Run a retrospective** — Say *"retrospective"* once you have 5+ memory entries to see patterns emerge

---

## Manual setup (without the script)

If you prefer not to run the setup script:

- Edit `config/pm-os-config.yaml` with your answers
- Copy `skills/` subfolders to `~/.cursor/skills/`
- Edit templates in `templates/` and copy outputs to `~/.cursor/` (rules, agents)

---

## Requirements

**Required:**
- **Cursor IDE** with MCP support
- **Python 3** (for setup script; `pip install -r requirements.txt`)

**Optional (for agents that connect to external tools):**
- **Slack, Google Drive, GitHub, Figma** — Setup auto-generates `.cursor/mcp.json` for these. You just add your API keys. See [MCP_SETUP.md](MCP_SETUP.md).
- **Jira, Linear, Notion, etc.** — Add via Cursor Settings → Tools & MCP (one-click from Marketplace).

> **15+ skills work immediately without any MCP.** During onboarding, MCPs are the **last step** and **optional** — you can skip and connect them anytime yourself via Cursor Settings → Tools & MCP or the Cursor plugin marketplace. See [MCP_SETUP.md](MCP_SETUP.md).

---

## Feedback Analyzer (Slack)

If you enabled the feedback analyzer:

1. Configure **Slack MCP** in Cursor (Settings → MCP) with access to your feedback channel.
2. In Cursor chat, say: *"Analyze feedback"*, *"Slack feedback analysis"*, or *"Customer feedback"*.
3. The agent searches your configured channel, classifies feedback by theme, and returns a PM report.

See [docs/agents.md](docs/agents.md) for details.

---

## Authors

| | GitHub | Role |
|---|---|---|
| **Sachin** | [@Sach1ng](https://github.com/Sach1ng) | Co-creator |
| **Hardik** | [@hardiktiwari](https://github.com/hardiktiwari) | Co-creator |

## Contributing

To add a new skill, create a folder in `skills/` with a `SKILL.md` following the existing format.

---

## Disclaimer

*This is a personal project and is not affiliated with, endorsed by, or representative of any employer.*

## License

MIT — see [LICENSE](LICENSE) for details.
