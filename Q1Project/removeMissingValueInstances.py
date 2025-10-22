#!/usr/bin/env python3
import csv
import sys
import os
import shutil

CASE_INSENSITIVE = True


def norm(s: str) -> str:
    return s.lower() if CASE_INSENSITIVE else s


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        sys.exit("❌ Empty CSV.")
    header, data = rows[0], rows[1:]
    if header and header[0].startswith("\ufeff"):
        header[0] = header[0].lstrip("\ufeff")
    return header, data


def save_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    if len(sys.argv) < 2:
        print("Usage: python drop_missing.py <input.csv> [output.csv]")
        sys.exit(1)

    input_csv = sys.argv[1]
    header, rows = load_csv(input_csv)

    print(f"Loaded {len(rows)} data rows, {len(header)} columns from {input_csv}\n")
    print("Columns:")
    for i, h in enumerate(header, start=1):
        print(f"  {i:>3}: {h}")

    choice = input(
        "\nAttribute to check for missing values (name or 1-based index): "
    ).strip()
    if not choice:
        sys.exit("No attribute provided. Aborting.")

    if choice.isdigit():
        col_idx = int(choice) - 1
        if not (0 <= col_idx < len(header)):
            sys.exit(f"❌ Index {choice} out of range (1–{len(header)}).")
        col_name = header[col_idx]
    else:
        lowered = [norm(h) for h in header]
        key = norm(choice)
        if key not in lowered:
            sys.exit(f"❌ Column '{choice}' not found.")
        col_idx = lowered.index(key)
        col_name = header[col_idx]

    # Default output name if not given
    if len(sys.argv) >= 3:
        output_csv = sys.argv[2]
    else:
        root, ext = os.path.splitext(input_csv)
        output_csv = f"{root}_drop_{col_name}{ext or '.csv'}"

    # Find rows to keep/drop
    missing = []
    kept = []
    for idx, row in enumerate(rows, start=2):  # start=2 for line number
        if len(row) <= col_idx:
            missing.append((idx, row))
            continue
        val = row[col_idx].strip()
        if val == "" or val == "?":
            missing.append((idx, row))
        else:
            kept.append(row)

    print(f"\nFound {len(missing)} row(s) with missing values in '{col_name}'.")
    if missing:
        print("Example (first 5):")
        for idx, row in missing[:5]:
            preview = ", ".join(row[:6]) + (" ..." if len(row) > 6 else "")
            print(f"  Line {idx}: {preview}")

    confirm = input("\nDo you want to delete these rows? [y/N]: ").strip().lower()
    if confirm not in ("y", "yes"):
        print("❎ Cancelled. No changes made.")
        sys.exit(0)

    # Backup if overwriting
    if os.path.abspath(input_csv) == os.path.abspath(output_csv):
        backup = input_csv + ".bak"
        shutil.copy2(input_csv, backup)
        print(f"[Backup] Original file copied to {backup}")

    save_csv(output_csv, header, kept)
    print(f"\n✅ Saved file without missing '{col_name}' rows to {output_csv}")
    print(f"Kept {len(kept)} rows, removed {len(missing)} rows.")


if __name__ == "__main__":
    main()
