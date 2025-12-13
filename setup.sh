#!/usr/bin/env bash

#######################################
# vizard installation script
#######################################

set -euo pipefail

INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/vizard"
BIN_DIR="$HOME/.local/bin"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
NC=$'\033[0m'

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║       Installing vizard                    ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════╝${NC}"
echo ""

# 1. Remove previous installation
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing previous installation..."
    rm -rf "$INSTALL_DIR"
fi
if [ -L "$BIN_DIR/vizard" ] || [ -f "$BIN_DIR/vizard" ]; then
    rm -f "$BIN_DIR/vizard"
fi

# 2. Create directories
echo "Creating installation directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# 3. Copy vizard executable
echo "Installing vizard executable..."
cp "$REPO_DIR/vizard" "$INSTALL_DIR/vizard"
chmod +x "$INSTALL_DIR/vizard"

# 4. Copy lib/
echo "Installing vizard libraries..."
cp -r "$REPO_DIR/lib" "$INSTALL_DIR/"

# 5. Copy templates/
echo "Installing templates..."
cp -r "$REPO_DIR/templates" "$INSTALL_DIR/"

# 6. Install cc_jupyter globally
echo ""
echo "Installing cc_jupyter globally..."

# Pinned version that we know works with patches
PINNED_VERSION="0.0.1"
VENDOR_WHEEL="$REPO_DIR/lib/vendor/claude_code_jupyter_staging-0.0.1-py3-none-any.whl"

if [ -f "$VENDOR_WHEEL" ]; then
    echo "  Using vendored version: $PINNED_VERSION"
    pip install --user "$VENDOR_WHEEL" --force-reinstall --no-deps 2>&1 | grep -v "already satisfied" || true
else
    echo -e "${YELLOW}  Vendored wheel not found, installing from PyPI${NC}"
    pip install --user claude-code-jupyter-staging==$PINNED_VERSION 2>&1 | grep -v "already satisfied" || true
fi

# Check installed version
INSTALLED_VERSION=$(python3 -c "import importlib.metadata; print(importlib.metadata.version('claude-code-jupyter-staging'))" 2>/dev/null || echo "unknown")

echo ""
echo "  Pinned version:    $PINNED_VERSION"
echo "  Installed version: $INSTALLED_VERSION"

if [ "$INSTALLED_VERSION" != "$PINNED_VERSION" ]; then
    echo -e "${YELLOW}  ⚠ Version mismatch detected${NC}"
    echo "  Patches are tested with version $PINNED_VERSION"
    echo "  If you experience issues, run: pip install --user --force-reinstall $VENDOR_WHEEL"
fi

# 7. Setup vizard_magic as importable package
echo ""
echo "Installing vizard_magic extension..."

# Copy vizard_magic package to user site-packages
USER_SITE=$(python3 -c "import site; print(site.USER_SITE)")
mkdir -p "$USER_SITE"
cp -r "$INSTALL_DIR/lib/vizard_magic" "$USER_SITE/"
echo "  ✓ Extension installed to: $USER_SITE/vizard_magic/"

# 8. Apply patches to global cc_jupyter
echo ""
echo "Patching global cc_jupyter..."
if [ -f "$INSTALL_DIR/lib/patch_global_cc_jupyter.sh" ]; then
    chmod +x "$INSTALL_DIR/lib/patch_global_cc_jupyter.sh"
    if "$INSTALL_DIR/lib/patch_global_cc_jupyter.sh"; then
        echo ""
    else
        echo -e "${YELLOW}  ⚠ Patching failed (see output above)${NC}"
        echo "  You can retry manually: $INSTALL_DIR/lib/patch_global_cc_jupyter.sh"
    fi
else
    echo -e "${YELLOW}  ⚠ Patcher not found (skipping)${NC}"
fi

# 9. Create symlink
echo "Creating symlink in $BIN_DIR..."
ln -s "$INSTALL_DIR/vizard" "$BIN_DIR/vizard"

echo ""
echo -e "${GREEN}✓ vizard installed successfully${NC}"
echo ""
echo "  Install location: $INSTALL_DIR"
echo "  Executable: $BIN_DIR/vizard"
echo ""

# 7. Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}⚠ $BIN_DIR is not in your PATH${NC}"
    echo ""
    echo "  Add this line to your ~/.bashrc or ~/.zshrc:"
    echo -e "  ${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
    echo ""
    echo "  Then reload your shell:"
    echo -e "  ${CYAN}source ~/.bashrc${NC}  (or source ~/.zshrc)"
    echo ""
else
    echo -e "${GREEN}✓ $BIN_DIR is in your PATH${NC}"
    echo ""
fi

echo "Get started:"
echo -e "  ${CYAN}vizard help${NC}      # Show help"
echo -e "  ${CYAN}cd ~/my-project${NC}  # Go to your project"
echo -e "  ${CYAN}vizard start${NC}     # Start JupyterLab"
echo ""
