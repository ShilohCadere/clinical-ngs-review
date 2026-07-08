"""
Tests for the ingestion layer.

These tests confirm that input validation catches missing required columns
before data reaches the analysis layer.
"""

import pandas as pd
import pytest

from clinical_ngs_review.ingest.validate_inputs import (
    REQUIRED_METADATA_COLUMNS,
    REQUIRED_QC_COLUMNS,
    validate_columns,
)


def test_qc_metrics_missing_required_column_raises_error():
    """
    QC metrics input should fail validation when a required column is missing.
    """
    qc_metrics = pd.DataFrame(
        {
            "sample_id": ["sample_001"],
            "alignment_rate": [97.2],
            "mean_coverage": [42.5],
            "duplication_rate": [12.0],
            # variant_count is intentionally missing
        }
    )

    with pytest.raises(ValueError, match="variant_count"):
        validate_columns(qc_metrics, REQUIRED_QC_COLUMNS, "QC metrics file")


def test_sample_metadata_missing_required_column_raises_error():
    """
    Sample metadata input should fail validation when a required column is missing.
    """
    sample_metadata = pd.DataFrame(
        {
            "sample_id": ["sample_001"],
            "run_id": ["RUN001"],
            # sample_type is intentionally missing
        }
    )

    with pytest.raises(ValueError, match="sample_type"):
        validate_columns(sample_metadata, REQUIRED_METADATA_COLUMNS, "Sample metadata file")


def test_valid_qc_metrics_columns_pass_validation():
    """
    QC metrics input should pass validation when all required columns are present.
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

    validate_columns(qc_metrics, REQUIRED_QC_COLUMNS, "QC metrics file")


def test_valid_sample_metadata_columns_pass_validation():
    """
    Sample metadata input should pass validation when all required columns are present.
    """
    sample_metadata = pd.DataFrame(
        {
            "sample_id": ["sample_001"],
            "run_id": ["RUN001"],
            "sample_type": ["tumor"],
        }
    )

    validate_columns(sample_metadata, REQUIRED_METADATA_COLUMNS, "Sample metadata file")