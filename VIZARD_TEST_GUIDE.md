# Vizard v2 Test Guide - Natural Language + Keywords

## What You Have

✅ **CLAUDE.md v2** - Natural language + keyword hybrid Vizard specification
✅ **sample_data.csv** - Test dataset with gene expression data

## Key Changes from v1

**v1 (DSL):** Rigid keyword-value syntax
**v2 (Natural):** Mix keywords and natural language freely

**New Features:**
- VIZARD keyword (optional trigger)
- DF/DATAFRAME keyword (polars default)
- FUNCTION keyword (generate function vs script)
- IMPORT keyword (include imports or assume they exist)
- HELP keyword (show help)
- Dynamic keywords (any CAPITALIZED word becomes a context keyword)
- Polars-first philosophy with streaming/chaining
- 7 example plot types: bar, scatter, line, volcano, heatmap, box, histogram

---

## How to Test

### Setup in Jupyter

```python
# Load the extension (check which command works for your installation)
%load_ext cc_jupyter
# or
%load_ext claude_code_jupyter
```

---

## Test Cases

### Test 1: Minimal Natural Language
```python
%cc DATA sample_data.csv - create a bar chart with gene_name on x-axis and expression_level on y-axis
```

**Expected:** Clean bar chart with Polars data loading, sensible defaults

---

### Test 2: Keywords Only (Concise)
```python
%cc DATA sample_data.csv PLOT bar X gene_name Y expression_level
```

**Expected:** Same result as Test 1, different input style

---

### Test 3: Mixed Style (Natural + Keywords)
```python
%cc Create a bar chart from DATA sample_data.csv showing X gene_name vs Y expression_level, colored by condition. Use a nice color scheme and add a title.
```

**Expected:** Bar chart with categorical color by condition, inferred title

---

### Test 4: Explicit VIZARD Trigger
```python
%cc VIZARD - make a scatter plot from sample_data.csv with gene_name on x and expression_level on y, colored by condition
```

**Expected:** Scatter plot with proper encoding

---

### Test 5: Test FUNCTION Keyword
```python
%cc DATA sample_data.csv PLOT bar X gene_name Y expression_level FUNCTION true
```

**Expected:** A reusable function definition (not inline script code) with docstring and parameters

---

### Test 6: Test IMPORT Keyword
```python
%cc DATA sample_data.csv PLOT bar X gene_name Y expression_level IMPORT true
```

**Expected:** Code starts with import statements (altair, polars, etc.)

---

### Test 7: Without IMPORT (Default)
```python
%cc DATA sample_data.csv PLOT bar X gene_name Y expression_level
```

**Expected:** No imports, assumes pl, alt exist, uses them directly

---

### Test 8: Conversational Refinement
```python
# First chart
%cc DATA sample_data.csv PLOT bar X gene_name Y expression_level

# In next cell - refine it
%cc Sort the bars by value descending and make them green

# In next cell - refine again
%cc Add value labels on top of the bars

# In next cell - save it
%cc Save this as gene_expression.png
```

**Expected:** Each refinement builds on previous, maintaining continuity

---

### Test 9: Dynamic Keywords
```python
%cc DATA sample_data.csv PLOT scatter X gene_name Y expression_level THRESHOLD 100
Highlight points where expression_level is above THRESHOLD in red, others in gray
```

**Expected:** THRESHOLD recognized as dynamic keyword, used to color points

---

### Test 10: Polars Chaining Style
```python
%cc DATA sample_data.csv
Filter to keep only rows where condition is 'treated'
Create a bar chart with gene_name on x and expression_level on y
Sort by expression_level descending
```

**Expected:** Code uses Polars streaming/chaining style for filtering before visualization

---

### Test 11: Multiple Plot Types

**Scatter:**
```python
%cc PLOT scatter from DATA sample_data.csv, X gene_name Y expression_level COLOR condition
```

**Line (if you have time series data):**
```python
%cc PLOT line showing time series from my_timeseries.csv
```

**Histogram:**
```python
%cc Create a histogram of expression_level from DATA sample_data.csv with 20 bins
```

---

### Test 12: Spelling Tolerance
```python
%cc DATA sample_data.csv PLOT bar X gene_name Y expression_level COLOUR blue TITEL Test Chart HIGHT 400
```

**Expected:** Recognizes COLOUR→COLOR, TITEL→TITLE, HIGHT→HEIGHT

---

### Test 13: HELP Command
```python
%cc HELP
```

**Expected:** Display help text with keyword definitions, no visualization generated

---

### Test 14: Saving to File
```python
%cc DATA sample_data.csv PLOT bar X gene_name Y expression_level OUTPUT save FILENAME test_chart.png
```

**Expected:** Code includes `chart.save('test_chart.png', scale_factor=2.0)`

---

### Test 15: Advanced - Volcano Plot (if you have suitable data)
```python
%cc DATA diff_expression.csv PLOT volcano X log2fc Y neg_log10_pvalue
Add threshold lines at x=±1.5 and y=1.3
Color red for upregulated, blue for downregulated, gray for non-significant
```

**Expected:** Polars chaining to categorize, threshold lines via layering

---

## Success Criteria

### Must Work:
- [ ] Natural language specifications generate correct code
- [ ] Keyword-only specifications work
- [ ] Mixed style works
- [ ] Polars is used by default (never pandas unless necessary)
- [ ] Code uses Polars chaining style when data prep needed
- [ ] FUNCTION keyword generates function vs script
- [ ] IMPORT keyword controls import generation
- [ ] Conversational refinement maintains context
- [ ] Dynamic keywords are recognized and used
- [ ] Spelling tolerance works

### Code Quality Checks:
- [ ] Generated code is clean and readable
- [ ] Uses pl.read_csv() not pd.read_csv()
- [ ] Layering with + operator when appropriate (bars + text)
- [ ] scale_factor=2.0 when saving
- [ ] Sensible defaults (colors, dimensions)
- [ ] Proper Altair type annotations (:N, :Q, :T)

### Edge Cases:
- [ ] Missing VIZARD keyword still works if keywords present
- [ ] Unknown plot types trigger helpful behavior (or fetch from gallery)
- [ ] Missing files generate reasonable error messages

---

## Feedback Questions

After testing, please share:

1. **Natural Language Feel:**
   - Does it feel natural to write specs?
   - Is the mix of keywords and prose smooth?
   - Any awkward phrasing required?

2. **Keyword Design:**
   - Are essential keywords clear?
   - Do dynamic keywords work intuitively?
   - Any keywords missing or unnecessary?

3. **Code Quality:**
   - Is generated code clean and Pythonic?
   - Does Polars streaming/chaining work as expected?
   - Are defaults sensible for your use cases?

4. **Consistency:**
   - Similar specs → similar outputs?
   - Conversational refinement smooth?
   - Appropriate level of variation?

5. **Missing Features:**
   - What plot types or customizations are you missing?
   - What bioinformatics-specific needs aren't addressed?
   - Any other keywords needed?

---

## Known Limitations (Phase 1)

- Only Altair backend (matplotlib coming later)
- Gallery fetching not yet tested
- Multi-panel layouts minimal examples
- No publication-specific features (DPI, specific formats) yet
- Some advanced Altair features may require natural language experimentation

---

## Next Steps After Your Testing

Based on your feedback, we'll:
1. **Refine CLAUDE.md** - Fix any issues, add missing keywords
2. **Add more examples** - Based on your most common use cases
3. **Test gallery fetching** - For unfamiliar plot types
4. **Create refined planning prompt** - For Step 3 (comprehensive Vizard expansion)
5. **Add more plot types** - Based on priority
6. **Begin matplotlib backend** - If Altair works well

---

**Ready to test!** Try a variety of specifications and see what works. The more edge cases you find, the better we can refine Vizard.
