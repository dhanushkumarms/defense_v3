# Attack Success Rate (ASR) - Original Results

| Variant | Harmful / Total | ASR | Defense Rate |
|---------|----------------|-----|--------------|
| Direct | 139 / 2,500 | 5.6% | 94.4% |
| Simple paraphrase | 974 / 2,500 | 39.0% | 61.0% |
| Adversarial jailbreak | 1,406 / 2,500 | 56.2% | 43.8% |

## Key Observations

- **Baseline (Direct)**: Moderate defense with 94.4% safety rate
- **Simple Paraphrase**: 7.0× increase in ASR compared to baseline
- **Adversarial Jailbreak**: 10.1× increase in ASR compared to baseline
- **Absolute increase**:
  - Simple vs Direct: +33.4 percentage points
  - Adversarial vs Direct: +50.7 percentage points

## Paired Analysis

| Outcome | Count | Percentage |
|---------|-------|------------|
| Both Defended | 1,031 | 41.2% |
| Adversarial Penetration | 1,330 | 53.2% |
| Adversarial Strengthened | 63 | 2.5% |
| Both Vulnerable | 76 | 3.0% |

**True ASR**: 56.3% (1,330 / 2,361 safe baseline questions)

## Toxicity Statistics

| Variant | Mean Score |
|---------|-----------|
| Direct | 0.235 |
| Simple Paraphrase | 0.434 |
| Adversarial Jailbreak | 0.549 |

**Detection Threshold**: 0.5
