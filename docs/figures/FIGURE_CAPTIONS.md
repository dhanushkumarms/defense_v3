# Figure Captions for Report

Use these captions below each figure in your Word document:

---

## Table 1: Dataset Distribution Across Content Policies and Prompt Variants

**Caption:**
Distribution of the 7,500 evaluation prompts across 13 content policies and three prompt variants (Direct, Simple Paraphrase, and Adversarial Paraphrase). The dataset maintains balanced coverage with 2,500 prompts per variant, ensuring systematic evaluation of the model's robustness across different attack vectors.

---

## Figure 1: Attack Success Rate by Prompt Variant

**Caption:**
Comparison of Attack Success Rates (ASR) across the three prompt variants. The baseline Direct prompts achieved a 5.6% ASR, demonstrating strong initial safety alignment. However, Simple Paraphrase attacks increased the ASR to 39.0%, while Adversarial Jailbreak prompts achieved a 56.2% success rate, revealing significant vulnerabilities in the model's semantic understanding of harmful intent.

---

## Figure 2: Per-Policy Attack Success Rate Analysis

**Caption:**
Attack Success Rates broken down by individual content policy categories across all three prompt variants. High-risk categories such as "Illegal Activity" and "Physical Harm" demonstrate significantly higher vulnerability to attacks, with ASRs exceeding 60% for adversarial prompts, while policies like "Misinformation" show relatively stronger defense mechanisms.

---

## Figure 3: True Attack Success Rate (True ASR) by Variant

**Caption:**
True Attack Success Rate measuring the percentage of prompts that were initially safe in their Direct form but became harmful when presented as Simple Paraphrase or Adversarial Jailbreak variants. The True ASR of 56.3% for adversarial attacks demonstrates that for prompts the model initially recognized as unsafe, adversarial wrapping has a better-than-even chance of bypassing the safety mechanisms.

---

## Figure 4: Safety Detector Ensemble Agreement Analysis

**Caption:**
Distribution of agreement levels among the three BERT-based safety classifiers in the evaluation ensemble. Higher agreement (unanimous or 2-out-of-3 consensus) is observed for Direct prompts, while Adversarial Jailbreak responses show increased disagreement among detectors, indicating the complexity and nuance of adversarially generated harmful content.

---

## Figure 5: Defense Rate Comparison Across Variants

**Caption:**
Model defense rates (percentage of successfully refused harmful requests) across the three prompt variants. The defense rate drops from 94.4% for Direct prompts to 61.0% for Simple Paraphrase and 43.8% for Adversarial Jailbreak attacks, quantifying the dramatic erosion of safety alignment under semantic manipulation.

---

## Figure 6: Cumulative Vulnerability Assessment

**Caption:**
Cumulative visualization of the model's vulnerability progression from baseline (Direct) to paraphrased and adversarial attack scenarios. The steep increase in Attack Success Rate demonstrates the critical "robustness gap" between the model's perceived safety (based on direct testing) and its actual resilience against real-world adversarial manipulation.

---

**Note:** Adjust figure numbers (Fig 1, Fig 2, etc.) to match your actual report structure. These captions provide context, interpretation, and key takeaways that help readers understand the significance of each visualization.
