# Generating README Example Images

This directory contains scripts and notebooks for generating example visualization images for the Vizard README.md.

## Quick Start

### Step 1: Generate Synthetic Data (if not already done)

```bash
cd /home/cdaniels/stuff/vizard/test
python3 generate_sample_data.py
```

This creates 8 CSV files in `data/`:
- sales.csv
- genes.csv
- timeseries.csv
- expression.csv
- data.csv
- diff_expression.csv
- expression_matrix.csv
- measurements.csv

### Step 2: Generate Images Using Jupyter Notebook

**Recommended approach:**

```bash
cd /home/cdaniels/stuff/vizard/test
jupyter notebook generate_images.ipynb
```

Then in the notebook:
1. Run all cells in order (Cell → Run All)
2. Each cell generates one visualization image
3. Images are saved to `docs/images/`
4. The final cell verifies all images were created

### Step 3: Verify Images

```bash
ls -lh docs/images/
```

You should see 8 PNG files:
- bar_chart_basic.png
- scatter_plot_basic.png
- line_chart_timeseries.png
- bar_chart_grouped.png
- scatter_faceted.png
- volcano_plot.png
- heatmap.png
- box_plot.png

## Files

- `generate_sample_data.py` - Creates synthetic CSV data files
- `generate_images.ipynb` - Jupyter notebook to generate visualization images (recommended)
- `data/` - Directory containing CSV files
- `docs/images/` - Output directory for generated images

## Troubleshooting

**Q: Images not saving?**
- Make sure you're running from the `test` directory
- Check that `docs/images/` directory exists
- Verify `vl-convert-python` is installed: `pip list | grep vl-convert`

**Q: %%cc magic not found?**
- Run `%load_ext vizard_magic` first
- Make sure vizard_magic is installed globally or in your environment

**Q: Data files not found?**
- Run `generate_sample_data.py` first
- Make sure you're in the `test` directory when running the notebook

## After Generating Images

Once all images are created, update the README.md to include them. See the parent directory's README.md for the updated version with inline images.
