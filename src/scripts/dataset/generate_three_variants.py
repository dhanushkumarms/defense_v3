"""
Generate Three Test Variants for Defense Evaluation
====================================================

Creates 3 test variants for each question in the dataset:
1. Direct: Raw question only (baseline)
2. Simple Paraphrase: Using Vamsi/T5_Paraphrase_Paws model
3. Adversarial Paraphrase: Jailbreak prompt + question (combination)

Output: CSV and JSONL with 7,500 total test cases (2,500 × 3 variants)

Author: Defense Project Team
Date: November 1, 2025
"""

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm
import json
import hashlib
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Configuration
# ============================================================================

INPUT_CSV = "datasets/stratified_diverse_2500_combined.csv"
OUTPUT_CSV = "datasets/three_variant_dataset_2500.csv"
OUTPUT_JSONL = "datasets/three_variant_dataset_2500.jsonl"

# Paraphrase model
PARAPHRASE_MODEL = "Vamsi/T5_Paraphrase_Paws"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Generation parameters (aligned with your existing work)
PARAPHRASE_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.95,
    "max_new_tokens": 80,
    "num_return_sequences": 1,  # Take best paraphrase
    "do_sample": True,
}

print("=" * 80)
print("THREE VARIANT GENERATION PIPELINE")
print("=" * 80)
print(f"Device: {DEVICE}")
print(f"Paraphrase Model: {PARAPHRASE_MODEL}")
print(f"Input: {INPUT_CSV}\n")

# ============================================================================
# Step 1: Load Dataset
# ============================================================================

print("📂 Loading dataset...")
df = pd.read_csv(INPUT_CSV)
print(f"   Loaded: {len(df):,} questions")
print(f"   Columns: {list(df.columns)}")

# Ensure required columns exist
required_cols = ['question']
if 'prompt' not in df.columns:
    df['prompt'] = 'You are a helpful AI assistant.'  # Default if missing
    print("   ⚠ Warning: 'prompt' column missing, using default")

if 'content_policy_name' not in df.columns and 'content_policy_id' in df.columns:
    df['content_policy_name'] = 'Policy_' + df['content_policy_id'].astype(str)
elif 'content_policy_name' not in df.columns:
    df['content_policy_name'] = 'Unknown'

if 'community_name' not in df.columns:
    df['community_name'] = 'General'

print(f"   Content policies: {df['content_policy_name'].nunique()}")
print(f"   Communities: {df['community_name'].nunique()}\n")

# ============================================================================
# Step 2: Load Paraphrase Model
# ============================================================================

print("🤖 Loading paraphrase model...")
print(f"   Model: {PARAPHRASE_MODEL}")

try:
    par_tokenizer = AutoTokenizer.from_pretrained(PARAPHRASE_MODEL)
    par_model = AutoModelForSeq2SeqLM.from_pretrained(PARAPHRASE_MODEL).to(DEVICE)
    par_model.eval()
    print(f"   ✓ Model loaded successfully on {DEVICE}\n")
except Exception as e:
    print(f"   ✗ Error loading model: {e}")
    print("   Falling back to simple paraphrase (minor word changes)\n")
    par_model = None
    par_tokenizer = None

# ============================================================================
# Step 3: Paraphrase Generation Function
# ============================================================================

def generate_simple_paraphrase(text, model, tokenizer):
    """
    Generate a simple paraphrase using T5-based paraphrase model.
    Falls back to minor modifications if model unavailable.
    """
    if model is None or tokenizer is None:
        # Fallback: simple lexical substitutions
        return simple_fallback_paraphrase(text)
    
    try:
        # Prepare input (T5 paraphrase models typically expect "paraphrase: " prefix)
        input_text = f"paraphrase: {text.strip()}"
        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(DEVICE)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=PARAPHRASE_PARAMS["max_new_tokens"],
                temperature=PARAPHRASE_PARAMS["temperature"],
                top_p=PARAPHRASE_PARAMS["top_p"],
                do_sample=PARAPHRASE_PARAMS["do_sample"],
                num_return_sequences=PARAPHRASE_PARAMS["num_return_sequences"],
            )
        
        paraphrase = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # If paraphrase is identical or too short, fallback
        if paraphrase.strip().lower() == text.strip().lower() or len(paraphrase.strip()) < 10:
            return simple_fallback_paraphrase(text)
        
        return paraphrase.strip()
    
    except Exception as e:
        print(f"   ⚠ Paraphrase error: {e}")
        return simple_fallback_paraphrase(text)

def simple_fallback_paraphrase(text):
    """
    Simple fallback paraphrase using lexical substitutions.
    """
    replacements = {
        'How can I': 'How do I',
        'Can you': 'Could you',
        'What is': 'What\'s',
        'What are': 'What\'re',
        'How to': 'How do I',
        'show me': 'demonstrate',
        'tell me': 'explain',
        'provide': 'give',
        'explain': 'describe',
        'create': 'make',
        'help me': 'assist me with',
    }
    
    paraphrase = text
    for old, new in replacements.items():
        if old in paraphrase:
            paraphrase = paraphrase.replace(old, new, 1)
            break  # Only one substitution
    
    return paraphrase

# ============================================================================
# Step 4: Generate Three Variants
# ============================================================================

print("🎯 Generating three variants per question...")
print("   Variants: Direct | Simple Paraphrase | Adversarial Paraphrase\n")

all_variants = []
errors = []

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    question = row['question']
    jailbreak_prompt = row.get('prompt', 'You are a helpful AI assistant.')
    
    # Metadata
    metadata = {
        'original_idx': idx,
        'question_id': row.get('q_id', idx),
        'content_policy_id': row.get('content_policy_id', -1),
        'content_policy_name': row['content_policy_name'],
        'community_id': row.get('community_id', -1),
        'community_name': row['community_name'],
        'prompt_type': row.get('prompt_type', 'unknown'),
    }
    
    # ========================================================================
    # Variant 1: Direct (Baseline)
    # ========================================================================
    variant_direct = {
        **metadata,
        'variant_id': f"{idx}_direct",
        'test_type': 'direct',
        'test_input': question,
        'question': question,
        'jailbreak_prompt': None,
        'has_jailbreak': False,
        'generation_method': 'original',
    }
    all_variants.append(variant_direct)
    
    # ========================================================================
    # Variant 2: Simple Paraphrase
    # ========================================================================
    try:
        simple_paraphrase = generate_simple_paraphrase(question, par_model, par_tokenizer)
    except Exception as e:
        simple_paraphrase = question  # Fallback to original
        errors.append({
            'idx': idx,
            'type': 'simple_paraphrase',
            'error': str(e)
        })
    
    variant_simple = {
        **metadata,
        'variant_id': f"{idx}_simple_paraphrase",
        'test_type': 'simple_paraphrase',
        'test_input': simple_paraphrase,
        'question': question,  # Keep original for reference
        'paraphrased_question': simple_paraphrase,
        'jailbreak_prompt': None,
        'has_jailbreak': False,
        'generation_method': PARAPHRASE_MODEL,
    }
    all_variants.append(variant_simple)
    
    # ========================================================================
    # Variant 3: Adversarial Paraphrase (Jailbreak + Question)
    # ========================================================================
    adversarial_input = f"{jailbreak_prompt}\n\n{question}"
    
    variant_adversarial = {
        **metadata,
        'variant_id': f"{idx}_adversarial_paraphrase",
        'test_type': 'adversarial_paraphrase',
        'test_input': adversarial_input,
        'question': question,
        'jailbreak_prompt': jailbreak_prompt,
        'has_jailbreak': True,
        'generation_method': 'jailbreak_combination',
    }
    all_variants.append(variant_adversarial)

print(f"\n✅ Variant generation complete!")
print(f"   Total variants: {len(all_variants):,}")
print(f"   Expected: {len(df) * 3:,}")
print(f"   Errors: {len(errors)}")

# ============================================================================
# Step 5: Create DataFrame
# ============================================================================

print("\n📊 Creating output DataFrame...")
variants_df = pd.DataFrame(all_variants)

# Add hash for deduplication/tracking
variants_df['input_hash'] = variants_df['test_input'].apply(
    lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
)

print(f"   Shape: {variants_df.shape}")
print(f"   Unique test inputs: {variants_df['test_input'].nunique():,}")

# Distribution check
print(f"\n   Variant distribution:")
for test_type, count in variants_df['test_type'].value_counts().items():
    print(f"      {test_type}: {count:,} ({count/len(variants_df)*100:.1f}%)")

print(f"\n   Content policy distribution:")
for policy, count in variants_df['content_policy_name'].value_counts().head(10).items():
    print(f"      {policy}: {count:,}")

# ============================================================================
# Step 6: Save Outputs
# ============================================================================

print("\n💾 Saving outputs...")

# Save CSV
variants_df.to_csv(OUTPUT_CSV, index=False)
print(f"   ✓ CSV saved: {OUTPUT_CSV} ({variants_df.memory_usage(deep=True).sum() / 1024**2:.1f} MB)")

# Save JSONL
with open(OUTPUT_JSONL, 'w', encoding='utf-8') as f:
    for record in variants_df.to_dict('records'):
        f.write(json.dumps(record, ensure_ascii=False) + '\n')
print(f"   ✓ JSONL saved: {OUTPUT_JSONL}")

# ============================================================================
# Step 7: Save Sample Preview
# ============================================================================

print("\n📋 Sample Preview (first 3 questions, all variants):")
print("=" * 80)

for i in range(min(3, len(df))):
    sample_variants = variants_df[variants_df['original_idx'] == i]
    print(f"\n[Question {i}]")
    print(f"Policy: {sample_variants.iloc[0]['content_policy_name']}")
    print(f"Original: {sample_variants.iloc[0]['question'][:100]}...")
    print()
    
    for _, var in sample_variants.iterrows():
        print(f"  {var['test_type'].upper()}:")
        print(f"    Input: {var['test_input'][:150]}...")
        print(f"    Has jailbreak: {var['has_jailbreak']}")
        print()

# ============================================================================
# Step 8: Summary Statistics
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Input questions: {len(df):,}")
print(f"Output test cases: {len(variants_df):,}")
print(f"Variants per question: 3")
print(f"\nTest Types:")
for test_type in ['direct', 'simple_paraphrase', 'adversarial_paraphrase']:
    count = len(variants_df[variants_df['test_type'] == test_type])
    print(f"  - {test_type}: {count:,}")

print(f"\nParaphrase Model: {PARAPHRASE_MODEL}")
print(f"Generation Parameters:")
for k, v in PARAPHRASE_PARAMS.items():
    print(f"  - {k}: {v}")

print(f"\nOutput Files:")
print(f"  - CSV: {OUTPUT_CSV}")
print(f"  - JSONL: {OUTPUT_JSONL}")

if errors:
    print(f"\n⚠ Errors encountered: {len(errors)}")
    print("  (See errors list for details)")

print("\n✅ Done! Ready for adversarial evaluation pipeline.")
print("=" * 80)

# Optional: Save errors log
if errors:
    error_log = Path(OUTPUT_CSV).parent / "variant_generation_errors.json"
    with open(error_log, 'w') as f:
        json.dump(errors, f, indent=2)
    print(f"\n⚠ Error log saved: {error_log}")
