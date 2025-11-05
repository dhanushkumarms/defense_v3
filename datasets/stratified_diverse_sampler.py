"""
Stratified Diverse Sampling for Forbidden Questions Dataset
============================================================

Samples 2500 unique prompts with:
- Equal distribution across communities (domains)
- Equal distribution across content policies
- Maximum content diversity (via TF-IDF cosine distance)
- Complete deduplication of questions

Author: Defense Project Team
Date: November 1, 2025
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Configuration
# ============================================================================

INPUT_FILE = "datasets/raw data/forbidden_question_set_with_prompts.csv"
OUTPUT_CSV = "datasets/stratified_diverse_2500.csv"
OUTPUT_JSONL = "datasets/stratified_diverse_2500.jsonl"
SAMPLE_SIZE = 2500
RANDOM_SEED = 42

# Diversity sampling parameters
DIVERSITY_WEIGHT = 0.7  # Weight for diversity vs random sampling (0=random, 1=max diversity)
BATCH_SIZE = 10000  # Process in batches for memory efficiency

print("=" * 80)
print("STRATIFIED DIVERSE SAMPLING")
print("=" * 80)
print(f"Target sample size: {SAMPLE_SIZE}")
print(f"Diversity weight: {DIVERSITY_WEIGHT}")
print(f"Random seed: {RANDOM_SEED}\n")

np.random.seed(RANDOM_SEED)

# ============================================================================
# Step 1: Load and Deduplicate Dataset
# ============================================================================

print("📂 Loading dataset...")
df = pd.read_csv(INPUT_FILE, low_memory=False)
print(f"   Initial rows: {len(df):,}")

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

# ============================================================================
# Step 2: Stratification Setup
# ============================================================================

print("\n📊 Analyzing stratification dimensions...")

# Check available columns
if 'community_name' not in df.columns:
    print("   Warning: 'community_name' not found, using 'community_id'")
    community_col = 'community_id'
else:
    community_col = 'community_name'

if 'content_policy_name' not in df.columns:
    print("   Warning: 'content_policy_name' not found, using 'content_policy_id'")
    policy_col = 'content_policy_id'
else:
    policy_col = 'content_policy_name'

# Fill missing values
df[community_col] = df[community_col].fillna('Unknown')
df[policy_col] = df[policy_col].fillna('Unknown')

# Get unique communities and policies
communities = df[community_col].unique()
policies = df[policy_col].unique()

print(f"   Communities: {len(communities)}")
print(f"   Content Policies: {len(policies)}")

# Calculate target samples per stratum
n_communities = len(communities)
n_policies = len(policies)
total_strata = n_communities * n_policies

samples_per_stratum = SAMPLE_SIZE // total_strata
remainder = SAMPLE_SIZE % total_strata

print(f"\n   Total strata (community × policy): {total_strata}")
print(f"   Base samples per stratum: {samples_per_stratum}")
print(f"   Remainder to distribute: {remainder}")

# ============================================================================
# Step 3: Diversity-Aware Sampling Function
# ============================================================================

def diverse_sample(group_df, n_samples, diversity_weight=0.7):
    """
    Sample n_samples from group_df with diversity awareness.
    
    Uses TF-IDF + cosine distance to maximize content diversity:
    - Pure random: diversity_weight=0
    - Pure diversity: diversity_weight=1
    - Hybrid (recommended): diversity_weight=0.5-0.8
    """
    # If group is smaller than requested, take all
    if len(group_df) <= n_samples:
        return group_df
    
    # If diversity_weight is 0, pure random sampling
    if diversity_weight == 0:
        return group_df.sample(n=n_samples, random_state=RANDOM_SEED)
    
    # If group is small, just random sample
    if len(group_df) < 50:
        return group_df.sample(n=n_samples, random_state=RANDOM_SEED)
    
    # For large groups, use diversity sampling
    questions = group_df['question'].fillna('').tolist()
    
    # TF-IDF vectorization (limit features for speed)
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        stop_words='english',
        min_df=2
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(questions)
    except:
        # Fallback to random if TF-IDF fails
        return group_df.sample(n=n_samples, random_state=RANDOM_SEED)
    
    # Iterative diverse sampling
    selected_indices = []
    candidate_indices = list(range(len(group_df)))
    
    # Start with a random seed
    seed_idx = np.random.choice(candidate_indices)
    selected_indices.append(seed_idx)
    candidate_indices.remove(seed_idx)
    
    # Iteratively select most diverse samples
    while len(selected_indices) < n_samples and candidate_indices:
        # Compute similarity of candidates to already selected
        selected_vectors = tfidf_matrix[selected_indices]
        candidate_vectors = tfidf_matrix[candidate_indices]
        
        similarities = cosine_similarity(candidate_vectors, selected_vectors)
        
        # For each candidate, find max similarity to any selected item
        max_similarities = similarities.max(axis=1)
        
        # Blend diversity score with randomness
        # Lower similarity = more diverse = higher score
        diversity_scores = 1 - max_similarities
        random_scores = np.random.random(len(candidate_indices))
        
        combined_scores = (diversity_weight * diversity_scores + 
                          (1 - diversity_weight) * random_scores)
        
        # Select candidate with highest combined score
        best_idx_in_candidates = combined_scores.argmax()
        best_idx = candidate_indices[best_idx_in_candidates]
        
        selected_indices.append(best_idx)
        candidate_indices.remove(best_idx)
    
    return group_df.iloc[selected_indices]

# ============================================================================
# Step 4: Stratified Sampling with Diversity
# ============================================================================

print("\n🎯 Performing stratified diverse sampling...")
print("   This may take a few minutes for large datasets...\n")

sampled_groups = []
samples_collected = 0

for i, community in enumerate(communities):
    for j, policy in enumerate(policies):
        # Get stratum data
        mask = (df[community_col] == community) & (df[policy_col] == policy)
        stratum_df = df[mask].copy()
        
        if len(stratum_df) == 0:
            continue
        
        # Calculate samples for this stratum (distribute remainder to first strata)
        n_samples_stratum = samples_per_stratum
        if (i * len(policies) + j) < remainder:
            n_samples_stratum += 1
        
        # Sample with diversity
        sampled = diverse_sample(stratum_df, n_samples_stratum, DIVERSITY_WEIGHT)
        sampled_groups.append(sampled)
        samples_collected += len(sampled)
        
        # Progress update every 10 strata
        if (i * len(policies) + j + 1) % 10 == 0:
            progress = (i * len(policies) + j + 1) / total_strata * 100
            print(f"   Progress: {progress:.1f}% | Samples collected: {samples_collected}/{SAMPLE_SIZE}")

# Combine all samples
sampled_df = pd.concat(sampled_groups, ignore_index=True)

print(f"\n✅ Sampling complete!")
print(f"   Total samples collected: {len(sampled_df):,}")

# ============================================================================
# Step 5: Final Verification
# ============================================================================

print("\n🔍 Verifying sample quality...")

# Check uniqueness
n_unique_questions = sampled_df['question'].nunique()
print(f"   Unique questions: {n_unique_questions}/{len(sampled_df)}")

# Check community distribution
community_dist = sampled_df[community_col].value_counts()
print(f"\n   Community distribution:")
for comm, count in community_dist.items():
    print(f"      {comm}: {count} ({count/len(sampled_df)*100:.1f}%)")

# Check policy distribution
policy_dist = sampled_df[policy_col].value_counts()
print(f"\n   Content policy distribution:")
for pol, count in policy_dist.items():
    print(f"      {pol}: {count} ({count/len(sampled_df)*100:.1f}%)")

# ============================================================================
# Step 6: Save Outputs
# ============================================================================

print("\n💾 Saving outputs...")

# Save CSV
sampled_df.to_csv(OUTPUT_CSV, index=False)
print(f"   ✓ CSV saved: {OUTPUT_CSV}")

# Save JSONL
sampled_df.to_json(OUTPUT_JSONL, orient='records', lines=True)
print(f"   ✓ JSONL saved: {OUTPUT_JSONL}")

# ============================================================================
# Step 7: Summary Statistics
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Input dataset: {len(df):,} unique questions")
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
