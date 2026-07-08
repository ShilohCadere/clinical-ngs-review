# Clinical NGS Review

## At a Glance

- Analyst-focused review system for interpreting sequencing QC results after pipeline execution.
- Applies configurable QC review rules to identify sample- and run-level findings.
- Generates structured analyst reports in CSV and Markdown formats.
- Demonstrates production-style software architecture, configurable analysis, and QC decision support using simulated sequencing data.

## Overview

Clinical NGS Review is a portfolio project that models the analytical review process performed after an NGS pipeline completes. Rather than performing alignment or variant calling, the project evaluates sequencing quality metrics, applies configurable review rules, identifies sample- and run-level QC findings, and produces analyst-facing review reports.

The repository emphasizes software architecture, analytical reasoning, and reproducible review workflows commonly found in production bioinformatics environments while using simulated data and non-clinical demonstration thresholds.

## Why This Project Exists

Generating sequencing QC metrics is only one step in an NGS workflow. Before downstream interpretation, those metrics must be reviewed to determine whether sequencing quality supports continued analysis and whether any findings warrant additional investigation.

This project demonstrates that review process.

Using configurable QC rules, the application evaluates sequencing metrics, prioritizes findings, detects recurring run-level patterns, and generates reports that communicate both the evidence observed and the recommended areas for further review.

The focus is not clinical interpretation or proprietary laboratory procedures. Instead, the project demonstrates how analytical reasoning, software design, and clear communication can be combined to support quality review within an NGS workflow.

## Workflow Architecture

Clinical NGS Review models the analytical review process that occurs after sequencing quality metrics have been generated. The application separates data ingestion, analytical reasoning, and reporting into independent layers to improve readability, maintainability, and testability.

```text
QC Metrics
      │
      ▼
Input Validation
      │
      ▼
Configurable Review Rules (YAML)
      │
      ▼
Sample-Level Findings
      │
      ▼
Run-Level Pattern Detection
      │
      ▼
Analyst Review Reports
      ├── CSV Summary Tables
      └── Markdown Review Report
```

## Repository Structure

```text
clinical-ngs-review/
├── clinical_ngs_review/
│   ├── analysis/      # QC rule evaluation and analytical reasoning
│   ├── ingest/        # Input loading and validation
│   ├── reporting/     # CSV and Markdown report generation
│   └── cli.py         # Command-line entry point
├── config/            # Configurable QC review rules
├── data/              # Example input datasets
├── reports/           # Generated report outputs
└── tests/             # Unit tests
```

The repository is organized around responsibility rather than technology. Each module performs one stage of the review workflow, allowing ingestion, analysis, reporting, and testing to evolve independently while keeping responsibilities clearly separated.

## Current Capabilities

Current functionality includes:

- Loading sequencing QC metrics and sample metadata from structured input files.
- Validating required input columns before analysis begins.
- Applying configurable QC review thresholds from YAML configuration.
- Classifying metrics as PASS, FLAG, or FAIL.
- Producing structured analyst findings with supporting evidence and recommended review actions.
- Prioritizing findings to guide analyst review order.
- Detecting recurring run-level QC patterns across multiple samples.
- Generating analyst-facing CSV summary tables and Markdown review reports.
- Verifying analytical logic through automated unit tests.

## Example Inputs

Example datasets are included to demonstrate the complete review workflow.

### QC Metrics

- Alignment rate
- Mean coverage
- Duplication rate
- Variant count

### Sample Metadata

- Sample identifier
- Run identifier
- Sample type

These example datasets are simulated and exist solely to demonstrate workflow behavior. They do not represent clinical sequencing data or proprietary laboratory outputs.

## Example Outputs

Successful execution generates analyst-facing review artifacts within the `reports/` directory.

### Review Summary (CSV)

Provides a concise sample-level summary including QC classifications and overall review status.

### Flagged Samples (CSV)

Contains only samples requiring analyst attention, along with their associated findings.

### Analyst Review Report (Markdown)

Summarizes:

- Overall run status
- Sample review counts
- Run-level QC observations
- Sample-level findings
- Supporting evidence
- Recommended review actions

The generated reports are intended to demonstrate structured QC review rather than clinical interpretation.

## Design Decisions

Several architectural decisions intentionally shape this project.

### Layer Separation

Input ingestion, analytical reasoning, and report generation are implemented as independent modules. This keeps responsibilities well-defined and allows each layer to be tested independently.

### Configurable Review Rules

QC thresholds are stored in YAML rather than embedded directly in code. Separating configuration from implementation allows review criteria to change without modifying the analytical workflow.

### Structured Findings

Findings are represented as structured data instead of formatted text. This allows the same analytical results to be reused across multiple reporting formats while keeping presentation separate from decision logic.

### Run-Level Reasoning

In addition to evaluating individual samples, the application identifies recurring QC findings across a sequencing run. This demonstrates how analytical review extends beyond isolated sample metrics.

### Test-Driven Validation

Core analytical behavior is verified through unit tests covering ingestion, rule evaluation, classification, run summarization, and report generation.

## Testing

Automated tests verify the analytical behavior of the application rather than external library functionality.

Current test coverage includes:

- Input validation
- QC rule evaluation
- PASS / FLAG / FAIL classification
- Sample-level finding generation
- Run-level pattern detection
- Markdown report generation

Run all tests with:

```bash
python -m pytest
```

At the time of publication, the project contains 13 automated unit tests covering the core analytical workflow.

## Future Improvements

Planned future development includes:

- Integrating directly with outputs from the companion Clinical NGS Workflow repository.
- Expanding support for additional QC metrics as analytical capabilities grow.
- Enhancing report generation while preserving the separation between analysis and presentation.
- Extending automated test coverage alongside future functionality.

Future development will continue to prioritize analytical reasoning, maintainable software architecture, and modular design over feature quantity.

## Technologies Used

Python • pandas • PyYAML • pytest • Markdown

## Author

**Shiloh Cadere**

Bioinformatics analyst focused on genomics QC, analytical review, workflow development, and reproducible bioinformatics software.