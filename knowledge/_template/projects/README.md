# Project Dossier Pattern

Each project (product, initiative, experiment) gets its own folder under `knowledge/projects/`. Copy this template folder and rename it for your project.

## Structure

```
knowledge/projects/my-project/
├── brief.md        # What is this project (living doc, updated when status changes)
├── updates.md      # What changed, newest first (agents append here)
├── metrics.md      # Dated metric snapshots (agents append here)
└── experiments/    # Experiment docs (one per experiment)
    └── _template.md
```

## Conventions

- **brief.md** — Read first. Agents and humans reference this for current state. Only update when status, scope, or direction materially changes.
- **updates.md** — Append-only, newest first. Each entry has a date and source tag (`[Slack]`, `[Standup]`, `[Manual]`). The Slack sync and program update commands write here automatically.
- **metrics.md** — Date-stamped snapshots. When metrics change, append a new dated section. Never overwrite old snapshots — they provide trend history.
- **experiments/** — One markdown file per experiment. Use `_template.md` as a starting point.
