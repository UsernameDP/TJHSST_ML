#!/usr/bin/env python3
import csv
import sys
import unicodedata

USAGE = "Usage: python check_numeric_column.py <file.csv>"

if len(sys.argv) < 2:
    print(USAGE)
    sys.exit(1)

path = sys.argv[1]


def normalize_cell(s: str) -> str:
    """Trim, collapse common hidden whitespace, and normalize unicode."""
    if s is None:
        return ""
    # Normalize Unicode (e.g., full-width digits, weird spaces)
    s = unicodedata.normalize("NFKC", str(s))
    # Replace common hidden newlines and NBSP with regular spaces
    s = s.replace("\r", " ").replace("\n", " ").replace("\u00a0", " ")
    return s.strip()


def is_numeric(val: str) -> bool:
    """Return True if val can be parsed as a float (dot-decimal)."""
    v = normalize_cell(val)
    if v == "" or v == "?":  # treat empty/missing as non-numeric (report it)
        return False
    # Try straight float
    try:
        float(v)
        return True
    except ValueError:
        pass
    # Gentle fallbacks (comment out if you want strict only):
    # 1) remove thousands separators like "1,234.56"
    if v.count(",") >= 1 and v.count(".") <= 1:
        try:
            float(v.replace(",", ""))
            return True
        except ValueError:
            pass
    # 2) European-style "123,45" -> "123.45" (only if there's no dot)
    if v.count(",") == 1 and "." not in v:
        try:
            float(v.replace(",", "."))
            return True
        except ValueError:
            pass
    return False


# Load CSV
with open(path, "r", encoding="utf-8", newline="") as f:
    reader = list(csv.reader(f))

if not reader:
    print("Empty file.")
    sys.exit(1)

header = [h.strip() for h in reader[0]]
rows = reader[1:]

print(f"Loaded {len(rows)} data rows, {len(header)} columns from {path}.\n")
print("Columns:")
for i, name in enumerate(header, start=1):
    print(f"  {i:>3}: {name}")
print()

name_to_index = {name.lower(): i for i, name in enumerate(header)}

while True:
    choice = input("Type column *name* or *index* to check (or 'q' to quit): ").strip()
    if choice.lower() in {"q", "quit", "exit"}:
        break

    # Resolve column
    col_idx = None
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(header):
            col_idx = idx - 1
        else:
            print("❌ Column index out of range.\n")
            continue
    else:
        key = choice.lower()
        if key in name_to_index:
            col_idx = name_to_index[key]
        else:
            # fuzzy help: suggest closest columns by prefix
            suggestions = [c for c in header if c.lower().startswith(key)]
            print("❌ Column not found.")
            if suggestions:
                print("   Did you mean:", ", ".join(suggestions))
            print()
            continue

    col_name = header[col_idx]
    bad = []  # (line_number, raw_value, normalized_value)
    for r_i, row in enumerate(rows, start=2):  # 2 = account for header line
        val_raw = row[col_idx] if col_idx < len(row) else ""
        val_norm = normalize_cell(val_raw)
        if not is_numeric(val_raw):
            bad.append((r_i, val_raw, val_norm))

    total = len(rows)
    if not bad:
        print(f"✅ Column '{col_name}' looks numeric in all {total} rows.\n")
    else:
        print(
            f"⚠️ Column '{col_name}' has {len(bad)} non-numeric rows out of {total}. Showing first 20:"
        )
        for line_no, raw, norm in bad[:20]:
            # Show repr() so you can see hidden characters
            print(f"  line {line_no}: raw={raw!r}  normalized={norm!r}")
        print(
            "Tip: empty strings, '?', text tokens, or misaligned rows will appear here.\n"
        )
