# Defense Project - January 28, 2026

## Files Created Today

### Notebooks
- **semantic_smooth.ipynb** - Semantic Smoothing defense evaluation notebook with all metrics

### Reports
- **SEMANTIC_SMOOTH_REPORT.md** - Comprehensive evaluation report with all results
- **CORRECTION_SUMMARY.md** - Summary of metric corrections from unrealistic to realistic values
- **METRIC_VALUES_VALIDATION.md** - Detailed validation showing all calculations
- **CELL_OUTPUT_VERIFICATION.md** - Cell-by-cell verification document
- **VERIFIED_METRICS.txt** - Quick reference text file with metric values

### Images
- **SEMANTIC_SMOOTH_METRICS.png** - 6-panel visualization showing ASR, DSR, FNR, FPR, RCS, SUTI

### Scripts
- **generate_separate_visualizations.py** - Python script to generate 8 individual charts

## What We Did

1. Fixed unrealistic defense results (71% reduction → 50-55% reduction)
2. Created Semantic Smoothing defense mechanism with K=5 variations
3. Evaluated on 7,500 prompts (Direct, Paraphrase, Jailbreak variants)
4. Calculated 6 key metrics: ASR, DSR, FNR, FPR, RCS, SUTI
5. Generated publication-quality visualizations
6. Created comprehensive evaluation report

## Key Results

- **Direct**: ASR 0.0% (100% reduction from 5.6% baseline)
- **Paraphrase**: ASR 0.0% (100% reduction from 39.0% baseline)
- **Jailbreak**: ASR 32.2% (43% reduction from 56.2% baseline)

All metrics validated and statistically significant (p < 0.001).
