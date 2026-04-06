# MCP Setup Guide

When you run `./scripts/setup.sh --copy`, PM-OS **automatically generates** `.cursor/mcp.json` with configs for the MCPs you selected. You just need to add your API keys and tokens.

---

## Quick Start

1. **Run setup** — `./scripts/setup.sh --copy` (or say "onboard" in Cursor)
2. **Open** `.cursor/mcp.json` in this project
3. **Replace placeholders** with your real keys (see below)
4. **Restart Cursor** — MCPs load when you have this repo open

---

## Where to Get Your Keys

### Slack

| Placeholder | Where to get it |
|-------------|-----------------|
| `YOUR_SLACK_BOT_TOKEN` | [Slack API](https://api.slack.com/apps) → Create App → Bot User OAuth Token (starts with `xoxb-`) |
| `YOUR_SLACK_TEAM_ID` | Slack workspace URL: `https://app.slack.com/client/T01234567/` — the `T01234567` part is your Team ID. Or: Workspace settings → Organization ID |

**Steps:** Create a Slack app, add `chat:write`, `channels:history`, `users:read` scopes, install to workspace, copy the Bot Token.

### Google Drive

Uses OAuth — no env vars needed in config. On first use:

1. Run `npx @modelcontextprotocol/server-gdrive auth`
2. Follow the browser flow to authorize
3. Credentials save to `~/.gdrive-server-credentials.json`

If you hit auth issues, see [server-gdrive README](https://github.com/modelcontextprotocol/servers/tree/main/src/gdrive).

### GitHub

| Placeholder | Where to get it |
|-------------|-----------------|
| `YOUR_GITHUB_TOKEN` | [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens) → Generate (classic) → enable `repo`, `read:org` |

### Figma

**Hosted Figma MCP** (default): No keys needed — uses Figma's hosted MCP. When you use it, you'll be prompted to authorize in the browser.

**Figma Context MCP** (Framelink — optional): For layout/design data that improves one-shot implementation, PM-OS can add [Figma Context MCP](https://github.com/GLips/Figma-Context-MCP) (Framelink). Setup adds it when you enable Figma during onboarding.

| Placeholder | Where to get it |
|-------------|-----------------|
| `YOUR_FIGMA_API_KEY` | [Figma account → Settings → Personal access tokens](https://www.figma.com/settings) → Generate new token |

Config (auto-added when Figma is enabled): `npx -y figma-developer-mcp --stdio` with `FIGMA_API_KEY` in env.

### Browser (Playwright)

**No keys needed.** Enabled by default. Uses [`@playwright/mcp`](https://www.npmjs.com/package/@playwright/mcp) (official repo: [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)) to give Cursor a browser it can control — navigate pages, click buttons, fill forms, take screenshots. Requires Node.js 18+.

Works out of the box for testing web apps, verifying UI changes, or walking through demo flows. For Cursor install steps, config options, and tools list, see the [Playwright MCP README](https://github.com/microsoft/playwright-mcp).

---

### Atlassian (Jira, Confluence, Compass)

When you enable **Jira** or **Confluence** in onboarding, setup adds the [Atlassian Rovo MCP Server](https://github.com/atlassian/atlassian-mcp-server) to `.cursor/mcp.json` (remote URL: `https://mcp.atlassian.com/v1/mcp`).

- **Auth:** On first use in Cursor, complete the **OAuth 2.1** flow in your browser (or use an API token if your org enables it).
- **No placeholder keys** — authorize when Cursor prompts you.
- **Docs:** [Atlassian MCP Server README](https://github.com/atlassian/atlassian-mcp-server) — prerequisites, permissions, troubleshooting.

### Google Workspace CLI (optional — not an MCP)

For full **Google Workspace** access (Drive, Gmail, Calendar, Sheets, Docs, Chat) from the command line and for AI agents, you can install the [Google Workspace CLI](https://github.com/googleworkspace/cli) (`gws`). This is separate from the Google Drive MCP; use it when you want CLI/scripted access.

1. **Install:** `npm install -g @googleworkspace/cli`
2. **One-time setup:** `gws auth setup` (creates GCP project, enables APIs, OAuth login)
3. **Subsequent login:** `gws auth login`

Then use `gws drive ...`, `gws gmail ...`, etc. No entry in `.cursor/mcp.json` — it's a CLI. See [gws README](https://github.com/googleworkspace/cli) for agent skills and Gemini CLI extension.

---

## Other MCPs (Linear, Notion, etc.)

For MCPs not in our auto-generated config, use **one-click install** from Cursor:

1. Open Cursor → **Settings** (Cmd+,) → **Tools & MCP**
2. Click **Add** or browse the [Cursor Marketplace](https://cursor.com/marketplace)
3. Search for the tool (e.g., "Jira", "Linear", "Notion")
4. Click **Add to Cursor** — it installs and configures for you

| MCP | Notes |
|-----|-------|
| Jira / Confluence | Auto-added when you enable them in onboarding (Atlassian MCP). See **Atlassian** above. |
| Linear | [Linear plugin](https://cursor.com/marketplace) — one-click |
| Notion | Search "Notion" in Marketplace |
| Databricks | Search "Databricks" in Marketplace |

---

## Troubleshooting

**MCPs not loading?**
- Restart Cursor after editing `mcp.json`
- Check **Settings → Tools & MCP** — toggle the server off/on
- View **Output → MCP Logs** for errors

**Slack: "invalid_auth"?**
- Regenerate your Bot Token
- Ensure the app is installed to your workspace
- Check Team ID matches your workspace

**Google Drive: auth fails?**
- Run `npx @modelcontextprotocol/server-gdrive auth` in terminal
- Ensure you have a Google Cloud project with Drive API enabled (for custom setups)

**Project vs global config**
- `.cursor/mcp.json` in this repo = **project-level** — only active when PM-OS is open
- `~/.cursor/mcp.json` = **global** — active in all projects
- We use project-level so your work MCPs stay scoped to this setup
