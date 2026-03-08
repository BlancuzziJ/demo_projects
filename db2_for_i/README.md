# DB2 for i (IBM i / AS400) — Python ODBC + pandas Demo

This demo shows how to connect to an **IBM DB2 for i** database from Python
using **ODBC**, execute SQL queries, and analyse the results with **pandas**.

---

## Prerequisites

### 1. IBM i Access ODBC Driver

Install the [IBM i Access Client Solutions](https://www.ibm.com/support/pages/ibm-i-access-client-solutions)
package for your platform, which bundles the **IBM i Access ODBC Driver**.

> On Linux you can also use the standalone
> [IBM i Access ODBC Driver for Linux](https://www.ibm.com/support/pages/odbc-driver-linux).

After installation, confirm the driver is visible to the ODBC Driver Manager:

```bash
# On Linux / macOS (unixODBC)
odbcinst -q -d

# On Windows
odbcad32.exe   # opens the ODBC Administrator GUI
```

The driver name used by default in this demo is **`IBM i Access ODBC Driver`**.
Set `DB2I_DRIVER` (see below) if your installation uses a different name.

### 2. Python dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

All credentials are supplied through **environment variables** — never
hard-code passwords in source files.

| Variable | Required | Description |
|---|---|---|
| `DB2I_HOST` | Yes* | IBM i hostname or IP address |
| `DB2I_USER` | Yes | Database user name |
| `DB2I_PASSWORD` | Yes | Database password |
| `DB2I_DSN` | No* | Pre-configured ODBC DSN name (replaces host-based string) |
| `DB2I_DRIVER` | No | ODBC driver name (default: `IBM i Access ODBC Driver`) |
| `DB2I_LIBRARY` | No | Default library / schema (default: `MYLIB`) |

\* Either `DB2I_HOST` **or** `DB2I_DSN` must be set.

### Setting variables (Linux / macOS)

```bash
export DB2I_HOST=my-ibmi-server
export DB2I_USER=myuser
export DB2I_PASSWORD=mypassword
export DB2I_LIBRARY=MYLIB
```

### Setting variables (Windows PowerShell)

```powershell
$env:DB2I_HOST     = "my-ibmi-server"
$env:DB2I_USER     = "myuser"
$env:DB2I_PASSWORD = "mypassword"
$env:DB2I_LIBRARY  = "MYLIB"
```

---

## Running the demo

```bash
python db2_query.py
```

The script will:

1. Open an ODBC connection to the IBM i system.
2. Query the `ORDERS` table and print a summary with per-customer lifetime
   sales totals computed by pandas.
3. Query the `INVENTORY` table and list items at or below the reorder level.
4. Close the connection.

Adjust the table and column names inside `db2_query.py` to match the actual
schema on your IBM i system.

---

## Key functions

| Function | Description |
|---|---|
| `build_connection_string()` | Builds the ODBC connection string from environment variables |
| `get_connection()` | Returns an open `pyodbc.Connection` |
| `query_to_dataframe(conn, sql, params)` | Executes a parameterised query and returns a `pd.DataFrame` |
| `summarise_dataframe(df, label)` | Prints shape, dtypes, and descriptive statistics |
| `analyse_sales(conn, library)` | Aggregates order totals per customer |
| `analyse_inventory(conn, library)` | Identifies low-stock and out-of-stock items |

---

## Security notes

* Credentials are read from environment variables at runtime and are never
  stored in the source file or version control.
* The `.gitignore` at the repository root already excludes `.env` files.
* Use parameterised queries (the `params` argument in `query_to_dataframe`)
  whenever incorporating user-supplied values in SQL to prevent SQL injection.
