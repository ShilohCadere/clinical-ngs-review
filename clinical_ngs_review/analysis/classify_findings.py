"""
Convert QC metric statuses into structured analyst findings.

A finding connects three pieces of analyst reasoning:
1. What was observed
2. Why it matters
3. What should be reviewed next

Findings also include review priority. Severity describes how concerning
a finding is; priority describes where an analyst should start reviewing.
"""

import pandas as pd


FINDING_RULES = {
    "alignment_status": {
        "metric": "alignment_rate",
        "category": "Low Alignment Rate",
        "unit": "%",
        "priority": 1,
        "recommendation": "Review sequence quality and alignment statistics before downstream analysis.",
    },
    "coverage_status": {
        "metric": "mean_coverage",
        "category": "Low Coverage",
        "unit": "x",
        "priority": 2,
        "recommendation": "Confirm sequencing depth and review whether coverage is sufficient for downstream interpretation.",
    },
    "duplication_status": {
        "metric": "duplication_rate",
        "category": "High Duplication Rate",
        "unit": "%",
        "priority": 3,
        "recommendation": "Review library complexity and duplication metrics before interpreting downstream results.",
    },
    "variant_count_status": {
        "metric": "variant_count",
        "category": "Low Variant Count",
        "unit": "",
        "priority": 4,
        "recommendation": "Review variant calling output and confirm whether variant yield is consistent with expectations.",
    },
}


def get_overall_status(statuses: list[str]) -> str:
    """
    Summarize multiple metric statuses into one sample-level status.
    """
    if "FAIL" in statuses:
        return "FAIL"

    if "FLAG" in statuses:
        return "FLAG"

    return "PASS"


def format_evidence(metric_name: str, value: float, unit: str) -> str:
    """
    Create a short evidence statement for a single metric.
    """
    if unit:
        return f"{metric_name} = {value}{unit}"

    return f"{metric_name} = {value}"


def build_findings(row: pd.Series) -> list[dict]:
    """
    Build structured findings for one sample.

    Returns an empty list when no review-triggering findings are present.
    """
    findings = []

    for status_column, rule in FINDING_RULES.items():
        status = row[status_column]

        if status == "PASS":
            continue

        metric_name = rule["metric"]
        metric_value = row[metric_name]

        findings.append(
            {
                "category": rule["category"],
                "severity": status,
                "priority": rule["priority"],
                "evidence": format_evidence(metric_name, metric_value, rule["unit"]),
                "recommendation": rule["recommendation"],
            }
        )

    return sorted(findings, key=lambda finding: finding["priority"])


def classify_findings(reviewed_metrics: pd.DataFrame) -> pd.DataFrame:
    """
    Add overall sample status and structured analyst findings.
    """
    classified_metrics = reviewed_metrics.copy()

    status_columns = list(FINDING_RULES.keys())

    classified_metrics["overall_status"] = classified_metrics[status_columns].apply(
        lambda row: get_overall_status(row.tolist()),
        axis=1,
    )

    classified_metrics["findings"] = classified_metrics.apply(
        build_findings,
        axis=1,
    )

    return classified_metrics