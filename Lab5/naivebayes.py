import csv

"""
LAST COLUMN IS TAKEN AS THE CLASS 
"""

from confusionMatrix import *


def getConditionProb(
    train_file, attribute, attribute_value, class_attribute, class_value
):
    with open(train_file, "r") as f:
        reader = csv.DictReader(f)

        total = 0
        counter = 0
        for row in reader:
            if row[class_attribute] == class_value:
                total += 1
                counter += 1 if row[attribute] == attribute_value else 0

        return counter / total


def getClassProb(train_file, class_value):
    with open(train_file, "r") as f:
        reader = csv.reader(f)
        next(reader)

        total = 0
        counter = 0
        for row in reader:
            total += 1
            counter += 1 if row[-1] == class_value else 0
        return counter / total


def naiveBayes(train_file):

    with open(train_file, "r") as f:
        attributes = []
        attribute_values = set()
        conditional_probability_dict = {}
        # ^ (attribute, attribute=value, class=class_value) -> probability
        class_attribute = ""
        class_values = set()
        class_probability_dict = {}

        reader = csv.reader(f)
        attributes = list(next(reader))
        class_attribute = attributes[-1]

        attributes = attributes[:-1]

        attribute_values = {attribute: set() for attribute in attributes}
        for row in reader:
            for i in range(len(row) - 1):
                attribute_values[attributes[i]].add(row[i])
            class_values.add(row[-1])

        for class_value in class_values:
            class_probability_dict[class_value] = getClassProb(train_file, class_value)

        for attribute in attributes:
            for attribute_value in attribute_values[attribute]:
                for class_value in class_values:
                    conditional_probability_dict[
                        (attribute, attribute_value, class_value)
                    ] = getConditionProb(
                        train_file,
                        attribute,
                        attribute_value,
                        class_attribute,
                        class_value,
                    )

    return (
        attributes,
        attribute_values,
        conditional_probability_dict,
        class_attribute,
        class_values,
        class_probability_dict,
    )


def testNaiveBayes(test_file, naivebayes_output):
    (
        attributes,
        attribute_values,
        conditional_probability_dict,
        class_attribute,
        class_values,
        class_probability_dict,
    ) = naivebayes_output

    prediction_values = []
    actual_values = []

    with open(test_file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            actual_values.append(row[class_attribute])
            class_probabilities = []

            for class_value in class_values:
                conditional_prob = 1
                class_prob = class_probability_dict[class_value]

                for attribute in row.keys():
                    if attribute == class_attribute:
                        continue
                    conditional_prob *= conditional_probability_dict[
                        (attribute, row[attribute], class_value)
                    ]

                class_probabilities.append((class_value, conditional_prob * class_prob))

            class_probabilities.sort(key=lambda x: x[1])

            prediction_values.append(class_probabilities[-1][0])

    for i in range(min(10, len(actual_values))):
        print(f"{i} : pred={prediction_values[i]}, actual={actual_values[i]}")

    return log_confusion_matrix(
        actual_values, prediction_values
    )  # THIS IS THE ONLY PART USING SKLEARN NAIVEBAYES ITSELF IS BUILT FROM SCRATCH
