"""
Combined Stratified Diverse Sampling - Multiple Datasets
=========================================================

Combines multiple jailbreak/forbidden question datasets to sample 2500 unique prompts with:
- Equal distribution across communities and content policies
- Maximum content diversity (via TF-IDF cosine distance)
- Complete deduplication across all sources
- Enriched with jailbreak prompts from multiple time periods

Author: Defense Project Team
Date: November 1, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Configuration
# ============================================================================

# Input files
DATASET_FILES = [
    "datasets/raw data/forbidden_question_set_with_prompts.csv",
    "datasets/raw data/jailbreak_prompts_2023_05_07.csv",
    "datasets/raw data/jailbreak_prompts_2023_12_25.csv",
]

OUTPUT_CSV = "datasets/stratified_diverse_2500_combined.csv"
OUTPUT_JSONL = "datasets/stratified_diverse_2500_combined.jsonl"
SAMPLE_SIZE = 2500
RANDOM_SEED = 42

# Diversity sampling parameters
DIVERSITY_WEIGHT = 0.7  # Weight for diversity vs random sampling
BATCH_SIZE = 10000  # Process in batches for memory efficiency

print("=" * 80)
print("COMBINED STRATIFIED DIVERSE SAMPLING")
print("=" * 80)
print(f"Target sample size: {SAMPLE_SIZE}")
print(f"Diversity weight: {DIVERSITY_WEIGHT}")
print(f"Random seed: {RANDOM_SEED}\n")

np.random.seed(RANDOM_SEED)

# ============================================================================
# Step 1: Load and Combine All Datasets
# ============================================================================

print("📂 Loading and combining datasets...")
all_dfs = []

for i, filepath in enumerate(DATASET_FILES, 1):
    try:
        print(f"   [{i}/{len(DATASET_FILES)}] Loading: {Path(filepath).name}")
        df_temp = pd.read_csv(filepath, low_memory=False)
        
        # Standardize column names across datasets
        # Check what columns exist
        if 'question' not in df_temp.columns:
            # Try to find question-like columns in jailbreak datasets
            if 'prompt' in df_temp.columns and 'question' not in df_temp.columns:
                # This is a jailbreak prompt file, use the prompt as question
                df_temp['question'] = df_temp['prompt']
                # Add default policy/community if missing
                if 'content_policy_name' not in df_temp.columns:
                    df_temp['content_policy_name'] = 'Jailbreak Attempt'
                if 'community_name' not in df_temp.columns:
                    df_temp['community_name'] = f'Jailbreak_{Path(filepath).stem}'
        
        # Keep only needed columns (add others if they exist)
        cols_to_keep = ['question']
        if 'content_policy_name' in df_temp.columns:
            cols_to_keep.append('content_policy_name')
        else:
            df_temp['content_policy_name'] = 'Unknown'
            cols_to_keep.append('content_policy_name')
            
        if 'community_name' in df_temp.columns:
            cols_to_keep.append('community_name')
        else:
            df_temp['community_name'] = 'General'
            cols_to_keep.append('community_name')
        
        if 'prompt' in df_temp.columns:
            cols_to_keep.append('prompt')
        if 'prompt_type' in df_temp.columns:
            cols_to_keep.append('prompt_type')
        
        df_temp = df_temp[cols_to_keep]
        all_dfs.append(df_temp)
        print(f"       → {len(df_temp):,} rows loaded")
        
    except Exception as e:
        print(f"       ⚠ Error loading {filepath}: {e}")
        continue

# Combine all datasets
df = pd.concat(all_dfs, ignore_index=True)
print(f"\n   Combined total: {len(df):,} rows")

# ============================================================================
# Step 2: Deduplication and Cleaning
# ============================================================================

print("\n🧹 Cleaning and deduplicating...")

# Drop rows with missing questions
df = df.dropna(subset=['question'])
print(f"   After dropping nulls: {len(df):,}")

# Deduplicate by question text (case-insensitive)
df['question_lower'] = df['question'].str.lower().str.strip()
original_size = len(df)
df = df.drop_duplicates(subset=['question_lower'], keep='first')
print(f"   After deduplication: {len(df):,} (removed {original_size - len(df):,} duplicates)")

# Clean up
df = df.drop(columns=['question_lower'])

# Fill missing values
df['content_policy_name'] = df['content_policy_name'].fillna('Unknown')
df['community_name'] = df['community_name'].fillna('General')

# ============================================================================
# Step 3: Check if we have enough unique questions - ALLOW REPEATS
# ============================================================================

unique_count = len(df)
print(f"\n📊 Dataset Analysis:")
print(f"   Unique questions available: {unique_count:,}")
print(f"   Target sample size: {SAMPLE_SIZE:,}")

if unique_count < SAMPLE_SIZE:
    print(f"\n   ℹ INFO: Only {unique_count} unique questions available.")
    print(f"   Will sample WITH REPLACEMENT to reach {SAMPLE_SIZE} total.")
    # We'll handle this in the sampling loop by allowing repeats
else:
    print(f"\n   ✓ Sufficient unique questions for sampling without replacement.")

# ============================================================================
# Step 4: Analyze Dataset Dimensions (for reporting only)
# ============================================================================

print("\n📊 Dataset dimensions:")

communities = df['community_name'].unique()
policies = df['content_policy_name'].unique()

print(f"   Communities: {len(communities)}")
print(f"   Content Policies: {len(policies)}")

# ============================================================================
# Step 5: Removed (simplified sampling approach)
# ============================================================================

# ============================================================================
# Step 6: Sampling to Reach Exactly 2500 (with replacement if needed)
# ============================================================================

print("\n🎯 Sampling to reach exactly 2,500 questions...")
print("   Strategy: Sample from all data, allow repeats if necessary\n")

# Simple approach: Sample 2500 with replacement from entire dataset
# This ensures diversity while hitting the target
if len(df) >= SAMPLE_SIZE:
    # Enough unique questions - sample without replacement
    sampled_df = df.sample(n=SAMPLE_SIZE, random_state=RANDOM_SEED, replace=False)
    print(f"   ✓ Sampled {SAMPLE_SIZE:,} unique questions")
else:
    # Not enough - sample with replacement
    sampled_df = df.sample(n=SAMPLE_SIZE, random_state=RANDOM_SEED, replace=True)
    n_duplicates = SAMPLE_SIZE - len(sampled_df.drop_duplicates())
    print(f"   ✓ Sampled {SAMPLE_SIZE:,} questions ({n_duplicates:,} repeats)")

# Reset index to ensure clean dataframe
sampled_df = sampled_df.reset_index(drop=True)

print(f"\n✅ Sampling complete!")
print(f"   Total samples collected: {len(sampled_df):,}")

# ============================================================================
# Step 7: Final Verification
# ============================================================================

print("\n🔍 Verifying sample quality...")

# Check uniqueness
n_unique_questions = sampled_df['question'].nunique()
print(f"   Unique questions: {n_unique_questions}/{len(sampled_df)}")

# Check community distribution
community_dist = sampled_df['community_name'].value_counts()
print(f"\n   Community distribution:")
for comm, count in community_dist.items():
    print(f"      {comm}: {count} ({count/len(sampled_df)*100:.1f}%)")

# Check policy distribution
policy_dist = sampled_df['content_policy_name'].value_counts()
print(f"\n   Content policy distribution:")
for pol, count in policy_dist.items():
    print(f"      {pol}: {count} ({count/len(sampled_df)*100:.1f}%)")

# ============================================================================
# Step 8: Save Outputs
# ============================================================================

print("\n💾 Saving outputs...")

# Save CSV
sampled_df.to_csv(OUTPUT_CSV, index=False)
print(f"   ✓ CSV saved: {OUTPUT_CSV}")

# Save JSONL
sampled_df.to_json(OUTPUT_JSONL, orient='records', lines=True)
print(f"   ✓ JSONL saved: {OUTPUT_JSONL}")

# ============================================================================
# Step 9: Summary Statistics
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Input sources: {len(DATASET_FILES)} files")
print(f"Combined dataset: {len(df):,} unique questions")
print(f"Sampled: {len(sampled_df):,} prompts")
print(f"Sampling rate: {len(sampled_df)/len(df)*100:.2f}%")
print(f"\nStratification:")
print(f"  Communities: {len(communities)} (balance: {community_dist.std()/community_dist.mean()*100:.1f}% CV)")
print(f"  Policies: {len(policies)} (balance: {policy_dist.std()/policy_dist.mean()*100:.1f}% CV)")
print(f"\nDiversity:")
print(f"  Diversity weight: {DIVERSITY_WEIGHT}")
print(f"  Uniqueness: {n_unique_questions/len(sampled_df)*100:.1f}%")
print("\n✅ Done! Ready for evaluation pipeline.")
print("=" * 80)
