#!/usr/bin/env bash
#
# PM OS Scheduler — Setup
#
# Installs dependencies, verifies API keys, and creates a macOS launchd
# agent so the scheduler starts automatically on login.
#
# Usage:
#   bash scheduler/setup.sh           # Full setup
#   bash scheduler/setup.sh --uninstall  # Remove launchd agent

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PLIST_NAME="com.pm-os.scheduler"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
VENV_DIR="$SCRIPT_DIR/.venv"
ENV_FILE="$SCRIPT_DIR/.env"

echo "=== PM OS Scheduler Setup ==="
echo

if [[ "$1" == "--uninstall" ]]; then
    echo "Uninstalling scheduler..."
    if launchctl list | grep -q "$PLIST_NAME" 2>/dev/null; then
        launchctl unload "$PLIST_PATH" 2>/dev/null || true
        launchctl bootout "gui/$(id -u)/$PLIST_NAME" 2>/dev/null || true
    fi
    rm -f "$PLIST_PATH"
    echo "  Done. Virtual env at $VENV_DIR preserved (delete manually if desired)."
    exit 0
fi

echo "1. Checking Python..."
if ! command -v python3 &>/dev/null; then
    echo "   Error: python3 is required."
    exit 1
fi
echo "   OK"

echo "2. Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "   Created $VENV_DIR"
else
    echo "   Exists: $VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet -r "$SCRIPT_DIR/requirements.txt"
echo "   Dependencies installed"

echo "3. Checking .env..."
if [ ! -f "$ENV_FILE" ]; then
    cp "$SCRIPT_DIR/.env.example" "$ENV_FILE"
    echo "   Created $ENV_FILE from template — fill in your API keys!"
    NEEDS_KEYS=true
else
    echo "   $ENV_FILE exists"
    NEEDS_KEYS=false
fi

echo "4. Verifying API keys..."
source "$ENV_FILE" 2>/dev/null || true
KEYS_OK=true
if [[ -z "$ANTHROPIC_API_KEY" || "$ANTHROPIC_API_KEY" == sk-ant-... ]]; then
    echo "   ANTHROPIC_API_KEY not set"
    KEYS_OK=false
else
    echo "   ANTHROPIC_API_KEY set"
fi
if [[ -z "$SLACK_BOT_TOKEN" || "$SLACK_BOT_TOKEN" == xoxb-... ]]; then
    echo "   SLACK_BOT_TOKEN not set"
    KEYS_OK=false
else
    echo "   SLACK_BOT_TOKEN set"
fi

echo "5. Creating launchd agent..."
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST_PATH" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${VENV_DIR}/bin/python</string>
        <string>${SCRIPT_DIR}/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${PROJECT_ROOT}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>$(printf '%s' "$HOME")</string>
        <key>PATH</key>
        <string>${VENV_DIR}/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>StandardOutPath</key>
    <string>${SCRIPT_DIR}/scheduler-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>${SCRIPT_DIR}/scheduler-stderr.log</string>
    <key>ProcessType</key>
    <string>Background</string>
    <key>ThrottleInterval</key>
    <integer>30</integer>
</dict>
</plist>
PLIST
echo "   Created $PLIST_PATH"

echo "6. Loading scheduler agent..."
if [[ "$KEYS_OK" == true ]]; then
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    if launchctl load "$PLIST_PATH" 2>/dev/null; then
        echo "   Scheduler loaded (runs at login)"
    else
        echo "   launchctl failed — try: launchctl bootstrap gui/\$(id -u) $PLIST_PATH"
    fi
else
    echo "   Scheduler NOT started — fill API keys in $ENV_FILE, then re-run setup.sh"
fi

echo
echo "=== Setup Complete ==="
echo
echo "Commands:"
echo "  python3 scheduler/main.py --doctor    # Diagnostics"
echo "  python3 scheduler/main.py             # Foreground scheduler"
echo "  python3 scheduler/main.py --run planday  # Run one command"
echo "  python3 scheduler/main.py --list         # All jobs"
echo "  bash scheduler/setup.sh --uninstall     # Remove LaunchAgent"
echo
if [[ "$KEYS_OK" != true ]]; then
    echo "ACTION NEEDED: Edit scheduler/.env with API keys, then re-run setup.sh"
fi
