
import os
import sys

import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILE = os.path.join(BASE_DIR, "customers.csv")
REQUIRED_COLUMNS = ["CustomerID", "Name", "City", "Purchases", "TotalSpent"]

SAMPLE_CSV = """CustomerID,Name,City,Purchases,TotalSpent
C01,Asha,Raipur,5,12000
C02,Bhavin,Durg,2,3000
C03,Chitra,Raipur,8,25000
C04,Deepak,Bhilai,1,800
C05,Esha,Durg,4,9000
C06,Farhan,Raipur,3,6000
C07,Gita,Bhilai,6,15000
C08,Hari,Durg,2,2200
"""


# Helpers
def money(value):
    """Format a rupee amount: whole numbers without decimals, others with 2."""
    value = float(value)
    if value == int(value):
        return f"Rs. {int(value)}"
    return f"Rs. {value:.2f}"


def money2(value):
    """Format a rupee amount always with 2 decimal places."""
    return f"Rs. {float(value):.2f}"


def create_sample_file(path=DEFAULT_FILE):
    """Write the sample dataset from the problem statement to disk."""
    with open(path, "w", newline="") as f:
        f.write(SAMPLE_CSV)


# Loading data (with missing-file / bad-data handling)
def load_customers(path):
    """
    Load and validate the customer CSV.
    Returns a DataFrame, or None if the file cannot be used
    (an error message is printed in that case).
    """
    try:
        df = pd.read_csv(path, skipinitialspace=True)
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{path}' is empty.")
        return None
    except pd.errors.ParserError as err:
        print(f"Error: Could not read '{path}' as a CSV file ({err}).")
        return None
    except (PermissionError, IsADirectoryError, OSError) as err:
        print(f"Error: Could not open '{path}' ({err}).")
        return None

    df.columns = [str(c).strip() for c in df.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        print("Error: CSV is missing required column(s): " + ", ".join(missing))
        return None

    # Clean text columns and make sure TotalSpent / Purchases are numeric
    for col in ("CustomerID", "Name", "City"):
        df[col] = df[col].astype(str).str.strip()
    df["TotalSpent"] = pd.to_numeric(df["TotalSpent"], errors="coerce")
    df["Purchases"] = pd.to_numeric(df["Purchases"], errors="coerce")

    bad_rows = int(df["TotalSpent"].isna().sum())
    if bad_rows:
        print(f"Warning: {bad_rows} row(s) with invalid TotalSpent were ignored.")
        df = df.dropna(subset=["TotalSpent"])

    if df.empty:
        print("Error: No valid customer records found in the file.")
        return None

    return df.reset_index(drop=True)


# Feature 1: Spending statistics
def spending_statistics(df):
    mean_spend = df["TotalSpent"].mean()
    median_spend = df["TotalSpent"].median()

    top = df[df["TotalSpent"] == df["TotalSpent"].max()]
    low = df[df["TotalSpent"] == df["TotalSpent"].min()]

    print(f"Mean spend: {money2(mean_spend)}")
    print(f"Median spend: {money2(median_spend)}")
    print(f"Highest: {', '.join(top['Name'])} ({money(top['TotalSpent'].iloc[0])})")
    print(f"Lowest: {', '.join(low['Name'])} ({money(low['TotalSpent'].iloc[0])})")


# Feature 2: High-value customers
def read_limit(raw=None):
    """
    Ask for the spending limit and validate it.
    Returns a float, or None if the input was invalid
    (an error message is printed in that case).
    """
    if raw is None:
        raw = input("Enter spending limit (Rs.): ")
    raw = raw.strip()
    try:
        limit = float(raw)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return None
    if limit != limit or limit in (float("inf"), float("-inf")):  # nan / inf
        print("Invalid amount. Please enter a number.")
        return None
    if limit < 0:
        print("Amount must be 0 or more.")
        return None
    return limit


def high_value_customers(df, limit):
    selected = df[df["TotalSpent"] >= limit]
    print(f"High-value customers (TotalSpent >= {money(limit)[4:]}): {len(selected)}")
    for _, row in selected.iterrows():
        print(f"{row['CustomerID']} | {row['Name']} | {row['City']} | "
              f"{money(row['TotalSpent'])}")


# Feature 3: City-wise summary
def city_wise_summary(df):
    summary = df.groupby("City", sort=False)["TotalSpent"].agg(["sum", "mean"])
    summary = summary.sort_values("sum", ascending=False)  # biggest city first
    for city, row in summary.iterrows():
        print(f"{city} : Total {money(row['sum'])} | Average {money2(row['mean'])}")


# Menu
MENU = """
===== Retail Customer Analyzer =====
1. Spending statistics
2. High-value customers
3. City-wise summary
4. Exit
"""


def run_menu(df):
    while True:
        print(MENU)
        choice = input("Enter your choice (1-4): ").strip()
        print()
        if choice == "1":
            spending_statistics(df)
        elif choice == "2":
            limit = read_limit()
            if limit is not None:
                high_value_customers(df, limit)
        elif choice == "3":
            city_wise_summary(df)
        elif choice == "4":
            print("Thank you for using Retail Customer Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")


# Built-in test cases (from the problem statement)
def run_tests():
    path = "_test_customers.csv"
    create_sample_file(path)
    df = load_customers(path)
    os.remove(path)

    import contextlib
    import io

    def capture(func, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            func(*args)
        return buf.getvalue().strip().splitlines()

    def check(name, actual, expected):
        ok = actual == expected
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            print("   expected:", expected)
            print("   actual  :", actual)
        return ok

    def limit_case(raw):
        return capture(lambda r: read_limit(r), raw)

    results = [
        check("Test Case 1: Normal input (Spending statistics)",
              capture(spending_statistics, df),
              ["Mean spend: Rs. 9125.00",
               "Median spend: Rs. 7500.00",
               "Highest: Chitra (Rs. 25000)",
               "Lowest: Deepak (Rs. 800)"]),

        check("Test Case 2: Boundary input (limit 25000)",
              capture(high_value_customers, df, read_limit("25000")),
              ["High-value customers (TotalSpent >= 25000): 1",
               "C03 | Chitra | Raipur | Rs. 25000"]),

        check("Test Case 3a: Invalid input 'abc'",
              limit_case("abc"),
              ["Invalid amount. Please enter a number."]),

        check("Test Case 3b: Invalid input '-500'",
              limit_case("-500"),
              ["Amount must be 0 or more."]),

        check("Test Case 4: City-wise summary",
              capture(city_wise_summary, df),
              ["Raipur : Total Rs. 43000 | Average Rs. 14333.33",
               "Bhilai : Total Rs. 15800 | Average Rs. 7900.00",
               "Durg : Total Rs. 14200 | Average Rs. 4733.33"]),
    ]

    print(f"\n{sum(results)}/{len(results)} checks passed.")
    return all(results)


# Main
def main():
    args = sys.argv[1:]

    if args and args[0] == "--test":
        sys.exit(0 if run_tests() else 1)

    path = args[0] if args else DEFAULT_FILE
    df = load_customers(path)

    # Missing file: let the user try another file or create the sample file
    while df is None:
        if os.path.exists(path):          # file exists but is unusable
            return
        try:
            answer = input("Enter another file name, type 'sample' to create the "
                           "sample file, or press Enter to quit: ").strip()
        except EOFError:
            return
        if not answer:
            return
        if answer.lower() == "sample":
            path = DEFAULT_FILE
            create_sample_file(path)
            print(f"Sample file '{path}' created.")
        else:
            path = answer
        df = load_customers(path)

    print(f"Loaded {len(df)} customer records from '{path}'.")
    run_menu(df)


if __name__ == "__main__":
    main()
