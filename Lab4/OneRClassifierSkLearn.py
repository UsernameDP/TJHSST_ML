import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
import random
from sklearn.tree import DecisionTreeClassifier, export_text


def main():
    args = sys.argv[1:]

    input_file = args[0]

    df = pd.read_csv(input_file)

    print("ATTRIBUTES:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")
    class_attribute = input("Choose Class Attribute INDX or Name: ")

    if class_attribute.isdigit():
        class_attribute = df.columns[int(class_attribute)]

    input_file_wo_ext = Path(input_file).stem
    train_df_input_file = f"{input_file_wo_ext}_train.csv"
    test_df_input_file = f"{input_file_wo_ext}_test.csv"
    train_df = pd.read_csv(train_df_input_file)
    test_df = pd.read_csv(test_df_input_file)

    X_train, y_train = (
        train_df.drop(columns=[class_attribute]),
        train_df[class_attribute],
    )
    X_test, y_test = test_df.drop(columns=[class_attribute]), test_df[class_attribute]

    clf = DecisionTreeClassifier(max_depth=1, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    train_error = 1 - clf.score(X_train, y_train)
    test_error = 1 - clf.score(X_test, y_test)
    print(f"Train Error: {train_error}")
    print(f"Test Error: { test_error}")
    print(export_text(clf, feature_names=list(X_train.columns), max_depth=2))


if __name__ == "__main__":
    main()
