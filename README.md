# Vizard: Natural Language Visualization Specification

**A declarative language for LLM-driven figure generation combining structured keywords with natural language.**

Vizard lets you create data visualizations by describing what you want in a mix of CAPITALIZED keywords and natural language, with intelligent defaults and stateful keyword persistence for iterative figure development.

---

## Features

- 🗣️ **Natural + Structured**: Mix CAPITALIZED keywords with plain English
- 💾 **Stateful**: Keywords persist across calls, enabling iterative refinement
- 🐻‍❄️ **Polars-first**: Modern, fast dataframe operations with streaming/chaining
- 📊 **Multi-engine**: Altair (default), Matplotlib, and Seaborn support
- 🔧 **Flexible**: Supports minimal to highly detailed specifications
- 🤖 **Intelligent**: LLM fills gaps with sensible defaults
- 🔄 **Conversational**: Refine figures through natural dialogue

---

## Installation

### 1. Clone and Install

```bash
git clone <repo-url> vizard
cd vizard
./setup.sh
```

This installs vizard to `~/.local/share/vizard/` and creates a symlink in `~/.local/bin/`.

**Note:** Ensure `~/.local/bin` is in your PATH. If not, add to your `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 2. Verify Installation

```bash
vizard version
vizard help
```

---

## Usage Modes

Vizard supports **two modes of operation** depending on your workflow:

### Mode 1: Global Installation (Recommended for Quick Use)

**When to use:** You want to use Vizard in any Jupyter environment without running `vizard start` first.

**What it does:**
- `setup.sh` installs `cc_jupyter` to `~/.local/lib/python*/site-packages/`
- Installs `vizard_magic` package to `~/.local/lib/python*/site-packages/`
- Applies patches to the global `cc_jupyter` installation
- Works in any Jupyter notebook (system-wide, conda envs, etc.)

**Usage:**
1. Run `./setup.sh` once
2. Open any Jupyter notebook
3. Load extension: `%load_ext vizard_magic`
4. Use `%%cc` magic cells with Vizard specs

**Advantages:**
- ✅ No per-project setup required
- ✅ Works across all Jupyter environments
- ✅ Simpler workflow for quick exploration
- ✅ Centralized cc_jupyter installation

**Limitations:**
- ⚠️ Global patching affects all projects using cc_jupyter
- ⚠️ Single version of cc_jupyter across all projects

### Mode 2: Per-Project Isolated (Recommended for Production)

**When to use:** You want isolated environments with pinned dependencies per project.

**What it does:**
- `vizard start` creates project-local `.venv/` with dependencies
- Installs `cc_jupyter` in the project's virtual environment
- Applies patches to the project-local `cc_jupyter`
- Each project has its own isolated dependency versions

**Usage:**
1. Navigate to your project directory
2. Run `vizard start` (copies templates, installs deps, starts Jupyter)
3. Open notebook at provided URL
4. Load extension: `%load_ext vizard_magic`
5. Use `%%cc` magic cells

**Advantages:**
- ✅ Complete dependency isolation per project
- ✅ Pin specific cc_jupyter versions per project
- ✅ Reproducible environments
- ✅ Safe for production/published research

**Limitations:**
- ⚠️ Requires `vizard start` for each project
- ⚠️ Larger disk usage (one .venv per project)

### Which Mode Should I Use?

| Scenario | Recommended Mode |
|----------|------------------|
| Quick data exploration | Global |
| Testing Vizard features | Global |
| Working across multiple small projects | Global |
| Published research / production | Per-Project |
| Need specific cc_jupyter version | Per-Project |
| Sharing reproducible analysis | Per-Project |

**Note:** Both modes can coexist. The per-project `.venv/` takes precedence when active, otherwise the global installation is used.

### Version Management

`setup.sh` installs a **pinned version** of `cc_jupyter` (currently 0.0.1) that is tested with Vizard's patches:

```bash
Pinned version:    0.0.1
Installed version: 0.0.1
```

If you see a version mismatch warning:
```bash
⚠ Version mismatch detected
Patches are tested with version 0.0.1
If you experience issues, run: pip install --user --force-reinstall <vendored-wheel>
```

This means a different version was found. You can force reinstall the vendored version:
```bash
pip install --user --force-reinstall ~/.local/share/vizard/lib/vendor/claude_code_jupyter_staging-0.0.1-py3-none-any.whl
~/.local/share/vizard/lib/patch_global_cc_jupyter.sh
```

---

## Quick Start

### 1. Start Jupyter

Navigate to your project directory and start JupyterLab:

```bash
cd ~/my-project
vizard start
```

This will:
- Copy templates (`pyproject.toml`, `CLAUDE.md`, notebook template)
- Install Python dependencies (altair, polars, jupyterlab, etc.)
- Start JupyterLab server
- Display connection URL

### 2. Load Extension in Notebook

In a Jupyter notebook cell:

```python
%load_ext vizard_magic
```

This loads the `%%cc` magic command with Vizard specification context.

### 3. Create Your First Figure

```python
# Simple bar chart
%cc DATA mydata.csv PLOT bar X category Y value

# Or use natural language
%cc Create a scatter plot from mydata.csv showing x vs y colored by group

# Mix both styles
%cc DATA mydata.csv - make a bar chart with X gene_name and Y expression_level, sorted by value
```

### 4. Iterate and Refine

```python
# Initial chart
%%cc
DATA sales.csv PLOT bar X product Y revenue

# Add color
%cc COLOR category

# Adjust dimensions
%cc WIDTH 800 HEIGHT 500

# Add styling with natural language
%cc Make the bars green and add value labels on top

# Check current state
%cc KEYWORDS

# Start fresh
%cc RESET
```

### 5. When Done

Stop the Jupyter server:

```bash
vizard stop
```

---

## CLI Commands

vizard provides several commands for managing your workspace:

```bash
vizard start [options]     # Start JupyterLab server
  -p, --port PORT          # Custom port (default: 9999)
  -t, --token TOKEN        # Custom token (default: auto-generated)
  --host HOST              # Custom hostname (default: system hostname)
  -f, --foreground         # Run in foreground

vizard stop [options]      # Stop JupyterLab server
  -p, --port PORT          # Stop server on specific port

vizard status              # Show server status and running instances

vizard clean [options]     # Remove runtime files
  --purge                  # Remove all vizard files including dependencies

vizard update              # Update CLAUDE.md and vizard executable

vizard version             # Show version information

vizard help                # Show help message
```

**Examples:**

```bash
# Start with custom port for remote server
vizard start --port 8888 --host myserver.example.com

# Check status
vizard status

# Clean up (keeps notebooks and dependencies)
vizard clean

# Full cleanup (removes everything except notebooks)
vizard clean --purge
```

---

## Core Concepts

### Keywords

**CAPITALIZED words are keywords** that control behavior and persist in `.vizard_state.json`:

**Essential Keywords:**
- `DATA` - Data source (file, URL, variable)
- `PLOT` - Chart type (bar, scatter, line, histogram, volcano, heatmap, box)
- `X`, `Y` - Axis columns
- `COLOR`, `ROW`, `COLUMN` - Visual encodings
- `ENGINE` - Visualization library (default: altair, also: matplotlib, seaborn)

**Code Generation:**
- `FUNCTION` - Generate reusable function (default: false)
- `IMPORT` - Include imports (default: false)

**Meta Commands:**
- `KEYWORDS` or `KEYS` - Show current state
- `RESET` - Clear state, restore defaults
- `HELP` - Show help documentation

**Full list:** See [CLAUDE.md](CLAUDE.md) for complete keyword reference.

### State Management

Vizard maintains keyword state in `.vizard_state.json`:

```python
# Set parameters
%cc WIDTH 700 HEIGHT 450 DATA mydata.csv

# Use persisted state in next call
%cc PLOT bar X category Y value
# ↑ Automatically uses WIDTH: 700, HEIGHT: 450

# Check state
%cc KEYWORDS
# Output:
# WIDTH: 700
# HEIGHT: 450
# DATA: mydata.csv
# PLOT: bar
# ...

# Clear state
%cc RESET
```

**Workflow Pattern:**
1. Iterate on a figure → State accumulates
2. Figure complete → Use it
3. Start new figure → `RESET` → Fresh state

### Natural Language + Keywords

Mix structured keywords with conversational language:

```python
# All keywords
%cc DATA genes.csv PLOT volcano X log2fc Y pvalue

# All natural
%cc Create a volcano plot from genes.csv with log2fc and pvalue

# Mixed (recommended)
%cc DATA genes.csv - create a volcano plot showing X log2fc vs Y pvalue, color upregulated genes red and downregulated blue
```

---

## Syntax Examples

### Basic Plots

```python
# Bar chart
%cc DATA sales.csv PLOT bar X product Y revenue

# Scatter plot with coloring
%cc DATA genes.csv PLOT scatter X expression Y pvalue COLOR significant

# Line chart
%cc DATA timeseries.csv PLOT line X date Y temperature COLOR location

# Histogram
%cc DATA values.csv PLOT histogram X measurement with 30 bins

# Box plot
%cc DATA measurements.csv PLOT box X group Y value
```

### Grouping & Faceting

```python
# Stacked bar chart
%cc DATA data.csv PLOT bar X gene Y expression COLOR condition GROUP_TYPE stacked

# Grouped bar chart (side-by-side)
%cc DATA data.csv PLOT bar X gene Y expression COLOR condition GROUP_TYPE grouped

# Faceted by rows
%cc DATA data.csv PLOT scatter X value1 Y value2 ROW condition

# Faceted grid
%cc DATA data.csv PLOT bar X gene Y count ROW condition COLUMN replicate
```

### Code Generation Options

```python
# Generate with imports
%cc DATA data.csv PLOT bar X category Y value IMPORT

# Generate reusable function
%cc DATA data.csv PLOT bar X category Y value FUNCTION IMPORT

# Default (no imports, script code)
%cc DATA data.csv PLOT bar X category Y value
```

### Conversational Refinement

```python
# Start
%cc DATA sales.csv PLOT bar X product Y revenue

# Refine with keywords
%cc WIDTH 800 COLOR category

# Refine with natural language
%cc Sort the bars descending and make them green

# Refine with both
%cc TITLE Q4 Sales Report and add value labels on top of each bar

# Save
%cc OUTPUT save FILENAME sales_report.png
```

---

## Advanced Features

### Dynamic Keywords

Any CAPITALIZED word becomes a context-specific keyword:

```python
%cc DATA genes.csv PLOT scatter X log2fc Y pvalue THRESHOLD 0.05
%cc Highlight points where pvalue < THRESHOLD in red
# THRESHOLD: 0.05 is now in state and can be used/modified
```

### Polars Data Manipulation

Vizard generates Polars streaming/chaining code when data prep is needed:

```python
%cc DATA results.csv
Filter to rows where pvalue < 0.05
Create a volcano plot showing log2fc vs pvalue
Color significant genes red

# Generated code uses Polars chaining:
# df = (pl.read_csv('results.csv')
#     .filter(pl.col('pvalue') < 0.05)
#     .with_columns([...]))
```

### Spelling Tolerance

Common typos are recognized:

```python
%cc DATA data.csv PLOT bar X cat Y val COLOUR blue TITEL My Chart HIGHT 450
# Works! Recognizes COLOUR→COLOR, TITEL→TITLE, HIGHT→HEIGHT
```

---

## Repository Structure

```
vizard/
├── vizard                         # Main executable (bash script)
├── setup.sh                       # Installation script
├── uninstall.sh                   # Uninstallation script
├── README.md                      # This file
├── pyproject.toml                 # Development dependencies
├── .gitignore                     # Git ignore patterns
├── lib/
│   └── vizard_magic/
│       └── __init__.py            # Jupyter IPython extension
├── templates/
│   ├── CLAUDE.md                  # Vizard specification (~30KB)
│   ├── pyproject.toml             # Project dependencies template
│   ├── vizard_template.ipynb      # Notebook template
│   └── purge_manifest.txt         # Cleanup manifest
└── test/
    ├── sample_data.csv            # Test dataset
    └── vizard_tests1.ipynb        # Test suite
```

**Per-Project Files (created by `vizard start`):**
```
<your-project>/
├── .env.jupyter              # Jupyter configuration
├── .jupyter.pid              # Process ID
├── .jupyter.log              # Server logs
├── pyproject.toml            # Python dependencies
├── uv.lock                   # Dependency lock file
├── .venv/                    # Virtual environment
├── CLAUDE.md                 # Vizard specification
├── .vizard_state.json        # Keyword state
├── .vizard_template.ipynb    # Notebook template
└── .claude/
    └── settings.json         # Claude Code permissions
```

---

## Default Values

```
ENGINE: altair
DF: polars
WIDTH: 600
HEIGHT: 400
FUNCTION: false
IMPORT: false
OUTPUT: display
```

Other keywords (X, Y, COLOR, etc.) have no defaults—they only appear in state when specified.

---

## Supported Plot Types (Phase 1)

- ✅ **Bar charts** - Simple, stacked, grouped
- ✅ **Scatter plots** - With size, color, shape encodings
- ✅ **Line charts** - Time series, multi-series
- ✅ **Histograms** - Configurable bins
- ✅ **Volcano plots** - Bioinformatics differential expression
- ✅ **Heatmaps** - Matrix visualizations
- ✅ **Box plots** - Distribution comparisons
- ✅ **Faceted plots** - Small multiples (row/column)

Coming soon: Violin plots, ridgeline plots, chord diagrams

---

## Design Philosophy

### Vizard is NOT:
- ❌ A rigid DSL with one-to-one code mapping
- ❌ A replacement for learning Altair/Matplotlib/Seaborn
- ❌ Guaranteed to produce identical code each time

### Vizard IS:
- ✅ Structured guidance via keywords
- ✅ LLM reasoning for intelligent defaults
- ✅ Balance of consistency and flexibility
- ✅ Iterative figure development workflow
- ✅ Natural language + structure hybrid

---

## Testing

Run the comprehensive test suite:

```bash
jupyter notebook vizard_tests1.ipynb
```

**Test coverage (35 tests):**
- Syntax variations
- Meta commands (KEYWORDS, RESET, HELP)
- Code generation (FUNCTION, IMPORT)
- Plot types
- Grouping & faceting
- Conversational refinement
- State persistence
- Dynamic keywords
- Spelling tolerance

---

## Examples

### Example 1: Simple Exploration

```python
%cc DATA experiment.csv PLOT bar X gene_name Y expression_level
%cc COLOR condition
%cc WIDTH 800
%cc Add value labels and sort by expression descending
```

### Example 2: Publication Figure

```python
%cc RESET
%cc DATA diff_expression.csv PLOT volcano X log2fc Y neg_log10_pvalue IMPORT
%cc Add threshold lines at x=±1.5 and y=1.3
%cc Color upregulated red, downregulated blue, non-significant gray
%cc TITLE Differential Gene Expression Analysis
%cc WIDTH 800 HEIGHT 800
%cc OUTPUT save FILENAME figure1_volcano.png
```

### Example 3: Grouped Comparison

```python
%cc DATA gene_expression.csv
%cc PLOT bar X gene_name Y expression_level
%cc COLOR condition GROUP_TYPE grouped
%cc ROW timepoint
%cc TITLE Gene Expression Across Conditions and Timepoints
```

---

## Workflow Tips

1. **Start simple**: Begin with minimal specification, iterate
2. **Use KEYWORDS often**: Check state to understand what's persisted
3. **RESET between figures**: Clear state when starting a new visualization
4. **Mix styles**: Use keywords for structure, natural language for styling
5. **Leverage state**: Set common parameters (WIDTH, HEIGHT) once, use many times
6. **Generate functions**: Use FUNCTION for reusable plotting code

---

## Troubleshooting

**Q: My plot isn't using the right dimensions**
- Check state with `%cc KEYWORDS` - are WIDTH/HEIGHT set?
- Use `%cc RESET` to clear old dimensions

**Q: Code has imports but I don't want them**
- IMPORT defaults to false - don't include IMPORT keyword
- Check if IMPORT is in state: `%cc KEYWORDS`

**Q: Keywords not persisting**
- Ensure keywords are CAPITALIZED
- Check `.vizard_state.json` exists in directory

**Q: LLM not recognizing Vizard specs**
- Use explicit trigger: `VZ` or `VIZARD` at start
- Ensure CLAUDE.md is in project directory

---

## Future Roadmap

**Phase 2: Refinement** (based on testing feedback)
- Gallery fetching for uncommon plot types
- Additional plot type examples
- Enhanced dynamic keywords

**Phase 3: Expansion**
- Additional plot types for all engines
- Multi-panel layout improvements
- Interactive features (brush, zoom, tooltips)

**Phase 4: Publication Mode**
- DPI control
- Panel labels (A, B, C)
- Journal-specific formats
- Fine-grained typography

---

## Contributing

This is an early prototype. Feedback welcome on:
- Keyword design
- Default values
- Natural language parsing
- Code quality
- Missing features

---

## License

To be determined.

---

## Acknowledgments

Built with:
- [Claude](https://claude.ai) (Anthropic) - LLM interpreter
- [Altair](https://altair-viz.github.io/) - Declarative visualization
- [Matplotlib](https://matplotlib.org/) - Comprehensive visualization
- [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization
- [Polars](https://pola.rs/) - Fast dataframes
- [Claude Code](https://github.com/anthropics/claude-code) - CLI tool

---

**Quick Reference:**

```python
# Essential commands
%cc KEYWORDS            # Show state
%cc RESET              # Clear state
%cc HELP               # Show help

# Basic syntax
%cc DATA file.csv PLOT bar X col1 Y col2

# Natural + keywords
%cc DATA file.csv - create a scatter plot with X val1 and Y val2 colored by group

# Iterate
%cc WIDTH 800 COLOR category TITLE My Chart
```

Ready to create beautiful visualizations with Vizard? Start with `vizard_tests1.ipynb`!
