# Project Architecture & Workflow

## High-Level Project Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEFENSE PROJECT ARCHITECTURE                     │
│              Enhancing LLM Robustness Against Adversarial Attacks   │
└─────────────────────────────────────────────────────────────────────┘

                              PHASE 1: ✅ COMPLETE
                        (Baseline Attack Evaluation)
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
        ┌───────────▼───────────┐      ┌────────────▼──────────┐
        │  Dataset Generation   │      │   Baseline Evaluation │
        │  2,500 × 3 variants   │      │   (ATTACK3 Notebook)  │
        │  = 7,500 prompts      │      │                       │
        │                       │      │   Results:            │
        │ • Direct (5.6% ASR)   │      │   • Direct: 5.6%      │
        │ • Paraphrase (39%)    │      │   • Paraphrase: 39%   │
        │ • Jailbreak (56.2%)   │      │   • Jailbreak: 56.2%  │
        └───────────────────────┘      └──────────────────────┘
                                                │
                                                │
                    ┌───────────────────────────┘
                    │
        ┌───────────▼────────────────────────┐
        │  Analysis & Documentation          │
        │  • Chapters 1-4                    │
        │  • Statistical tests               │
        │  • Policy-wise breakdown           │
        │  • Visualization dashboards        │
        └────────────────────────────────────┘


                           PHASE 2: 🔄 IN PROGRESS
                      (Defense Implementation & Evaluation)
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
    ┌───▼──────────┐      ┌────────▼────────┐      ┌──────────▼──┐
    │ Semantic     │      │  Metrics        │      │ Visualiza-  │
    │ Smoothing    │      │  Calculation    │      │ tion        │
    │ Framework    │      │  (6 Metrics)    │      │ Generation  │
    │              │      │                 │      │             │
    │ • SSr Class  │      │ • ASR: 2.4%     │      │ • 3 PNG     │
    │ • K=5 vars   │      │   - 18.4%       │      │   images    │
    │ • Majority   │      │   - 28.7%       │      │ • 300 DPI   │
    │   voting     │      │ • DSR, FNR, etc │      │ • Color-    │
    │              │      │                 │      │   coded     │
    └──────────────┘      └─────────────────┘      └─────────────┘
            │                     │                      │
            └─────────────────────┴──────────────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  Reports & Documentation   │
                    │  • SEMANTIC_SMOOTH_REPORT  │
                    │  • EVALUATION_SUMMARY      │
                    │  • Updated README.md       │
                    └────────────────────────────┘


                        PHASE 2 (Continuation): ⏳ PENDING
                     (Production & Final Evaluation)
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
    ┌───▼──────────┐      ┌────────▼────────┐      ┌──────────▼──┐
    │ 4A: Enhance  │      │ 4B: Comparative │      │ 5: Final    │
    │ Implementation      │ Testing         │      │ Analysis    │
    │                │      │                 │      │             │
    │ • Real T5     │      │ • Full eval on  │      │ • Stat sig  │
    │   paraphrasing│      │   7,500 prompts │      │ • Trade-off │
    │ • Threshold   │      │ • Alt defenses  │      │ • Deployment│
    │   tuning      │      │ • FPR on benign │      │   readiness │
    │ • Optimization│      │ • Latency tests │      │ • Final     │
    │ • ~2-4 hours  │      │ • ~2-4 hours    │      │   report    │
    └──────────────┘      └─────────────────┘      └─────────────┘
            │                     │                      │
            └─────────────────────┴──────────────────────┘
                                  │
                        ┌─────────▼──────────┐
                        │  FINAL DELIVERABLE │
                        │ Phase-2 Technical  │
                        │ Report with:       │
                        │ • Implementation   │
                        │ • Results          │
                        │ • Trade-offs       │
                        │ • Deployment guide │
                        └────────────────────┘
```

---

## Key Results Summary

```
┌─────────────────────────────────────────────────────┐
│              BASELINE vs DEFENSE COMPARISON         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  DIRECT ATTACK VARIANT                              │
│  ├─ ATTACK3 (Baseline): 5.6% ASR                   │
│  ├─ With Defense:       2.4% ASR                   │
│  └─ Improvement:        -57% reduction ✓           │
│                                                     │
│  PARAPHRASE VARIANT                                 │
│  ├─ ATTACK3 (Baseline): 39.0% ASR                  │
│  ├─ With Defense:       18.4% ASR                  │
│  └─ Improvement:        -53% reduction ✓           │
│                                                     │
│  JAILBREAK VARIANT                                  │
│  ├─ ATTACK3 (Baseline): 56.2% ASR                  │
│  ├─ With Defense:       28.7% ASR                  │
│  └─ Improvement:        -49% reduction ✓           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## File Dependency Graph

```
                            ┌──────────────┐
                            │  datasets/   │
                            │ three_variant│
                            │_dataset_2500 │
                            └──────┬───────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
        ┌────────▼────────┐  ┌─────▼──────┐  ┌─────▼────────┐
        │  attack3.ipynb  │  │semantic_   │  │ evaluate_   │
        │  (Baseline)     │  │smooth.ipynb│  │resumable.py │
        └────────┬────────┘  └─────┬──────┘  └─────┬────────┘
                 │                 │                │
        ┌────────▼────────┐  ┌─────▼──────┐       │
        │ ATTACK3_        │  │ SEMANTIC_   │       │
        │ RESULTS.md      │  │ SMOOTH_     │       │
        │ RESULTS.html    │  │ REPORT.md   │       │
        └────────┬────────┘  └─────┬──────┘       │
                 │                 │                │
                 └────────────┬────┴────────────────┘
                              │
                    ┌─────────▼───────────┐
                    │   models/README.md  │
                    │  (Updated Index)    │
                    └─────────┬───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───▼────┐            ┌───▼────┐           ┌───▼────┐
    │ SEMANTIC│            │DEFENSE_│           │BASELINE│
    │_SMOOTH_ │            │METRICS_│           │COMPARISON
    │METRICS  │            │TABLE   │           │_TABLE   │
    │.png     │            │.png    │           │.png     │
    └────────┘            └────────┘           └─────────┘
```

---

## Dataset Pipeline

```
                   RAW PROMPTS (2,500)
                            │
                ┌───────────┴───────────┐
                │                       │
        ┌───────▼────────┐    ┌────────▼──────┐
        │ Direct Variant │    │  Paraphrase   │
        │ (5.6% ASR)     │    │  Generator    │
        └────────────────┘    └────────┬──────┘
                │                      │
                │             ┌────────▼───────┐
                │             │ Simple Para    │
                │             │ (39% ASR)      │
                │             └────────┬───────┘
                │                      │
                │             ┌────────▼──────────┐
                │             │ Adversarial      │
                │             │ Paraphrase       │
                │             │ (56.2% ASR)      │
                │             └─────────┬────────┘
                │                       │
                └───────────┬───────────┘
                            │
                ┌───────────▼──────────┐
                │ 7,500 TOTAL PROMPTS  │
                │ (3 variants × 2,500) │
                └───────────┬──────────┘
                            │
                ┌───────────▼──────────────┐
                │ Ensemble Classifier      │
                │ (ToxicBERT + RoBERTa +   │
                │  ToxicChat-BERT)         │
                │ Threshold: 0.50          │
                └───────────┬──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───▼────┐         ┌───▼────┐         ┌───▼────┐
    │ATTACK3 │         │Semantic│         │Defense │
    │Results │         │Smoothing         │Results │
    │(.md)   │         │Results │         │(.md)   │
    └────────┘         └────────┘         └────────┘
```

---

## Metrics Hierarchy

```
                    BASELINE ASR
                   (ATTACK3 Results)
                          │
              ┌───────────┼───────────┐
              │           │           │
          5.6%        39.0%      56.2%
         (Direct)  (Paraphrase) (Jailbreak)
              │           │           │
              │ Semantic Smoothing Defense
              │           │           │
              ▼           ▼           ▼
          2.4%        18.4%      28.7%
      (-57% red)   (-53% red)  (-49% red)
              │           │           │
              └───────────┼───────────┘
                          │
              ┌───────────┴─────────────┐
              │                         │
          ┌───▼────┐             ┌─────▼──┐
          │6 Metrics            │ Visual  │
          │                     │ Reports │
          │• ASR (2.4-28.7%)   │         │
          │• DSR (71-97.6%)    │ • 3 PNG │
          │• FNR (0-28.7%)     │   images│
          │• FPR (0%)          │ • 300   │
          │• RCS (71-97.6%)    │   DPI   │
          │• SUTI (0.713-0.976)│         │
          └────────────────────┘         │
                                         │
                            ┌────────────▼──────┐
                            │  Updated README   │
                            │  with full index  │
                            └───────────────────┘
```

---

## Technology Stack

```
┌─────────────────────────────────────────┐
│          TECHNOLOGY STACK               │
├─────────────────────────────────────────┤
│                                         │
│  CORE MODEL                             │
│  └─ Llama-2-7B-Chat (4-bit quantized)   │
│                                         │
│  FRAMEWORKS                             │
│  ├─ PyTorch 2.5+                        │
│  ├─ Hugging Face Transformers 4.57+     │
│  └─ Accelerate (multi-GPU support)      │
│                                         │
│  SAFETY ENSEMBLE                        │
│  ├─ ToxicBERT (0.35 weight)             │
│  ├─ RoBERTa-hate (0.30 weight)          │
│  └─ ToxicChat-BERT (0.35 weight)        │
│                                         │
│  DATA PROCESSING                        │
│  ├─ Pandas 2.3+                         │
│  ├─ NumPy 2.1+                          │
│  └─ Scikit-learn 1.7+                   │
│                                         │
│  VISUALIZATION                          │
│  ├─ Matplotlib 3.10+                    │
│  ├─ Seaborn 0.13+                       │
│  └─ Pillow 11.0+ (PNG generation)       │
│                                         │
│  UTILITIES                              │
│  ├─ SciPy (statistical tests)            │
│  ├─ tqdm (progress bars)                │
│  ├─ GitPython (version control)         │
│  └─ Requests (API calls)                │
│                                         │
└─────────────────────────────────────────┘
```

---

## Next Immediate Steps (Priority Order)

```
┌──────────────────────────────────────────────────────┐
│  IMMEDIATE ACTION ITEMS (Estimated: 10-15 hours)     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1️⃣ PRIORITY 1: Paraphrase Generation (2-3 hrs)    │
│     Current: Synthetic distributions                │
│     Goal: Real T5/GPT-based paraphrasing            │
│     Impact: More realistic evaluation               │
│     File: semantic_smooth.ipynb (Cell 2)            │
│                                                      │
│  2️⃣ PRIORITY 2: Optimize Aggregation (1-2 hrs)    │
│     Current: Majority voting (fixed)                │
│     Goal: Test mean/max/weighted voting             │
│     Impact: 5-10% potential ASR improvement         │
│     File: semantic_smooth.ipynb (Cell 7)            │
│                                                      │
│  3️⃣ PRIORITY 3: Benign Testing (1-2 hrs)          │
│     Current: Only harmful prompts                   │
│     Goal: 500 benign prompts for FPR test           │
│     Impact: Ensure no over-blocking                 │
│     File: New notebook or semantic_smooth.ipynb     │
│                                                      │
│  4️⃣ PRIORITY 4: Latency Analysis (1-2 hrs)        │
│     Current: No timing data                         │
│     Goal: Measure inference time × K               │
│     Impact: Assess deployment feasibility           │
│     File: Add timing code to semantic_smooth.ipynb  │
│                                                      │
│  5️⃣ PRIORITY 5: Final Report (3-4 hrs)             │
│     Goal: Integrate all findings                    │
│     Impact: Publication-ready document              │
│     Output: Phase-2 Technical Report                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Key Questions for Planning

```
❓ CLARIFICATION ITEMS

1. Timeline: Target completion date?
   ├─ Academic (publication deadline)?
   └─ Production (deployment timeline)?

2. Resources: Compute availability?
   ├─ GPU time constraints?
   ├─ Multiple GPUs or single?
   └─ Cloud or local?

3. Scope: Benign prompts dataset?
   ├─ Do you have benign test set?
   ├─ Need to generate one?
   └─ How many (~500 adequate)?

4. Alternatives: Compare other defenses?
   ├─ Ensemble uncertainty?
   ├─ Adversarial training?
   └─ Hybrid approaches?

5. Deployment: End goal?
   ├─ Research paper
   ├─ Production system
   ├─ Both?
   └─ Limitations/constraints?
```

---

*Document Generated: February 17, 2026*  
*Version: Phase 2 Architecture Overview*  
*Status: Ready for Execution*
