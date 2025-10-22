#!/usr/bin/env python3
import csv
import sys
import os
import shutil

if len(sys.argv) < 2:
    print("Usage: python toNumeric.py <input.csv> [output.csv]")
    sys.exit(1)

input_file = sys.argv[1]

# Default output (built later once we know column name)
output_file = None
if len(sys.argv) >= 3:
    output_file = sys.argv[2]

# Load CSV
with open(input_file, "r", encoding="utf-8", newline="") as f:
    reader = list(csv.reader(f))
    if not reader:
        print("Empty CSV.")
        sys.exit(1)
    header = reader[0]
    rows = reader[1:]

print(f"Loaded {len(rows)} data rows, {len(header)} columns.")

# Show available columns
print("\nAvailable columns:")
for i, name in enumerate(header, start=1):
    print(f"  {i:>3}: {name}")

# Ask user for column
choice = input("\nEnter column name or index to convert: ").strip()

if choice.isdigit():
    col_idx = int(choice) - 1
    if not (0 <= col_idx < len(header)):
        print(f"❌ Column index {choice} out of range (1–{len(header)})")
        sys.exit(1)
    col_name = header[col_idx]
else:
    lowered = [h.lower().strip() for h in header]
    if choice.lower() not in lowered:
        print(f"❌ Column '{choice}' not found. Available: {header}")
        sys.exit(1)
    col_idx = lowered.index(choice.lower())
    col_name = header[col_idx]

# Build default output if not provided
if output_file is None:
    root, ext = os.path.splitext(input_file)
    output_file = f"{root}_{col_name}_numeric{ext or '.csv'}"

print(f"Checking column '{col_name}' (index {col_idx+1}) for non-numeric values...")


def is_numeric_string(s: str) -> bool:
    s = s.strip()
    if s == "" or s == "?":
        return True
    try:
        float(s)
        return True
    except ValueError:
        return False


# Scan rows for bad values
for i, row in enumerate(rows, start=2):  # start=2 accounts for header row
    if col_idx >= len(row):
        continue  # treat as empty
    val = row[col_idx].strip()
    if val == "" or val == "?":
        continue
    if not is_numeric_string(val):
        print(f"\n❌ Found non-numeric value in column '{col_name}':")
        print(f"- Row {i}: could not convert {val!r} to numeric. Full row:")
        print(f"  {row}")
        print("\n🚫 Operation aborted. No file has been written.")
        sys.exit(1)

# If we reach here, all values are numeric (or allowed)
for row in rows:
    if col_idx < len(row):
        v = row[col_idx].strip()
        if v == "" or v == "?":
            continue
        row[col_idx] = str(float(v))

# Backup if overwriting
if os.path.abspath(input_file) == os.path.abspath(output_file):
    backup_file = input_file + ".bak"
    shutil.copy2(input_file, backup_file)
    print(f"[Backup] Original file copied to {backup_file}")

# Save
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"\n✅ All values converted successfully. Saved cleaned file to {output_file}")
