"""Tests for command-line configuration and output handling."""

from clinical_ngs_review.cli import build_parser


def test_cli_defaults_preserve_example_workflow():
    """Running without options should continue to use bundled example inputs."""
    args = build_parser().parse_args([])

    assert args.metrics == "data/example_qc_metrics.csv"
    assert args.metadata == "data/example_sample_metadata.csv"
    assert args.rules == "config/review_rules.yml"
    assert args.output_dir == "reports"


def test_cli_accepts_custom_paths():
    """Users should be able to supply their own inputs and output directory."""
    args = build_parser().parse_args(
        [
            "--metrics",
            "inputs/metrics.csv",
            "--metadata",
            "inputs/metadata.csv",
            "--rules",
            "config/custom.yml",
            "--output-dir",
            "results/custom_run",
        ]
    )

    assert args.metrics == "inputs/metrics.csv"
    assert args.metadata == "inputs/metadata.csv"
    assert args.rules == "config/custom.yml"
    assert args.output_dir == "results/custom_run"
