"""
vizard IPython Extension
Loads cc_jupyter magic commands for Vizard visualization specifications
"""

def load_ipython_extension(ipython):
    """Load cc_jupyter extension and set up Vizard environment."""
    import sys
    from pathlib import Path
    import shutil

    errors = []

    # 1. Load cc_jupyter (third-party package from site-packages via uv sync)
    try:
        import cc_jupyter
        cc_jupyter.load_ipython_extension(ipython)
    except ImportError:
        errors.append("cc_jupyter not found - ensure 'uv sync' was run and .venv is activated")
    except Exception as e:
        errors.append(f"Error loading cc_jupyter: {e}")

    # 2. Add vizard lib directory to path (for future extensions)
    vizard_lib = Path.home() / ".local/share/vizard/lib"
    if vizard_lib.exists() and str(vizard_lib) not in sys.path:
        sys.path.append(str(vizard_lib))

    # 3. Copy CLAUDE.md if not present in current working directory
    cwd = Path.cwd()
    claude_md_dest = cwd / "CLAUDE.md"
    claude_md_template = Path.home() / ".local/share/vizard/templates/CLAUDE.md"

    if not claude_md_dest.exists():
        if claude_md_template.exists():
            try:
                shutil.copy2(claude_md_template, claude_md_dest)
                print(f"✓ Copied CLAUDE.md to {cwd}")
            except Exception as e:
                errors.append(f"Failed to copy CLAUDE.md: {e}")
        else:
            errors.append("CLAUDE.md template not found (run vizard setup)")

    # 4. Display results
    if errors:
        print("⚠️  vizard extensions loaded with errors:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✓ vizard extensions loaded (%%cc magic available)")


def unload_ipython_extension(ipython):
    """Unload extensions (best effort)."""
    try:
        import cc_jupyter
        if hasattr(cc_jupyter, 'unload_ipython_extension'):
            cc_jupyter.unload_ipython_extension(ipython)
    except:
        pass
