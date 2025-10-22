import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
import random

from confusionMatrix import *


def calcError(df, class_attribute, attribute, class_attribute_value, attribute_value):
    instances_with_attrib_value = 0
    instances_with_wrong_class_value = 0
    for indx, row in df.iterrows():
        if row[attribute] == attribute_value:
            instances_with_attrib_value += 1
            if row[class_attribute] != class_attribute_value:
                instances_with_wrong_class_value += 1
    return (
        1
        if instances_with_attrib_value == 0
        else instances_with_wrong_class_value / instances_with_attrib_value
    )


def calcRuleSetError(df, class_attribute, attribute, ruleSet):
    instances = df.shape[0]
    instances_wrong = 0
    for indx, row in df.iterrows():
        if ruleSet[row[attribute]] != row[class_attribute]:
            instances_wrong += 1
    return instances_wrong / instances


def main():
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

    input_file_wo_ext = Path(input_file).stem
    train_df_input_file = f"{input_file_wo_ext}_train.csv"
    test_df_input_file = f"{input_file_wo_ext}_test.csv"
    train_df = pd.read_csv(train_df_input_file)
    test_df = pd.read_csv(test_df_input_file)

    ### We first train the model
    ### At the end of training, we should get attribute, {attrVal1: classVal, attrVal2: classVal, ...}

    attributes_to_check = list(df.columns)
    attributes_to_check.remove(class_attribute)

    attribute_performences = {}
    attribute_rule_sets = {}

    class_attribute_values = df[class_attribute].unique()

    for attribute in attributes_to_check:
        attribute_values = df[attribute].unique()

        attribute_rule_set = {value: None for value in attribute_values}

        for attribute_value in attribute_values:
            class_value_performences = {}

            for class_attribute_value in class_attribute_values:
                error_rate = calcError(
                    train_df,
                    class_attribute,
                    attribute,
                    class_attribute_value,
                    attribute_value,
                )
                class_value_performences[class_attribute_value] = error_rate

            min_val = min(class_value_performences.values())
            tied = [k for k, v in class_value_performences.items() if v == min_val]
            winner = random.choice(tied)

            attribute_rule_set[attribute_value] = winner

        if len(attribute_values) != len(attribute_rule_set):
            raise Exception("Something went wrong while making rule set for attribute")
        attribute_performences[attribute] = calcRuleSetError(
            train_df, class_attribute, attribute, attribute_rule_set
        )
        attribute_rule_sets[attribute] = attribute_rule_set

        print(f"Attribute ({attribute}) finished")
    print(attribute_performences)

    min_val = min(attribute_performences.values())
    tied = [k for k, v in attribute_performences.items() if v == min_val]
    winner_attribute = random.choice(tied)
    winner_ruleSet = attribute_rule_sets[winner_attribute]

    print("##TRAINING RESULTS##")
    print(f"Winning Attribute: {winner_attribute}")
    print(f"Error: {attribute_performences[winner_attribute]}")
    print(f"Winning RuleSet: ")
    for key in winner_ruleSet.keys():
        print(f"{key} : {winner_ruleSet[key]}")

    print("##TESTING RESULTS##")
    print(
        f"Error: {calcRuleSetError(test_df, class_attribute, winner_attribute, winner_ruleSet )}"
    )
    prediction_values = []
    actual_values = []

    for indx, row in test_df.iterrows():
        prediction_values.append(winner_ruleSet[row[winner_attribute]])
        actual_values.append(row[class_attribute])

    data = log_confusion_matrix(actual_values, prediction_values)
    logMetrics(data)


if __name__ == "__main__":
    main()
