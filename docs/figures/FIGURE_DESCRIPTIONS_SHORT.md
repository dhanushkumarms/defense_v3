# One-Line Figure Descriptions for Report

Copy these descriptions to place under each figure in your Word document:

---

**Table 1: Dataset Distribution by Content Policy and Prompt Variant**  
*File: `outputs/evaluation_results/table_dataset_distribution.png`*

Distribution of 7,500 evaluation prompts across 13 content policies and three prompt variants showing balanced allocation with Jailbreak Attempt category containing the majority of test cases.

---

**Figure 1: Attack Success Rate Comparison**  
*File: `outputs/evaluation_results/fig_1_asr_comparison.png`*

Bar chart comparing Attack Success Rate (ASR) and Defense Rate across three variants, demonstrating 10.1× increase in ASR from Direct (5.6%) to Adversarial Jailbreak (56.2%) with corresponding defense degradation.

---

**Figure 2: Per-Policy Attack Success Rate**  
*File: `outputs/evaluation_results/fig_2_per_policy_asr.png`*

Violin plot and histogram showing toxicity score distributions across attack variants, with adversarial jailbreaks producing bimodal distribution around 0.5 threshold indicating sophisticated evasion patterns.

---

**Figure 3: True Attack Success Rate Analysis**  
*File: `outputs/evaluation_results/fig_3_true_asr.png`*

Heatmap matrix displaying vulnerability levels across 12 content policies, with Financial Advice (71.3%), Privacy Violence (62.9%), and Economic Harm (61.0%) showing highest adversarial ASR.

---

**Figure 4: Safety Detector Agreement**  
*File: `outputs/evaluation_results/fig_4_safety_agreement.png`*

Paired comparison outcomes showing 56.3% True ASR where 1,330 initially safe prompts were successfully penetrated by adversarial jailbreak variants, with only 2.5% adversarially strengthened cases.

---

**Figure 5: Defense Rate by Variant**  
*File: `outputs/evaluation_results/fig_5_defense_rate.png`*

Bar chart illustrating detector ensemble agreement distribution, showing dramatic shift from 94% split consensus for Direct prompts to 50% unanimous disagreement for Adversarial attacks.

---

**Figure 6: Cumulative Vulnerability**  
*File: `outputs/evaluation_results/fig_6_cumulative_vulnerability.png`*

Comprehensive evaluation dashboard summarizing key findings including 56.2% adversarial ASR, 0.549 mean toxicity score, top 5 vulnerable policies, and 7.0× relative effectiveness of simple paraphrase attacks.

---

---
