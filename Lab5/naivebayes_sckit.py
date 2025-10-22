import csv
from sklearn.naive_bayes import CategoricalNB
from bidict import bidict


from confusionMatrix import *


def naiveBayes(train_file):

    attributes = []
    attribute_values = {}
    class_attribute = ""
    class_values = set()
    attribute_mapper = {}
    class_mapper = bidict()

    with open(train_file, "r") as f:

        reader = csv.reader(f)
        attributes = list(next(reader))
        class_attribute = attributes[-1]

        attributes = attributes[:-1]

        attribute_values = {attribute: set() for attribute in attributes}
        for row in reader:
            for i in range(len(row) - 1):
                attribute_values[attributes[i]].add(row[i])
            class_values.add(row[-1])

    for attribute in attribute_values.keys():
        values = attribute_values[attribute]
        values = list(values)
        values.sort()

        attribute_values[attribute] = values

        attribute_mapper[attribute] = bidict()
        for i in range(len(values)):
            attribute_mapper[attribute][values[i]] = i
    class_values = list(class_values)
    class_values.sort()
    class_mapper = bidict({class_values[i]: i for i in range(len(class_values))})

    train_encoded = []
    with open(train_file, "r") as f:
        r = csv.reader(f)
        next(r)
        for line in r:
            line_list = list(line)
            actual_class_value = class_mapper[line_list.pop()]
            encoded_attribute_instances = [
                attribute_mapper[attributes[i]][line_list[i]]
                for i in range(len(line_list))
            ]

            encoded_attribute_instances.append(actual_class_value)

            train_encoded.append(encoded_attribute_instances)

    X = [instance[:-1] for instance in train_encoded]
    y = [instance[-1] for instance in train_encoded]

    clf = CategoricalNB()
    clf.fit(X, y)

    return (
        clf,
        attributes,
        attribute_values,
        class_attribute,
        class_values,
        attribute_mapper,
        class_mapper,
    )


def testNaiveBayes(test_file, naivebayes_output):
    (
        clf,
        attributes,
        attribute_values,
        class_attribute,
        class_values,
        attribute_mapper,
        class_mapper,
    ) = naivebayes_output

    prediction_values = []
    actual_values = []

    with open(test_file, "r") as f:
        r = csv.reader(f)
        next(r)

        for line in r:
            inp = [
                attribute_mapper[attributes[i]][line[i]] for i in range(len(line) - 1)
            ]

            prediction_values.append(clf.predict([inp])[0])
            actual_values.append(line[-1])
    prediction_values = list(map(lambda x: class_mapper.inv[x], prediction_values))

    for i in range(min(10, len(actual_values))):
        print(f"{i} : pred={prediction_values[i]}, actual={actual_values[i]}")

    return log_confusion_matrix(actual_values, prediction_values)
