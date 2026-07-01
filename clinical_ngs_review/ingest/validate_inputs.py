"""
Input validation for clinical-ngs-review.

This file checks that input tables have the columns the analysis layer expects.
Keeping validation separate from loading makes errors easier to understand.
"""

from pathlib import Path

import pandas as pd


REQUIRED_QC_COLUMNS = {
    "sample_id",
    "alignment_rate",
    "mean_coverage",
    "duplication_rate",
    "variant_count",
}

REQUIRED_METADATA_COLUMNS = {
    "sample_id",
    "run_id",
    "sample_type",
}


def validate_columns(
    dataframe: pd.DataFrame,
    required_columns: set[str],
    file_label: str,
) -> None:
    """
    Confirm that a table contains all required columns.

    Args:
        dataframe: Loaded pandas DataFrame.
        required_columns: Column names needed for downstream analysis.
        file_label: Human-readable file name for error messages.

    Raises:
        ValueError: If one or more required columns are missing.
    """
    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"{file_label} is missing required columns: {missing}")


def validate_file_exists(file_path: str | Path, file_label: str) -> None:
    """
    Confirm that an expected input file exists before trying to read it.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_label} not found: {path}")