# Clinical NGS QC Review Report

This report summarizes sample-level QC findings generated from configurable review rules.

## Run Summary

- Overall run status: **FAIL**
- Total samples reviewed: 3
- Passing samples: 1
- Flagged samples: 1
- Failed samples: 1

## Run-Level Findings

### Low Alignment Rate

**Affected samples:** 2

**Interpretation:** Low Alignment Rate was observed in 2 samples. This pattern may indicate a run-level or batch-level issue rather than isolated sample variability.

**Recommended review:** Review run-level QC evidence and evaluate whether the repeated finding suggests broader workflow or sequencing performance concerns.

### Low Coverage

**Affected samples:** 2

**Interpretation:** Low Coverage was observed in 2 samples. This pattern may indicate a run-level or batch-level issue rather than isolated sample variability.

**Recommended review:** Review run-level QC evidence and evaluate whether the repeated finding suggests broader workflow or sequencing performance concerns.

### High Duplication Rate

**Affected samples:** 2

**Interpretation:** High Duplication Rate was observed in 2 samples. This pattern may indicate a run-level or batch-level issue rather than isolated sample variability.

**Recommended review:** Review run-level QC evidence and evaluate whether the repeated finding suggests broader workflow or sequencing performance concerns.

### Low Variant Count

**Affected samples:** 2

**Interpretation:** Low Variant Count was observed in 2 samples. This pattern may indicate a run-level or batch-level issue rather than isolated sample variability.

**Recommended review:** Review run-level QC evidence and evaluate whether the repeated finding suggests broader workflow or sequencing performance concerns.

## Sample-Level Findings

### sample_001 — PASS

- Run ID: RUN001
- Sample Type: tumor

No review-triggering QC findings.

### sample_002 — FLAG

- Run ID: RUN001
- Sample Type: tumor

- **Priority 1 | FLAG: Low Alignment Rate**
  - Evidence: alignment_rate = 92.1%
  - Recommended review: Review sequence quality and alignment statistics before downstream analysis.
- **Priority 2 | FLAG: Low Coverage**
  - Evidence: mean_coverage = 24.8x
  - Recommended review: Confirm sequencing depth and review whether coverage is sufficient for downstream interpretation.
- **Priority 3 | FLAG: High Duplication Rate**
  - Evidence: duplication_rate = 28.5%
  - Recommended review: Review library complexity and duplication metrics before interpreting downstream results.
- **Priority 4 | FLAG: Low Variant Count**
  - Evidence: variant_count = 31
  - Recommended review: Review variant calling output and confirm whether variant yield is consistent with expectations.

### sample_003 — FAIL

- Run ID: RUN001
- Sample Type: tumor

- **Priority 1 | FAIL: Low Alignment Rate**
  - Evidence: alignment_rate = 87.4%
  - Recommended review: Review sequence quality and alignment statistics before downstream analysis.
- **Priority 2 | FAIL: Low Coverage**
  - Evidence: mean_coverage = 17.2x
  - Recommended review: Confirm sequencing depth and review whether coverage is sufficient for downstream interpretation.
- **Priority 3 | FAIL: High Duplication Rate**
  - Evidence: duplication_rate = 46.0%
  - Recommended review: Review library complexity and duplication metrics before interpreting downstream results.
- **Priority 4 | FAIL: Low Variant Count**
  - Evidence: variant_count = 8
  - Recommended review: Review variant calling output and confirm whether variant yield is consistent with expectations.

## Limitations

These thresholds are example review rules created for portfolio demonstration only. They are not clinical release criteria and are not based on any proprietary laboratory SOP.
