from sklearn.metrics import precision_score, recall_score, accuracy_score


def logMetrics(confusionMatrix):
    n_classes = len(confusionMatrix)
    y_true, y_pred = [], []

    for actual in range(n_classes):
        for predicted in range(n_classes):
            count = confusionMatrix[actual][predicted]
            y_true.extend([actual] * count)
            y_pred.extend([predicted] * count)

    # Calculate metrics using sklearn
    precisions = precision_score(y_true, y_pred, average=None, zero_division=0)
    recalls = recall_score(y_true, y_pred, average=None, zero_division=0)
    accuracy = accuracy_score(y_true, y_pred)

    print("Metrics:")
    print("Precision:")
    for i, p in enumerate(precisions):
        print(f"\tCol {i}: {p}")
    print("Recall:")
    for i, r in enumerate(recalls):
        print(f"\tRow {i}: {r}")
    print(f"Accuracy: {accuracy}")
