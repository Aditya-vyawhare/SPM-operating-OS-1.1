# slack-sync

Sync strategic content from Slack channels to project knowledge files.

## Steps

1. **Read channel messages** — Get the last 75 messages from each configured channel:
   - Channel 1: `YOUR_CHANNEL_ID_1` (e.g. team working channel)
   - Channel 2: `YOUR_CHANNEL_ID_2` (e.g. cross-functional channel)

2. **Apply storage bar** — Only write content that meets these criteria:
   - Strategic decisions or direction changes
   - Durable learnings (experiment results, customer insights)
   - Milestone announcements or blockers
   - **Skip:** routine status, social chatter, meeting logistics, duplicates

3. **Check for duplicates** — Read the target `knowledge/projects/<project>/updates.md`. Skip any content already captured.

4. **Write updates** — For qualifying content:
   - Append a dated entry to `knowledge/projects/<project>/updates.md` (newest first)
   - Tag each entry with `[Slack]` source
   - If metrics are mentioned, also append to `knowledge/projects/<project>/metrics.md`

5. **Respect cooldown** — Check `.cursor/hooks/state/slack-sync-last-run.json`. If last run was < 24h ago, skip unless user passes `--force` or `force`.

6. **Record run** — Update the cooldown state file with current timestamp.
