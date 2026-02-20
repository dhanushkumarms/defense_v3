import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def analyze_llm_results(json_file_path):
    """
    Analyzes LLM experiment results from a JSON file, aggregates data,
    prints a summary table, and generates Matplotlib plots.

    Args:
        json_file_path (str): The path to the JSON file containing the results.
    """
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'. Check file format.")
        return

    # Prepare data for DataFrame
    processed_data = []
    for prompt_id, prompt_data in data.items():
        domain = prompt_data.get('domain', 'Unknown')
        for variant_name, metrics in prompt_data['variants'].items():
            processed_data.append({
                'prompt_id': prompt_id,
                'domain': domain,
                'variant': variant_name.capitalize(), # Capitalize for consistent display (Original, Simple, Adversarial)
                'runtime': metrics.get('runtime_s', 0.0),
                'length': metrics.get('response_length', 0),
                'detector_score': metrics.get('detector_score', 0.0),
                'unsafe_label': metrics.get('unsafe_label', False)
            })

    df = pd.DataFrame(processed_data)

    # --- Aggregation ---
    aggregated_df = df.groupby(['domain', 'variant']).agg(
        mean_runtime=('runtime', 'mean'),
        mean_length=('length', 'mean'),
        mean_detector_score=('detector_score', 'mean')
    ).reset_index()

    # --- Print Tabulated Results ---
    print("### Overall Results Aggregated by Prompt Domain and Variant 📊")
    print("\nThis table shows the average (mean) values for runtime, response length, and detector score,")
    print("grouped first by the prompt's domain and then by its variant.")
    print("\n" + "="*80) # Separator for readability
    print(aggregated_df.to_string(index=False))
    print("="*80 + "\n") # Separator for readability

    # --- Matplotlib Visualizations ---

    # Ensure consistent order for variants in plots
    variant_order = ['Original', 'Simple', 'Adversarial']
    aggregated_df['variant'] = pd.Categorical(aggregated_df['variant'], categories=variant_order, ordered=True)
    aggregated_df = aggregated_df.sort_values(['domain', 'variant'])

    # Get unique domains for plotting
    domains = aggregated_df['domain'].unique()
    num_domains = len(domains)
    colors = plt.cm.get_cmap('Paired', num_domains * len(variant_order)) # More distinct colors

    # Plot 1: Mean Detector Score
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    width = 0.25 # width of bars

    x = np.arange(len(domains)) # the label locations for domains

    for i, variant in enumerate(variant_order):
        variant_data = aggregated_df[aggregated_df['variant'] == variant]
        # Align bars for each domain group
        bar_positions = [j + i * width - width for j in x]
        bars = ax1.bar(bar_positions, variant_data['mean_detector_score'], width, label=variant)
        # Add labels on bars
        for bar in bars:
            yval = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 2), ha='center', va='bottom', fontsize=8)


    ax1.set_xlabel('Prompt Domain')
    ax1.set_ylabel('Mean Detector Score')
    ax1.set_title('Mean Detector Score by Domain and Variant')
    ax1.set_xticks(x)
    ax1.set_xticklabels(domains, rotation=45, ha='right')
    ax1.legend(title='Variant')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save figure instead of showing it
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()
    image_path = os.path.join(script_dir, "mean_detector_score.png")
    fig1.savefig(image_path, dpi=300, bbox_inches='tight')
    plt.close(fig1)
    print(f"Saved 'Mean Detector Score' plot to: {image_path}")