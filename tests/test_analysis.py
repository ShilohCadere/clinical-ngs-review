"""
Tests for the analysis layer.

These tests focus on project logic:
- QC rule evaluation
- finding classification
- run-level summaries
"""

import pandas as pd

from clinical_ngs_review.analysis.apply_rules import (
    apply_rules,
    evaluate_maximum_rule,
    evaluate_minimum_rule,
)
from clinical_ngs_review.analysis.classify_findings import (
    classify_findings,
    get_overall_status,
)
from clinical_ngs_review.analysis.summarize_run import summarize_run


def test_minimum_rule_returns_pass_flag_fail():
    """
    Metrics where higher values are better should return expected statuses.
    """
    rule = {
        "pass_min": 95,
        "flag_min": 90,
        "fail_below": 90,
    }

    assert evaluate_minimum_rule(97, rule) == "PASS"
    assert evaluate_minimum_rule(92, rule) == "FLAG"
    assert evaluate_minimum_rule(88, rule) == "FAIL"


def test_maximum_rule_returns_pass_flag_fail():
    """
    Metrics where lower values are better should return expected statuses.
    """
    rule = {
        "pass_max": 20,
        "flag_max": 40,
        "fail_above": 40,
    }

    assert evaluate_maximum_rule(12, rule) == "PASS"
    assert evaluate_maximum_rule(28, rule) == "FLAG"
    assert evaluate_maximum_rule(46, rule) == "FAIL"


def test_apply_rules_adds_status_columns():
    """
    Applying rules should add one status column for each QC metric.
    """
    qc_metrics = pd.DataFrame(
        {
            "sample_id": ["sample_001"],
            "alignment_rate": [97.2],
            "mean_coverage": [42.5],
            "duplication_rate": [12.0],
            "variant_count": [63],
        }
    )

    review_rules = {
        "alignment_rate": {"pass_min": 95, "flag_min": 90, "fail_below": 90},
        "mean_coverage": {"pass_min": 30, "flag_min": 20, "fail_below": 20},
        "duplication_rate": {"pass_max": 20, "flag_max": 40, "fail_above": 40},
        "variant_count": {"pass_min": 50, "flag_min": 10, "fail_below": 10},
    }

    reviewed_metrics = apply_rules(qc_metrics, review_rules)

    assert reviewed_metrics.loc[0, "alignment_status"] == "PASS"
    assert reviewed_metrics.loc[0, "coverage_status"] == "PASS"
    assert reviewed_metrics.loc[0, "duplication_status"] == "PASS"
    assert reviewed_metrics.loc[0, "variant_count_status"] == "PASS"


def test_overall_status_prioritizes_fail_then_flag_then_pass():
    """
    Overall status should escalate to the most severe metric status.
    """
    assert get_overall_status(["PASS", "PASS", "PASS"]) == "PASS"
    assert get_overall_status(["PASS", "FLAG", "PASS"]) == "FLAG"
    assert get_overall_status(["PASS", "FAIL", "FLAG"]) == "FAIL"


def test_classify_findings_creates_structured_findings():
    """
    Non-passing metric statuses should become structured analyst findings.
    """
    reviewed_metrics = pd.DataFrame(
        {
            "sample_id": ["sample_001"],
            "alignment_rate": [87.4],
            "mean_coverage": [17.2],
            "duplication_rate": [46.0],
            "variant_count": [8],
            "alignment_status": ["FAIL"],
            "coverage_status": ["FAIL"],
            "duplication_status": ["FAIL"],
            "variant_count_status": ["FAIL"],
        }
    )

    classified_metrics = classify_findings(reviewed_metrics)
    findings = classified_metrics.loc[0, "findings"]

    assert classified_metrics.loc[0, "overall_status"] == "FAIL"
    assert len(findings) == 4
    assert findings[0]["category"] == "Low Alignment Rate"
    assert findings[0]["priority"] == 1
    assert findings[0]["severity"] == "FAIL"


def test_summarize_run_detects_recurrent_findings():
    """
    Repeated finding categories across samples should become run-level findings.
    """
    classified_metrics = pd.DataFrame(
        {
            "sample_id": ["sample_001", "sample_002"],
            "overall_status": ["FLAG", "FAIL"],
            "findings": [
                [
                    {
                        "category": "Low Coverage",
                        "severity": "FLAG",
                        "priority": 2,
                        "evidence": "mean_coverage = 24.8x",
                        "recommendation": "Review coverage.",
                    }
                ],
                [
                    {
                        "category": "Low Coverage",
                        "severity": "FAIL",
                        "priority": 2,
                        "evidence": "mean_coverage = 17.2x",
                        "recommendation": "Review coverage.",
                    }
                ],
            ],
        }
    )

    run_summary = summarize_run(classified_metrics)

    assert run_summary["run_status"] == "FAIL"
    assert run_summary["total_samples"] == 2
    assert len(run_summary["recurrent_findings"]) == 1
    assert run_summary["recurrent_findings"][0]["category"] == "Low Coverage"
    assert run_summary["recurrent_findings"][0]["affected_samples"] == 2