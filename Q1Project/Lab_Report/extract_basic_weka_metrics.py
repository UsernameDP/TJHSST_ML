import re
import sys
import os


def extract_metrics(text):
    metrics = {}

    # --- Accuracy ---
    acc_match = re.search(r"Correctly Classified Instances\s+\d+\s+([\d.]+)", text)
    if acc_match:
        metrics["Accuracy"] = float(acc_match.group(1))

    # --- Weighted Avg. line ---
    weighted_line = None
    in_section = False
    for line in text.splitlines():
        if "Detailed Accuracy By Class" in line:
            in_section = True
        elif in_section and "Weighted Avg" in line:
            weighted_line = line.strip()
            break

    if weighted_line:
        # remove "?" and isolate numbers, skip bare "." tokens
        weighted_line = weighted_line.replace("?", " ").strip()
        nums = [x for x in re.findall(r"[\d.]+", weighted_line) if x not in {".", ""}]

        # usually: TP FP Precision Recall F-Measure MCC ROC PRC
        if len(nums) >= 7:
            try:
                metrics["TP Rate"] = float(nums[0])
                metrics["FP Rate"] = float(nums[1])
                metrics["ROC Area"] = float(nums[6])
            except ValueError:
                pass  # ignore any malformed values
        else:
            # fallback: try explicit ROC match
            roc_match = re.search(r"Weighted Avg\.[^\d]*([\d.]+)\s*$", weighted_line)
            if roc_match:
                try:
                    metrics["ROC Area"] = float(roc_match.group(1))
                except ValueError:
                    pass

    return metrics


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_basic_weka_metrics.py <weka_output.txt>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    metrics = extract_metrics(text)

    print(f"\n📄 File: {os.path.basename(file_path)}")
    if metrics:
        for k, v in metrics.items():
            print(f"{k:12}: {v}")
    else:
        print("No metrics found in this file.")


if __name__ == "__main__":
    main()
