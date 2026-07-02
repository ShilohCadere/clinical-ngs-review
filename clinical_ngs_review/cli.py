"""
Command-line entry point for clinical-ngs-review.

This wires together the current MVP:
load inputs -> apply rules -> classify findings -> summarize run.
"""

from clinical_ngs_review.analysis.apply_rules import apply_rules, load_review_rules
from clinical_ngs_review.analysis.classify_findings import classify_findings
from clinical_ngs_review.analysis.summarize_run import summarize_run
from clinical_ngs_review.ingest.load_metrics import load_qc_metrics


def print_sample_findings(classified_metrics) -> None:
    """
    Print sample-level findings in a readable format for the command line.
    """
    print("\nSample Review Results")

    for _, row in classified_metrics.iterrows():
        print(f"\n{row['sample_id']} - {row['overall_status']}")

        if not row["findings"]:
            print("  No review-triggering QC findings")
            continue

        for finding in row["findings"]:
            print(f"  {finding['severity']}: {finding['category']}")
            print(f"    Evidence: {finding['evidence']}")
            print(f"    Recommended review: {finding['recommendation']}")


def main() -> None:
    """
    Run the MVP review workflow using example files.
    """
    qc_metrics = load_qc_metrics("data/example_qc_metrics.csv")
    review_rules = load_review_rules("config/review_rules.yml")

    reviewed_metrics = apply_rules(qc_metrics, review_rules)
    classified_metrics = classify_findings(reviewed_metrics)
    run_summary = summarize_run(classified_metrics)

    print_sample_findings(classified_metrics)

    print("\nRun Summary")
    for key, value in run_summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()