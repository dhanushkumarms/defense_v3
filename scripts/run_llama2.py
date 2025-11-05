from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

model_name = "meta-llama/Llama-2-7b-hf"

print("Loading tokenizer and model...")

tokenizer = AutoTokenizer.from_pretrained(model_name)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

# Define GPU and CPU memory limits (RTX 3050 Ti: 4GB, CPU: remaining)
max_mem = {
    0: "4000MB",   # GPU 0
    "cpu": "12GB"  # CPU RAM for offloaded layers
}

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",   # automatically dispatch layers
    max_memory=max_mem
)

prompt = "Explain semantic smoothing in simple terms."
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

print("Generating response...")
outputs = model.generate(**inputs, max_new_tokens=150)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
