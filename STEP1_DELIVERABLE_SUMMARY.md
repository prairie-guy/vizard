# Vizard Step 1 Deliverable Summary

## What Was Built

**Vizard v2: Natural Language + Keywords with Stateful Persistence**

A declarative language for LLM-driven figure generation that combines structured keywords with natural language, featuring persistent keyword state for iterative figure development.

---

## Files Delivered

### 1. CLAUDE.md (948 lines, ~6.5K tokens)
**The core Vizard system prompt**

**New in v2:**
- ✨ **State management system** - `.vizard_state.json` for persistent keywords
- ✨ **Defaults table** - Clear specification of default values
- ✨ **Grouping & faceting** - GROUP_TYPE, ROW, COLUMN keywords
- ✨ **Additional encodings** - SIZE, SHAPE, OPACITY keywords
- ✨ **Meta commands** - KEYWORDS/KEYS, RESET
- ✨ **Function example** (Section 8) - Shows FUNCTION keyword usage
- ✨ **Grouping example** (Section 9) - Stacked, grouped, faceted plots
- ✨ **9 plot examples** (was 7) - Added function and grouping examples

**Contains:**
- State management documentation (.vizard_state.json workflow)
- Defaults table (ENGINE, DF, WIDTH, HEIGHT, FUNCTION, IMPORT, OUTPUT)
- Syntax rules (optional VIZARD/VZ trigger, CAPITALIZED keywords)
- Essential keywords: DATA, PLOT, X, Y, COLOR, ROW, COLUMN, SIZE, SHAPE, OPACITY, GROUP_TYPE, ENGINE, DF, FUNCTION, IMPORT
- Useful keywords: TITLE, WIDTH, HEIGHT, OUTPUT, FILENAME
- Meta commands: HELP, KEYWORDS/KEYS, RESET
- Dynamic keywords system (any CAPITALIZED word becomes context keyword)
- Polars-first philosophy with streaming/chaining style guide
- Altair fundamentals (marks, encodings, transforms, composition, faceting)
- 9 complete examples: bar, scatter, line, volcano, heatmap, box, histogram, function, grouping/faceting
- Conversational refinement patterns with state updates
- Gallery fetching instructions for unfamiliar plots

**Key Design Principles:**
- Natural language mixed with keyword anchors
- LLM reasoning for defaults, not rigid parsing
- Stateful keywords persist across calls
- Polars ALWAYS preferred over Pandas
- Streaming/chaining style absolute preference
- Balance consistency with flexibility

---

### 2. vizard_tests1.ipynb
**Comprehensive test notebook with 35 tests**

**Replaces:** VIZARD_TEST_GUIDE.md (now a notebook for interactive testing)

**Test categories (robust Option C structure):**
1. **Setup & Basics** (2 tests) - Load imports, verify data
2. **Syntax Variations** (5 tests) - Keywords-only, natural language, mixed, VIZARD/VZ triggers
3. **Meta Commands** (4 tests) - KEYWORDS, RESET, HELP
4. **Code Generation** (3 tests) - IMPORT, FUNCTION keywords
5. **Plot Types** (4 tests) - Bar, scatter, histogram, box
6. **Grouping & Faceting** (4 tests) - Stacked, grouped, ROW, COLUMN
7. **Conversational Refinement** (6 tests) - State accumulation, natural refinement
8. **State Persistence** (4 tests) - Persistence, RESET behavior
9. **Dynamic Keywords** (4 tests) - THRESHOLD example, state updates
10. **Spelling Tolerance** (1 test) - Typo recognition

**Format:** Jupyter notebook with markdown explanations and code cells ready to run

---

### 3. README.md
**Comprehensive project documentation**

**New file** providing:
- Project overview and features
- Quick start guide
- Core concepts (keywords, state management)
- Syntax examples (basic plots, grouping, faceting, refinement)
- Advanced features (dynamic keywords, Polars integration)
- Default values table
- Supported plot types
- Design philosophy
- Testing instructions
- Troubleshooting
- Future roadmap
- Quick reference

---

### 4. sample_data.csv
**Test dataset for initial experiments**

10 rows of gene expression data:
- gene_name (5 genes)
- expression_level (quantitative values)
- condition (treated vs control)

---

## Key Features

### State Management (NEW!)

**Persistent keyword state via `.vizard_state.json`:**
- All CAPITALIZED keywords saved to JSON
- State persists across Vizard calls
- Enables iterative figure development
- Per-directory state (each project has own state)
- KEYWORDS/KEYS command shows current state
- RESET command clears state, restores defaults

**Workflow:**
```
Iterate on figure → State accumulates
Figure complete → Use it
New figure → RESET → Clean state
```

### Default Values (NEW!)

**Clear defaults table:**
```
ENGINE: altair
DF: polars
WIDTH: 600
HEIGHT: 400
FUNCTION: false
IMPORT: false
OUTPUT: display
```

Column mappings (X, Y, COLOR, etc.) have no defaults - only appear when specified.

### Syntax Flexibility

✅ **Natural language:** "Create a bar chart from sample.csv showing genes vs expression"
✅ **Keywords only:** "DATA sample.csv PLOT bar X gene Y expression"
✅ **Mixed:** "Create a bar chart from DATA sample.csv with X gene and Y expression"

### Essential Keywords (Expanded!)

**Data & Plot:**
- **DATA** - Data source
- **DF/DATAFRAME** - polars (default) or pandas
- **PLOT** - Chart type

**Visual Encodings:**
- **X, Y** - Axis columns
- **COLOR** - Column to color by
- **ROW, COLUMN** - Faceting (NEW!)
- **SIZE** - Point/mark size encoding (NEW!)
- **SHAPE** - Point shape encoding (NEW!)
- **OPACITY** - Transparency encoding (NEW!)

**Grouping:**
- **GROUP_TYPE** - grouped (side-by-side) or stacked (NEW!)

**Rendering:**
- **ENGINE** - altair (default), matplotlib, or seaborn

**Code Generation:**
- **FUNCTION** - Generate function (true) vs script (false, default)
- **IMPORT** - Include imports (true) vs assume them (false, default)

**Meta Commands (NEW!):**
- **KEYWORDS/KEYS** - Show current state
- **RESET** - Clear state, restore defaults
- **HELP** - Show help documentation

### Grouping & Faceting (NEW!)

**Stacked bars:**
```
GROUP_TYPE stacked
```

**Grouped bars (side-by-side):**
```
GROUP_TYPE grouped
```

**Faceted plots:**
```
ROW condition          # Small multiples in rows
COLUMN replicate       # Small multiples in columns
ROW cond COLUMN rep    # Grid layout
```

### Dynamic Keywords

Any CAPITALIZED word not predefined becomes a context-specific keyword:
```
THRESHOLD 0.05
Highlight points where pvalue < THRESHOLD
```
THRESHOLD: 0.05 saved to state, usable in future calls.

### Polars-First Philosophy

- ALWAYS use Polars over Pandas
- Streaming/chaining style ABSOLUTE preference
- Example: `df = pl.read_csv('data.csv').filter(...).with_columns(...)`

### Supported Plot Types (Phase 1)

1. **Bar charts** - Simple, stacked, grouped
2. **Scatter plots** - With size, color, shape encodings
3. **Line charts** - Time series, multi-series
4. **Histograms** - Configurable bins
5. **Volcano plots** - Differential expression (bioinformatics)
6. **Heatmaps** - Matrix visualizations
7. **Box plots** - Distribution comparisons
8. **Faceted plots** - Small multiples (row/column grids)

### Code Generation Style

- Clean, readable Python
- Layering with + operator (bars + text)
- Text overlays with mark_text(dy=-5)
- scale_factor=2.0 for saving
- display() for notebook output
- Proper Altair type annotations (:N, :Q, :T)
- No comments except docstrings in functions
- Type hints for functions

---

## Design Decisions Made

### 1. State Management: Invisible to User

- Claude reads/writes `.vizard_state.json` automatically
- User never sees state file logic in generated code
- State persists across sessions, cell deletion
- Clean separation: keywords → state, natural language → context window

### 2. VIZARD Keyword: Optional

- `VIZARD`, `vizard`, `VZ`, `vz` all work
- If present → definitely Vizard mode
- If absent but keywords present → still Vizard
- Provides explicit trigger when needed

### 3. Keywords: CAPITALIZED (Case-Sensitive)

- Clear visual distinction from natural language
- Spelling tolerance (COLOUR→COLOR, HIGHT→HEIGHT)
- No colons required (though acceptable)
- All CAPITALIZED words saved to JSON state

### 4. Two Keyword Classes

**Defaults-based keywords:** Always in state with default values
- ENGINE, DF, WIDTH, HEIGHT, FUNCTION, IMPORT, OUTPUT

**Column mapping keywords:** Only in state when specified
- X, Y, COLOR, ROW, COLUMN, SIZE, SHAPE, OPACITY, GROUP_TYPE
- TITLE, FILENAME (situational)

### 5. GROUP_TYPE: Single Keyword

- Instead of separate STACKED/GROUPED keywords
- Values: `grouped` or `stacked`
- Avoids mutually exclusive keyword complexity

### 6. RESET vs RESET_STATE

- Chose shorter, clearer command: RESET
- Matches user intuition
- Commonly needed workflow action

### 7. Multi-Engine Support

- Default: Altair backend (declarative)
- ENGINE keyword supports: altair (default), matplotlib, seaborn
- Language doesn't marry any single visualization library

### 8. Polars Over Pandas

- Modern, faster, better API
- Streaming/chaining preferred style
- Pandas only if absolutely necessary

### 9. Conversational Refinement + State

- Natural language uses context window
- CAPITALIZED keywords update state
- Hybrid: state persistence + conversational flexibility

---

## How It Addresses Your Requirements

### ✅ "Reasonably defined prompt as declarative language"

Keywords provide structure, natural language provides flexibility, state provides persistence

### ✅ "Broad range of specification (general to specific)"

- General: "Create a bar chart from data.csv"
- Specific: "DATA data.csv PLOT bar X category Y value COLOR blue GROUP_TYPE grouped TITLE Chart WIDTH 800 HEIGHT 600"

### ✅ "Keywords for specifications"

Essential + useful + dynamic keyword system with state persistence

### ✅ "Reasonable defaults"

Clear defaults table, LLM reasoning fills gaps with sensible choices

### ✅ "Previously generated code as input to refine"

Conversational refinement pattern built-in, state accumulates across refinements

### ✅ "Consistent python code"

More specific specs → more deterministic output. Stateful keywords increase consistency within a figure iteration session. Balance between consistency and LLM flexibility.

### ✅ "Iterative figure development workflow" (NEW REQUIREMENT)

State persistence enables: iterate → refine → iterate → RESET → new figure

---

## Token Budget

**CLAUDE.md Size:** ~6,500 tokens (was 5,000)
**Impact:** Still minimal - loaded once per session
**Response Time:** Fast - good balance of detail and efficiency
**Addition justification:** State management + grouping/faceting documentation essential for functionality

---

## Testing Instructions

### Run Comprehensive Test Suite

```bash
jupyter notebook vizard_tests1.ipynb
```

**35 tests organized in 10 categories:**
1. Setup & Basics (2)
2. Syntax Variations (5)
3. Meta Commands (4)
4. Code Generation (3)
5. Plot Types (4)
6. Grouping & Faceting (4)
7. Conversational Refinement (6)
8. State Persistence (4)
9. Dynamic Keywords (4)
10. Spelling Tolerance (1)

**After testing, provide feedback on:**
- Does state management feel natural?
- Are defaults sensible?
- Is grouping/faceting intuitive?
- Does RESET workflow make sense?
- Code quality acceptable?
- What's missing?

---

## Future Phases

**Phase 2: Refinement**
- Based on your testing feedback
- Add missing keywords/features
- Test gallery fetching
- Refine examples
- Potential Polars data manipulation section

**Phase 3: Expansion**
- More plot types (violin, ridgeline, etc.)
- Multi-panel layouts (concatenation patterns)
- Interactive features (brush, zoom, tooltips)
- Matplotlib backend

**Phase 4: Publication Mode**
- DPI control
- Panel labels (A, B, C)
- Journal-specific formats
- Fine-grained typography
- Multi-panel layout refinements

---

## Questions to Consider During Testing

1. Does state management feel natural or confusing?
2. Is the RESET workflow clear and useful?
3. Do grouping keywords (GROUP_TYPE, ROW, COLUMN) work intuitively?
4. Are defaults (WIDTH: 600, HEIGHT: 400) appropriate?
5. Is Polars chaining working as expected?
6. Does conversational refinement + state feel smooth?
7. Are there missing essential keywords?
8. What bioinformatics-specific features are needed?
9. Should there be more/fewer default values?
10. Is KEYWORDS output format helpful?

---

## File Size Summary

- **CLAUDE.md**: 948 lines (~6.5K tokens) - Core system
- **README.md**: 387 lines - User documentation
- **vizard_tests1.ipynb**: 35 tests in 10 categories - Comprehensive testing
- **sample_data.csv**: 11 lines - Test data
- **STEP1_DELIVERABLE_SUMMARY.md**: This file - Implementation details

**Total documentation**: ~1,500 lines of comprehensive specification and testing

---

**You now have a working Vizard v2 prototype with stateful keywords!**

Test it with `vizard_tests1.ipynb`, provide feedback, and we'll iterate toward a production-ready system.
