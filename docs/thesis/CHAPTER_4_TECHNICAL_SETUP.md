# CHAPTER 4: TECHNICAL SPECIFICATIONS AND ENVIRONMENT

A core tenet of reproducible research is the transparent documentation of the environment in which the experiments were conducted. This chapter provides a detailed specification of the hardware and software stack used for this project. Our setup was intentionally designed around consumer-grade components to demonstrate that impactful AI safety research is feasible without access to large-scale, enterprise-level computing infrastructure.

---

### 4.1 Hardware Requirements

The entire experimental pipeline, from data processing and model inference to safety evaluation, was executed on a single laptop. The specifications of this machine are detailed below.

| **Component** | **Specification** | **Role in Project** |
| :--- | :--- | :--- |
| **CPU** | **12th Gen Intel Core i7** | Responsible for all data pre-processing, script execution, and orchestration. Managed data loading with pandas and file I/O operations. |
| **GPU** | **NVIDIA GeForce RTX 3050 Ti (Laptop)** | The primary compute device for all neural network inference. Ran the Llama-2-7B model and the three BERT-based safety classifiers. |
| **VRAM** | **4 GB** | This limited memory was a critical constraint, necessitating the use of 4-bit quantization to load and run the 7-billion parameter model. |
| **RAM** | **16 GB** | Held the Python environment, datasets, and model parameters that were offloaded from or staged for the GPU. |

---

### 4.2 Software Requirements

The project was built on a foundation of open-source software. All dependencies were meticulously managed to ensure stability and reproducibility.

| **Component** | **Specification** | **Role in Project** |
| :--- | :--- | :--- |
| **Operating System** | **Windows 11** | The host environment for all development and execution. |
| **Terminal** | **Windows PowerShell** | Used for executing all scripts and managing the project environment. |
| **Programming Language** | **Python 3.10** | The core language used for all scripting, data processing, and model interaction. |

#### 4.2.1 Core Libraries and Frameworks

The following table details the key Python libraries and frameworks that formed the backbone of our experimental pipeline. The versions listed are exact, ensuring that the environment can be perfectly replicated.

| **Library** | **Version** | **Role and Justification** |
| :--- | :--- | :--- |
| ***torch*** | ***2.5.1+cu121*** | The fundamental deep learning framework. Used for all tensor operations and for running the models on the GPU. |
| ***transformers*** | ***4.57.0*** | The high-level Hugging Face library for downloading, configuring, and running all transformer models (Llama 2 and the safety classifiers). |
| ***bitsandbytes*** | ***0.48.1*** | ***Critical Library.*** Provided the 4-bit NormalFloat (NF4) quantization capability, which compressed the Llama 2 model to fit within the 4GB VRAM constraint. |
| ***accelerate*** | ***1.10.1*** | A Hugging Face library used to streamline the process of running models on mixed-precision or memory-constrained hardware. |
| ***pandas*** | ***2.3.3*** | The primary tool for data manipulation. Used to load, clean, and iterate through the prompt datasets stored in CSV files. |
| ***numpy*** | ***2.1.2*** | The fundamental package for numerical operations. Used for handling arrays and performing calculations on the safety scores. |
| ***datasets*** | ***4.1.1*** | A Hugging Face library used for efficient data loading and processing, especially when working with large datasets. |
| ***safetensors*** | ***0.6.2*** | A secure and fast format for storing model weights. Used by default by transformers for loading models. |
| ***sentencepiece*** | ***0.2.1*** | The tokenizer used by the Llama 2 model to convert text prompts into numerical tokens for the model to process. |
| ***tqdm*** | ***4.67.1*** | A utility library for creating progress bars in the terminal, providing essential real-time feedback during long-running inference jobs. |
| ***PyYAML*** | ***6.0.3*** | Used for parsing configuration files, if any, to manage experimental parameters in a clean and readable format. |
| ***requests*** | ***2.32.5*** | The standard library for making HTTP requests, used by Hugging Face libraries to download models and other assets from the web. |

This comprehensive specification provides a clear and reproducible blueprint of the technical environment, ensuring that our results can be validated and our methods can be built upon by other researchers in the field.
