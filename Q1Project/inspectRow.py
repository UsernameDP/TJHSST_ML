#!/usr/bin/env python3
import csv
import sys

if len(sys.argv) < 2:
    print("Usage: python script.py <csv_file>")
    sys.exit(1)

file_name = sys.argv[1]

# Load the file once
with open(file_name, "r", encoding="utf-8", newline="") as f:
    reader = list(csv.reader(f))
    header = reader[0]
    rows = reader[1:]

print(f"Loaded {len(rows)} data rows (header excluded).")

while True:
    choice = input("Enter data row number to view (or 'q' to quit): ")
    if choice.lower() == "q":
        break

    try:
        row_num = int(choice)
        if 1 <= row_num <= len(rows):  # now starts at 1 for the first data row
            row = rows[row_num - 1]
            print(f"\nRow {row_num}:")
            for col_name, value in zip(header, row):
                print(f"  {col_name}: {value}")
            print()
        else:
            print(f"❌ Row number out of range (valid: 1–{len(rows)}).")
    except ValueError:
        print("❌ Please enter a valid number or 'q'.")
