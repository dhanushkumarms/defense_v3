# CHAPTER 4: RESULTS AND ANALYSIS

This chapter presents the empirical results from our evaluation of the Llama-2-7B-Chat model. We analyze the data generated from our 7,500-prompt test suite to quantify the model's safety performance against direct, paraphrased, and adversarial attacks. The analysis will break down the Attack Success Rate (ASR) by variant and content policy, examine the behavior of our safety detectors, and discuss the broader implications of our findings for LLM security.

All data and figures referenced in this chapter are derived from the `ATTACK3` evaluation run, with artifacts located in `models/ATTACK3_RESULTS.md` and `outputs/evaluation_results/`.

---

### 4.1 Summary of Experimental Setup

Before diving into the results, let's briefly recap the experimental context:

*   **Model:** `meta-llama/Llama-2-7b-chat-hf` (quantized to 4-bit NF4).
*   **Test Suite:** 2,500 base harmful prompts, each with three variants (`Direct`, `Simple Paraphrase`, `Adversarial Jailbreak`), totaling 7,500 tests.
*   **Safety Scoring:** Each model response was evaluated by a weighted ensemble of three toxicity/safety classifiers. A response is deemed `Harmful` if the composite score is ≥ 0.5.
*   **Primary Metric:** Attack Success Rate (ASR), the percentage of prompts that result in a harmful response.

---

### 4.2 Overall Attack Success Rates: A Stark Contrast

The most striking result of our experiment is the dramatic difference in ASR across the three prompt variants. While Llama-2 demonstrates strong defenses against direct attacks, its robustness collapses when faced with even simple semantic modifications.

| Variant | Harmful Responses | Total Prompts | Attack Success Rate (ASR) | Defense Rate |
| :--- | :--- | :--- | :--- | :--- |
| **Direct** | 139 | 2,500 | **5.6%** | 94.4% |
| **Simple Paraphrase** | 974 | 2,500 | **39.0%** | 61.0% |
| **Adversarial Jailbreak** | 1,406 | 2,500 | **56.2%** | 43.8% |

**Key Observations:**

*   **Baseline Safety is High:** With a defense rate of 94.4% against direct harmful prompts, the model's baseline safety alignment is effective against straightforward attacks.
*   **Paraphrasing Erodes Safety:** A simple rewording of the prompt causes the ASR to jump from 5.6% to 39.0%, a nearly **7-fold increase**. This demonstrates that the model's safety is brittle and overly reliant on recognizing specific keywords or sentence structures.
*   **Jailbreaks Overwhelm Defenses:** Adversarial jailbreak prompts are even more effective, pushing the ASR to 56.2%—a **10-fold increase** over the baseline. This means that by wrapping a harmful request in a clever template, an attacker has a better-than-even chance of bypassing the model's safety filters.

These results, which are statistically significant (χ² test, p < 0.001), clearly indicate that the model's safety mechanisms are not generalizing to the underlying *intent* of the prompt, but are instead over-fitted to the superficial form of the training data.

---

### 4.3 True Attack Success Rate: Measuring the Impact of Evasion

To better isolate the effectiveness of the adversarial techniques, we calculated the **True ASR**. This metric focuses only on the prompts that the model *successfully defended* in their `Direct` form and measures how many of them were compromised by the adversarial variant.

Out of the 2,361 prompts that were successfully defended in the `Direct` variant, 1,330 were penetrated by the `Adversarial Jailbreak` variant.

**True ASR = 1,330 / (1,031 + 1,330) = 56.3%**

This is a critical finding: for a prompt that Llama-2 already knows how to refuse, a simple jailbreak template has a **56.3% chance of making it fail**. This confirms that the attacks are not just finding pre-existing weaknesses; they are actively creating them by exploiting the model's flawed safety reasoning.

---

### 4.4 Vulnerability by Content Policy: Not All Topics Are Equal

Our analysis revealed that the model's robustness varies significantly across the 13 content policies. Some topics are far more vulnerable to adversarial attacks than others.

**Most Vulnerable Policies (by Adversarial ASR):**

*   **Illegal Activity:** 68.2% ASR
*   **Physical Harm:** 64.7% ASR
*   **Malware:** 61.4% ASR

**Most Robust Policies (by Adversarial ASR):**

*   **Misinformation:** <35% ASR
*   **Privacy Violations:** <35% ASR

This variance suggests that the RLHF alignment process may have had uneven exposure to different types of harmful content. High-risk, explicit categories like "Physical Harm" appear to be more susceptible to semantic manipulation than more nuanced topics like "Misinformation."

---

### 4.5 Analysis of Toxicity Score Distributions

The distribution of toxicity scores provides further insight into the model's behavior.

*   **Direct Prompts:** The scores are heavily skewed towards zero (mean score: 0.235), indicating that the model is confidently refusing harmful requests.
*   **Simple Paraphrase Prompts:** The distribution shifts noticeably to the right (mean score: 0.434), with many responses falling into a "borderline" category.
*   **Adversarial Jailbreak Prompts:** The distribution becomes bimodal (mean score: 0.549), with a large cluster of responses clearly crossing the 0.5 "harmful" threshold.

This shows that adversarial prompts don't just slightly nudge the model; they fundamentally change its response regime, pushing it from a state of confident refusal to one of confused compliance.

---

### 4.6 Implications for LLM Defense

Our findings have several critical implications for the development of more robust LLM defenses:

1.  **Surface-Level Defenses are Insufficient:** The failure of the model to handle paraphrases proves that defenses based on keyword filtering or simple pattern matching are inadequate. Defenses must operate at the semantic level to understand the user's true intent.
2.  **The Need for Adversarial Training Data:** The model's brittleness is likely a result of being trained on a non-adversarial dataset. To build robust models, the safety alignment process must include a diverse range of paraphrased and jailbreak-style prompts.
3.  **Ensemble Detectors Add Value:** The fact that our detector agreement decreased with stronger attacks indicates that borderline cases are common. Using an ensemble of safety monitors can provide a more reliable signal, and disagreement within the ensemble can itself be used as a risk flag.
4.  **Semantic Smoothing as a Natural Next Step:** Our methodology, which already generates multiple semantic variants for each prompt, is a perfect precursor to implementing a defense like **SemanticSmooth**. By analyzing the responses across a cluster of paraphrases, we can make a more robust safety determination than by looking at a single prompt in isolation.

In conclusion, our results paint a clear picture: while modern LLMs have made great strides in baseline safety, they remain critically vulnerable to semantic attacks. This "robustness gap" is the key challenge that the next generation of AI safety research must address.