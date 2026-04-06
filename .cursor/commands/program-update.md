# program-update

Generate and post a daily program update across all active workstreams.

## Steps

1. **Gather** content for each workstream: status (one line), wins/progress, blockers/risks, next/focus.
   - Read Daily Standup doc (Google Drive: `YOUR_STANDUP_DOC_ID`) and Monday Planning doc (`YOUR_MONDAY_PLANNING_DOC_ID`).
   - Search Slack (last 24h) for relevant terms across your workstreams.

2. **Format** the message using this template (Slack mrkdwn):

```
*Daily Program Update — [Today's date]*

*1. [Workstream A]*
• Status: [one line]
• [Win/progress]
• [Blocker/risk if any]
• Next: [focus]

*2. [Workstream B]*
• Status: [one line]
• [Win/progress]
• [Blocker/risk if any]
• Next: [focus]
```

3. **Send to Slack** — `slack_send_dm` with `user_id` `YOUR_SLACK_USER_ID`.

4. **Update the log** — Append to `daily-program-update-slack.md` (newest first).

5. **Update project files** — For each workstream with meaningful updates:
   - Append dated entry to `knowledge/projects/<project>/updates.md`
   - Refresh `knowledge/projects/<project>/brief.md` if status materially changed.

6. **Confirm** to user.
