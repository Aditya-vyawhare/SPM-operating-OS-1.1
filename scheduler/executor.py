"""
Command executor — sends command prompts to Claude API with tool_use.

Reads the command .md file, builds a system prompt with member context,
and runs a tool_use conversation loop until Claude finishes. Tools:
Slack (send/search), Google Drive (read doc), filesystem (read/write).
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / "scheduler" / ".env")

import anthropic

from tools import TOOL_DEFINITIONS, dispatch_tool

log = logging.getLogger("scheduler.executor")

MODEL = "claude-sonnet-4-20250514"
MAX_TURNS = 15


def _build_system_prompt() -> str:
    member_path = PROJECT_ROOT / "config" / "pm-os-config.yaml"
    member_context = ""
    if member_path.exists():
        member_context = member_path.read_text()

    return f"""You are a PM OS agent scheduler. You execute PM workflow commands
automatically. You have access to Slack, Google Drive, and the local filesystem via tools.

Follow the command instructions exactly. When the command says to post to Slack, use the
slack_send_dm or slack_send_message tool. When it says to read a Google Doc, use the
read_google_doc tool. When it says to update a local file, use write_file.

Today's date: {datetime.now().strftime('%A %B %d, %Y')}

Config:
{member_context}

Important:
- Execute the full workflow described in the command.
- Use tools for all external operations (Slack, Google Drive, files).
- Be concise in Slack messages.
- If a tool fails, log the error and continue with the rest of the workflow.
- Return a brief summary of what you did when finished.
"""


def execute_command(name: str, command_path: Path) -> dict:
    command_content = command_path.read_text()
    client = anthropic.Anthropic()

    system_prompt = _build_system_prompt()
    messages = [{"role": "user", "content": f"Execute this command now:\n\n{command_content}"}]

    log.info(f"Executing command: {name}")

    for turn in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL, max_tokens=4096,
            system=system_prompt, tools=TOOL_DEFINITIONS, messages=messages,
        )

        if response.stop_reason == "end_turn":
            final_text = ""
            for block in response.content:
                if block.type == "text":
                    final_text += block.text
            log.info(f"Command {name} completed in {turn + 1} turn(s)")
            return {"status": "success", "summary": final_text, "turns": turn + 1}

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    log.info(f"  Tool call: {block.name}({json.dumps(block.input)[:200]})")
                    try:
                        result = dispatch_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result", "tool_use_id": block.id,
                            "content": json.dumps(result) if isinstance(result, (dict, list)) else str(result),
                        })
                    except Exception as e:
                        log.error(f"  Tool error: {block.name} — {e}")
                        tool_results.append({
                            "type": "tool_result", "tool_use_id": block.id,
                            "content": f"Error: {e}", "is_error": True,
                        })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            log.warning(f"Unexpected stop_reason: {response.stop_reason}")
            return {"status": "error", "summary": f"Unexpected stop: {response.stop_reason}"}

    log.warning(f"Command {name} hit max turns ({MAX_TURNS})")
    return {"status": "max_turns", "summary": f"Reached {MAX_TURNS} turns without completing"}
