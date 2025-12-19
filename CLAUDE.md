# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**IMPORTANT: Two Different CLAUDE.md Files**
- `vizard/CLAUDE.md` (THIS FILE) - Developer guidance for working on the vizard codebase
- `vizard/templates/CLAUDE.md` - The Vizard DSL specification that gets copied to user projects and loaded into Claude's context when interpreting `%%cc` cells. DO NOT CONFUSE THESE.

## Project Overview

Vizard is a natural language DSL that compiles high-level declarations to Altair & Matplotlib visualization code. It combines structured CAPITALIZED keywords with natural language to specify data visualizations, using an LLM (Claude) as the interpreter.

**Key Components:**
- `vizard` - Bash script CLI for managing JupyterLab servers and project workspaces
- `lib/vizard_magic/` - IPython extension that loads cc_jupyter and the Vizard specification
- `templates/CLAUDE.md` - The Vizard DSL specification (~1200 lines) loaded into Claude's context
- `templates/pyproject.toml` - Python dependencies template for per-project environments

## Installation & Development

```bash
# Install vizard globally
./setup.sh

# Verify installation
vizard version

# Per-project usage
cd ~/my-project
vizard start           # Creates .venv, installs deps, starts JupyterLab
vizard stop            # Stop server
vizard clean --purge   # Remove all vizard files
```

**Dependencies managed via uv:**
- polars, altair, matplotlib, seaborn (visualization stack)
- jupyterlab, cc_jupyter (Claude Code Jupyter integration)

## Testing

Run the comprehensive test suite in `test/vizards_test.ipynb`:

```bash
cd test
jupyter lab vizards_test.ipynb
```

**Test notebooks:**
- `vz_test.ipynb` - Basic tests
- `vz_*_polars_*.ipynb` - Polars wrangling tests
- `vz_*_altair_test.ipynb` - Altair-specific tests

## Architecture

### How Vizard Works

1. User loads `%load_ext vizard_magic` in Jupyter notebook
2. `vizard_magic` loads `cc_jupyter` (Claude Code Jupyter extension)
3. User writes `%%cc` cells with Vizard specifications (keywords + natural language)
4. Claude interprets the spec using `templates/CLAUDE.md` as context
5. Claude generates Python visualization code (Polars + Altair/Matplotlib)
6. Generated code executes in the notebook

### State Management

Vizard maintains keyword state in `.vizard_state.json`:
- Persisted: ENGINE, DF, WIDTH, HEIGHT, DATA, PLOT, X, Y, COLOR, etc.
- Ephemeral (per-cell only): FILTER, SELECT, DROP, SORT, ADD, GROUP, etc.
- Meta commands: KEYWORDS, RESET, HELP

### The `||` Delimiter

Separates data wrangling (Polars) from plotting (Altair):
```
DATA genes.csv FILTER pvalue < 0.05 || PLOT scatter X expression Y pvalue
```

## Key Files

| File | Purpose |
|------|---------|
| `vizard` | Main CLI (bash), manages JupyterLab servers |
| `setup.sh` | Global installation script |
| `lib/vizard_magic/__init__.py` | IPython extension loader |
| `lib/patch_jupyter_magic.sh` | Per-project cc_jupyter patcher |
| `lib/patch_global_cc_jupyter.sh` | Global cc_jupyter patcher |
| `templates/CLAUDE.md` | **Vizard DSL specification** - NOT this file! See warning above |
| `templates/pyproject.toml` | Project dependencies template |
| `templates/purge_manifest.txt` | Files removed by `vizard clean --purge` |

## Modifying the Vizard DSL

**The Vizard language specification lives in `templates/CLAUDE.md` (not this file).**

That file (~1200 lines) defines:
- §1: Core concepts, keyword tables, syntax patterns
- §2: State management specification
- §3: Data loading (DATA) and wrangling keywords (FILTER, SELECT, ADD, etc.)
- §4: Plotting specification (PLOT, X, Y, COLOR, LAYER, etc.)
- §5: Code generation rules
- §6-8: Examples and meta commands

When modifying keywords or behavior:
1. Edit `templates/CLAUDE.md` (the DSL spec, not this file)
2. Run `vizard update` in a project directory to copy the new spec
3. Validate with test notebooks
