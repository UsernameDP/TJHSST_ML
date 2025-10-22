import pandas as pd


def compare_unique_counts(train_csv, test_csv):
    train = pd.read_csv(train_csv)
    test = pd.read_csv(test_csv)

    print(f"{'Attribute':<30} {'Train Unique':<15} {'Test Unique':<15}")
    print("-" * 60)

    for col in train.columns:
        if col not in test.columns:
            print(f"{col:<30} {'MISSING':<15} {'N/A':<15}")
            continue

        train_unique = train[col].nunique(dropna=True)
        test_unique = test[col].nunique(dropna=True)

        diff_flag = "⚠️" if train_unique != test_unique else ""
        print(f"{col:<30} {train_unique:<15} {test_unique:<15} {diff_flag}")

    print("-" * 60)
    print("⚠️ = different number of distinct values")


# Example usage:
compare_unique_counts("final_train.csv", "final_test.csv")
