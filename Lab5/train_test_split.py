import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

args = sys.argv[1:]

input_file = args[0]

df = pd.read_csv(input_file)

##PRINT ATTRIBUTES
print("ATTRIBUTES:")
for i, col in enumerate(df.columns):
    print(f"{i}: {col}")
class_attribute = input("Choose Class Attribute INDX or Name: ")

if class_attribute.isdigit():
    class_attribute = df.columns[int(class_attribute)]

X = df.drop(columns=[class_attribute])
y = df[class_attribute]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=20
)

train_df = X_train.copy()
train_df[class_attribute] = y_train.copy()

test_df = X_test.copy()
test_df[class_attribute] = y_test.copy()

input_file_wo_ext = Path(input_file).stem
train_df_output = f"{input_file_wo_ext}_train.csv"
test_df_output = f"{input_file_wo_ext}_test.csv"

train_df.to_csv(train_df_output, index=False)
test_df.to_csv(test_df_output, index=False)
