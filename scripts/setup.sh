#!/bin/bash
# PM Operating System — Setup wrapper
# Runs setup.py; installs deps if needed.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Check for Python 3
if ! command -v python3 &>/dev/null; then
  echo "Error: python3 not found. Please install Python 3."
  exit 1
fi

# Install deps if needed
if ! python3 -c "import yaml, jinja2" 2>/dev/null; then
  echo "Installing dependencies (PyYAML, Jinja2)..."
  pip install -r requirements.txt -q
fi

# Run setup
python3 scripts/setup.py "$@"
