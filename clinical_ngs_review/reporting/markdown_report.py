"""
Generate an analyst-facing Markdown review report.
"""


def format_run_summary(run_summary: dict) -> str:
    """
    Format the run-level summary section.
    """
    lines = [
        "## Run Summary",
        "",
        f"- Overall run status: **{run_summary['run_status']}**",
        f"- Total samples reviewed: {run_summary['total_samples']}",
        f"- Passing samples: {run_summary['passing_samples']}",
        f"- Flagged samples: {run_summary['flagged_samples']}",
        f"- Failed samples: {run_summary['failed_samples']}",
        "",
    ]

    return "\n".join(lines)


def format_run_level_findings(run_summary: dict) -> str:
    """
    Format recurrent run-level findings.

    These findings describe patterns observed across multiple samples.
    """
    lines = [
        "## Run-Level Findings",
        "",
    ]

    recurrent_findings = run_summary["recurrent_findings"]

    if not recurrent_findings:
        lines.append("No recurrent QC patterns were detected.")
        lines.append("")
        return "\n".join(lines)

    for finding in recurrent_findings:
        lines.append(f"### {finding['category']}")
        lines.append("")
        lines.append(f"**Affected samples:** {finding['affected_samples']}")
        lines.append("")
        lines.append(f"**Interpretation:** {finding['interpretation']}")
        lines.append("")
        lines.append(f"**Recommended review:** {finding['recommended_review']}")
        lines.append("")

    return "\n".join(lines)


def format_sample_findings(classified_metrics) -> str:
    """
    Format sample-level findings for Markdown output.
    """
    lines = ["## Sample-Level Findings", ""]

    for _, row in classified_metrics.iterrows():
        lines.append(f"### {row['sample_id']} — {row['overall_status']}")
        lines.append("")
        lines.append(f"- Run ID: {row['run_id']}")
        lines.append(f"- Sample Type: {row['sample_type']}")
        lines.append("")

        if not row["findings"]:
            lines.append("No review-triggering QC findings.")
            lines.append("")
            continue

        for finding in row["findings"]:
            lines.append(
                f"- **Priority {finding['priority']} | "
                f"{finding['severity']}: {finding['category']}**"
            )
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
        (
            "This report summarizes sample-level QC findings generated "
            "from configurable review rules."
        ),
        "",
        format_run_summary(run_summary),
        format_run_level_findings(run_summary),
        format_sample_findings(classified_metrics),
        "## Limitations",
        "",
        (
            "These thresholds are example review rules created for portfolio "
            "demonstration only. They are not clinical release criteria and "
            "are not based on any proprietary laboratory SOP."
        ),
        "",
    ]

    return "\n".join(report_sections)