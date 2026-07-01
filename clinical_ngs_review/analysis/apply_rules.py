"""
Apply QC review rules to sample-level metrics.

This module turns raw metric values into PASS / FLAG / FAIL calls.
It does not decide the final run summary or write reports.
"""

from pathlib import Path

import pandas as pd
import yaml


def load_review_rules(file_path: str | Path) -> dict:
    """
    Load review rules from a YAML configuration file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Review rules file not found: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def evaluate_minimum_rule(value: float, rule: dict) -> str:
    """
    Evaluate metrics where higher values are better.

    Examples:
        alignment_rate
        mean_coverage
        variant_count
    """
    if value < rule["fail_below"]:
        return "FAIL"

    if value < rule["pass_min"]:
        return "FLAG"

    return "PASS"


def evaluate_maximum_rule(value: float, rule: dict) -> str:
    """
    Evaluate metrics where lower values are better.

    Example:
        duplication_rate
    """
    if value > rule["fail_above"]:
        return "FAIL"

    if value > rule["pass_max"]:
        return "FLAG"

    return "PASS"


def apply_rules(qc_metrics: pd.DataFrame, review_rules: dict) -> pd.DataFrame:
    """
    Apply configured QC rules to each sample.

    Returns a copy of the input table with one status column per metric.
    """
    reviewed_metrics = qc_metrics.copy()

    reviewed_metrics["alignment_status"] = reviewed_metrics["alignment_rate"].apply(
        lambda value: evaluate_minimum_rule(value, review_rules["alignment_rate"])
    )

    reviewed_metrics["coverage_status"] = reviewed_metrics["mean_coverage"].apply(
        lambda value: evaluate_minimum_rule(value, review_rules["mean_coverage"])
    )

    reviewed_metrics["duplication_status"] = reviewed_metrics["duplication_rate"].apply(
        lambda value: evaluate_maximum_rule(value, review_rules["duplication_rate"])
    )

    reviewed_metrics["variant_count_status"] = reviewed_metrics["variant_count"].apply(
        lambda value: evaluate_minimum_rule(value, review_rules["variant_count"])
    )

    return reviewed_metrics