#!/usr/bin/env bash

#######################################
# vizard uninstallation script
#######################################

set -euo pipefail

INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/vizard"
BIN_DIR="$HOME/.local/bin"

# Colors
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
NC=$'\033[0m'

echo ""
echo "Uninstalling vizard..."
echo ""

# Remove symlink
if [ -L "$BIN_DIR/vizard" ] || [ -f "$BIN_DIR/vizard" ]; then
    rm -f "$BIN_DIR/vizard"
    echo -e "${GREEN}✓${NC} Removed vizard command"
else
    echo -e "${YELLOW}⚠${NC} vizard command not found"
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}✓${NC} Removed vizard installation"
else
    echo -e "${YELLOW}⚠${NC} vizard installation directory not found"
fi

echo ""
echo -e "${GREEN}✓ vizard uninstalled${NC}"
echo ""
echo -e "${YELLOW}Note:${NC} Per-project files (.venv, notebooks, etc.) were not removed"
echo "      Use 'vizard clean --purge' in project directories before uninstalling"
echo "      if you want to clean up project-specific files."
echo ""
