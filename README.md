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

## Quick Start

### 1. Setup

Ensure Claude Code and claude-code-jupyter are installed, then load the extension in a Jupyter notebook:

```python
%load_ext cc_jupyter

# Load visualization libraries (one-time setup)
import altair as alt
import polars as pl
```

### 2. Create Your First Figure

```python
# Simple bar chart
%cc DATA mydata.csv PLOT bar X category Y value

# Or use natural language
%cc Create a scatter plot from mydata.csv showing x vs y colored by group

# Mix both styles
%cc DATA mydata.csv - make a bar chart with X gene_name and Y expression_level, sorted by value
```

### 3. Iterate and Refine

```python
# Initial chart
%cc DATA sales.csv PLOT bar X product Y revenue

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

## File Structure

```
vizard/
├── CLAUDE.md                      # Core Vizard system prompt (~5K tokens)
├── README.md                      # This file
├── pyproject.toml                 # Python project configuration
├── sample_data.csv                # Test dataset
├── vizard_tests1.ipynb            # Comprehensive test suite (35 tests)
├── STEP1_DELIVERABLE_SUMMARY.md   # Implementation details
└── .vizard_state.json             # Keyword state (auto-generated)
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
