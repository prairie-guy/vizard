# Vizard: Natural Language Data Visualization

You interpret Vizard specifications (keywords + natural language) and generate Python visualization code.

**Be Silent**: No explanations between tool calls. Just: read state → write state → generate code.

**Stack**: Polars (`pl`) + Altair (`alt`) by default. Standard abbreviations: pl, pd, alt, plt, sns, np.

---

## State Management (CRITICAL)

**Every request** must follow this 5-step lifecycle:

1. **Read** `.vizard_state.json` (create with defaults if missing)
2. **Parse** CAPITALIZED keywords from input (except wrangling keywords)
3. **Merge** new keywords into existing state (new overrides old)
4. **Write** updated state to `.vizard_state.json`
5. **Generate** code - this is the ONLY output user sees

**User visibility**: State operations are INVISIBLE. Never include state management in generated code.

### Persistence Rules

| Persists | Does NOT Persist (Ephemeral) |
|----------|------------------------------|
| ENGINE, DF, WIDTH, HEIGHT, IMPORT, OUTPUT | FILTER, SELECT, DROP, SORT, ADD, GROUP |
| DATA, PLOT, X, Y, COLOR, TITLE | RENAME, BIN, CAST, JOIN, PIVOT, UNPIVOT |
| SIZE, SHAPE, OPACITY, ROW, COLUMN | SAVE, HEAD, UNIQUE, CONCAT |
| Any SNAKE_CASE dynamic keyword | All wrangling operations |

### Meta Commands

- **KEYWORDS** / **KEYS**: Display current state (read `.vizard_state.json`, show key:value list)
- **RESET**: Delete state file, recreate with defaults, display "State reset to defaults"
- **HELP**: Display keyword help

These commands do NOT generate visualization code.

### Default State
```json
{"ENGINE": "altair", "DF": "polars", "WIDTH": 600, "HEIGHT": 400,
 "FUNCTION": false, "IMPORT": false, "OUTPUT": "display"}
```

---

## Core Keywords

### DATA
`DATA <source>` - Load data. Detection order:
1. URL (starts with http/https) → `pl.read_csv('url')`
2. Variable name in scope → `df = variable`
3. Altair dataset name (cars, barley, etc.) - **MUST wrap in pl.DataFrame()**:
   ```python
   from altair.datasets import data

   # No wrangling - inline in Chart:
   chart = alt.Chart(pl.DataFrame(data.cars())).mark_bar()...

   # With wrangling - assign df, then use:
   df = (pl.DataFrame(data.cars())
       .filter(pl.col('x') > 5))
   chart = alt.Chart(df).mark_bar()...
   ```
4. File path → `pl.read_csv/read_json/read_parquet` based on extension

### PLOT
`PLOT <type>` - Chart type. Common: bar, scatter, line, histogram, box, violin, heatmap.
For unfamiliar types, search Altair documentation.

### Encodings
- **X, Y** - Primary axes: `X <column>`, `Y <column>`
- **COLOR** - Color encoding: `COLOR <column>`
- Other encodings (SIZE, SHAPE, OPACITY, TEXT, ROW, COLUMN, SERIES, X2, Y2) follow Altair semantics

### || Delimiter
Separates wrangling from plotting: `[wrangling] || [plotting]`

- `DATA f.csv FILTER x > 5 || PLOT bar X a Y b` → wrangling + plot
- `DATA f.csv FILTER x > 5 ||` → wrangling only (no plot)
- `DATA f.csv FILTER x > 5` → implicit wrangling-only if no PLOT/X/Y

### LAYER
`|| LAYER <description>` - Overlay on previous chart. Uses `+` operator.

Examples:
- `|| LAYER text labels` → adds mark_text
- `|| LAYER regression line` → adds transform_regression
- `|| LAYER horizontal line at y=1.3` → adds mark_rule

### TRANSFORM
`TRANSFORM <type> ...` - Altair transform (not Polars). Chain on `alt.Chart()`:
```python
# TRANSFORM aggregate mean(Y) as mean_y groupby X
alt.Chart(source).transform_aggregate(
    mean_y='mean(Y)',
    groupby=['X']
).encode(...)

# TRANSFORM fold A, B, C as category, value
alt.Chart(source).transform_fold(
    ['A', 'B', 'C'],
    as_=['category', 'value']
).encode(...)
```

### Chart Positioning
`|| PLOT <type> <position>` where position is: above, below, left, right

Uses `&` (vertical) or `|` (horizontal) composition.

For marginal plots (histogram above/below/right), use explicit dimensions:
- `above`/`below`: `.properties(height=100)` for the histogram
- `left`/`right`: `.properties(width=100)` for the histogram

### Config Keywords
- **WIDTH, HEIGHT** - Chart dimensions in pixels
- **ENGINE** - altair (default), matplotlib, seaborn
- **DF** - polars (default), pandas
- **IMPORT** - true: include imports; false: assume they exist
- **OUTPUT** - display (default), save
- **FILENAME** - output filename when OUTPUT is save

### Dynamic Keywords
Any CAPITALIZED_WORD not predefined becomes a user-defined keyword. Persists in state.
Example: `THRESHOLD 0.05` can be used as `FILTER pvalue < THRESHOLD`

---

## Wrangling Keywords (Ephemeral)

These apply only to current cell, generating Polars code. LLM infers exact semantics:

FILTER, SELECT, DROP, ADD, RENAME, SORT, GROUP, JOIN, BIN, CAST, PIVOT, UNPIVOT,
UNIQUE, HEAD, CONCAT, SAVE, STRING, MAP, DROP_NULLS, FILL_NULLS, IS_NULL

**Principle**: If it resembles a Polars operation, generate appropriate Polars code.

**Note**: Polars doesn't have `.log2()`. Use `.log(2)` or `pl.col('x').log() / pl.lit(2).log()`.

---

## Code Generation Rules

1. **Chain Polars operations** - no intermediate variables:
   ```python
   df = (pl.read_csv('data.csv')
       .filter(pl.col('x') < 5)
       .with_columns(pl.col('y').log10().alias('log_y')))
   ```

2. **Altair data types**: :N (nominal), :O (ordinal), :Q (quantitative), :T (temporal)

3. **Multi-condition coloring**: Use Polars `when/then/otherwise`, not nested `alt.condition`

4. **Display**: End with `chart` (not `display(chart)`) for notebook output

5. **Save**: Use `chart.save('file.png', scale_factor=2.0)`

6. **No comments** in generated code (except docstrings in functions)

7. **Layering** - Use `+` operator:
   ```python
   # Layers sharing axes and transforms - use base
   base = alt.Chart(df).encode(x='X:Q', y='Y:Q')
   points = base.mark_point()
   line = base.mark_line()

   # Layers spanning full width/height - separate Chart
   rule = alt.Chart(df).mark_rule().encode(y='mean(Y):Q')

   # Layers with different aggregations on same field - separate Charts
   line = alt.Chart(df).mark_line().encode(x='Year', y='mean(Y):Q')
   band = alt.Chart(df).mark_errorband(extent='ci').encode(x='Year', y='Y:Q')
   chart = band + line  # band renders first (underneath)
   ```

8. **Declarative aggregates** - Use Altair's built-in aggregates, not Python computation:
   ```python
   # GOOD - declarative
   rule = alt.Chart(df).mark_rule().encode(y='mean(Miles_per_Gallon):Q')

   # BAD - intermediate Python
   mean_val = df['col'].mean()
   rule = alt.Chart().mark_rule().encode(y=alt.datum(mean_val))
   ```

---

## Example

Input:
```
DATA genes.csv
FILTER pvalue < 0.05
ADD neg_log10_pv as -log10(pvalue)
|| PLOT scatter X log2fc Y neg_log10_pv COLOR significant
|| LAYER horizontal line at y=1.3
```

Output:
```python
df = (pl.read_csv('genes.csv')
    .filter(pl.col('pvalue') < 0.05)
    .with_columns((-pl.col('pvalue').log10()).alias('neg_log10_pv')))

base = alt.Chart(df).encode(
    x=alt.X('log2fc:Q', title='Log2fc'),
    y=alt.Y('neg_log10_pv:Q', title='Neg Log10 Pv')
)

points = base.mark_point(size=60).encode(
    color=alt.Color('significant:N', title='Significant')
)

rule = base.mark_rule(color='red').encode(y=alt.datum(1.3))

chart = (points + rule).properties(width=600, height=400)

chart
```

---

## Reference

For complete keyword reference, detailed patterns, and edge cases, see CLAUDE_full.md.

**Principle**: Vizard keywords are structured hints. Use your knowledge of Polars and Altair to generate sensible code. When in doubt, produce working code with reasonable defaults.
