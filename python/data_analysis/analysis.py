"""
Sales Data Analysis Demo
========================
Loads a sample sales CSV, cleans the data, prints summary statistics,
and saves revenue charts to the output/ directory.
"""

import os
import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend – no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Sample data (inline so the script runs without an external file)
# ---------------------------------------------------------------------------
SAMPLE_CSV = """order_id,date,region,product,quantity,unit_price
1,2024-01-05,North,Widget A,10,25.00
2,2024-01-12,South,Widget B,5,40.00
3,2024-02-03,East,Widget A,8,25.00
4,2024-02-18,North,Widget C,3,60.00
5,2024-03-07,West,Widget B,12,40.00
6,2024-03-15,South,Widget A,7,25.00
7,2024-04-02,East,Widget C,4,60.00
8,2024-04-20,North,Widget B,9,40.00
9,2024-05-11,West,Widget A,15,25.00
10,2024-05-28,South,Widget C,6,60.00
11,2024-06-09,North,Widget A,11,25.00
12,2024-06-30,East,Widget B,8,40.00
"""


def load_data(csv_text: str) -> pd.DataFrame:
    """Load CSV text into a DataFrame and cast types."""
    df = pd.read_csv(io.StringIO(csv_text))
    df["date"] = pd.to_datetime(df["date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df


def print_summary(df: pd.DataFrame) -> None:
    """Print high-level summary statistics."""
    print("=== Sales Summary ===")
    print(f"Total orders : {len(df)}")
    print(f"Total revenue: ${df['revenue'].sum():,.2f}")
    print(f"Date range   : {df['date'].min().date()} – {df['date'].max().date()}")

    print("\n--- Revenue by Region ---")
    by_region = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    print(by_region.to_string())

    print("\n--- Top Products by Revenue ---")
    by_product = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    print(by_product.to_string())


def plot_revenue_by_region(df: pd.DataFrame, output_dir: str) -> None:
    """Bar chart of total revenue per region."""
    by_region = df.groupby("region")["revenue"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(7, 4))
    by_region.plot(kind="bar", ax=ax, color="steelblue", edgecolor="white")
    ax.set_title("Total Revenue by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Revenue ($)")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()

    path = os.path.join(output_dir, "revenue_by_region.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"\nSaved: {path}")


def plot_monthly_trend(df: pd.DataFrame, output_dir: str) -> None:
    """Line chart of monthly revenue."""
    monthly = (
        df.set_index("date")
        .resample("ME")["revenue"]
        .sum()
        .reset_index()
    )
    monthly["month"] = monthly["date"].dt.strftime("%b %Y")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(monthly["month"], monthly["revenue"], marker="o", color="darkorange")
    ax.set_title("Monthly Revenue Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()

    path = os.path.join(output_dir, "monthly_trend.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"Saved: {path}")


def main() -> None:
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    df = load_data(SAMPLE_CSV)
    print_summary(df)
    plot_revenue_by_region(df, output_dir)
    plot_monthly_trend(df, output_dir)


if __name__ == "__main__":
    main()
