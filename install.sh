#!/bin/bash

# Script to auto-generate the anime_downloader.desktop file

# Set variables
APP_NAME="Anime Downloader"
COMMENT="Download anime episodes with a modern GUI"
PYTHON_PATH="$(which python3)"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_DIR/.venv/bin/python"
MAIN_PATH="$PROJECT_DIR/src/main.py"
DESKTOP_FILE="$PROJECT_DIR/anime_downloader.desktop"
ICON_NAME="applications-multimedia"
CATEGORIES="AudioVideo;Video;"
TERMINAL="false"
STARTUP_NOTIFY="true"

# Use venv python if exists, else fallback to system python
if [ -x "$VENV_PATH" ]; then
    EXEC="$VENV_PATH $MAIN_PATH"
else
    EXEC="$PYTHON_PATH $MAIN_PATH"
fi

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_NAME
Comment=$COMMENT
Exec=$EXEC
Icon=$ICON_NAME
Terminal=$TERMINAL
Categories=$CATEGORIES
StartupNotify=$STARTUP_NOTIFY
EOF

echo "Desktop entry generated at: $DESKTOP_FILE"

# Optionally, make it executable and suggest installation
chmod +x "$DESKTOP_FILE"
echo "You can move it to ~/.local/share/applications/ to add it to your app menu:"
echo "  mv \"$DESKTOP_FILE\" ~/.local/share/applications/"
