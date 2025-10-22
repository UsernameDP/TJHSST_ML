#!/usr/bin/env python3
import csv
import sys
import os
import shutil

if len(sys.argv) < 2:
    print("Usage: python numericToNominal.py <input.csv> [output.csv]")
    sys.exit(1)

input_file = sys.argv[1]

# Default output file name
if len(sys.argv) >= 3:
    output_file = sys.argv[2]
else:
    root, ext = os.path.splitext(input_file)
    output_file = f"{root}_nominal{ext or '.csv'}"

# Safety backup if overwriting
if os.path.abspath(input_file) == os.path.abspath(output_file):
    backup_path = input_file + ".bak"
    shutil.copy2(input_file, backup_path)
    print(f"[Backup] Created backup at {backup_path}")

# Load CSV
with open(input_file, encoding="utf-8", newline="") as f:
    reader = list(csv.reader(f))
    if not reader:
        print("File is empty.")
        sys.exit(1)
    header, rows = reader[0], reader[1:]

print(f"Loaded {len(rows)} data rows, {len(header)} columns.\n")

# Show available columns
print("Available columns:")
for i, name in enumerate(header, start=1):
    print(f"  {i:>3}: {name}")

# Ask user for column
choice = input("\nEnter column name or index to convert to nominal: ").strip()

if choice.isdigit():
    col_idx = int(choice) - 1
    if not (0 <= col_idx < len(header)):
        print(f"❌ Column index {choice} is out of range.")
        sys.exit(1)
    col_name = header[col_idx]
else:
    lowered = [h.lower().strip() for h in header]
    if choice.lower() not in lowered:
        print(f"❌ Column '{choice}' not found.")
        sys.exit(1)
    col_idx = lowered.index(choice.lower())
    col_name = header[col_idx]

print(f"\nConverting column '{col_name}' (index {col_idx+1}) to nominal...")

# Convert: wrap values in a prefix like "val_" so Weka doesn't treat them as numeric
for row in rows:
    if col_idx < len(row):
        val = row[col_idx].strip()
        if val != "":
            row[col_idx] = f"{val}_val"

# Save
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"\n✅ Saved with nominal conversion: {output_file}")
