"""
Convert QC metric statuses into analyst-style findings.

A finding explains why a sample was flagged instead of only reporting
that a metric crossed a threshold.
"""

import pandas as pd


def get_overall_status(statuses: list[str]) -> str:
    """
    Summarize multiple metric statuses into one sample-level status.
    """
    if "FAIL" in statuses:
        return "FAIL"

    if "FLAG" in statuses:
        return "FLAG"

    return "PASS"


def build_sample_finding(row: pd.Series) -> str:
    """
    Create a short human-readable finding for one sample.
    """
    findings = []

    if row["alignment_status"] != "PASS":
        findings.append(f"{row['alignment_status']}: alignment rate {row['alignment_rate']}%")

    if row["coverage_status"] != "PASS":
        findings.append(f"{row['coverage_status']}: mean coverage {row['mean_coverage']}x")

    if row["duplication_status"] != "PASS":
        findings.append(f"{row['duplication_status']}: duplication rate {row['duplication_rate']}%")

    if row["variant_count_status"] != "PASS":
        findings.append(f"{row['variant_count_status']}: variant count {row['variant_count']}")

    if not findings:
        return "No review-triggering QC findings"

    return "; ".join(findings)


def classify_findings(reviewed_metrics: pd.DataFrame) -> pd.DataFrame:
    """
    Add overall sample status and analyst-style findings.
    """
    classified_metrics = reviewed_metrics.copy()

    status_columns = [
        "alignment_status",
        "coverage_status",
        "duplication_status",
        "variant_count_status",
    ]

    classified_metrics["overall_status"] = classified_metrics[status_columns].apply(
        lambda row: get_overall_status(row.tolist()),
        axis=1,
    )

    classified_metrics["finding_summary"] = classified_metrics.apply(
        build_sample_finding,
        axis=1,
    )

    return classified_metrics