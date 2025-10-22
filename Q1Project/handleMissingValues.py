#!/usr/bin/env python3
import sys
import csv
import math
import shutil
from collections import Counter
from pathlib import Path
from datetime import datetime

# Missing tokens (after trim, case-insensitive)
MISSING_TOKENS = {"", "na", "n/a", "null", "none", "nan", "?"}


def is_missing(val: str) -> bool:
    if val is None:
        return True
    s = str(val).strip()
    return s.lower() in MISSING_TOKENS


def try_float(s: str):
    try:
        return float(str(s).strip())
    except Exception:
        return None


def compute_mean(values):
    total, cnt = 0.0, 0
    for v in values:
        if v is not None and not math.isnan(v):
            total += v
            cnt += 1
    return (total / cnt) if cnt > 0 else None


def compute_median(values):
    xs = sorted(v for v in values if v is not None and not math.isnan(v))
    n = len(xs)
    if n == 0:
        return None
    mid = n // 2
    if n % 2 == 1:
        return xs[mid]
    else:
        return (xs[mid - 1] + xs[mid]) / 2.0


def compute_mode_preserve_first(rows, attr):
    counts = Counter()
    first_seen_index = {}
    idx = 0
    for r in rows:
        raw = r.get(attr, "")
        if is_missing(raw):
            idx += 1
            continue
        val = str(raw).strip()
        counts[val] += 1
        if val not in first_seen_index:
            first_seen_index[val] = idx
        idx += 1
    if not counts:
        return None
    max_count = max(counts.values())
    candidates = [v for v, c in counts.items() if c == max_count]
    candidates.sort(key=lambda v: first_seen_index[v])
    return candidates[0]


def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def make_backup_if_same(input_path: Path, output_path: Path | None):
    """If output equals input, make an immediate timestamped backup."""
    if output_path is not None and output_path.resolve() == input_path.resolve():
        backup_name = f"{input_path.stem}_backup_{ts()}{input_path.suffix}"
        backup_path = input_path.with_name(backup_name)
        shutil.copy2(input_path, backup_path)
        print(f"Backup created: {backup_path}")


def sanitize_for_filename(s: str) -> str:
    bad = '/\\:*?"<>|'
    out = "".join("_" if c in bad else c for c in str(s).strip())
    return "_".join(out.split())


def save_csv(path: Path, fieldnames, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {path}")


def main():
    # Args: input.csv [output.csv]
    if len(sys.argv) < 2:
        print("Usage: handleMissingValues.py <input.csv> [output.csv]")
        sys.exit(1)

    input_path = Path(sys.argv[1]).resolve()
    if not input_path.exists():
        print(f"Input not found: {input_path}")
        sys.exit(1)

    output_path = None
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2]).resolve()

    # If output is same as input, create immediate backup
    make_backup_if_same(input_path, output_path)

    # Load CSV
    with open(input_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if not fieldnames:
        print("No headers found.")
        sys.exit(1)

    print(f"Loaded {len(rows)} rows.")
    print("Columns (1-based indices):")
    for i, col in enumerate(fieldnames, start=1):
        print(f"  [{i}] {col}")

    while True:
        choice = input("Pick attribute index or name (blank to finish): ").strip()
        if choice == "":
            break

        # Resolve attr
        if choice.isdigit():
            idx1 = int(choice)
            idx0 = idx1 - 1
            if idx0 < 0 or idx0 >= len(fieldnames):
                print("Invalid index.")
                continue
            attr = fieldnames[idx0]
        else:
            if choice not in fieldnames:
                print(f"Column '{choice}' not found.")
                continue
            attr = choice

        kind = (
            input(f"Type for '{attr}'? Enter 'nominal', 'numeric', or 'discrete': ")
            .strip()
            .lower()
        )
        while kind not in {"nominal", "numeric", "discrete"}:
            kind = (
                input("Please enter 'nominal', 'numeric', or 'discrete': ")
                .strip()
                .lower()
            )

        if kind == "numeric":
            # Gather numeric values
            numeric_vals = []
            for r in rows:
                v = r.get(attr, "")
                if is_missing(v):
                    continue
                num = try_float(v)
                if num is not None:
                    numeric_vals.append(num)

            mean_val = compute_mean(numeric_vals)
            if mean_val is None:
                print(
                    f"Cannot compute mean for '{attr}' (no valid numeric values). Skipping."
                )
                continue

            replaced = 0
            for r in rows:
                v = r.get(attr, "")
                if is_missing(v) or try_float(v) is None:
                    r[attr] = str(mean_val)
                    replaced += 1
            print(f"[{attr}] numeric: mean={mean_val:.6g}, replaced {replaced} cells.")

        elif kind == "nominal":
            mode_val = compute_mode_preserve_first(rows, attr)
            if mode_val is None:
                print(
                    f"Cannot compute mode for '{attr}' (no non-missing values). Skipping."
                )
                continue
            replaced = 0
            for r in rows:
                if is_missing(r.get(attr, "")):
                    r[attr] = mode_val
                    replaced += 1
            print(f"[{attr}] nominal: mode='{mode_val}', replaced {replaced} cells.")

        else:  # discrete
            # Strategy prompt with default = median-rounded
            strategy = (
                input(
                    "Discrete strategy: 'mode' or 'median-rounded' [median-rounded]: "
                )
                .strip()
                .lower()
            )
            if strategy not in {"mode", "median-rounded", ""}:
                print("Unknown strategy. Using 'median-rounded'.")
                strategy = ""
            if strategy == "" or strategy == "median-rounded":
                # compute median then round to nearest int
                vals = []
                for r in rows:
                    v = r.get(attr, "")
                    if is_missing(v):
                        continue
                    num = try_float(v)
                    if num is not None:
                        vals.append(num)
                med = compute_median(vals)
                if med is None:
                    print(f"Cannot compute median for '{attr}'. Skipping.")
                    continue
                fill_val = int(round(med))
                replaced = 0
                for r in rows:
                    v = r.get(attr, "")
                    if is_missing(v) or try_float(v) is None:
                        r[attr] = str(fill_val)
                        replaced += 1
                print(
                    f"[{attr}] discrete (median-rounded): median={med:.6g} -> fill={fill_val}, replaced {replaced} cells."
                )
            else:
                # mode over string-trimmed values, but ensure fill is integer-like if possible
                mode_val = compute_mode_preserve_first(rows, attr)
                if mode_val is None:
                    print(f"Cannot compute mode for '{attr}'. Skipping.")
                    continue
                # try to cast to int if it looks numeric
                num = try_float(mode_val)
                if num is not None:
                    mode_val = str(int(round(num)))
                replaced = 0
                for r in rows:
                    if (
                        is_missing(r.get(attr, ""))
                        or try_float(r.get(attr, "")) is None
                    ):
                        r[attr] = mode_val
                        replaced += 1
                print(
                    f"[{attr}] discrete (mode): fill='{mode_val}', replaced {replaced} cells."
                )

        # Decide output path
        if output_path is None:
            base = input_path.with_suffix("")
            attr_safe = sanitize_for_filename(attr)
            out = Path(f"{base}_missing_{attr_safe}.csv").resolve()
        else:
            out = output_path  # may equal input; backup already handled

        save_csv(out, fieldnames, rows)

        again = input("Impute another attribute? (y/N): ").strip().lower()
        if again != "y":
            break


if __name__ == "__main__":
    main()
