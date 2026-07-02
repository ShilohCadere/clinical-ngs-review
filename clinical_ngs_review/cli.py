"""
Command-line entry point for clinical-ngs-review.

This wires together the current workflow:
load inputs -> merge metadata -> apply rules -> classify findings
-> summarize run -> write reports.
"""

from pathlib import Path

from clinical_ngs_review.analysis.apply_rules import apply_rules, load_review_rules
from clinical_ngs_review.analysis.classify_findings import classify_findings
from clinical_ngs_review.analysis.summarize_run import summarize_run
from clinical_ngs_review.ingest.load_metrics import (
    load_qc_metrics,
    load_sample_metadata,
)
from clinical_ngs_review.reporting.markdown_report import generate_markdown_report
from clinical_ngs_review.reporting.report_tables import (
    build_flagged_samples_table,
    build_review_summary_table,
)


def merge_qc_with_metadata(qc_metrics, sample_metadata):
    """
    Add sample metadata to the QC metrics table.

    This keeps measured QC values separate from sample context until
    the point where analysis needs both.
    """
    merged_data = qc_metrics.merge(
        sample_metadata,
        on="sample_id",
        how="left",
    )

    return merged_data


def write_outputs(classified_metrics, run_summary: dict) -> None:
    """
    Write CSV and Markdown report outputs to the reports directory.
    """
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    review_summary = build_review_summary_table(classified_metrics)
    flagged_samples = build_flagged_samples_table(classified_metrics)
    markdown_report = generate_markdown_report(classified_metrics, run_summary)

    review_summary.to_csv(reports_dir / "review_summary.csv", index=False)
    flagged_samples.to_csv(reports_dir / "flagged_samples.csv", index=False)

    with open(reports_dir / "analyst_review_report.md", "w", encoding="utf-8") as file:
        file.write(markdown_report)


def main() -> None:
    """
    Run the review workflow using example files.
    """
    qc_metrics = load_qc_metrics("data/example_qc_metrics.csv")
    sample_metadata = load_sample_metadata("data/example_sample_metadata.csv")
    review_rules = load_review_rules("config/review_rules.yml")

    merged_data = merge_qc_with_metadata(qc_metrics, sample_metadata)
    reviewed_metrics = apply_rules(merged_data, review_rules)
    classified_metrics = classify_findings(reviewed_metrics)
    run_summary = summarize_run(classified_metrics)

    write_outputs(classified_metrics, run_summary)

    print("Review complete. Outputs written to reports/")


if __name__ == "__main__":
    main()