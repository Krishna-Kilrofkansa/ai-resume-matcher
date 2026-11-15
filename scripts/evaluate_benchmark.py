import os
import sys
import json
import time
import psutil
import numpy as np
from scipy.stats import spearmanr

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.matching.pipeline import MatchingPipeline


def run_benchmark():
    process = psutil.Process(os.getpid())
    start_rss = process.memory_info().rss / 1e6

    print("=" * 65)
    print("AI RESUME MATCHER: BENCHMARK & EVALUATION SUITE")
    print("=" * 65)
    print(f"Initial Memory Footprint: {start_rss:.1f} MB RSS")

    # Load Sample JD
    jd_path = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "data", "sample_jd.txt")
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    # Load Ground Truth
    gt_path = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "data", "ground_truth.json")
    with open(gt_path, "r", encoding="utf-8") as f:
        gt_data = json.load(f)

    test_resumes_dir = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "data", "test_resumes")
    gt_candidates = {c["filename"]: c for c in gt_data["candidates"]}

    # Initialize Pipeline
    t0 = time.time()
    pipeline = MatchingPipeline()
    model_load_time = time.time() - t0
    after_model_rss = process.memory_info().rss / 1e6
    print(f"Model Load Time: {model_load_time:.2f}s | Memory after Model: {after_model_rss:.1f} MB RSS (Delta: +{after_model_rss - start_rss:.1f} MB)")

    # Run Batch Matching
    resume_files = [os.path.join(test_resumes_dir, f) for f in os.listdir(test_resumes_dir) if f.endswith(('.pdf', '.docx'))]
    print(f"Processing batch of {len(resume_files)} resumes...")

    t_batch_start = time.time()
    rankings = pipeline.rank_resumes(resume_files, jd_text)
    total_batch_time = time.time() - t_batch_start
    peak_rss = process.memory_info().rss / 1e6

    print(f"Batch Processing Completed in {total_batch_time:.2f}s (Average: {total_batch_time/len(resume_files):.2f}s / resume)")
    print(f"Peak Memory Footprint: {peak_rss:.1f} MB RSS")
    print("-" * 65)

    # 1. Evaluate Parsing Metrics (Precision, Recall, F1)
    precisions = []
    recalls = []
    f1_scores = []
    exp_errors = []
    expected_ranks = []
    system_ranks = []

    print("\n--- INDIVIDUAL CANDIDATE MATCHING RESULTS ---")
    print(f"{'Rank':<5} {'Candidate':<18} {'Format':<6} {'Score':<7} {'Exp(Cand/Req)':<14} {'Skills Matched':<25}")
    print("-" * 75)

    for r in rankings:
        fn = r["filename"]
        gt = gt_candidates.get(fn, {})

        matched_skills = set(r["matched_skills"])
        gt_skills = set(gt.get("skills", []))

        # Precision & Recall
        cand_extracted_all = set(r["all_skills"])
        true_positives = len(cand_extracted_all.intersection(gt_skills))
        p = true_positives / max(1, len(cand_extracted_all))
        rec = true_positives / max(1, len(gt_skills))
        f1 = (2 * p * rec) / (p + rec) if (p + rec) > 0 else 0.0

        precisions.append(p)
        recalls.append(rec)
        f1_scores.append(f1)

        # Experience error
        gt_exp = gt.get("relevant_years_exp", 0.0)
        exp_errors.append(abs(r["relevant_experience"] - gt_exp))

        # Rankings for correlation
        expected_ranks.append(gt.get("expected_rank", 12))
        system_ranks.append(r["rank"])

        exp_str = f"{r['relevant_experience']}y / {gt_data['required_years']}y"
        matched_str = ", ".join(r["matched_skills"][:3]) + (f" (+{len(r['matched_skills'])-3})" if len(r["matched_skills"]) > 3 else "")
        print(f"#{r['rank']:<4} {r['candidate_name']:<18} {gt.get('format', 'pdf').upper():<6} {r['overall_score']:<7.1f}% {exp_str:<14} {matched_str:<25}")

    # Calculate Macro Averages
    macro_p = np.mean(precisions) * 100
    macro_r = np.mean(recalls) * 100
    macro_f1 = np.mean(f1_scores) * 100
    mean_exp_err = np.mean(exp_errors)

    # 2. Calculate Spearman's Rank Correlation Coefficient
    spearman_corr, p_value = spearmanr(expected_ranks, system_ranks)

    print("\n" + "=" * 65)
    print("FINAL BENCHMARK EVALUATION SUMMARY")
    print("=" * 65)
    print(f"1. Skills Extraction Precision: {macro_p:.1f}%")
    print(f"2. Skills Extraction Recall:    {macro_r:.1f}%")
    print(f"3. Skills Extraction F1-Score:  {macro_f1:.1f}%")
    print(f"4. Mean Experience Delta:       {mean_exp_err:.2f} years")
    print(f"5. Spearman Rank Correlation:   rho = {spearman_corr:.3f} (p-value: {p_value:.2e})")
    print(f"6. System Memory Footprint:     Peak {peak_rss:.1f} MB RSS (Zero Docker overhead)")
    print("=" * 65)

    # Save benchmark report to JSON
    report_path = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "data", "benchmark_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "metrics": {
                "precision": round(macro_p, 1),
                "recall": round(macro_r, 1),
                "f1_score": round(macro_f1, 1),
                "mean_experience_error": round(float(mean_exp_err), 2),
                "spearman_rank_correlation": round(float(spearman_corr), 3),
                "p_value": float(p_value),
                "peak_memory_mb": round(peak_rss, 1),
                "total_batch_time_sec": round(total_batch_time, 2),
                "avg_time_per_resume_sec": round(total_batch_time / len(resume_files), 2)
            },
            "rankings": rankings
        }, f, indent=2)
    print(f"Saved Benchmark Report to {report_path}")


if __name__ == "__main__":
    run_benchmark()
