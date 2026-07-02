# Clinical NGS QC Review Report

This report summarizes sample-level QC findings generated from configured review rules.

## Run Summary

- Overall run status: **FAIL**
- Total samples reviewed: 3
- Passing samples: 1
- Flagged samples: 1
- Failed samples: 1

## Sample-Level Findings

### sample_001 — PASS

No review-triggering QC findings.

### sample_002 — FLAG

- **FLAG: Low Alignment Rate**
  - Evidence: alignment_rate = 92.1%
  - Recommended review: Review sequence quality and alignment statistics before downstream analysis.
- **FLAG: Low Coverage**
  - Evidence: mean_coverage = 24.8x
  - Recommended review: Confirm sequencing depth and review whether coverage is sufficient for downstream interpretation.
- **FLAG: High Duplication Rate**
  - Evidence: duplication_rate = 28.5%
  - Recommended review: Review library complexity and duplication metrics before interpreting downstream results.
- **FLAG: Low Variant Count**
  - Evidence: variant_count = 31
  - Recommended review: Review variant calling output and confirm whether variant yield is consistent with expectations.

### sample_003 — FAIL

- **FAIL: Low Alignment Rate**
  - Evidence: alignment_rate = 87.4%
  - Recommended review: Review sequence quality and alignment statistics before downstream analysis.
- **FAIL: Low Coverage**
  - Evidence: mean_coverage = 17.2x
  - Recommended review: Confirm sequencing depth and review whether coverage is sufficient for downstream interpretation.
- **FAIL: High Duplication Rate**
  - Evidence: duplication_rate = 46.0%
  - Recommended review: Review library complexity and duplication metrics before interpreting downstream results.
- **FAIL: Low Variant Count**
  - Evidence: variant_count = 8
  - Recommended review: Review variant calling output and confirm whether variant yield is consistent with expectations.

## Limitations

These thresholds are example review rules for portfolio demonstration only. They are not clinical release criteria and are not based on any proprietary SOP.
