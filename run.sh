#!/bin/bash
# Anime Downloader Launcher Script

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment and run the application
cd "$SCRIPT_DIR"
.venv/bin/python src/main.py "$@"
