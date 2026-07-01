"""
Data loading functions for clinical-ngs-review.

This module only reads and validates input files.
It does not apply QC rules or generate reports.
"""

from pathlib import Path

import pandas as pd

from clinical_ngs_review.ingest.validate_inputs import (
    REQUIRED_METADATA_COLUMNS,
    REQUIRED_QC_COLUMNS,
    validate_columns,
    validate_file_exists,
)


def load_qc_metrics(file_path: str | Path) -> pd.DataFrame:
    """
    Load the QC metrics table.

    The table contains one row per sample and numeric QC metrics used
    by the analysis layer.
    """
    validate_file_exists(file_path, "QC metrics file")

    qc_metrics = pd.read_csv(file_path)
    validate_columns(qc_metrics, REQUIRED_QC_COLUMNS, "QC metrics file")

    return qc_metrics


def load_sample_metadata(file_path: str | Path) -> pd.DataFrame:
    """
    Load the sample metadata table.

    Metadata is kept separate from QC metrics so sample context can be
    changed without modifying the measured QC values.
    """
    validate_file_exists(file_path, "Sample metadata file")

    sample_metadata = pd.read_csv(file_path)
    validate_columns(sample_metadata, REQUIRED_METADATA_COLUMNS, "Sample metadata file")

    return sample_metadata