"""
Create report-ready tables from reviewed QC results.

This module prepares output tables. It does not write files directly.
"""

import pandas as pd


def build_review_summary_table(classified_metrics: pd.DataFrame) -> pd.DataFrame:
    """
    Build a compact sample-level summary table for CSV output.
    """
    return classified_metrics[
        [
            "sample_id",
            "alignment_status",
            "coverage_status",
            "duplication_status",
            "variant_count_status",
            "overall_status",
        ]
    ].copy()


def build_flagged_samples_table(classified_metrics: pd.DataFrame) -> pd.DataFrame:
    """
    Build a table containing only samples that require review.
    """
    flagged_samples = classified_metrics[
        classified_metrics["overall_status"] != "PASS"
    ].copy()

    return flagged_samples[
        [
            "sample_id",
            "overall_status",
            "findings",
        ]
    ]