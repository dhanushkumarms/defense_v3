"""
Plot dataset distribution by policy and prompt variant.

- Reads a combined dataset (~7,500 rows; 2,500 prompts × 3 variants).
- Prints counts per policy and per variant to the console.
- Saves a PNG figure visualizing counts per policy for the three variants.

By default, searches the `datasets/` folder for a likely combined file, preferring:
- three_variant_dataset_2500.csv / .jsonl
- stratified_diverse_2500_combined.csv / .jsonl
- stratified_diverse_2500.csv / .jsonl

Usage (PowerShell):
  python scripts/plot_dataset_distribution.py
  python scripts/plot_dataset_distribution.py --input "datasets/three_variant_dataset_2500.csv" --output "outputs/evaluation_results/fig_dataset_policy_variant_distribution.png"

Dependencies: pandas, pillow (both are in requirements.txt).
"""

from __future__ import annotations
import argparse
import os
import sys
from typing import Optional, Tuple, List

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# ---------------------------
# Helpers to locate the dataset
# ---------------------------
LIKELY_FILES = [
    "three_variant_dataset_2500.csv",
    "three_variant_dataset_2500.jsonl",
    "stratified_diverse_2500_combined.csv",
    "stratified_diverse_2500_combined.jsonl",
    "stratified_diverse_2500.csv",
    "stratified_diverse_2500.jsonl",
]

POLICY_CANDIDATES = [
    "content_policy_name", "policy", "category", "content_policy", "policy_category", "label"
]
VARIANT_CANDIDATES = [
    "test_type", "variant", "prompt_variant", "attack_variant", "prompt_type", "type",
    "variant_type", "variant_name", "variant_idx", "variant_index", "variant_id"
]

VARIANT_NORMALIZATION = {
    # common strings → canonical labels
    "direct": "Direct",
    "baseline": "Direct",
    "simple": "Simple Paraphrase",
    "paraphrase": "Simple Paraphrase",
    "simple paraphrase": "Simple Paraphrase",
    "adversarial": "Adversarial Paraphrase",
    "jailbreak": "Adversarial Paraphrase",
    "adversarial paraphrase": "Adversarial Paraphrase",
}

NUMERIC_VARIANT_MAP = {
    0: "Direct",
    1: "Simple Paraphrase",
    2: "Adversarial Paraphrase",
}

COLORS = {
    "Direct": (52, 119, 235),              # blue
    "Simple Paraphrase": (247, 166, 15),   # orange
    "Adversarial Paraphrase": (232, 78, 60), # red
}


def find_default_input(base_dir: str) -> Optional[str]:
    ds_dir = os.path.join(base_dir, "datasets")
    if not os.path.isdir(ds_dir):
        return None
    for name in LIKELY_FILES:
        candidate = os.path.join(ds_dir, name)
        if os.path.isfile(candidate):
            return candidate
    # Fall back to first CSV/JSONL in datasets/
    for fname in os.listdir(ds_dir):
        if fname.lower().endswith((".csv", ".jsonl")):
            return os.path.join(ds_dir, fname)
    return None


def read_dataset(path: str) -> pd.DataFrame:
    if path.lower().endswith(".csv"):
        return pd.read_csv(path)
    if path.lower().endswith(".jsonl") or path.lower().endswith(".json"):
        return pd.read_json(path, lines=True)
    raise ValueError(f"Unsupported file type: {path}")


def pick_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    cols_lower = {c.lower(): c for c in df.columns}
    for key in candidates:
        if key in cols_lower:
            return cols_lower[key]
    return None


def normalize_variant(series: pd.Series) -> pd.Series:
    # Try numeric mapping first
    if pd.api.types.is_numeric_dtype(series):
        return series.map(NUMERIC_VARIANT_MAP).fillna(series.astype(str))

    # Otherwise normalize strings
    def norm(x):
        if pd.isna(x):
            return x
        s = str(x).strip().lower()
        # match common tokens
        for k, v in VARIANT_NORMALIZATION.items():
            if k in s:
                return v
        return s.title()

    return series.map(norm)


def summarize_counts(df: pd.DataFrame, policy_col: str, variant_col: str) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    df = df.copy()
    df[variant_col] = normalize_variant(df[variant_col])

    # Keep only three canonical variants if they exist; otherwise keep what we have
    canonical = ["Direct", "Simple Paraphrase", "Adversarial Paraphrase"]
    if set(canonical).issubset(set(df[variant_col].unique())):
        df = df[df[variant_col].isin(canonical)]
    
    by_policy_variant = (
        df.groupby([policy_col, variant_col])
          .size()
          .rename("count")
          .reset_index()
    )
    totals_by_policy = by_policy_variant.groupby(policy_col)["count"].sum().sort_values(ascending=False)
    totals_by_variant = by_policy_variant.groupby(variant_col)["count"].sum().sort_values(ascending=False)
    return by_policy_variant, totals_by_policy, totals_by_variant


# ---------------------------
# Drawing functions (Pillow)
# ---------------------------

def draw_grouped_bar_chart(
    by_policy_variant: pd.DataFrame,
    totals_by_policy: pd.Series,
    output_path: str,
    title: str = "Dataset Distribution by Policy and Variant",
    width: int = 1400,
    left_margin: int = 300,
    right_margin: int = 80,
    top_margin: int = 100,
    bottom_margin: int = 100,
    bar_height: int = 16,
    bar_gap_within: int = 8,  # gap between variant bars inside a policy group
    group_gap: int = 14,      # gap between policy groups
):
    policies = list(totals_by_policy.index)
    variants = ["Direct", "Simple Paraphrase", "Adversarial Paraphrase"]

    # Pivot to have variant columns
    pivot = by_policy_variant.pivot(index=by_policy_variant.columns[0], columns=by_policy_variant.columns[1], values="count").fillna(0)
    pivot = pivot.reindex(index=policies, columns=variants, fill_value=0)

    # Compute scaling
    max_count = int(pivot.values.max()) if pivot.values.size > 0 else 1
    plot_width = width - left_margin - right_margin

    # Height calculation
    group_height = 3 * bar_height + 2 * bar_gap_within
    height = top_margin + bottom_margin + len(policies) * (group_height + group_gap)

    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Title
    draw.text((left_margin, 20), title, fill=(0, 0, 0), font=font)

    # Legend
    legend_x = width - right_margin - 280
    legend_y = 20
    for i, v in enumerate(variants):
        color = COLORS.get(v, (100, 100, 100))
        box = [legend_x, legend_y + i * 20, legend_x + 14, legend_y + i * 20 + 14]
        draw.rectangle(box, fill=color)
        draw.text((legend_x + 20, legend_y + i * 20), v, fill=(0, 0, 0), font=font)

    # Draw axes (just baseline line)
    axis_y = top_margin - 10
    draw.line([(left_margin, axis_y), (width - right_margin, axis_y)], fill=(200, 200, 200), width=1)

    # Bars per policy
    y = top_margin
    for policy in policies:
        # Policy label
        draw.text((10, y + group_height // 2 - 6), str(policy), fill=(0, 0, 0), font=font)

        # Draw each variant bar
        for idx, v in enumerate(variants):
            count = int(pivot.loc[policy, v]) if v in pivot.columns else 0
            # scale to plot width
            w = 0 if max_count == 0 else int((count / max_count) * plot_width)
            bar_y1 = y + idx * (bar_height + bar_gap_within)
            bar_y2 = bar_y1 + bar_height
            x1 = left_margin
            x2 = left_margin + max(w, 1)  # ensure visible for count>0
            color = COLORS.get(v, (100, 100, 100))
            draw.rectangle([x1, bar_y1, x2, bar_y2], fill=color)
            # count label at end of bar
            draw.text((x2 + 6, bar_y1), str(count), fill=(60, 60, 60), font=font)

        # total per policy on the right
        total = int(totals_by_policy.loc[policy])
        draw.text((width - right_margin - 60, y + group_height // 2 - 6), str(total), fill=(0, 0, 0), font=font)

        y += group_height + group_gap

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)


# ---------------------------
# Main
# ---------------------------

def main():
    parser = argparse.ArgumentParser(description="Summarize dataset by policy and variant and render image.")
    parser.add_argument("--input", type=str, default=None, help="Path to dataset file (CSV or JSONL). Defaults to a likely file under datasets/.")
    parser.add_argument("--output", type=str, default=os.path.join("outputs", "evaluation_results", "fig_dataset_policy_variant_distribution.png"), help="Path to save the PNG figure.")
    args = parser.parse_args()

    base_dir = os.getcwd()
    input_path = args.input or find_default_input(base_dir)
    if not input_path:
        print("[ERROR] Could not find a dataset file. Pass --input <path-to-file>.")
        sys.exit(1)

    if not os.path.isfile(input_path):
        print(f"[ERROR] Input file not found: {input_path}")
        sys.exit(1)

    print(f"[INFO] Reading dataset: {input_path}")
    df = read_dataset(input_path)

    policy_col = pick_column(df, POLICY_CANDIDATES)
    variant_col = pick_column(df, VARIANT_CANDIDATES)

    if policy_col is None:
        print(f"[ERROR] Could not find a policy/category column. Looked for: {POLICY_CANDIDATES}")
        print("        Please rename your column to one of the expected names or pass a preprocessed file.")
        sys.exit(1)

    if variant_col is None:
        print(f"[ERROR] Could not find a variant column. Looked for: {VARIANT_CANDIDATES}")
        print("        Expected something like 'variant' with values for Direct, Simple Paraphrase, Adversarial Paraphrase (or 0/1/2).")
        sys.exit(1)

    print(f"[INFO] Detected policy column: {policy_col}")
    print(f"[INFO] Detected variant column: {variant_col}")

    by_policy_variant, totals_by_policy, totals_by_variant = summarize_counts(df, policy_col, variant_col)

    total_rows = int(by_policy_variant["count"].sum())
    distinct_policies = len(totals_by_policy)
    print("\n=== Dataset Summary ===")
    print(f"Total rows: {total_rows}")
    print(f"Policies: {distinct_policies}")

    print("\n=== Overall counts by variant ===")
    for var, cnt in totals_by_variant.items():
        print(f"{var:>22}: {int(cnt)}")

    print("\n=== Counts by policy and variant ===")
    # Pretty print grouped counts
    # Build a table-like printout per policy
    pivot = by_policy_variant.pivot(index=policy_col, columns=by_policy_variant.columns[1], values="count").fillna(0)
    # Ensure expected variant ordering if present
    desired_cols = ["Direct", "Simple Paraphrase", "Adversarial Paraphrase"]
    cols = [c for c in desired_cols if c in pivot.columns] + [c for c in pivot.columns if c not in desired_cols]
    pivot = pivot[cols]
    # Sort by total descending
    pivot["TOTAL"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("TOTAL", ascending=False)

    # Print header
    header = [policy_col] + list(cols) + ["TOTAL"]
    print(" | ".join([h.center(24) for h in header]))
    print("-" * (27 * len(header)))
    for policy, row in pivot.iterrows():
        vals = [str(policy)] + [str(int(row.get(c, 0))) for c in cols] + [str(int(row["TOTAL"]))]
        print(" | ".join([v.ljust(24) for v in vals]))

    # Draw and save figure
    output_path = args.output
    print(f"\n[INFO] Saving figure to: {output_path}")
    draw_grouped_bar_chart(by_policy_variant, totals_by_policy, output_path)
    print("[DONE] Distribution image saved. You can paste it in your report.")


if __name__ == "__main__":
    main()
