#!/usr/bin/env python3
import csv
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python script.py <input.csv> [output.csv]")
    sys.exit(1)

input_file = sys.argv[1]

# Default output if not specified
if len(sys.argv) >= 3:
    output_file = sys.argv[2]
else:
    root, ext = os.path.splitext(input_file)
    output_file = f"{root}_clean{ext or '.csv'}"

with open(input_file, "r", encoding="utf-8", newline="") as infile, open(
    output_file, "w", encoding="utf-8", newline=""
) as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # clean each cell: remove quotes, replace newlines, and trim spaces
        cleaned_row = [
            cell.replace('"', "")
            .replace("'", "")
            .replace("\n", " ")
            .replace("\r", " ")
            .strip()
            for cell in row
        ]
        writer.writerow(cleaned_row)

print(f"Cleaned CSV saved as {output_file}")
