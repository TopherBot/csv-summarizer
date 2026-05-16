#!/usr/bin/env python3
"""csv_summarizer.py

A tiny, robust CLI utility that prints a quick summary of a CSV file.

Features
--------
- Pre‑flight checks for file existence and readability.
- Graceful handling of common CSV errors.
- Optional numeric statistics (mean, min, max) for user‑selected columns.

Usage
-----
    python csv_summarizer.py <path_to_csv> [--numeric col1 col2 ...]
"""

import argparse
import csv
import os
import sys
from statistics import mean
from typing import List, Dict, Any


def error_exit(message: str, exit_code: int = 1) -> None:
    """Print an error to stderr and exit with the given code."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)


def preflight_check(path: str) -> None:
    """Ensure *path* exists, is a file, and is readable.

    Raises
    ------
    SystemExit
        If any check fails, the program exits with a descriptive message.
    """
    if not os.path.exists(path):
        error_exit(f"File '{path}' does not exist.")
    if not os.path.isfile(path):
        error_exit(f"'{path}' is not a regular file.")
    if not os.access(path, os.R_OK):
        error_exit(f"File '{path}' is not readable.")


def load_csv(path: str) -> List[Dict[str, str]]:
    """Load CSV contents into a list of dictionaries.

    Returns
    -------
    List[Dict[str, str]]
        Each row as a mapping of column name → value.
    """
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                error_exit("CSV appears to have no header row.")
            rows = list(reader)
            return rows
    except csv.Error as e:
        error_exit(f"CSV parsing error: {e}")
    except UnicodeDecodeError as e:
        error_exit(f"Encoding error while reading '{path}': {e}")


def print_basic_summary(rows: List[Dict[str, str]]) -> None:
    """Print row count and column names."""
    if not rows:
        print("The CSV file is empty (no data rows).")
        return
    row_count = len(rows)
    columns = rows[0].keys()
    print(f"Rows: {row_count}")
    print("Columns: " + ", ".join(columns))


def compute_numeric_stats(rows: List[Dict[str, str]], columns: List[str]) -> None:
    """Compute and print mean, min, max for each specified numeric column.

    Non‑numeric values are ignored with a warning.
    """
    for col in columns:
        values: List[float] = []
        for i, row in enumerate(rows, start=1):
            raw = row.get(col)
            if raw is None:
                error_exit(f"Column '{col}' not found in row {i}.")
            try:
                values.append(float(raw))
            except ValueError:
                print(f"Warning: Non‑numeric value '{raw}' in column '{col}' (row {i}) ignored.", file=sys.stderr)
        if not values:
            print(f"Column '{col}' has no valid numeric data.")
            continue
        col_mean = mean(values)
        col_min = min(values)
        col_max = max(values)
        print(f"Stats for '{col}': mean={col_mean:.2f}, min={col_min}, max={col_max}")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize a CSV file with robust error handling.")
    parser.add_argument("csv_path", help="Path to the CSV file to summarise.")
    parser.add_argument(
        "--numeric",
        nargs="*",
        metavar="COL",
        help="List of column names to compute numeric statistics for.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    preflight_check(args.csv_path)
    rows = load_csv(args.csv_path)
    print_basic_summary(rows)
    if args.numeric:
        compute_numeric_stats(rows, args.numeric)


if __name__ == "__main__":
    main()
