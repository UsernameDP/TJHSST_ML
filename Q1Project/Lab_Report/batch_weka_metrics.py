import os
import sys
from extract_basic_weka_metrics import extract_metrics


def log_all_metrics(folder):
    if not os.path.exists(folder):
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)

    print(f"\n📂 Scanning folder: {os.path.abspath(folder)}\n")
    print(
        f"{'File':40} | {'Accuracy':10} | {'TP Rate':8} | {'FP Rate':8} | {'ROC Area':8}"
    )
    print("-" * 85)

    files_found = False
    for filename in sorted(os.listdir(folder)):
        if filename.lower().endswith(".txt"):
            files_found = True
            file_path = os.path.join(folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            metrics = extract_metrics(text)

            accuracy = (
                f"{metrics.get('Accuracy', 0):.4f}" if "Accuracy" in metrics else "N/A"
            )
            tpr = f"{metrics.get('TP Rate', 0):.3f}" if "TP Rate" in metrics else "N/A"
            fpr = f"{metrics.get('FP Rate', 0):.3f}" if "FP Rate" in metrics else "N/A"
            roc = (
                f"{metrics.get('ROC Area', 0):.3f}" if "ROC Area" in metrics else "N/A"
            )

            print(f"{filename:40} | {accuracy:10} | {tpr:8} | {fpr:8} | {roc:8}")

    if not files_found:
        print("⚠️  No .txt files found in the specified folder.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_weka_metrics.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    log_all_metrics(folder)
