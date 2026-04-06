#!/usr/bin/env python3
"""
PM OS — Automatic Agent Scheduler

Runs scheduled commands (planday, slack-sync, program-update, etc.)
at configured times. Each command is executed by sending its prompt to the
Claude API with tool_use for Slack, Google Drive, and filesystem operations.

Usage:
    python scheduler/main.py              # Run the schedule loop
    python scheduler/main.py --run planday # Run a single command immediately
    python scheduler/main.py --list       # List all scheduled commands
    python scheduler/main.py --doctor     # Diagnose LaunchAgent, venv, .env
    python scheduler/main.py --dry-run    # Show schedule without executing
"""

import argparse
import json
import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / "scheduler" / ".env")

import schedule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PROJECT_ROOT / "scheduler" / "scheduler.log"),
    ],
)
log = logging.getLogger("scheduler")


# ---------------------------------------------------------------------------
# Schedule config — customize command names, files, and times to your workflow
# ---------------------------------------------------------------------------

SCHEDULE_CONFIG = {
    "planday": {
        "file": ".cursor/commands/planday.md",
        "schedule": "weekdays_at_0830",
        "description": "Morning planning — weekly goals, priorities, Slack DM",
    },
    "slack-sync": {
        "file": ".cursor/commands/slack-sync.md",
        "schedule": "daily_at_1658",
        "description": "Slack channel sync — strategic learnings → project updates.md",
    },
    "program-update": {
        "file": ".cursor/commands/program-update.md",
        "schedule": "weekdays_at_1700",
        "description": "EOD status across workstreams → Slack + log",
    },
}

SLACK_SYNC_STATE = PROJECT_ROOT / ".cursor" / "hooks" / "state" / "slack-sync-last-run.json"
SLACK_SYNC_COOLDOWN_SEC = 24 * 60 * 60


def _slack_sync_seconds_since_last_run() -> Optional[float]:
    if not SLACK_SYNC_STATE.is_file():
        return None
    try:
        data = json.loads(SLACK_SYNC_STATE.read_text())
        ts = data.get("lastRunAt")
        if not ts:
            return None
        if ts.endswith("Z"):
            last = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            last = datetime.fromisoformat(ts)
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - last).total_seconds()
    except Exception as e:
        log.warning(f"Could not read slack-sync state: {e}")
        return None


def _slack_sync_should_run(force: bool) -> Tuple[bool, str]:
    if force:
        return True, ""
    elapsed = _slack_sync_seconds_since_last_run()
    if elapsed is None:
        return True, ""
    if elapsed < SLACK_SYNC_COOLDOWN_SEC:
        remaining_h = (SLACK_SYNC_COOLDOWN_SEC - elapsed) / 3600
        return False, (
            f"Skipping slack-sync: last run {elapsed/3600:.1f}h ago "
            f"({remaining_h:.1f}h left in 24h cooldown). Use --force to bypass."
        )
    return True, ""


def _slack_sync_record_run(source: str = "scheduler") -> None:
    SLACK_SYNC_STATE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "lastRunAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lastRunSource": source,
    }
    SLACK_SYNC_STATE.write_text(json.dumps(payload, indent=2) + "\n")


def run_command(name: str, dry_run: bool = False, force: bool = False):
    config = SCHEDULE_CONFIG.get(name)
    if not config:
        log.error(f"Unknown command: {name}")
        return

    if name == "slack-sync" and not dry_run:
        ok, skip_msg = _slack_sync_should_run(force=force)
        if not ok:
            log.info(skip_msg)
            return

    log.info(f"{'[DRY RUN] ' if dry_run else ''}Running: {name} — {config['description']}")
    if dry_run:
        return

    try:
        if "script" in config:
            script_path = PROJECT_ROOT / config["script"]
            if not script_path.exists():
                log.error(f"Script not found: {script_path}")
                return
            proc = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(PROJECT_ROOT),
                capture_output=True, text=True, check=False,
            )
            if proc.returncode == 0:
                log.info(f"Completed: {name}")
            else:
                log.error(f"Failed: {name} (exit={proc.returncode})")
                if proc.stderr.strip():
                    log.error(proc.stderr.strip())
            return

        command_path = PROJECT_ROOT / config["file"]
        if not command_path.exists():
            log.error(f"Command file not found: {command_path}")
            return
        from executor import execute_command
        result = execute_command(name, command_path)
        log.info(f"Completed: {name} — {result.get('status', 'unknown')}")
        if name == "slack-sync" and result.get("status") == "success":
            _slack_sync_record_run(source="scheduler" if not force else "scheduler-force")
    except Exception:
        log.exception(f"Failed: {name}")


def setup_schedule(dry_run: bool = False):
    def job(name):
        return lambda: run_command(name, dry_run)

    schedule.every().monday.at("08:30").do(job("planday"))
    schedule.every().tuesday.at("08:30").do(job("planday"))
    schedule.every().wednesday.at("08:30").do(job("planday"))
    schedule.every().thursday.at("08:30").do(job("planday"))
    schedule.every().friday.at("08:30").do(job("planday"))

    schedule.every().day.at("16:58").do(job("slack-sync"))

    schedule.every().monday.at("17:00").do(job("program-update"))
    schedule.every().tuesday.at("17:00").do(job("program-update"))
    schedule.every().wednesday.at("17:00").do(job("program-update"))
    schedule.every().thursday.at("17:00").do(job("program-update"))
    schedule.every().friday.at("17:00").do(job("program-update"))

    log.info("Schedule registered:")
    for j in schedule.get_jobs():
        log.info(f"  {j}")


def print_doctor():
    plist = Path.home() / "Library/LaunchAgents/com.pm-os.scheduler.plist"
    env_path = PROJECT_ROOT / "scheduler" / ".env"
    venv_py = PROJECT_ROOT / "scheduler" / ".venv" / "bin" / "python"

    print("\n=== PM OS scheduler doctor ===\n")

    print("1. macOS LaunchAgent")
    if plist.is_file():
        print(f"   OK  Plist exists: {plist}")
    else:
        print(f"   !!  Missing: {plist}")
        print("       Fix: bash scheduler/setup.sh")
    print()

    print("2. Virtualenv")
    if venv_py.is_file():
        print(f"   OK  {venv_py}")
    else:
        print("   !!  Missing — run: python3 -m venv scheduler/.venv && pip install -r scheduler/requirements.txt")
    print()

    print("3. API keys (scheduler/.env)")
    if env_path.is_file():
        print(f"   OK  {env_path} exists")
        load_dotenv(env_path)
        ak = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        sk = os.environ.get("SLACK_BOT_TOKEN", "").strip()
        print(f"   {'OK' if len(ak) > 20 else '!!'} ANTHROPIC_API_KEY")
        print(f"   {'OK' if sk.startswith('xoxb-') else '!!'} SLACK_BOT_TOKEN")
    else:
        print(f"   !!  Missing — copy from scheduler/.env.example")
    print()

    print("4. Quick test: python3 scheduler/main.py --list\n")


def list_commands():
    print("\nAvailable commands:\n")
    timing_map = {
        "weekdays_at_0830": "Mon-Fri 8:30 AM",
        "daily_at_1658": "Daily 4:58 PM (24h cooldown)",
        "weekdays_at_1700": "Mon-Fri 5:00 PM",
    }
    for name, config in SCHEDULE_CONFIG.items():
        timing = timing_map.get(config["schedule"], config["schedule"])
        print(f"  {name:25s} {timing:30s} {config['description']}")
    print()


def main():
    parser = argparse.ArgumentParser(description="PM OS Agent Scheduler")
    parser.add_argument("--run", metavar="COMMAND", help="Run a single command immediately")
    parser.add_argument("--list", action="store_true", help="List all scheduled commands")
    parser.add_argument("--dry-run", action="store_true", help="Show schedule without executing")
    parser.add_argument("--force", action="store_true", help="Bypass 24h cooldown for slack-sync")
    parser.add_argument("--doctor", action="store_true", help="Print diagnostics for auto-run")
    args = parser.parse_args()

    if args.doctor:
        print_doctor()
        return
    if args.list:
        list_commands()
        return
    if args.run:
        run_command(args.run, force=args.force)
        return

    def shutdown(signum, frame):
        log.info("Shutting down scheduler...")
        sys.exit(0)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    log.info("PM OS Scheduler starting (pid=%s)", os.getpid())
    log.info(f"Project root: {PROJECT_ROOT}")
    setup_schedule(args.dry_run)

    log.info("Scheduler running. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
