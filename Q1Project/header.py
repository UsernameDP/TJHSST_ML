#!/usr/bin/env python3
import csv
import sys

if len(sys.argv) < 2:
    print("Usage: python print_headers.py <file.csv>")
    sys.exit(1)

path = sys.argv[1]

with open(path, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)  # first row is the header
    print(headers)  # raw as a Python list
    print(",".join(headers))  # raw as a single CSV-style line
