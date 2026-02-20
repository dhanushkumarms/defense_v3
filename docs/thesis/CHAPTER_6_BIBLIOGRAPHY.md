# CHAPTER 6: ANNOTATED BIBLIOGRAPHY

This chapter provides an annotated list of the key papers, models, and software that our project is built upon. For a college project like ours, standing on the shoulders of giants is the only way to get things done, so it's important to give credit where it's due. Each reference includes a short note explaining how it fits into our work.

---

### Core LLM, Attack, and Defense Papers

This section covers the foundational research that defines our project's landscape, from the core language model we investigated to the attack strategies we employed and the defenses we plan to build.

1.  **Touvron, H., et al. (2023). *Llama 2: Open Foundation and Fine-Tuned Chat Models*. arXiv:2307.09288.**
    > **Our Take:** This is the main paper for Llama 2, the hero (and sometimes villain) of our story. We specifically used the Llama-2-7B-Chat-hf model, and this paper explains its architecture, training, and most importantly, its initial safety alignment. Understanding this was crucial for analyzing why it fails.

2.  **Zou, A., et al. (2023). *Universal and Transferable Adversarial Attacks on Aligned Language Models*. arXiv:2307.15043.**
    > **Our Take:** This paper introduced the Greedy Coordinate Gradient (GCG) attack, which is the state-of-the-art for generating powerful adversarial suffixes. While we used a simpler dataset of jailbreaks for our experiment, the ideas in this paper represent the "final boss" of adversarial attacks that future defenses must defeat.

3.  **Robey, A., et al. (2023). *SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks*. arXiv:2310.03684.**
    > **Our Take:** This is the key paper for our proposed future work. It introduces Semantic Smoothing (which they call SmoothLLM), a defense that involves creating multiple noisy copies of a prompt and checking for a consensus in safety decisions. Our entire "Phase 2" plan is based on implementing and testing this defense.

4.  **Li, J., et al. (2023). *On the Robustness of Language Models to Adversarial Paraphrasing*. ACL 2023.**
    > **Our Take:** This paper was the direct inspiration for the `Simple Paraphrase` variant in our dataset. It highlights that even simple semantic paraphrasing can be a highly effective attack vector, a finding that our results strongly confirmed (ASR of 39.0%).

5.  **Wei, A., et al. (2023). *Jailbroken: How Does LLM Safety Training Fail?*. NeurIPS 2023.**
    > **Our Take:** This work provides a great analysis of *why* safety training fails, categorizing different types of jailbreaks. It helped us frame our results and understand that the failures we observed are part of a well-documented pattern in the field.

6.  **Chao, P., et al. (2023). *Jailbreaking Black Box Large Language Models in Twenty Queries*. arXiv:2310.08419.**
    > **Our Take:** This paper explores how to jailbreak models with limited query access. While we had full white-box access, this paper is important because it shows that these vulnerabilities are not just academic; they can be exploited in real-world, black-box scenarios.

---

### Safety Evaluation and Detector Models

To judge whether an attack was successful, we needed a reliable "safety umpire." We built an ensemble of three different BERT-based models for this. These are the papers and resources behind our detectors.

7.  **Hanu, L., & Unitary team. (2020). *Detoxify: Toxic Comment Classification with Transformers*. [GitHub](https://github.com/unitaryai/detoxify).**
    > **Our Take:** This is the library behind our first detector, `unitary/toxic-bert`. It's a classic, widely-used model for general toxicity detection and formed the baseline of our safety ensemble.

8.  **Vidgen, B., et al. (2021). *Learning from the Worst: Dynamically Generated Datasets to Improve Online Hate Detection*. ACL 2021.**
    > **Our Take:** This paper describes the process used to create the dataset for our second detector, `facebook/roberta-hate-speech-dynabench-r4-target`. This model is specifically good at detecting hate speech, which made it a valuable specialist in our ensemble.

9.  **Zheng, L., et al. (2023). *ToxicChat: Uncovering Hidden Challenges of Toxicity Detection in Real-World User-AI Conversations*. EMNLP 2023.**
    > **Our Take:** This paper is behind our third and most modern detector, `lmsys/toxic-chat-bert-base-uncased`. It's trained on data from real user-chatbot interactions, making it particularly relevant for evaluating the conversational responses from Llama 2.

---

### Core Technologies and Libraries

This project wouldn't have been possible without the open-source ecosystem. These are the tools that did the heavy lifting.

10. **Dettmers, T., et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314.**
    > **Our Take:** This paper is pure magic. It introduced the 4-bit NormalFloat (NF4) quantization method that allowed us to run a 7-billion parameter model on a single 4GB consumer GPU. Without QLoRA and the `bitsandbytes` library that implements it, this project would have been impossible on our hardware.

11. **Wolf, T., et al. (2020). *Transformers: State-of-the-Art Natural Language Processing*. EMNLP 2020.**
    > **Our Take:** The Hugging Face `transformers` library is the backbone of our entire pipeline. It's how we loaded the Llama 2 model, tokenized inputs, and ran inference. It's the industry standard for a reason.

12. **Paszke, A., et al. (2019). *PyTorch: An Imperative Style, High-Performance Deep Learning Library*. NeurIPS 2019.**
    > **Our Take:** All our models run on PyTorch. It's the framework that powers the `transformers` library and our custom evaluation scripts. Its flexibility and strong community support make it the default choice for deep learning research.

13. **Devlin, J., et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL-HLT 2019.**
    > **Our Take:** The original BERT paper. All three of our safety detector models are based on BERT or its variants (like RoBERTa), making this one of the most important foundational papers for our evaluation methodology.


