#!/usr/bin/env python3
import csv
import sys
import unicodedata

MISSING_THRESHOLD = 0.70
MISSING_TOKENS = {"", "?", "na", "nan", "n/a", "null", "none"}


def normalize_cell(s: str) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", str(s))
    return s.replace("\r", " ").replace("\n", " ").strip()


def is_missing(value: str) -> bool:
    return normalize_cell(value).lower() in MISSING_TOKENS


def truncate(val: str, maxlen=25) -> str:
    v = normalize_cell(val)
    return (v[:maxlen] + "…") if len(v) > maxlen else v


if len(sys.argv) < 2:
    print("Usage: python find_missing_rows.py <input.csv>")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file, encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    expected = len(header)

    line_no = 1  # header is line 1
    bad_rows = []

    for row in reader:
        line_no += 1
        # normalize row length
        if len(row) < expected:
            row = row + [""] * (expected - len(row))
        elif len(row) > expected:
            row = row[:expected]

        missing = sum(1 for v in row if is_missing(v))
        ratio = missing / expected
        if ratio >= MISSING_THRESHOLD:
            bad_rows.append((line_no, ratio, row))

# Report
if not bad_rows:
    print(f"✅ No rows with >= {int(MISSING_THRESHOLD*100)}% missing in {input_file}")
else:
    print(
        f"⚠️ Found {len(bad_rows)} rows with >= {int(MISSING_THRESHOLD*100)}% missing:\n"
    )
    for ln, ratio, row in bad_rows:
        preview = [truncate(v) for v in row[:6]]  # first 6 attributes as preview
        print(f"Line {ln} — {ratio:.0%} missing | Preview: {preview}")
