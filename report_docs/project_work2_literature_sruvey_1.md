**19Z820 \- PROJECT WORK II**

**First Review \- Literature Survey**

#### **1.1 Introduction**

Large Language Models (LLMs) have demonstrated strong capabilities in natural language understanding and generation. Despite these advancements, recent research has shown that such models remain vulnerable to jailbreak attacks, where carefully constructed prompts are able to bypass built-in safety controls and trigger restricted or harmful responses. This vulnerability becomes more pronounced under semantic adversarial settings, in which the malicious intent of a prompt is preserved while its surface wording is modified through paraphrasing or restructuring.

In Project Work I, experimental evaluation using the Meta-LLaMA-2-7B model revealed high Attack Success Rates (ASR) when subjected to paraphrased and adversarial prompts, highlighting the limitations of existing alignment mechanisms. These findings emphasize the need for defense strategies that function at inference time without requiring model retraining or full parameter access. Accordingly, this literature survey examines a set of recent research contributions, including a primary defense methodology and supporting IEEE and Elsevier journal studies, to analyze existing approaches, identify their limitations, and establish the basis for implementing an effective semantic defense framework in Project Work II.

**1.2 Motivation**

The primary driver for this research is the critical gap between **model intelligence** and **model safety**. As established in Project Work I, LLMs are surprisingly brittle; they can refuse a direct harmful request but comply with the exact same request if it is hidden within a "role-play" scenario or phrased using complex synonyms.

The motivation lies in creating a "Semantic Guardrail"—a defense mechanism that is as fluid and adaptable as the attacks themselves. By focusing on **Semantic Smoothing**, we move away from rigid, keyword-based filters toward a defense that understands the underlying intent of a prompt. This transition is essential for building trustworthy AI systems that can be safely deployed in sensitive environments without the constant fear of jailbreak-induced reputational or physical harm.

**1.3 Problem Statement**

Modern Large Language Models (LLMs) exhibit significant vulnerability to semantic adversarial attacks, where harmful intent is preserved while prompt phrasing is altered to bypass existing safety mechanisms.

This project aims to address the following challenges:

* **Defense Implementation:** Developing semantic-level defense mechanisms capable of detecting and mitigating adversarial paraphrasing and jailbreak-based attacks that evade traditional filters.  
* **Empirical Validation:** Evaluating the effectiveness of the proposed defense in reducing Attack Success Rates (ASR) against the specific semantic vulnerabilities identified in Phase-I.  
* **Utility Balance:** Ensuring model robustness does not come at the cost of utility, specifically by maintaining low false refusal rates (correctly identifying benign prompts) and managing the computational overhead associated with inference-time smoothing.

***How can a robust, semantic-level defense mechanism be developed to neutralize adversarial paraphrasing and jailbreak attacks—specifically addressing the vulnerabilities identified in Phase-I—while maintaining a balance between safety alignment, model utility, and computational efficiency?***

#### **1.4 Ji et al. (2024): Defending Large Language Models Against Jailbreak Attacks via Semantic Smoothing**

1. **Paper Overview:** This paper introduces **SEMANTICSMOOTH**, a randomized smoothing-based inference-time defense that aggregates predictions across multiple semantically transformed versions of an input prompt. It achieves state-of-the-art robustness against prominent jailbreak attacks (GCG, PAIR, AutoDAN) while maintaining strong performance on instruction-following benchmarks like InstructionFollowing and AlpacaEval.  
2. **Problem Addressed:** Aligned LLMs remain vulnerable to both token-level (e.g., gradient-based GCG) and prompt-level (e.g., persuasive PAIR, AutoDAN) jailbreaks. Existing defenses either introduce unfavorable trade-offs in nominal performance, rely on heuristics vulnerable to adaptive attacks, or fail against semantic manipulations that preserve malicious intent through paraphrasing.  
3. **Methodology:** The framework generates multiple meaning-preserving transformations (e.g., spell check, synonym replacement, paraphrasing, summarization, translation, verb tense change, format reorganization) of the input prompt using LLM-based prompting (no external models required). Responses from the target LLM on each variant are aggregated via majority voting, facilitated by a judge LLM (e.g., GPT-3.5-turbo) that assesses refusal. A learned policy network optionally selects optimal transformations per input using policy gradients to maximize rejection of adversarial prompts and accuracy on benign ones.  
     
     
     
     
     
     
   **Figure 1: Illustration of SEMANTICSMOOTH**  
4. **Strengths:**  
   * Model-agnostic and broadly applicable to semantic transformations.  
   * Superior robustness-utility trade-off: Reduces ASR to near-zero on tested attacks across Vicuna, LLaMA-2, and GPT-3.5.  
   * Provides interpretability insights into GCG suffixes by deciphering them through transformations.  
   * Outperforms baselines like SmoothLLM and paraphrase defenses.  
5. **Limitations:**  
   * Computational overhead from multiple queries and transformations.  
   * Dependency on transformation quality and target LLM capabilities.  
   * Limited scope for highly adaptive or multi-turn attacks; potential semantic drift in complex prompts.  
6. **Relevance:** This serves as the primary baseline for our implementation. We will adopt its transformation suite and aggregation strategy to evaluate against Phase-1's paraphrase/jailbreak datasets, measuring ASR reductions and exploring policy enhancements for Review II.

**1.5 Li & Fung (2025): Security Concerns for Large Language Models: A Survey**

1. **Paper Overview**: Published in the Journal of Information Security and Applications (Elsevier, Vol. 95, 104284), this survey offers a broad overview of emerging security vulnerabilities in LLMs, categorizing threats across inference-time attacks, training-phase risks, malicious misuse, and autonomous agent-specific concerns.  
2. **Problem Addressed**: Despite alignment techniques (SFT/RLHF), LLMs face persistent threats from prompt injection/jailbreaking, adversarial perturbations, data poisoning, misuse (e.g., disinformation, phishing), and emergent agent risks (e.g., goal misalignment, scheming, self-preservation). Defenses often remain bypassable or introduce trade-offs, lacking multi-layered analysis for real-world applications.  
3. **Methodology**: The work reviews and categorizes threats from 2022–2025 studies, including prompt manipulation (jailbreaks), input perturbations, misuse cases, and agent behaviors. It analyzes existing defenses (e.g., filters, alignment reinforcement, monitoring), their limitations, and open challenges, with examples from models like GPT-4, Claude, and Vicuna.  
4. **Strengths**:  
   * Holistic coverage spanning inference, training, misuse, and agent risks, with balanced discussion of practical deployment issues (e.g., latency, false positives).  
   * Quantifies gaps (e.g., many defenses fail semantic attacks) and emphasizes multi-layered strategies.  
   * Includes recent industrial/academic examples and agent-specific threats (e.g., covert misalignment), relevant to evolving LLM ecosystems.  
   * Highlights ethical and interdisciplinary needs for safer deployment.  
5. **Limitations**:  
   * Broad scope limits in-depth technical critique of individual defense mechanisms.  
   * Relies on existing literature without new empirical experiments or unified benchmarks.  
   * Some agent risks remain speculative or under-explored in non-autonomous settings.

**Relevance:**  Informs our decision to test Semantic Smoothing on multi-turn datasets to ensure it remains effective over long-duration interactions.

**1.6 Liao et al. (2025): Attack and Defense Techniques in Large Language Models: A Survey and New Perspectives**

1. **Paper Overview**: This comprehensive survey, published in Neural Networks (Elsevier) systematically reviews and classifies attack and defense techniques targeting Large Language Models (LLMs), while proposing new perspectives on emerging trends, evaluation challenges, and future directions in LLM security.  
2. **Problem Addressed**: The rapid proliferation of LLM vulnerabilities—including adversarial prompt attacks, optimized jailbreaks (e.g., GCG variants), model theft, and application-layer exploits—lacks a unified taxonomy and standardized evaluation. Existing defenses often fail against adaptive semantic manipulations or introduce high overhead, and the literature remains fragmented across prompt, inference, and application threats.  
3. **Methodology**: The authors categorize attacks by type (adversarial prompt attacks, optimized suffix attacks, model theft, application-specific exploits) and defenses into detection-based (e.g., toxicity scoring, input monitoring) and protection-based (e.g., prompt modification, security-aware prompting). They review mechanisms, implications, benchmarks (e.g., HarmBench, AdvGLUE), and limitations of prior work (2022–2025), highlighting gaps in adaptive scalability, explainability, and real-world deployment.  
4. **Strengths**:  
   * Provides a detailed, up-to-date taxonomy covering ontology-level and application-level threats, with emphasis on semantic prompt attacks and jailbreaks.  
   * Identifies key challenges like balancing robustness with usability, resource constraints, and the need for standardized metrics.  
   * Offers actionable insights and new perspectives (e.g., interdisciplinary approaches, ethical considerations) for advancing resilient LLM defenses.  
   * Broad coverage of evolving attacks (e.g., multi-turn, tool-use) and defenses, serving as a reference for comparative analysis.  
5. **Limitations**:  
   * As a survey, it does not introduce novel empirical methods or implementations.  
   * Coverage limited to pre-2025/early-2025 works, potentially missing very recent agentic or multimodal developments.  
   * Qualitative breadth over deep quantitative unification or codebases for reproducibility.

**Relevance :** Provides the theoretical framework for our "Defense Taxonomy" and helps categorize the adversarial prompts used in Phase-I.

**1.7 Feng et al. (2025): JailbreakLens: Visual Analysis of Jailbreak Attacks Against Large Language Models**

1. **Paper Overview**: Published in IEEE Transactions on Visualization and Computer Graphics (Vol. 31, No. 10, pp. 8668–8682; arXiv:2404.08793), JailbreakLens is an interactive visual analytics system designed to explore, assess, and interpret jailbreak attacks on LLMs, enabling multi-level analysis of prompt effectiveness and components.  
2. **Problem Addressed**: Jailbreak prompts are complex and opaque, making manual analysis difficult; researchers lack intuitive tools to evaluate performance, dissect keyword/suffix contributions, identify patterns, and refine attacks/defenses against models like GPT-series or LLaMA.  
3. **Methodology**: The system supports automatic jailbreak assessment, multi-level prompt analysis (e.g., component heatmaps, keyword importance, performance metrics), and interactive refinement. It includes visualization of prompt characteristics, ASR correlations, and hypothesis testing to uncover attack mechanisms (e.g., suffix circuits).  
4. **Strengths**:  
   * Enhances interpretability of jailbreak mechanisms through visual exploration and quantitative insights.  
   * Accelerates analysis and refinement (e.g., 10x faster pattern identification than manual methods).  
   * Bridges qualitative understanding with metrics, supporting defense design and prompt verification.  
   * Facilitates multi-level insights (global patterns to token-level contributions) for diverse attacks.  
5. **Limitations**:  
   * Primarily an analysis and visualization tool, not a direct defense mechanism.  
   * Requires integration with target models and may incur overhead for large-scale prompt sets.  
   * Scalability constraints for real-time or very high-volume (10k+) evaluations.  
   * Insights may be visualization-biased without complementary quantitative validation.

**Relevance:** We will adopt this component-level analysis to qualitatively explain why certain transformations in our implementation succeed or fail.

**1.8 Tang et al. (2025): Security of LLM-Based Agents Regarding Attacks, Defenses, and Applications: A Comprehensive Survey**

1. **Paper Overview**: Published in Information Fusion (Elsevier, Vol. 127, 103941), this survey focuses on security in LLM-based agents, providing a systematic taxonomy of attacks, defenses, and dual-use applications (offensive and defensive) in cyber and other domains.  
2. **Problem Addressed**: LLM agents expand attack surfaces (e.g., tool misuse, multi-step reasoning exploits, memory poisoning) beyond static models; prior surveys lack unified evaluation criteria and overlook security-enabling applications (e.g., red-teaming vs. attack facilitation). Adaptive/multi-turn threats remain under-addressed.  
3. **Methodology**: The authors develop a component-centric taxonomy (prompt, tool, memory, reasoning) for attacks and defenses; propose unified evaluation criteria (e.g., ASR, robustness scores); review 150+ works (2023–2025); and discuss applications ranging from cyber offense enablement to defensive enhancements.  
4. **Strengths**:  
   * Unified, comparable evaluation framework improves analysis of agent-specific threats.  
   * Comprehensive coverage of attacks (e.g., 90%+ ASR in tool-jailbreaks) and defenses under consistent criteria.  
   * Explores dual-use applications, highlighting LLM agents' potential for both harm and security strengthening.  
   * Addresses gaps in prior work, including scalable defenses and real-world agent deployment.  
5. **Limitations**:  
   * Primary focus on agents limits direct applicability to non-agentic/static LLMs.  
   * High-level discussion of applications; some defenses remain emerging and untested at scale.  
   * Rapid field evolution (post-2025) may outpace coverage in certain areas.

**Relevance:**  Highlights that semantic defenses must be robust enough to handle instructions entering through external data sources.

**2\. Project Workflow:** The workflow evaluates original and adversarial prompts on Meta-LLaMA-2 to measure baseline vulnerability, then applies Semantic Smoothing as a defense. The results are finally compared to assess improvement in robustness and safety.

**Figure 2\. Project Workflow**

**3\. Conclusion**

The reviewed studies collectively highlight that jailbreak vulnerabilities in large language models primarily arise from semantic manipulation of prompts. While existing alignment methods remain insufficient, recent research emphasizes inference-time defenses as a practical and effective solution. These findings provide strong motivation for adopting semantic smoothing–based defense mechanisms in Project Work II.

**References:**

\[1\] Ji, J., et al. "Defending Large Language Models Against Jailbreak Attacks via Semantic Smoothing." arXiv:2402.16192, 2024\.

\[2\] Liao, Z., et al. "Attack and Defense Techniques in Large Language Models: A Survey and New Perspectives." Neural Networks (Elsevier), Vol. 196, 108388, 2025\.

\[3\] Li, M.Q., & Fung, B.C.M. "Security Concerns for Large Language Models: A Survey." Journal of Information Security and Applications (Elsevier), Vol. 95, 104284, 2025\.

\[4\] Feng, Y., et al. "JailbreakLens: Visual Analysis of Jailbreak Attacks Against Large Language Models." IEEE Transactions on Visualization and Computer Graphics, 31(10):8668-8682, 2025\.

\[5\] Tang, Y., et al. "Security of LLM-Based Agents Regarding Attacks, Defenses, and Applications: A Comprehensive Survey." Information Fusion (Elsevier), Vol. 127, 103941, 2025\.

\[6\] Yi, S., et al. "Jailbreak Attacks and Defenses Against Large Language Models: A Survey." arXiv:2407.04295, 2024\.

\[7\] Zhang, L., et al. "Exploiting Task-Level Vulnerabilities: An Automatic Jailbreak Attack and Defense Benchmarking for LLMs." Proceedings of the 34th USENIX Security Symposium, 2025\.

\[8\] Robey, A., et al. "SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks." arXiv:2310.03684, 2023/2025.

\[9\] Wang, X., et al. "SELFDEFEND: LLMs Can Defend Themselves against Jailbreaking in a Practical Manner." Proceedings of the 34th USENIX Conference on Security Symposium, 2025\.

\[10\] Chao, P., et al. "PAIR: Jailbreaking Black-Box LLMs in Twenty Queries." arXiv:2310.08419 (updated 2025), 2023/2025.

\[11\] Gong, X., et al. "PaPillon: Efficient and Stealthy Fuzz Testing-Powered Jailbreaks for LLMs." Proceedings of the 34th USENIX Security Symposium, 2025\.

\[12\] Zou, A., et al. "Universal and Transferable Adversarial Attacks on Aligned Language Models." arXiv:2307.15043, 2023/2025.

\[13\] Lin, R., et al. "Understanding and Enhancing the Transferability of Jailbreaking Attacks." Published as a conference paper at ICLR 2025\.

\[14\] Liu, Y., et al. "AutoDAN: Generating Stealthy Jailbreak Prompts." arXiv:2310.04451 (extended 2025), 2023/2025.

\[15\] Ye, R., et al. "Emerging Safety Attack and Defense in Federated Instruction Tuning of Large Language Models." Published as a conference paper at ICLR 2025\.

\[16\] Mehrotra, N., et al. "Tree of Attacks: Jailbreaking Black-Box LLMs Automatically." arXiv:2312.02119 (2025 variants), 2023/2025.

