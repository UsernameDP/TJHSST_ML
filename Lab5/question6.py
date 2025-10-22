from roc import *

data = [610, 630, 650, 680, 720, 760, 780, 810, 845]
actual_values = [False, True, False, True, False, False, True, True, True]
tpr_fpr = set()

for threshold in range(min(data), max(data) + 1):
    predicted_values = get_predicted_values(data, threshold)
    tpr_fpr.add(
        (
            calc_FPR(actual_values, predicted_values),
            calc_TPR(actual_values, predicted_values),
        )
    )
tpr_fpr = list(tpr_fpr)
tpr_fpr.sort(key=lambda x: 2 * x[0] + x[1])
print(tpr_fpr)
fpr_values = [coord[0] for coord in tpr_fpr]
tpr_values = [coord[1] for coord in tpr_fpr]
plotROC(fpr_values, tpr_values)
