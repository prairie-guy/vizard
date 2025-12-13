# Vendored Dependencies

This directory contains vendored (bundled) versions of dependencies that are known to work with vizard's patching system.

## claude_code_jupyter_staging-0.0.1-py3-none-any.whl

**Package:** `claude-code-jupyter-staging`
**Version:** 0.0.1
**Source:** PyPI (https://pypi.org/)
**Date Vendored:** December 12, 2024

**Why Vendored:**
- Provides stable, tested version of cc_jupyter that works with vizard patches
- Fallback if PyPI version changes or breaks compatibility
- Ensures reproducible installations

**Usage:**
The setup.sh script will use this vendored wheel if available, otherwise falls back to installing from PyPI.

**Patching:**
This version is known to work with the patches in `lib/patch_jupyter_magic.sh`:
- PATCH 1: Permission error fix for `/root/code` check
- PATCH 2: Decorative header removal

**Updating:**
If you need to update to a newer version:
1. Test the new version with vizard
2. Verify patches still apply correctly
3. Update this wheel file
4. Update PINNED_VERSION in setup.sh
