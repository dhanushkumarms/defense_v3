from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from pathlib import Path

def get_llama_response(prompt: str, max_length: int = 100) -> str:
    """
    Get a response from Llama 2 model for a given prompt
    
    Args:
        prompt: Input text prompt
        max_length: Maximum length of generated response
        
    Returns:
        Generated response text
    """
    # Initialize model and tokenizer
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Encode prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True
        )
    
    # Decode and return response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    # Set up paths
    project_root = Path(__file__).parent.parent
    prompts_dir = project_root / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    
    input_file = prompts_dir / "input_prompt.txt"
    output_file = prompts_dir / "output_response.txt"
    
    # Read prompt from file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            test_prompt = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        exit(1)

    # Get response
    response = get_llama_response(test_prompt)
    
    # Write response to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Prompt:\n{test_prompt}\n\nResponse:\n{response}")
    
    print(f"Response written to {output_file}")
