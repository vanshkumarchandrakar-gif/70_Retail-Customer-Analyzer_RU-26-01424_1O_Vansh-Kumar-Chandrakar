# Retail Customer Analyzer

| | |
|---|---|
| **Name** | Vansh Kumar Chandrakar |
| **ERP** | RU-25-01424-1O |
| **PS No.** | 70 |
| **Project Title** | Retail Customer Analyzer |
| **Program** | B.Tech Computer Science and Engineering, First Semester |
| **University** | Rungta International Skills University |
| **Language** | Python 3 |

---

## Overview

Retail Customer Analyzer is a console-based Python program that reads retail customer data from a CSV file using **Pandas** and answers three common business questions:

- How much do customers spend on average, and who spends the most and the least?
- Which customers are high-value, based on a limit entered by the user?
- How does spending differ from city to city?

## Concepts Used

- **Pandas:** reading CSV files and working with DataFrames
- **Filtering:** selecting rows with a condition (`TotalSpent >= limit`)
- **Grouping:** `groupby` for city-wise totals and averages
- **Statistics:** mean, median, maximum and minimum
- **Input validation and error handling:** missing files, bad data, invalid user input

## Features

1. **Spending statistics:** shows the mean, median, highest and lowest `TotalSpent`, with the customer names for the highest and lowest.
2. **High-value customers:** the user enters a limit, and the program lists every customer whose `TotalSpent` is greater than or equal to it.
3. **City-wise summary:** shows the total and average spending for each city, largest city first.
4. **Input validation:** rejects non-numeric and negative limits with clear messages.
5. **Missing file handling:** if `customers.csv` is not found, the program lets the user enter another file name, create the sample file, or quit.
6. **Built-in test runner:** `--test` checks all four test cases automatically.

## Project Structure

```
.
├── retail_customer_analyzer.py   # main program
├── customers.csv                 # sample data (8 customers)
└── README.md
```

## Data Format

`customers.csv` has 5 columns and 8 sample rows:

```
CustomerID,Name,City,Purchases,TotalSpent
C01,Asha,Raipur,5,12000
C02,Bhavin,Durg,2,3000
C03,Chitra,Raipur,8,25000
C04,Deepak,Bhilai,1,800
C05,Esha,Durg,4,9000
C06,Farhan,Raipur,3,6000
C07,Gita,Bhilai,6,15000
C08,Hari,Durg,2,2200
```

## How to Run

1. Make sure Python 3 is installed, then install Pandas:
   ```
   pip install pandas
   ```
2. Open a terminal in the project folder and start the program:
   ```
   python retail_customer_analyzer.py
   ```
3. Choose an option from the menu:
   ```
   ===== Retail Customer Analyzer =====
   1. Spending statistics
   2. High-value customers
   3. City-wise summary
   4. Exit
   ```

To use a different CSV file, pass its name: `python retail_customer_analyzer.py other_file.csv`

## Test Cases

| # | Scenario | Input | Expected Output |
|---|---|---|---|
| 1 | Normal input | Menu 1 (Spending statistics) | Mean Rs. 9125.00, Median Rs. 7500.00, Highest: Chitra (Rs. 25000), Lowest: Deepak (Rs. 800) |
| 2 | Boundary input | Menu 2, limit `25000` | 1 customer: `C03 \| Chitra \| Raipur \| Rs. 25000` |
| 3 | Invalid input | Menu 2, limit `abc` / `-500` | `Invalid amount. Please enter a number.` / `Amount must be 0 or more.` |
| 4 | Different valid scenario | Menu 3 (City-wise summary) | Raipur Rs. 43000 (avg 14333.33), Bhilai Rs. 15800 (avg 7900.00), Durg Rs. 14200 (avg 4733.33) |

To run all test cases automatically:

```
python retail_customer_analyzer.py --test
```

Expected result:

```
[PASS] Test Case 1: Normal input (Spending statistics)
[PASS] Test Case 2: Boundary input (limit 25000)
[PASS] Test Case 3a: Invalid input 'abc'
[PASS] Test Case 3b: Invalid input '-500'
[PASS] Test Case 4: City-wise summary

5/5 checks passed.
```

## Sample Output

```
Mean spend: Rs. 9125.00
Median spend: Rs. 7500.00
Highest: Chitra (Rs. 25000)
Lowest: Deepak (Rs. 800)
```

```
Raipur : Total Rs. 43000 | Average Rs. 14333.33
Bhilai : Total Rs. 15800 | Average Rs. 7900.00
Durg : Total Rs. 14200 | Average Rs. 4733.33
```

## How It Works

- `load_customers()` reads the CSV with `pd.read_csv()`, checks that all 5 required columns exist, converts `TotalSpent` to numbers and skips invalid rows.
- `spending_statistics()` uses `.mean()`, `.median()`, `.max()` and `.min()` on the `TotalSpent` column.
- `read_limit()` validates the user's limit, and `high_value_customers()` filters the DataFrame with a boolean condition.
- `city_wise_summary()` groups the data by `City` and aggregates `sum` and `mean`.
- The program finds `customers.csv` next to the script, so it works no matter which folder it is started from.

## Error Handling

| Situation | Behaviour |
|---|---|
| CSV file missing | Prints an error and offers to use another file or create the sample file |
| Empty file or missing columns | Prints a clear error message |
| Invalid `TotalSpent` values | Those rows are skipped with a warning |
| Limit is not a number | `Invalid amount. Please enter a number.` |
| Limit is negative | `Amount must be 0 or more.` |
| Invalid menu choice | Asks the user to enter 1, 2, 3 or 4 |
