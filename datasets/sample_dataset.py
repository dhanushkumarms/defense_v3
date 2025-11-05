import pandas as pd
import os

def sample_dataset(csv_file_path, output_file_path=None, samples_per_group=1):
    """
    Performs stratified random sampling from the dataset.
    Ensures at least one row from each unique combination of:
    - community_name
    - prompt_type
    - content_policy_name
    
    Args:
        csv_file_path (str): Path to the input CSV file
        output_file_path (str): Path to save the sampled CSV (optional)
        samples_per_group (int): Number of samples per unique combination
    
    Returns:
        pd.DataFrame: Sampled dataframe
    """
    try:
        # Load the dataset
        df = pd.read_csv(csv_file_path)
        print(f"Loaded dataset with {len(df)} rows")
        
        # Check if required columns exist
        required_cols = ['community_name', 'prompt_type', 'content_policy_name']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Warning: Missing columns: {missing_cols}")
            print(f"Available columns: {df.columns.tolist()}")
            return None
        
        # Group by the three columns and sample
        sampled_df = df.groupby(
            ['community_name', 'prompt_type', 'content_policy_name'],
            group_keys=False
        ).apply(lambda x: x.sample(min(len(x), samples_per_group), random_state=42))
        
        # Reset index for clean output
        sampled_df = sampled_df.reset_index(drop=True)
        
        # Print statistics
        print(f"\n=== Sampling Statistics ===")
        print(f"Original dataset size: {len(df)}")
        print(f"Sampled dataset size: {len(sampled_df)}")
        print(f"Number of unique groups: {len(sampled_df.groupby(required_cols))}")
        
        print("\n=== Distribution by Group ===")
        group_counts = sampled_df.groupby(required_cols).size().reset_index(name='count')
        print(group_counts.to_string(index=False))
        
        # Save to file if output path provided
        if output_file_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_file_path = os.path.join(script_dir, "sampled_dataset.csv")
        
        sampled_df.to_csv(output_file_path, index=False)
        print(f"\n✓ Saved sampled dataset to: {output_file_path}")
        
        return sampled_df
        
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    # Try to find the CSV file in common locations
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(script_dir, "raw data", "forbidden_question_set_with_prompts.csv"),
        os.path.join(script_dir, "forbidden_question_set_with_prompts.csv"),
        r"c:\Users\tenys\defense_project\datasets\raw data\forbidden_question_set_with_prompts.csv",
        r"c:\Users\tenys\defense_project\forbidden_question_set_with_prompts.csv",
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if csv_path is None:
        print("Error: Could not find 'forbidden_question_set_with_prompts.csv'")
        print("\nSearched in:")
        for path in possible_paths:
            print(f"  - {path}")
        print("\nPlease check if the file exists and update the path in the script.")
        print("\nAvailable CSV files in 'raw data' directory:")
        raw_data_dir = os.path.join(script_dir, "raw data")
        if os.path.exists(raw_data_dir):
            for file in os.listdir(raw_data_dir):
                if file.endswith('.csv'):
                    print(f"  - {file}")
    else:
        print(f"Found CSV at: {csv_path}\n")
        # Perform sampling (1 row per unique combination by default)
        sampled_data = sample_dataset(csv_path, samples_per_group=1)
