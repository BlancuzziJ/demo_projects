# Sales Data Analysis

A demo Python project that loads a sample sales dataset, cleans the data, computes summary statistics, and generates basic visualizations using **pandas** and **matplotlib**.

## What it demonstrates

- Reading CSV data with `pandas`
- Cleaning and transforming a DataFrame (handling missing values, type casting)
- Computing grouped aggregations (revenue by region, top products)
- Plotting bar charts and a monthly trend line with `matplotlib`

## Setup

```bash
pip install -r requirements.txt
python analysis.py
```

## Output

Running the script prints a summary table to the terminal and saves two chart images:

- `output/revenue_by_region.png`
- `output/monthly_trend.png`
