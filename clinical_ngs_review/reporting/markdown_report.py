"""
Generate an analyst-facing Markdown review report.
"""


def format_run_summary(run_summary: dict) -> str:
    """
    Format the run-level summary section.
    """
    return "\n".join(
        [
            "## Run Summary",
            "",
            f"- Overall run status: **{run_summary['run_status']}**",
            f"- Total samples reviewed: {run_summary['total_samples']}",
            f"- Passing samples: {run_summary['passing_samples']}",
            f"- Flagged samples: {run_summary['flagged_samples']}",
            f"- Failed samples: {run_summary['failed_samples']}",
            "",
        ]
    )


def format_sample_findings(classified_metrics) -> str:
    """
    Format sample-level findings for Markdown output.
    """
    lines = ["## Sample-Level Findings", ""]

    for _, row in classified_metrics.iterrows():
        lines.append(f"### {row['sample_id']} — {row['overall_status']}")
        lines.append("")

        if not row["findings"]:
            lines.append("No review-triggering QC findings.")
            lines.append("")
            continue

        for finding in row["findings"]:
            lines.append(f"- **{finding['severity']}: {finding['category']}**")
            lines.append(f"  - Evidence: {finding['evidence']}")
            lines.append(f"  - Recommended review: {finding['recommendation']}")

        lines.append("")

    return "\n".join(lines)


def generate_markdown_report(classified_metrics, run_summary: dict) -> str:
    """
    Generate the full analyst review report.
    """
    report_sections = [
        "# Clinical NGS QC Review Report",
        "",
        "This report summarizes sample-level QC findings generated from configured review rules.",
        "",
        format_run_summary(run_summary),
        format_sample_findings(classified_metrics),
        "## Limitations",
        "",
        "These thresholds are example review rules for portfolio demonstration only. "
        "They are not clinical release criteria and are not based on any proprietary SOP.",
        "",
    ]

    return "\n".join(report_sections)