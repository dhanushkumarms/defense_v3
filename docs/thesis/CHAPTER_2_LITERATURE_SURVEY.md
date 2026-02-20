# CHAPTER 2

## LITERATURE SURVEY

This chapter keeps it short and practical: what the community has learned about jailbreak attacks on LLMs, what works to defend, and what matters for our pipeline. Plain English, no fluff.

### 2.1 Jailbreaks and Adversarial Paraphrasing: The Core Problem

Modern LLMs are trained to be both helpful and harmless. But two failure modes repeatedly show up in studies:

- Competing objectives: the model tries too hard to follow instructions and forgets safety rules when the request is wrapped in a story or a role-play (Wei et al., 2023).
- Mismatched generalization: safety training sees specific phrases; paraphrased or unusual wording slips through even if the intent is the same (Wei et al., 2023; Li et al., 2023).

A key insight: small changes in surface form (paraphrase, suffix) can cause large changes in behavior. This explains why our baseline is strong on direct prompts but weak on paraphrased/jailbreak versions.

### 2.2 Attack Methods We Should Care About

- Human-crafted paraphrases and templates
  - DAN-style prompts, role-play, emotional appeals, self-referential tricks ("for research only"). Cheap and very effective.
- Automated suffix search (GCG)
  - Greedy Coordinate Gradient finds short adversarial suffixes that jailbreak many models and even transfer to closed models like GPT-4 (Zou et al., 2023).
- Evolutionary/LLM-as-attacker methods
  - AutoDAN and red-teaming with an LLM that iteratively probes safety (Perez & Ribeiro, 2022). Low human effort, high coverage.
- Multi-turn and context attacks
  - Slowly steer the model across turns to bypass one-shot filters; combine with tool-use or code blocks.

Takeaway for our project: even simple paraphrases already open a big hole; we don’t need fancy gradients to show real risk.

### 2.3 Defense Mechanisms: What Works, What Breaks

- Input and output filtering (guard models)
  - Pros: easy to deploy, modular. Cons: guard models can be jailbroken too; coverage lags novel attacks.
- Adversarial training
  - Fine-tune with paraphrased/jailbreak data. Pros: improves robustness to seen attacks. Cons: expensive, may overfit, can hurt helpfulness.
- Policy shaping (Constitutional AI / RLAIF)
  - Use rules and AI-feedback to align refusals. Good general behavior; still vulnerable to clever paraphrases.
- Semantic Smoothing (Robey et al., 2023)
  - Defend by checking multiple paraphrases of the same prompt and aggregating safety. If many variants are unsafe, reject the original. This targets intent, not keywords. Strong results against diverse attacks, minor helpfulness drop.
- Defense-in-depth
  - Rate limiting, policy-specific thresholds, human-in-the-loop on borderline cases, logging for continuous improvement.

Why this matters to us: our pipeline already generates variants. That makes Semantic Smoothing very natural to add and test.

### 2.4 Datasets and Evaluation Protocols

- Public prompts and jailbreak sets
  - Community red-team lists and curated policy sets (e.g., 2023–2024 jailbreak and regular prompt collections like the ones in our `datasets/raw data/`).
- Variant-based testing
  - For each base prompt: direct, simple paraphrase, and adversarial paraphrase. Compute Attack Success Rate (ASR) per variant and true ASR (penetrations where the direct form was safe).
- Safety measurement
  - Ensemble toxicity/harm classifiers (e.g., ToxicBERT, RoBERTa-hate, ToxicChat-BERT) with calibrated thresholds. Track category-wise performance (13 policy areas in our project) to spot weak spots.

This protocol lets us report honest robustness gaps, not just cherry-picked safety refusals.

### 2.5 What We Learn for Our Project (Actionable)

- Expect large robustness gaps: paraphrasing can multiply failures by 10–50× vs. direct prompts.
- Prefer intent-level defenses: add Semantic Smoothing to our pipeline (we already have paraphrase generation and scoring).
- Tune per-policy thresholds: vulnerability varies by category; a single global threshold is rarely optimal.
- Keep a small adversarial training loop: fine-tune (or prompt-tune) on the worst paraphrases we find to harden the model.
- Evaluate transfer and multi-turn: test a few universal suffixes and simple multi-turn setups to avoid a one-shot bias.

### 2.6 Key References (short list)

- Wei et al. (2023). Jailbroken: How Does LLM Safety Training Fail?
- Li et al. (2023). On the Robustness of Language Models to Adversarial Paraphrasing.
- Zou et al. (2023). Universal and Transferable Adversarial Attacks on Aligned LMs (GCG).
- Robey et al. (2023). Defending LLMs Against Jailbreak Attacks via Semantic Smoothing.
- Perez & Ribeiro (2022). Red Teaming Language Models with Language Models.
- Carlini et al. (2023). Are Aligned Neural Networks Adversarially Aligned?
- Touvron et al. (2023). Llama 2: Open Foundation and Fine-Tuned Chat Models.
- Hanu & Unitary (2020). Detoxify: Toxic Comment Classification.

—
This survey is intentionally concise and tied to our setup: focus on paraphrase/jailbreak attacks, evaluate with ASR and true ASR, and prioritize Semantic Smoothing as the next practical defense to implement and test.
