#!/usr/bin/env python3
import csv
import sys
import os
import shutil

if len(sys.argv) < 3:
    print("Usage: python script.py <input.csv> <output.csv>")
    sys.exit(1)

INPUT = sys.argv[1]
OUTPUT = sys.argv[2]

# If input and output are the same, make a safety backup first
if os.path.abspath(INPUT) == os.path.abspath(OUTPUT):
    root, ext = os.path.splitext(INPUT)
    backup_path = f"{root}_backup{ext or '.csv'}"
    shutil.copy2(INPUT, backup_path)
    print(f"[Backup] Created backup at: {backup_path}")

# Load rows into memory
with open(INPUT, encoding="utf-8", newline="") as f:
    reader = list(csv.reader(f))
    if not reader:
        print("File is empty.")
        sys.exit(1)
    header, rows = reader[0], reader[1:]

print(f"Loaded {len(rows)} data rows (plus header) from {INPUT}.")


def save(rows_):
    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows_)
    print(f"Saved {len(rows_)} rows to {OUTPUT}")


def _trunc_cell(s: str, max_len: int = 30) -> str:
    s = "" if s is None else str(s)
    return (s[: max_len - 1] + "…") if len(s) > max_len else s


def preview_row(row, max_cells: int = 6, max_cell_len: int = 30) -> str:
    """
    Return a compact string preview of a row:
    - Shows up to `max_cells` cells.
    - Each cell truncated to `max_cell_len` characters.
    """
    shown = row[:max_cells]
    parts = [_trunc_cell(c, max_cell_len) for c in shown]
    suffix = " …(+more cells)" if len(row) > max_cells else ""
    return "[" + " | ".join(parts) + "]" + suffix


while True:
    cmd = input("Enter row number to delete (q to quit): ").strip()
    if cmd.lower() in ("q", "quit", "exit", ""):
        break
    try:
        n = int(cmd)
        if n < 2 or n > len(rows) + 1:
            print(f"Row {n} is out of range (valid data rows are 2–{len(rows)+1})")
            continue

        idx = n - 2  # adjust for header at line 1
        candidate = rows[idx]
        preview = preview_row(candidate)

        print(f"\nAbout to delete line {n}. Preview (truncated):\n  {preview}")
        confirm = (
            input("Are you sure you want to delete this row? [y/N]: ").strip().lower()
        )

        if confirm in ("y", "yes"):
            removed = rows.pop(idx)
            print(f"✅ Deleted line {n}.")
            save(rows)
        else:
            print("❎ Deletion cancelled. No changes saved.")

    except ValueError:
        print("Please enter a valid integer row number or 'q' to quit.")
