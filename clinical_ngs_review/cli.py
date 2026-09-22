"""
Command-line entry point for clinical-ngs-review.

This wires together the workflow:
load inputs -> merge metadata -> apply rules -> classify findings
-> summarize run -> write reports.
"""

import argparse
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


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser for the review workflow."""
    parser = argparse.ArgumentParser(
        description="Apply configurable QC review rules and generate analyst-facing reports."
    )
    parser.add_argument(
        "--metrics",
        default="data/example_qc_metrics.csv",
        help="Path to the sequencing QC metrics CSV.",
    )
    parser.add_argument(
        "--metadata",
        default="data/example_sample_metadata.csv",
        help="Path to the sample metadata CSV.",
    )
    parser.add_argument(
        "--rules",
        default="config/review_rules.yml",
        help="Path to the YAML review-rules file.",
    )
    parser.add_argument(
        "--output-dir",
        default="reports",
        help="Directory where CSV and Markdown reports will be written.",
    )
    return parser


def merge_qc_with_metadata(qc_metrics, sample_metadata):
    """
    Add sample metadata to the QC metrics table.

    This keeps measured QC values separate from sample context until
    the point where analysis needs both.
    """
    return qc_metrics.merge(
        sample_metadata,
        on="sample_id",
        how="left",
    )


def write_outputs(classified_metrics, run_summary: dict, output_dir: str | Path) -> None:
    """Write CSV and Markdown report outputs to the selected directory."""
    reports_dir = Path(output_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    review_summary = build_review_summary_table(classified_metrics)
    flagged_samples = build_flagged_samples_table(classified_metrics)
    markdown_report = generate_markdown_report(classified_metrics, run_summary)

    review_summary.to_csv(reports_dir / "review_summary.csv", index=False)
    flagged_samples.to_csv(reports_dir / "flagged_samples.csv", index=False)

    with open(reports_dir / "analyst_review_report.md", "w", encoding="utf-8") as file:
        file.write(markdown_report)


def run_workflow(
    metrics_path: str | Path,
    metadata_path: str | Path,
    rules_path: str | Path,
    output_dir: str | Path,
) -> None:
    """Run the complete analytical review workflow for the supplied inputs."""
    qc_metrics = load_qc_metrics(metrics_path)
    sample_metadata = load_sample_metadata(metadata_path)
    review_rules = load_review_rules(rules_path)

    merged_data = merge_qc_with_metadata(qc_metrics, sample_metadata)
    reviewed_metrics = apply_rules(merged_data, review_rules)
    classified_metrics = classify_findings(reviewed_metrics)
    run_summary = summarize_run(classified_metrics)

    write_outputs(classified_metrics, run_summary, output_dir)


def main() -> None:
    """Parse command-line arguments and run the review workflow."""
    args = build_parser().parse_args()
    run_workflow(args.metrics, args.metadata, args.rules, args.output_dir)
    print(f"Review complete. Outputs written to {args.output_dir}/")


if __name__ == "__main__":
    main()
