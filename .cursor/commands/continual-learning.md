# continual-learning

Run the `continual-learning` skill now. Use the `agents-memory-updater` subagent for the full memory update flow.

## Incremental transcript processing

Use the index file at `.cursor/hooks/state/continual-learning-index.json`.

1. **Read the index** — get previously indexed transcripts and their `mtimeMs` values.
2. **List transcripts** on disk (each `<uuid>/<uuid>.jsonl` in the agent-transcripts folder).
3. **Diff against index:**
   - New file (not in index) → process it.
   - Existing file with `mtimeMs` newer than indexed value → process it.
   - Matching `mtimeMs` → skip.
4. **Remove stale entries** — delete index entries whose files no longer exist on disk.

## Extract high-signal content from new/updated transcripts

For each transcript to process, extract only:

- Recurring user corrections (things the user corrected the agent on 2+ times)
- Durable workspace facts (file locations, conventions, tool configs, data schemas)

Exclude: one-off tasks, transient debugging, secrets/credentials, ephemeral data.

## Update AGENTS.md

1. Read current contents.
2. De-duplicate — skip facts already captured.
3. Append genuinely new, durable entries under the appropriate section:
   - `## Learned User Preferences` — behavioral corrections and interaction patterns.
   - `## Learned Workspace Facts` — file locations, schemas, conventions, tool configs.

## Update project folders

Using the **same transcripts**, check for durable product-specific updates:
- Metrics snapshots, experiment status/results, brief-worthy status changes.
- Write into `knowledge/projects/<product>/` files (`updates.md` newest first, `metrics.md` date-stamped, `brief.md` only if status materially changed).

## Refresh the index

Set `mtimeMs` for all processed transcripts to their current mtime. Remove deleted entries. Write back to the index file.

## If no updates

If no meaningful updates exist after processing, respond exactly: `No high-signal memory updates.`
