#!/usr/bin/env python3
"""
Generate synthetic CSV data files for Vizard README examples.

Creates 8 CSV files in the test/data/ directory with realistic data distributions.
Uses fixed random seed for reproducibility.
"""

import csv
from pathlib import Path
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

# Output directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

print("Generating synthetic data files...")
print(f"Output directory: {DATA_DIR}")
print()

# =============================================================================
# 1. sales.csv - Product revenue data for bar charts
# =============================================================================
print("1. Creating sales.csv...")
products = [
    ("Product A", 45000, "Electronics"),
    ("Product B", 32000, "Furniture"),
    ("Product C", 58000, "Electronics"),
    ("Product D", 23000, "Office Supplies"),
    ("Product E", 41000, "Furniture"),
    ("Product F", 28000, "Office Supplies"),
    ("Product G", 51000, "Electronics"),
    ("Product H", 36000, "Furniture"),
]

with open(DATA_DIR / "sales.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["product", "revenue", "category"])
    writer.writerows(products)

# =============================================================================
# 2. genes.csv - Gene expression and p-values for scatter plots
# =============================================================================
print("2. Creating genes.csv...")
gene_names = [
    "BRCA1", "TP53", "EGFR", "MYC", "KRAS", "PTEN", "AKT1", "BRAF",
    "PIK3CA", "RB1", "ERBB2", "CDKN2A", "VHL", "APC", "SMAD4", "ATM",
    "CDH1", "FGFR2", "NRAS", "HRAS", "STK11", "MLH1", "MSH2", "FBXW7",
    "NOTCH1", "JAK2", "KIT", "RET", "ALK", "MET"
]

with open(DATA_DIR / "genes.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["gene_name", "expression", "pvalue", "significant"])

    for gene in gene_names:
        # Create mix of significant and non-significant genes
        if random.random() < 0.4:  # 40% significant
            expression = random.uniform(4.0, 7.0)  # Higher expression
            pvalue = random.uniform(0.0001, 0.05)  # Low p-value
            significant = "True"
        else:
            expression = random.uniform(1.0, 4.0)  # Lower expression
            pvalue = random.uniform(0.05, 1.0)  # High p-value
            significant = "False"

        writer.writerow([gene, round(expression, 2), round(pvalue, 4), significant])

# =============================================================================
# 3. timeseries.csv - Temperature time series for line charts
# =============================================================================
print("3. Creating timeseries.csv...")
locations = ["New York", "Los Angeles", "Chicago"]
start_date = datetime(2024, 1, 1)
base_temps = {"New York": 20, "Los Angeles": 28, "Chicago": 15}

with open(DATA_DIR / "timeseries.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["date", "temperature", "location"])

    for day in range(30):  # 30 days of data
        date = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
        for location in locations:
            # Add seasonal trend and random variation
            base = base_temps[location]
            trend = day * 0.2  # Warming trend
            noise = random.uniform(-3, 3)
            temp = round(base + trend + noise, 1)
            writer.writerow([date, temp, location])

# =============================================================================
# 4. expression.csv - Gene expression by condition for grouped bar charts
# =============================================================================
print("4. Creating expression.csv...")
genes_expr = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "PTEN"]
conditions = ["treated", "control"]

with open(DATA_DIR / "expression.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["gene_name", "expression_level", "condition"])

    for gene in genes_expr:
        base_level = random.uniform(3.0, 7.0)
        for condition in conditions:
            # Treated has higher expression on average
            if condition == "treated":
                level = base_level + random.uniform(0.5, 2.0)
            else:
                level = base_level + random.uniform(-1.0, 0.5)
            writer.writerow([gene, round(level, 2), condition])

# =============================================================================
# 5. data.csv - Faceted scatter plot data
# =============================================================================
print("5. Creating data.csv...")
conditions_facet = ["control", "treated"]
replicates = ["rep1", "rep2", "rep3"]

with open(DATA_DIR / "data.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["value1", "value2", "condition", "replicate"])

    for condition in conditions_facet:
        for replicate in replicates:
            # Generate 10 data points per condition-replicate combination
            for _ in range(10):
                # Create correlation between value1 and value2
                value1 = random.uniform(0, 10)
                if condition == "treated":
                    value2 = value1 * 1.5 + random.uniform(-2, 2)  # Stronger correlation
                else:
                    value2 = value1 * 0.8 + random.uniform(-3, 3)  # Weaker correlation

                writer.writerow([
                    round(value1, 2),
                    round(value2, 2),
                    condition,
                    replicate
                ])

# =============================================================================
# 6. diff_expression.csv - Volcano plot data
# =============================================================================
print("6. Creating diff_expression.csv...")
import math

with open(DATA_DIR / "diff_expression.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["gene_name", "log2fc", "neg_log10_pvalue"])

    for i, gene in enumerate(gene_names + [f"Gene{j}" for j in range(30)]):  # 60 total genes
        # Create different gene expression patterns
        if i < 10:  # Upregulated (high log2fc, low pvalue)
            log2fc = random.uniform(1.5, 4.0)
            pvalue = random.uniform(0.0001, 0.01)
        elif i < 20:  # Downregulated (low log2fc, low pvalue)
            log2fc = random.uniform(-4.0, -1.5)
            pvalue = random.uniform(0.0001, 0.01)
        else:  # Not significant
            log2fc = random.uniform(-1.5, 1.5)
            pvalue = random.uniform(0.05, 1.0)

        neg_log10_pvalue = -math.log10(pvalue) if pvalue > 0 else 10
        writer.writerow([gene, round(log2fc, 2), round(neg_log10_pvalue, 2)])

# =============================================================================
# 7. expression_matrix.csv - Sample × gene matrix for heatmap
# =============================================================================
print("7. Creating expression_matrix.csv...")
samples = [f"Sample{i+1}" for i in range(5)]
genes_heatmap = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "PTEN", "AKT1", "BRAF", "PIK3CA", "RB1"]

with open(DATA_DIR / "expression_matrix.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["sample", "gene", "expression"])

    for sample in samples:
        for gene in genes_heatmap:
            # Create patterns - some genes are correlated across samples
            if gene in ["BRCA1", "TP53"]:
                # High expression group
                expression = random.uniform(5.0, 8.0)
            elif gene in ["PIK3CA", "RB1"]:
                # Low expression group
                expression = random.uniform(1.0, 3.0)
            else:
                # Medium expression
                expression = random.uniform(3.0, 6.0)

            writer.writerow([sample, gene, round(expression, 2)])

# =============================================================================
# 8. measurements.csv - Box plot data
# =============================================================================
print("8. Creating measurements.csv...")
groups = ["Control", "Treated", "High Dose"]

with open(DATA_DIR / "measurements.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["group", "value"])

    # Control group - lower values
    for _ in range(25):
        value = random.gauss(20, 3)  # mean=20, std=3
        writer.writerow(["Control", round(value, 2)])

    # Treated group - medium values
    for _ in range(25):
        value = random.gauss(28, 4)  # mean=28, std=4
        writer.writerow(["Treated", round(value, 2)])

    # High Dose group - higher values with more variation
    for _ in range(25):
        value = random.gauss(35, 5)  # mean=35, std=5
        writer.writerow(["High Dose", round(value, 2)])

print()
print("✓ All 8 CSV files generated successfully!")
print()
print("Files created:")
for i, filename in enumerate([
    "sales.csv", "genes.csv", "timeseries.csv", "expression.csv",
    "data.csv", "diff_expression.csv", "expression_matrix.csv", "measurements.csv"
], 1):
    filepath = DATA_DIR / filename
    print(f"  {i}. {filename:25s} ({filepath.stat().st_size} bytes)")

print()
print(f"Total files: 8")
print(f"Location: {DATA_DIR}")
