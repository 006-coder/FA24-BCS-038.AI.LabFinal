import json
import csv
import os
import time
import numpy as np
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def run_evaluation():
    # 1. Open the file with explicit UTF-8 to prevent the Windows decode crash
    with open("test_dataset.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # Setup evaluation folders required by the rubric [cite: 23, 27]
    os.makedirs("data", exist_ok=True)
    os.makedirs("results/json_logs", exist_ok=True)

    results = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
    total_latency = 0
    evaluation_records = []  # This tracks rows to build your CSV file smoothly

    print(f"Starting evaluation on {len(test_data)} sample test cases...")

    for idx, entry in enumerate(test_data):
        # Generate a fallback unique key dynamically on the fly
        input_id = entry.get("id", f"case_{idx + 1:03d}")
        prompt_text = entry.get("text", "")
        expected = entry.get("expected_status", "ALLOW")

        # Automatically determine metadata properties for the rubric's schema mapping
        has_pii = "TRUE" if expected == "MASK" else "FALSE"
        attack_type = "PROMPT_INJECTION" if expected == "BLOCK" else "NONE"

        start_time = time.time()

        # Send payload matching your main.py structure
        response = client.post("/check-security", json={
            "input_id": input_id,
            "text": prompt_text
        })

        latency_ms = int((time.time() - start_time) * 1000)
        total_latency += (latency_ms / 1000.0)

        # Parse the standard institutional JSON response body [cite: 44-65]
        response_json = response.json()
        actual_decision = response_json.get("decision", "ALLOW")
        final_risk = response_json.get("final_risk", 0.0)
        detected_lang = response_json.get("language", "en")

        # SAVE INDIVIDUAL AUDITABLE JSON RESPONSES [cite: 27, 43]
        json_log_path = f"results/json_logs/{input_id}.json"
        with open(json_log_path, "w", encoding="utf-8") as json_f:
            json.dump(response_json, json_f, indent=4, ensure_ascii=False)

        # Confusion Matrix Categorization Logic mapping to the JSON schema
        if actual_decision == expected:
            if actual_decision in ["BLOCK", "MASK"]:
                results["TP"] += 1
            else:
                results["TN"] += 1
        else:
            if actual_decision == "ALLOW":
                results["FN"] += 1
            else:
                results["FP"] += 1

        # Append data records matching your exact CSV column requirements
        evaluation_records.append({
            "id": input_id,
            "prompt": prompt_text,
            "language": detected_lang,
            "attack_type": attack_type,
            "has_pii": has_pii,
            "expected_policy": expected,
            "predicted_policy": actual_decision,
            "latency_ms": latency_ms
        })

    # =====================================================================
    # PERFORMANCE METRICS AND LATENCY STATS (Calculated outside the loop!)
    # =====================================================================
    total_cases = len(test_data)
    accuracy = (results["TP"] + results["TN"]) / total_cases if total_cases > 0 else 0
    avg_latency_sec = total_latency / total_cases if total_cases > 0 else 0

    precision = results["TP"] / (results["TP"] + results["FP"]) if (results["TP"] + results["FP"]) > 0 else 0
    recall = results["TP"] / (results["TP"] + results["FN"]) if (results["TP"] + results["FN"]) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # Extract latency list from evaluation records to calculate summary percentiles [cite: 161]
    latency_list = [row["latency_ms"] for row in evaluation_records]
    mean_lat = np.mean(latency_list)
    median_lat = np.median(latency_list)
    p95_lat = np.percentile(latency_list, 95)

    print(f"\n==========================================")
    print(f"--- MANDATORY LAB FINAL EVALUATION SCORES ---")
    print(f"==========================================")
    print(f"Total Test Cases Processed: {total_cases}")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Precision: {precision:.2f}")
    print(f"Recall (Sensitivity): {recall:.2f}")
    print(f"F1-Score Metrics: {f1_score:.2f}")
    print(f"Matrix Counts: {results}")
    print(f"------------------------------------------")
    print(f"Mean Latency: {mean_lat:.2f} ms")
    print(f"Median Latency: {median_lat:.2f} ms")
    print(f"p95 Latency: {p95_lat:.2f} ms")
    print(f"==========================================\n")

    # SAVE DATA SET SUMMARY AS METRICS_SUMMARY.JSON [cite: 166]
    metrics_summary_path = "results/metrics_summary.json"
    os.makedirs("results", exist_ok=True)
    with open(metrics_summary_path, "w", encoding="utf-8") as summary_f:
        json.dump({
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "f1_score": round(f1_score, 2),
            "average_latency_sec": round(avg_latency_sec, 4),
            "latency_stats_ms": {
                "mean": round(mean_lat, 2),
                "median": round(median_lat, 2),
                "p95": round(p95_lat, 2)
            },
            "confusion_matrix": results
        }, summary_f, indent=4)

    # WRITE THE REQUIRED data/final_eval.csv FILE ARTIFACT [cite: 23, 117-119]
    csv_path = "data/final_eval.csv"
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Institutional header row columns [cite: 118-119]
        writer.writerow(["id", "prompt", "language", "attack_type", "has_pii", "expected_policy", "predicted_policy", "latency_ms"])

        for row in evaluation_records:
            writer.writerow([
                row["id"],
                row["prompt"],
                row["language"],
                row["attack_type"],
                row["has_pii"],
                row["expected_policy"],
                row["predicted_policy"],
                row["latency_ms"]
            ])

    print(f"Successfully generated mandatory Lab Final asset at: {csv_path}")
    print(f"Saved independent JSON response logs to: results/json_logs/")


if __name__ == "__main__":
    run_evaluation()