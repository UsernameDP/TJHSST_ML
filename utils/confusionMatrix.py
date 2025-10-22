from sklearn.metrics import confusion_matrix


def log_confusion_matrix(actual_values, predicted_values):
    cm = confusion_matrix(actual_values, predicted_values)
    labels = sorted(list(set(actual_values + predicted_values)))

    print("Confusion Matrix:")
    print("Labels:", labels)
    print()

    header = "Pred→\t" + "\t".join(labels)
    print(header)
    for i, row_label in enumerate(labels):
        row_values = "\t".join(str(v) for v in cm[i])
        print(f"Act={row_label}\t{row_values}")

    return cm.tolist()


def logMetrics(confusionMatrix):
    """Predicted
    actual   TP FN
             FP TN
    """

    attributes = len(confusionMatrix)
    precisions = []
    recall = []

    for i in range(attributes):
        numerator = confusionMatrix[i][i]
        # sum over the row fixed column
        denominator = 0
        for j in range(attributes):
            denominator += confusionMatrix[j][i]
        precisions.append(numerator / denominator)

        denominator = 0
        for j in range(attributes):
            denominator += confusionMatrix[i][j]
        recall.append(numerator / denominator)

    trace = sum([confusionMatrix[i][i] for i in range(attributes)])
    matrixSum = sum([sum(confusionMatrix[i]) for i in range(attributes)])

    accuracy = trace / matrixSum

    print("Metrics:")
    print("Precision:")
    for i in range(len(precisions)):
        print(f"\tCol {i}: {precisions[i]}")
    print("Recall:")
    for i in range(len(recall)):
        print(f"\tRow {i}: {recall[i]}")

    print(f"Accuracy: {accuracy}")
