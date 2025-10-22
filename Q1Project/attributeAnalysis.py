#!/usr/bin/env python3
import csv
import sys
from collections import Counter

if len(sys.argv) < 2:
    print("Usage: python distinct_values.py <file.csv>")
    sys.exit(1)

path = sys.argv[1]

with open(path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    # Show attributes in numbered list
    print("Available attributes (columns):")
    for i, attr in enumerate(reader.fieldnames, start=1):
        print(f"{i}: {attr}")
    print()

    # Ask user which column to analyze (name or number)
    choice = input("Enter the attribute (column name or number) to check: ").strip()

    if choice.isdigit():
        col_num = int(choice)
        if not (1 <= col_num <= len(reader.fieldnames)):
            print(f"❌ Column number {col_num} is out of range.")
            sys.exit(1)
        attribute = reader.fieldnames[col_num - 1]  # convert to 0-based index
    else:
        if choice not in reader.fieldnames:
            print(f"❌ Column '{choice}' not found in CSV.")
            sys.exit(1)
        attribute = choice

    counts = Counter()
    for row in reader:
        val = row[attribute].strip()
        if val != "":  # skip empty cells
            counts[val] += 1

# Print results in table format
print(f"\nDistinct values for '{attribute}':\n")
print(f"{'Value':<30} | {'Frequency'}")
print("-" * 45)
for value, freq in counts.most_common():
    print(f"{value:<30} | {freq}")

print("-" * 45)
print(f"Total distinct values: {len(counts)}")
