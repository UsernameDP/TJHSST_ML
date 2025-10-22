#!/usr/bin/env python3
import sys
import pandas as pd
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("Usage: python select_columns.py <input.csv> <output.csv>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Error: file not found - {input_path}")
        sys.exit(1)

    df = pd.read_csv(input_path)
    print(f"Loaded {input_path} ({len(df)} rows, {len(df.columns)} columns)\n")

    print("ATTRIBUTES (1-based):")
    for i, col in enumerate(df.columns, start=1):
        print(f"{i}: {col}")
    print()

    selected = []
    while True:
        choice = input(
            "Enter column index(es) or name(s) (comma-separated, q to quit): "
        ).strip()
        if choice.lower() == "q":
            break

        entries = [c.strip() for c in choice.split(",") if c.strip()]
        for entry in entries:
            # Handle 1-based numeric indices
            if entry.isdigit():
                idx_1based = int(entry)
                if 1 <= idx_1based <= len(df.columns):
                    col = df.columns[idx_1based - 1]  # convert to 0-based
                else:
                    print(f"Invalid index (1-based): {entry}")
                    continue
            else:
                if entry not in df.columns:
                    print(f"Invalid column name: {entry}")
                    continue
                col = entry

            if col in selected:
                print(f"{col} already selected.")
            else:
                selected.append(col)
                print(f"Added: {col}")

        if selected:
            print("Currently selected:", ", ".join(selected))
        print()

    if not selected:
        print("No columns selected. Exiting.")
        sys.exit(0)

    df[selected].to_csv(output_path, index=False)
    print(f"\nSaved {len(selected)} columns to {output_path}")
    print("Selected columns:")
    for col in selected:
        print(f"- {col}")


if __name__ == "__main__":
    main()
