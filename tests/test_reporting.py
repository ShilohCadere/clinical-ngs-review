"""
Tests for the reporting layer.

These tests confirm that report generation includes the major sections
and communicates run-level and sample-level findings.
"""

import pandas as pd

from clinical_ngs_review.reporting.markdown_report import generate_markdown_report


def test_markdown_report_contains_core_sections():
    """
    Markdown report should include the main analyst review sections.
    """
    classified_metrics = pd.DataFrame(
        {
            "sample_id": ["sample_001"],
            "run_id": ["RUN001"],
            "sample_type": ["tumor"],
            "overall_status": ["PASS"],
            "findings": [[]],
        }
    )

    run_summary = {
        "run_status": "PASS",
        "total_samples": 1,
        "passing_samples": 1,
        "flagged_samples": 0,
        "failed_samples": 0,
        "recurrent_findings": [],
    }

    report = generate_markdown_report(classified_metrics, run_summary)

    assert "# Clinical NGS QC Review Report" in report
    assert "## Run Summary" in report
    assert "## Run-Level Findings" in report
    assert "## Sample-Level Findings" in report
    assert "## Limitations" in report


def test_markdown_report_includes_recurrent_findings():
    """
    Markdown report should communicate recurrent run-level findings.
    """
    classified_metrics = pd.DataFrame(
        {
            "sample_id": ["sample_001"],
            "run_id": ["RUN001"],
            "sample_type": ["tumor"],
            "overall_status": ["FAIL"],
            "findings": [
                [
                    {
                        "category": "Low Coverage",
                        "severity": "FAIL",
                        "priority": 2,
                        "evidence": "mean_coverage = 17.2x",
                        "recommendation": "Review coverage.",
                    }
                ]
            ],
        }
    )

    run_summary = {
        "run_status": "FAIL",
        "total_samples": 1,
        "passing_samples": 0,
        "flagged_samples": 0,
        "failed_samples": 1,
        "recurrent_findings": [
            {
                "category": "Low Coverage",
                "affected_samples": 2,
                "interpretation": "Low Coverage was observed in 2 samples.",
                "recommended_review": "Review run-level QC evidence.",
            }
        ],
    }

    report = generate_markdown_report(classified_metrics, run_summary)

    assert "Low Coverage" in report
    assert "Affected samples" in report
    assert "Review run-level QC evidence" in report


def test_markdown_report_includes_sample_priority():
    """
    Markdown report should include finding priority for sample-level review.
    """
    classified_metrics = pd.DataFrame(
        {
            "sample_id": ["sample_001"],
            "run_id": ["RUN001"],
            "sample_type": ["tumor"],
            "overall_status": ["FAIL"],
            "findings": [
                [
                    {
                        "category": "Low Alignment Rate",
                        "severity": "FAIL",
                        "priority": 1,
                        "evidence": "alignment_rate = 87.4%",
                        "recommendation": "Review alignment.",
                    }
                ]
            ],
        }
    )

    run_summary = {
        "run_status": "FAIL",
        "total_samples": 1,
        "passing_samples": 0,
        "flagged_samples": 0,
        "failed_samples": 1,
        "recurrent_findings": [],
    }

    report = generate_markdown_report(classified_metrics, run_summary)

    assert "Priority 1" in report
    assert "FAIL: Low Alignment Rate" in report
    assert "alignment_rate = 87.4%" in report