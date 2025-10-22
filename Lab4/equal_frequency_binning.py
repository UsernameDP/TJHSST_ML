import pandas as pd
import os


import pandas as pd
import os


import pandas as pd
import os


def equal_frequency_binning(input_csv, output_csv=None, bins=4, class_name=None):
    if class_name == None:
        raise Exception("You must input class_name")

    df = pd.read_csv(input_csv)

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        if col == class_name:
            df[class_name] = df[class_name].astype(str) + "-str"
            continue

        unique_vals = df[col].nunique(dropna=True)
        actual_bins = min(bins, unique_vals)

        if actual_bins <= 1:
            print(f"Skipping column '{col}': only one unique value.")
            continue
        try:
            df[col] = pd.qcut(df[col], q=actual_bins, duplicates="drop")
            df[col] = df[col].astype(str)
        except ValueError as e:
            print(f"⚠️ Could not bin column '{col}': {e}")

    if output_csv is None:
        base, ext = os.path.splitext(input_csv)
        output_csv = f"{base}_binned{ext}"

    df.to_csv(output_csv, index=False)
    print(f"Binned dataset saved to: {output_csv}")


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]

    input_file = args[0]
    class_name = args[1]
    bins = int(args[2])
    equal_frequency_binning(input_file, bins=bins, class_name=class_name)
