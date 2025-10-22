#!/usr/bin/env python3
import csv
import sys
import os
import shutil

# Toggle case-insensitive matching
CASE_INSENSITIVE = True


def normalize(name: str) -> str:
    return name.lower() if CASE_INSENSITIVE else name


def main(input_file, output_file):
    # Load CSV
    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = list(csv.reader(infile))
        if not reader:
            print("❌ Empty CSV.")
            sys.exit(1)
        header, rows = reader[0], reader[1:]

    print(f"Loaded {len(rows)} rows, {len(header)} columns.\n")

    print("Available columns:")
    for i, h in enumerate(header, start=1):
        print(f"  {i:>3}: {h}")

    # Ask user which attribute to remove
    choice = input("\nWhich attribute do you want to remove? (index or name): ").strip()
    if not choice:
        print("No attribute specified. Exiting.")
        sys.exit(0)

    # Figure out index
    if choice.isdigit():
        col_idx = int(choice) - 1
        if not (0 <= col_idx < len(header)):
            print(f"❌ Index {choice} is out of range (1–{len(header)}).")
            sys.exit(1)
        col_name = header[col_idx]
    else:
        lowered = [normalize(h) for h in header]
        if normalize(choice) not in lowered:
            print(f"❌ Column '{choice}' not found.")
            sys.exit(1)
        col_idx = lowered.index(normalize(choice))
        col_name = header[col_idx]

    # Backup if overwriting
    if os.path.abspath(input_file) == os.path.abspath(output_file):
        backup_file = input_file + ".bak"
        shutil.copy2(input_file, backup_file)
        print(f"[Backup] Original file copied to {backup_file}")

    # Save new file without that column
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        new_header = [h for i, h in enumerate(header) if i != col_idx]
        writer.writerow(new_header)
        for row in rows:
            if len(row) < len(header):
                row = row + [""] * (len(header) - len(row))
            writer.writerow([v for i, v in enumerate(row) if i != col_idx])

    print(f"\n✅ Saved cleaned file as {output_file}")
    print(f"Removed column: {col_name} (index {col_idx+1})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_col.py input.csv output.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
