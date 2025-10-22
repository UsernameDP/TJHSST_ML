#!/usr/bin/env python3
import csv
import sys
import os
import shutil

CASE_INSENSITIVE = True  # header name matching


def norm(s: str) -> str:
    return s.lower() if CASE_INSENSITIVE else s


def parse_values_list(s: str):
    """Accept '1;2;3' or '1,2,3' → ['1','2','3'] (trimmed)."""
    parts = []
    for chunk in s.split(";"):
        for t in chunk.split(","):
            t = t.strip()
            if t:
                parts.append(t)
    return parts


def split_cell_tokens(cell: str):
    """'1; 2 ;3' → ['1','2','3']; ''/'?' → []"""
    if cell is None:
        return []
    cell = str(cell).strip()
    if cell == "" or cell == "?":
        return []
    return [t.strip() for t in cell.split(";") if t.strip()]


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        sys.exit("❌ Empty CSV.")
    header, data = rows[0], rows[1:]
    if header and header[0].startswith("\ufeff"):  # strip BOM
        header[0] = header[0].lstrip("\ufeff")
    return header, data


def save_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    if len(sys.argv) < 2:
        print("Usage: python onehot_semicolon.py <input.csv> [output.csv]")
        sys.exit(1)

    input_csv = sys.argv[1]

    header, rows = load_csv(input_csv)
    print(f"Loaded {len(rows)} data rows, {len(header)} columns from {input_csv}\n")

    print("Columns:")
    for i, h in enumerate(header, start=1):
        print(f"  {i:>3}: {h}")

    # Choose column (name or 1-based index)
    choice = input("\nAttribute to one-hot encode (name or 1-based index): ").strip()
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

    # If no output filename provided, build default
    if len(sys.argv) >= 3:
        output_csv = sys.argv[2]
    else:
        root, ext = os.path.splitext(input_csv)
        output_csv = f"{root}_encode_{col_name}{ext or '.csv'}"

    # Get the full set of possible values
    print("\nEnter ALL possible values for this attribute (e.g., 1;2;3;4).")
    vals_input = input("Values> ").strip()
    vals = parse_values_list(vals_input)
    if not vals:
        sys.exit("❌ No values provided.")
    vals_set = set(vals)
    new_cols = [f"{col_name}__{v}" for v in vals]

    # Drop original?
    drop_orig = input(
        f"Drop original column '{col_name}'? [y/N]: "
    ).strip().lower() in ("y", "yes")

    # Output header
    out_header = []
    for i, h in enumerate(header):
        if i == col_idx:
            if not drop_orig:
                out_header.append(h)
            out_header.extend(new_cols)
        else:
            out_header.append(h)

    # Backup if overwriting same file
    if os.path.abspath(input_csv) == os.path.abspath(output_csv):
        backup = input_csv + ".bak"
        shutil.copy2(input_csv, backup)
        print(f"[Backup] Original file copied to {backup}")

    # Encode
    unknown_values = set()
    duplicate_rows_detected = 0
    out_rows = []

    for row in rows:
        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))

        cell = row[col_idx] if col_idx < len(row) else ""
        tokens = split_cell_tokens(cell)
        if tokens and len(tokens) != len(set(tokens)):
            duplicate_rows_detected += 1

        present = set(tokens)  # deduplicate duplicates like '6;6;6'
        for p in present:
            if p not in vals_set:
                unknown_values.add(p)

        # <-- changed to T/F instead of 0/1
        indicators = ["T" if v in present else "F" for v in vals]

        new_row = []
        for i, val in enumerate(row):
            if i == col_idx:
                if not drop_orig:
                    new_row.append(val)
                new_row.extend(indicators)
            else:
                new_row.append(val)
        out_rows.append(new_row)

    save_csv(output_csv, out_header, out_rows)

    print(f"\n✅ Saved one-hot encoded file to {output_csv}")
    print(f"Created {len(new_cols)} indicator columns.")
    if duplicate_rows_detected:
        print(
            f"ℹ️ Rows with duplicate tokens (e.g., '6;6;6'): {duplicate_rows_detected} (deduplicated via set)"
        )
    if unknown_values:
        preview = ", ".join(sorted(list(unknown_values))[:10])
        extra = (
            "" if len(unknown_values) <= 10 else f" (+{len(unknown_values)-10} more)"
        )
        print(f"⚠️ Encountered values not in your provided list: {preview}{extra}")
        print("   These were encoded as F in all indicator columns.")


if __name__ == "__main__":
    main()
