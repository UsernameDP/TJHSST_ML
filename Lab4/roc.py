import matplotlib.pyplot as plt


def get_predicted_values(data, threshold):
    return [value >= threshold for value in data]


def calc_TPR(actual_values, predicted_values):
    tp = 0
    p = 0

    for i in range(len(actual_values)):
        if actual_values[i]:
            p += 1
            if predicted_values[i]:
                tp += 1

    return tp / p


def calc_FPR(actual_values, predicted_values):
    fp = 0
    n = 0

    for i in range(len(actual_values)):
        if not actual_values[i]:
            n += 1
            if predicted_values[i]:
                fp += 1

    return fp / n


def plotROC(fpr_values, tpr_values):
    plt.figure(figsize=(6, 6))
    plt.plot([0, 1], [0, 1], "k--", label="y = x (random guess)")
    plt.plot(fpr_values, tpr_values, marker="o", label="ROC curve")
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("True Positive Rate (TPR)")
    plt.title("ROC Curve")
    plt.legend()
    plt.grid(True)
    plt.show()
