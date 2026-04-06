# Agent Schedule — Cadence Map

Overview of all automated agent runs, whether triggered by the headless scheduler (`scheduler/main.py`) or Cursor-native IDE cron (`.cursor/agent-schedules.json`).

## Daily Schedule

| Time | Command | Source | What it does |
|------|---------|--------|-------------|
| 8:30 AM (Mon-Fri) | `/planday` | IDE cron + scheduler | Reads weekly goals, Slack, builds P0/P1/Backlog, sends to Slack DM |
| 4:58 PM (daily) | `/slack-sync` | IDE cron + scheduler | Syncs strategic Slack content to project knowledge files (24h cooldown) |
| 5:00 PM (Mon-Fri) | `/program-update` | IDE cron + scheduler | EOD status across workstreams → Slack + log |

## Continual Learning

Runs automatically via the [Continual Learning plugin](https://cursor.com/marketplace/cursor/continual-learning) after every agent conversation. No cron needed — the `stop` hook triggers it.

## Adding a New Scheduled Command

1. Create a slash command in `.cursor/commands/<name>.md`
2. Add an entry to `.cursor/agent-schedules.json` for IDE-native cron
3. (Optional) Add an entry to `scheduler/main.py` `SCHEDULE_CONFIG` for headless runs
4. Update this file

## Two Execution Modes

| Mode | How it runs | Requires |
|------|------------|----------|
| **IDE cron** (`.cursor/agent-schedules.json`) | Cursor runs the command when the IDE is open | Cursor open |
| **Headless scheduler** (`scheduler/main.py`) | Python process runs independently via macOS LaunchAgent | `scheduler/.env` with API keys |

Both can run the same commands. The headless scheduler is useful for runs that should happen even when Cursor is closed.
