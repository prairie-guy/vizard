"""
vizard IPython Extension
Loads cc_jupyter magic commands for Vizard visualization specifications
"""

def load_ipython_extension(ipython):
    """Load cc_jupyter extension."""
    import sys
    from pathlib import Path

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

    # Display results
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
