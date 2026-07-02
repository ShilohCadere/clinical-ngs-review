"""
Create run-level summaries from reviewed sample metrics.

This module answers: what is the overall QC story for the run?
"""

import pandas as pd


def count_sample_statuses(classified_metrics: pd.DataFrame) -> dict:
    """
    Count PASS / FLAG / FAIL sample statuses.
    """
    status_counts = classified_metrics["overall_status"].value_counts().to_dict()

    return {
        "total_samples": len(classified_metrics),
        "passing_samples": status_counts.get("PASS", 0),
        "flagged_samples": status_counts.get("FLAG", 0),
        "failed_samples": status_counts.get("FAIL", 0),
    }


def determine_run_status(sample_counts: dict) -> str:
    """
    Determine the overall run status from sample-level statuses.
    """
    if sample_counts["failed_samples"] > 0:
        return "FAIL"

    if sample_counts["flagged_samples"] > 0:
        return "FLAG"

    return "PASS"


def detect_recurrent_findings(classified_metrics: pd.DataFrame) -> list[dict]:
    """
    Detect finding categories that appear in multiple samples.

    This adds run-level reasoning by identifying whether the same QC concern
    is isolated to one sample or repeated across multiple samples.
    """
    finding_counts = {}

    for _, row in classified_metrics.iterrows():
        for finding in row["findings"]:
            category = finding["category"]

            if category not in finding_counts:
                finding_counts[category] = 0

            finding_counts[category] += 1

    recurrent_findings = []

    for category, count in finding_counts.items():
        if count < 2:
            continue

        recurrent_findings.append(
            {
                "category": category,
                "affected_samples": count,
                "interpretation": (
                    f"{category} was observed in {count} samples. "
                    "This pattern may indicate a run-level or batch-level issue "
                    "rather than isolated sample variability."
                ),
                "recommended_review": (
                    "Review run-level QC evidence and evaluate whether the repeated "
                    "finding suggests broader workflow or sequencing performance concerns."
                ),
            }
        )

    return recurrent_findings


def summarize_run(classified_metrics: pd.DataFrame) -> dict:
    """
    Summarize sample-level review results into a run-level review summary.
    """
    sample_counts = count_sample_statuses(classified_metrics)
    run_status = determine_run_status(sample_counts)
    recurrent_findings = detect_recurrent_findings(classified_metrics)

    return {
        "run_status": run_status,
        **sample_counts,
        "recurrent_findings": recurrent_findings,
    }