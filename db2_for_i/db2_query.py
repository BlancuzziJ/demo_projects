"""
DB2 for i (IBM i / AS400) Database Query and Pandas Analysis using ODBC.

This demo connects to a DB2 for i database via ODBC, executes SQL queries, and
performs data analysis using pandas.

Prerequisites:
  - IBM i Access ODBC Driver installed on the client machine.
  - An ODBC Data Source Name (DSN) configured, or direct connection string.
  - Environment variables set for connection credentials (see README.md).

Usage:
  python db2_query.py
"""

import os
import sys

import pandas as pd
import pyodbc


# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------

def build_connection_string() -> str:
    """Build an ODBC connection string from environment variables.

    Required environment variables:
        DB2I_HOST     - IBM i hostname or IP address
        DB2I_USER     - Database user name
        DB2I_PASSWORD - Database password

    Optional environment variables:
        DB2I_DSN      - Pre-configured ODBC DSN name (overrides host-based string)
        DB2I_DRIVER   - ODBC driver name
                        (default: "IBM i Access ODBC Driver")
        DB2I_LIBRARY  - Default schema / library
                        (default: not set)
    """
    dsn = os.environ.get("DB2I_DSN")
    if dsn:
        user = os.environ.get("DB2I_USER", "")
        password = os.environ.get("DB2I_PASSWORD", "")
        return f"DSN={dsn};UID={user};PWD={password};"

    host = os.environ.get("DB2I_HOST")
    user = os.environ.get("DB2I_USER")
    password = os.environ.get("DB2I_PASSWORD")
    driver = os.environ.get("DB2I_DRIVER", "IBM i Access ODBC Driver")
    library = os.environ.get("DB2I_LIBRARY", "")

    if not host or not user or not password:
        raise EnvironmentError(
            "Missing required environment variables. Set DB2I_HOST, DB2I_USER, "
            "and DB2I_PASSWORD (or DB2I_DSN, DB2I_USER, DB2I_PASSWORD)."
        )

    conn_str = f"DRIVER={{{driver}}};SYSTEM={host};UID={user};PWD={password};"
    if library:
        conn_str += f"DBQ={library};"
    return conn_str


def get_connection() -> pyodbc.Connection:
    """Return an open pyodbc connection to the DB2 for i database."""
    conn_str = build_connection_string()
    conn = pyodbc.connect(conn_str, autocommit=True)
    return conn


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def query_to_dataframe(conn: pyodbc.Connection, sql: str, params=None) -> pd.DataFrame:
    """Execute *sql* and return the result set as a pandas DataFrame.

    Args:
        conn:   An open pyodbc connection.
        sql:    SQL query string.  Use ``?`` as parameter placeholders.
        params: Iterable of parameter values (optional).

    Returns:
        A pandas DataFrame with one row per result-set row.
    """
    if params is None:
        params = []
    cursor = conn.cursor()
    cursor.execute(sql, params)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    return pd.DataFrame.from_records(rows, columns=columns)


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def summarise_dataframe(df: pd.DataFrame, label: str = "") -> None:
    """Print a concise summary of *df* to stdout."""
    title = f"  {label}  " if label else "  DataFrame Summary  "
    bar = "=" * max(len(title) + 4, 40)
    print(f"\n{bar}")
    print(title)
    print(bar)
    print(f"Shape : {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    print("\nData types:")
    print(df.dtypes.to_string())
    print("\nDescriptive statistics (numeric columns):")
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        print(numeric.describe().to_string())
    else:
        print("  (no numeric columns)")
    print("\nFirst 5 rows:")
    print(df.head().to_string())


def analyse_sales(conn: pyodbc.Connection, library: str) -> None:
    """Example analysis: total sales by customer from an order-detail table.

    Adjust the table/column names to match your DB2 for i schema.

    Args:
        conn:    An open pyodbc connection.
        library: The DB2 for i library (schema) that contains the tables.
    """
    sql = f"""
        SELECT
            CUST_ID,
            ORDER_DATE,
            SUM(LINE_TOTAL) AS TOTAL_AMOUNT
        FROM {library}.ORDERS
        GROUP BY
            CUST_ID,
            ORDER_DATE
        ORDER BY
            ORDER_DATE DESC,
            TOTAL_AMOUNT DESC
        FETCH FIRST 100 ROWS ONLY
    """
    df = query_to_dataframe(conn, sql)
    summarise_dataframe(df, label="Sales by Customer (top 100)")

    # Aggregate to per-customer totals
    customer_totals = (
        df.groupby("CUST_ID")["TOTAL_AMOUNT"]
        .sum()
        .reset_index()
        .rename(columns={"TOTAL_AMOUNT": "LIFETIME_SALES"})
        .sort_values("LIFETIME_SALES", ascending=False)
    )
    print("\nTop 10 customers by lifetime sales:")
    print(customer_totals.head(10).to_string(index=False))


def analyse_inventory(conn: pyodbc.Connection, library: str) -> None:
    """Example analysis: low-stock items from an inventory table.

    Adjust the table/column names to match your DB2 for i schema.

    Args:
        conn:    An open pyodbc connection.
        library: The DB2 for i library (schema) that contains the tables.
    """
    sql = f"""
        SELECT
            ITEM_ID,
            ITEM_DESC,
            QTY_ON_HAND,
            REORDER_LEVEL
        FROM {library}.INVENTORY
        WHERE QTY_ON_HAND <= REORDER_LEVEL
        ORDER BY QTY_ON_HAND
        FETCH FIRST 50 ROWS ONLY
    """
    df = query_to_dataframe(conn, sql)
    summarise_dataframe(df, label="Low-Stock Inventory Items")

    # Flag items that are completely out of stock
    out_of_stock = df[df["QTY_ON_HAND"] == 0]
    print(f"\nItems completely out of stock: {len(out_of_stock)}")
    if not out_of_stock.empty:
        print(out_of_stock.to_string(index=False))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Run the DB2 for i demo queries and analysis."""
    library = os.environ.get("DB2I_LIBRARY", "MYLIB")

    try:
        print("Connecting to DB2 for i …")
        conn = get_connection()
        print("Connected successfully.\n")
    except EnvironmentError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1
    except pyodbc.Error as exc:
        print(f"Database connection error: {exc}", file=sys.stderr)
        return 1

    try:
        analyse_sales(conn, library)
        analyse_inventory(conn, library)
    except pyodbc.Error as exc:
        print(f"Query error: {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()
        print("\nConnection closed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
