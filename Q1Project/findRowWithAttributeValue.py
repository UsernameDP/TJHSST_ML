import arff
import sys

if len(sys.argv) < 2:
    print("Usage: python print_arff_rows.py <file.arff>")
    sys.exit(1)

path = sys.argv[1]

with open(path, "r", encoding="utf-8") as f:
    dataset = arff.load(f)

# # Print header info
# print("Relation:", dataset["relation"])
# print("Attributes:", [name for name, _ in dataset["attributes"]])
# print()

# # Print rows
# for i, row in enumerate(dataset["data"], start=1):
#     print(f"Row {i}: {row}")
