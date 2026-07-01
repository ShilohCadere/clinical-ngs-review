"""
Create run-level summaries from reviewed sample metrics.

This module answers: what is the overall QC story for the run?
"""

import pandas as pd


def summarize_run(classified_metrics: pd.DataFrame) -> dict:
    """
    Summarize sample-level review results into run-level counts.
    """
    status_counts = classified_metrics["overall_status"].value_counts().to_dict()

    total_samples = len(classified_metrics)
    failed_samples = status_counts.get("FAIL", 0)
    flagged_samples = status_counts.get("FLAG", 0)
    passing_samples = status_counts.get("PASS", 0)

    if failed_samples > 0:
        run_status = "FAIL"
    elif flagged_samples > 0:
        run_status = "FLAG"
    else:
        run_status = "PASS"

    return {
        "run_status": run_status,
        "total_samples": total_samples,
        "passing_samples": passing_samples,
        "flagged_samples": flagged_samples,
        "failed_samples": failed_samples,
    }