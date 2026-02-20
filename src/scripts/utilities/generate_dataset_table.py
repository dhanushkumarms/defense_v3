"""
Generate a clean table image showing dataset distribution by policy and variant.

Creates a professional-looking table PNG that can be pasted into reports.

Usage (PowerShell):
  python scripts/generate_dataset_table.py
"""

from __future__ import annotations
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# Configuration
INPUT_FILE = "datasets/three_variant_dataset_2500.csv"
OUTPUT_FILE = "outputs/evaluation_results/table_dataset_distribution.png"

POLICY_COL = "content_policy_name"
VARIANT_COL = "test_type"

# Table styling - IMPROVED FOR WORD DOCUMENT
TABLE_WIDTH = 1600
CELL_HEIGHT = 65
HEADER_HEIGHT = 80
PADDING = 12  # Reduced padding for better fit
FONT_SIZE_HEADER = 20
FONT_SIZE_BODY = 18

# Colors - More professional and readable
COLOR_HEADER_BG = (41, 128, 185)    # Professional blue
COLOR_HEADER_TEXT = (255, 255, 255) # White
COLOR_ROW_ODD = (236, 240, 241)     # Light gray
COLOR_ROW_EVEN = (255, 255, 255)    # White
COLOR_TEXT = (33, 33, 33)           # Almost black for readability
COLOR_BORDER = (149, 165, 166)      # Medium gray border
COLOR_TOTAL_BG = (52, 152, 219)     # Highlighted blue for totals
COLOR_TOTAL_TEXT = (255, 255, 255)  # White text for total row

def load_and_summarize():
    """Load dataset and compute counts."""
    df = pd.read_csv(INPUT_FILE)
    
    # Normalize variant names
    variant_map = {
        'direct': 'Direct',
        'simple_paraphrase': 'Simple Paraphrase',
        'paraphrase': 'Simple Paraphrase',
        'adversarial': 'Adversarial Paraphrase',
        'adversarial_paraphrase': 'Adversarial Paraphrase',
        'jailbreak': 'Adversarial Paraphrase',
    }
    
    df[VARIANT_COL] = df[VARIANT_COL].str.lower().map(variant_map).fillna(df[VARIANT_COL])
    
    # Get counts
    counts = df.groupby([POLICY_COL, VARIANT_COL]).size().unstack(fill_value=0)
    
    # Ensure expected columns exist
    for col in ['Direct', 'Simple Paraphrase', 'Adversarial Paraphrase']:
        if col not in counts.columns:
            counts[col] = 0
    
    # Reorder columns
    col_order = ['Direct', 'Simple Paraphrase', 'Adversarial Paraphrase']
    counts = counts[[c for c in col_order if c in counts.columns]]
    
    # Add total column
    counts['Total'] = counts.sum(axis=1)
    
    # Sort by total descending
    counts = counts.sort_values('Total', ascending=False)
    
    # Add summary row
    totals = counts.sum()
    totals.name = 'TOTAL'
    counts = pd.concat([counts, totals.to_frame().T])
    
    return counts

def draw_table(df: pd.DataFrame, output_path: str):
    """Draw a professional table as PNG."""
    
    # Calculate dimensions
    num_rows = len(df) + 1  # +1 for header
    num_cols = len(df.columns) + 1  # +1 for policy name column
    
    table_height = HEADER_HEIGHT + (len(df) * CELL_HEIGHT)
    
    # Create image
    img = Image.new('RGB', (TABLE_WIDTH, table_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Try to load a better font, fall back to default
    try:
        font_header = ImageFont.truetype("arialbd.ttf", FONT_SIZE_HEADER)  # Bold Arial
        font_body = ImageFont.truetype("arialbd.ttf", FONT_SIZE_BODY)      # Bold for all
        font_body_bold = ImageFont.truetype("arialbd.ttf", FONT_SIZE_BODY + 2)  # Extra bold for totals
    except:
        try:
            font_header = ImageFont.truetype("arial.ttf", FONT_SIZE_HEADER)
            font_body = ImageFont.truetype("arial.ttf", FONT_SIZE_BODY)
            font_body_bold = ImageFont.truetype("arialbd.ttf", FONT_SIZE_BODY)
        except:
            font_header = ImageFont.load_default()
            font_body = ImageFont.load_default()
            font_body_bold = ImageFont.load_default()
    
    # Column widths (adjust to number of columns) - More space for "Adversarial Paraphrase"
    num_data_cols = len(df.columns)
    if num_data_cols == 4:
        col_widths = [
            int(TABLE_WIDTH * 0.30),  # Policy name - reduced
            int(TABLE_WIDTH * 0.15),  # Direct
            int(TABLE_WIDTH * 0.23),  # Simple Paraphrase
            int(TABLE_WIDTH * 0.22),  # Adversarial Paraphrase - increased
            int(TABLE_WIDTH * 0.10),  # Total
        ]
    elif num_data_cols == 3:
        col_widths = [
            int(TABLE_WIDTH * 0.35),  # Policy name
            int(TABLE_WIDTH * 0.20),  # Direct
            int(TABLE_WIDTH * 0.25),  # Simple Paraphrase
            int(TABLE_WIDTH * 0.20),  # Total
        ]
    else:
        # Generic distribution
        policy_width = int(TABLE_WIDTH * 0.30)
        data_width = int((TABLE_WIDTH - policy_width) / num_data_cols)
        col_widths = [policy_width] + [data_width] * num_data_cols
    
    # Draw header
    headers = ['Content Policy'] + list(df.columns)
    x = 0
    for i, (header, width) in enumerate(zip(headers, col_widths)):
        # Background
        draw.rectangle([x, 0, x + width, HEADER_HEIGHT], fill=COLOR_HEADER_BG)
        
        # Border (thicker for better visibility)
        draw.rectangle([x, 0, x + width, HEADER_HEIGHT], outline=COLOR_BORDER, width=2)
        
        # Text (centered)
        bbox = draw.textbbox((0, 0), header, font=font_header)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x + (width - text_width) // 2
        text_y = (HEADER_HEIGHT - text_height) // 2
        draw.text((text_x, text_y), header, fill=COLOR_HEADER_TEXT, font=font_header)
        
        x += width
    
    # Draw data rows
    y = HEADER_HEIGHT
    for row_idx, (policy, row) in enumerate(df.iterrows()):
        is_total_row = policy == 'TOTAL'
        bg_color = COLOR_TOTAL_BG if is_total_row else (COLOR_ROW_ODD if row_idx % 2 == 0 else COLOR_ROW_EVEN)
        text_color = COLOR_TOTAL_TEXT if is_total_row else COLOR_TEXT
        
        x = 0
        
        # Policy name cell
        draw.rectangle([x, y, x + col_widths[0], y + CELL_HEIGHT], fill=bg_color, outline=COLOR_BORDER, width=2)
        policy_text = str(policy)
        font_to_use = font_body_bold if is_total_row else font_body
        draw.text((x + PADDING, y + PADDING), policy_text, fill=text_color, font=font_to_use)
        x += col_widths[0]
        
        # Value cells
        for col_idx, value in enumerate(row):
            draw.rectangle([x, y, x + col_widths[col_idx + 1], y + CELL_HEIGHT], 
                          fill=bg_color, outline=COLOR_BORDER, width=2)
            
            value_text = str(int(value)) if pd.notna(value) else '0'
            bbox = draw.textbbox((0, 0), value_text, font=font_to_use)
            text_width = bbox[2] - bbox[0]
            text_x = x + (col_widths[col_idx + 1] - text_width) // 2
            draw.text((text_x, y + PADDING), value_text, fill=text_color, font=font_to_use)
            
            x += col_widths[col_idx + 1]
        
        y += CELL_HEIGHT
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"✓ Table image saved: {output_path}")

def main():
    print("Loading dataset...")
    df = load_and_summarize()
    
    print("\nDataset Summary:")
    print(df.to_string())
    
    print("\nGenerating table image...")
    draw_table(df, OUTPUT_FILE)
    print("\n✅ Done! You can now paste the table image into your report.")

if __name__ == "__main__":
    main()
