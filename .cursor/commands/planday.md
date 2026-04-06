# planday

Run the daily planning workflow:

1. Read weekly goals from Monday Planning doc (Google Drive: `YOUR_MONDAY_PLANNING_DOC_ID`)
2. Ingest Slack messages from last 24h (`from:me OR to:me`, count: 30)
3. Read the last update from daily standup doc (Google Drive: `YOUR_STANDUP_DOC_ID`)
4. Assess progress on each weekly goal with status emojis
5. Identify spillovers from the last daily update and place them into P0, P1, or Backlog
6. Build today's priorities tied to weekly goals in this structure: P0, P1, Backlog
7. Include a concise Yesterday Summary (completed, in progress, blocked)
8. Send the full plan to my Slack DM (user_id: `YOUR_SLACK_USER_ID`)
9. Update the daily standup doc

Output format:
1. Weekly goals and progress
2. P0
3. P1
4. Backlog
5. Yesterday summary

Use the weekly-planner skill for full instructions.
