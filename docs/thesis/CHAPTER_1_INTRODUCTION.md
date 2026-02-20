# CHAPTER 1

## INTRODUCTION

### 1.1 Problem Identification

Large Language Models (LLMs) like Llama-2 are trained to be helpful and safe. In normal cases, they refuse clearly harmful questions. But in real life, attackers don’t always ask directly. They rephrase, wrap the request in a story, or use clever jailbreak prompts. The meaning stays harmful, but the words look harmless.

This gap between “surface form” (the exact words) and “intent” (what the user really wants) is the main weakness. Today’s safety training often catches known phrases, but it struggles when the same idea is expressed differently. As a result, models that look safe in simple tests can fail badly under adversarial paraphrasing. That failure is not just academic—it can lead to harmful outputs in the wild.

In short: LLM safety is brittle under paraphrasing. Even small changes in wording can bypass guardrails. Closing this robustness gap is the core problem we tackle in this project.

### 1.2 Problem Statement

Our project studies how easily a safety-aligned LLM can be tricked by paraphrased and jailbreak prompts, and how to measure and reduce that risk.

Concretely, we:

- Build a test suite of harmful questions (2,500 base prompts), and create three variants for each: direct, simple paraphrase, and adversarial paraphrase (jailbreak style). Total ≈ 7,500 tests.
- Run the target model (Llama-2-7B-Chat, 4-bit quantized for efficiency) and collect responses for all variants.
- Score each response with an ensemble of safety classifiers (ToxicBERT, RoBERTa-hate, ToxicChat-BERT) and label them as Safe or Harmful.
- Compute Attack Success Rate (ASR) for each variant and analyze how paraphrasing changes outcomes compared to direct questions.

Baseline results show a clear pattern: direct harmful questions have a very low success rate, but paraphrased and jailbreak versions dramatically increase ASR. This quantifies the brittleness of current safety training and motivates stronger, intent-aware defenses.

### 1.3 Motivation of the Work

As students and researchers, we want AI that is both useful and safe. Right now, models can be “book smart” about safety—good at textbook examples—but still fail when the same harmful intent is hidden in friendly language. That’s risky for real users and real platforms.

Our motivation is twofold:

1. Practical safety: Show, with data, how big the gap is between direct and paraphrased attacks, so teams don’t get a false sense of security from easy tests.
2. Better defenses: Move beyond keyword or pattern matching and focus on the meaning. We plan to explore Semantic Smoothing—a defense that checks multiple paraphrases of the same prompt. If several versions tend to produce unsafe outputs, the system rejects the original. This aligns the defense with intent, not just wording.

We believe this approach balances simplicity and effectiveness. It’s easy to add on top of existing systems and directly targets the failure mode we observe.

### Report Organization

- Chapter 1 introduces the problem, states our goals, and explains why this work matters.
- Chapter 2 reviews related work: jailbreak attacks, why safety training fails, and existing defenses.
- Chapter 3 explains our methodology: dataset construction (2,500 × 3 variants), model setup, and the safety evaluation pipeline.
- Chapter 4 presents results and analysis: baseline ASR, the jump under paraphrasing, policy-wise trends, and what these numbers mean.
- Chapter 5 concludes the work and outlines future directions, including implementing and evaluating Semantic Smoothing at scale.

—
Written in simple, clear English to reflect how a young research scholar from Tamil Nadu would explain the work: straightforward, honest about limitations, and focused on impact.
