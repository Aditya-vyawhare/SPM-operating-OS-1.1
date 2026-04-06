"""
Tool implementations for the scheduler executor.

Provides Slack, Google Drive, and filesystem tools that Claude can call
via tool_use during command execution.

Required env vars:
    SLACK_BOT_TOKEN  — Slack Bot User OAuth Token (xoxb-...)
    GOOGLE_CREDENTIALS_PATH — Path to Google OAuth credentials JSON (optional)
"""

import json
import logging
import os
from pathlib import Path

log = logging.getLogger("scheduler.tools")

TOOL_DEFINITIONS = [
    {
        "name": "slack_send_dm",
        "description": "Send a direct message to a Slack user by user ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Slack user ID (e.g. W012WHKRA4C)"},
                "text": {"type": "string", "description": "Message text (supports Slack mrkdwn)"},
            },
            "required": ["user_id", "text"],
        },
    },
    {
        "name": "slack_send_message",
        "description": "Send a message to a Slack channel by channel name or ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "channel": {"type": "string", "description": "Channel name or ID"},
                "text": {"type": "string", "description": "Message text (supports Slack mrkdwn)"},
            },
            "required": ["channel", "text"],
        },
    },
    {
        "name": "slack_search_messages",
        "description": "Search Slack messages matching a query.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Slack search query"},
                "count": {"type": "integer", "description": "Max results (default 20)"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "slack_get_channel_messages",
        "description": "Get recent messages from a Slack channel.",
        "input_schema": {
            "type": "object",
            "properties": {
                "channel": {"type": "string", "description": "Channel ID or name"},
                "limit": {"type": "integer", "description": "Max messages (default 75, max 100)"},
            },
            "required": ["channel"],
        },
    },
    {
        "name": "read_google_doc",
        "description": "Read a Google Doc by document ID. Returns plain text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "document_id": {"type": "string", "description": "Google Doc ID"},
            },
            "required": ["document_id"],
        },
    },
    {
        "name": "read_file",
        "description": "Read a local file and return its contents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute or project-relative file path"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a local file. Supports overwrite, prepend, and append modes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute or project-relative file path"},
                "content": {"type": "string", "description": "Content to write"},
                "mode": {
                    "type": "string",
                    "enum": ["overwrite", "prepend", "append"],
                    "description": "Write mode (default: overwrite)",
                },
            },
            "required": ["path", "content"],
        },
    },
]

_slack_client = None
_gdrive_service = None
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _get_slack_client():
    global _slack_client
    if _slack_client is None:
        from slack_sdk import WebClient
        token = os.environ.get("SLACK_BOT_TOKEN")
        if not token:
            raise RuntimeError("SLACK_BOT_TOKEN not set. Add it to scheduler/.env")
        _slack_client = WebClient(token=token)
    return _slack_client


def _get_gdrive_service():
    global _gdrive_service
    if _gdrive_service is not None:
        return _gdrive_service

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]
    token_path = PROJECT_ROOT / "scheduler" / ".gdrive_token.json"
    creds_path = os.environ.get(
        "GOOGLE_CREDENTIALS_PATH",
        str(PROJECT_ROOT / "scheduler" / "credentials.json"),
    )

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not Path(creds_path).exists():
                raise RuntimeError(
                    f"Google credentials not found at {creds_path}. "
                    "Download OAuth Desktop credentials from Google Cloud Console "
                    "and save as scheduler/credentials.json"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    _gdrive_service = build("docs", "v1", credentials=creds)
    return _gdrive_service


def _slack_send_dm(user_id: str, text: str) -> dict:
    client = _get_slack_client()
    resp = client.conversations_open(users=[user_id])
    channel_id = resp["channel"]["id"]
    result = client.chat_postMessage(channel=channel_id, text=text)
    return {"ok": result["ok"], "channel": channel_id, "ts": result["ts"]}


def _slack_send_message(channel: str, text: str) -> dict:
    client = _get_slack_client()
    result = client.chat_postMessage(channel=channel, text=text)
    return {"ok": result["ok"], "channel": channel, "ts": result["ts"]}


def _slack_search(query: str, count: int = 20) -> dict:
    client = _get_slack_client()
    result = client.search_messages(query=query, count=count, sort="timestamp", sort_dir="desc")
    messages = result.get("messages", {}).get("matches", [])
    return {
        "total": result.get("messages", {}).get("total", 0),
        "matches": [
            {
                "text": m.get("text", ""), "user": m.get("user", ""),
                "channel": m.get("channel", {}).get("name", ""),
                "ts": m.get("ts", ""), "permalink": m.get("permalink", ""),
            }
            for m in messages[:count]
        ],
    }


def _slack_get_channel_messages(channel: str, limit: int = 75) -> dict:
    client = _get_slack_client()
    limit = max(1, min(int(limit or 75), 100))
    ref = channel.strip().lstrip("#")
    channel_id = ref
    if not (ref.startswith("C") or ref.startswith("G")):
        cursor = None
        while True:
            kwargs = {"types": "public_channel,private_channel", "limit": 200}
            if cursor:
                kwargs["cursor"] = cursor
            resp = client.conversations_list(**kwargs)
            for ch in resp.get("channels", []):
                if ch.get("name") == ref:
                    channel_id = ch["id"]
                    break
            else:
                cursor = resp.get("response_metadata", {}).get("next_cursor")
                if not cursor:
                    raise ValueError(f"Channel not found: {channel}")
                continue
            break

    result = client.conversations_history(channel=channel_id, limit=limit)
    messages = result.get("messages", [])
    return {
        "channel_id": channel_id, "count": len(messages),
        "messages": [
            {"user": m.get("user", ""), "text": m.get("text", ""), "ts": m.get("ts", "")}
            for m in messages
        ],
    }


def _read_google_doc(document_id: str) -> str:
    service = _get_gdrive_service()
    doc = service.documents().get(documentId=document_id).execute()
    content = doc.get("body", {}).get("content", [])
    text_parts = []
    for element in content:
        if "paragraph" in element:
            for run in element["paragraph"].get("elements", []):
                text_content = run.get("textRun", {}).get("content", "")
                if text_content:
                    text_parts.append(text_content)
    return "".join(text_parts)


def _resolve_path(path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else PROJECT_ROOT / p


def _read_file(path: str) -> str:
    resolved = _resolve_path(path)
    if not resolved.exists():
        return f"File not found: {resolved}"
    return resolved.read_text()


def _write_file(path: str, content: str, mode: str = "overwrite") -> dict:
    resolved = _resolve_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    if mode == "append":
        with open(resolved, "a") as f:
            f.write(content)
    elif mode == "prepend":
        existing = resolved.read_text() if resolved.exists() else ""
        resolved.write_text(content + existing)
    else:
        resolved.write_text(content)
    return {"ok": True, "path": str(resolved), "mode": mode}


_DISPATCH = {
    "slack_send_dm": lambda inp: _slack_send_dm(inp["user_id"], inp["text"]),
    "slack_send_message": lambda inp: _slack_send_message(inp["channel"], inp["text"]),
    "slack_search_messages": lambda inp: _slack_search(inp["query"], inp.get("count", 20)),
    "slack_get_channel_messages": lambda inp: _slack_get_channel_messages(inp["channel"], inp.get("limit", 75)),
    "read_google_doc": lambda inp: _read_google_doc(inp["document_id"]),
    "read_file": lambda inp: _read_file(inp["path"]),
    "write_file": lambda inp: _write_file(inp["path"], inp["content"], inp.get("mode", "overwrite")),
}


def dispatch_tool(name: str, inputs: dict):
    handler = _DISPATCH.get(name)
    if not handler:
        raise ValueError(f"Unknown tool: {name}")
    return handler(inputs)
