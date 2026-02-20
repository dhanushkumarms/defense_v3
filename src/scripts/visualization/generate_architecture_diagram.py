"""
Semantic Smoothing v2.0 - Architecture Diagram Generator
Creates a visual representation of the 4-component architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

# Title
ax.text(5, 13.5, 'Semantic Smoothing v2.0 Architecture', 
        ha='center', fontsize=20, fontweight='bold', 
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#1976D2', edgecolor='black', linewidth=2, alpha=0.9),
        color='white')

# Input Layer
input_box = FancyBboxPatch((0.5, 11.5), 9, 1, boxstyle="round,pad=0.1", 
                          edgecolor='black', facecolor='#E3F2FD', linewidth=2)
ax.add_patch(input_box)
ax.text(5, 12, 'INPUT: Harmful Prompt', ha='center', va='center', 
        fontsize=14, fontweight='bold')

# Arrow from input to Component 1
arrow1 = FancyArrowPatch((5, 11.5), (5, 10.8), 
                        arrowstyle='->', mutation_scale=30, linewidth=3, color='#424242')
ax.add_patch(arrow1)

# ===================== COMPONENT 1 =====================
comp1_box = FancyBboxPatch((0.3, 8.5), 4.4, 2.2, boxstyle="round,pad=0.15",
                          edgecolor='#1976D2', facecolor='#BBDEFB', linewidth=3)
ax.add_patch(comp1_box)
ax.text(2.5, 10.3, 'COMPONENT 1', ha='center', fontsize=12, fontweight='bold', color='#1976D2')
ax.text(2.5, 10, 'Enhanced Paraphrase Generator', ha='center', fontsize=11, fontweight='bold')
ax.text(2.5, 9.6, '• Dual-Model (T5 + Sentence-Transformer)', ha='center', fontsize=9)
ax.text(2.5, 9.3, '• K=7 variations (up from K=5)', ha='center', fontsize=9)
ax.text(2.5, 9.0, '• Quality filtering & diversity scoring', ha='center', fontsize=9)
ax.text(2.5, 8.7, '• Intent preservation metrics', ha='center', fontsize=9)

# Arrow Component 1 to Component 2
arrow2 = FancyArrowPatch((4.7, 9.6), (5.3, 9.6),
                        arrowstyle='->', mutation_scale=30, linewidth=3, color='#424242')
ax.add_patch(arrow2)

# ===================== COMPONENT 2 =====================
comp2_box = FancyBboxPatch((5.3, 8.5), 4.4, 2.2, boxstyle="round,pad=0.15",
                          edgecolor='#388E3C', facecolor='#C8E6C9', linewidth=3)
ax.add_patch(comp2_box)
ax.text(7.5, 10.3, 'COMPONENT 2', ha='center', fontsize=12, fontweight='bold', color='#388E3C')
ax.text(7.5, 10, 'Dynamic Ensemble Weighting', ha='center', fontsize=11, fontweight='bold')
ax.text(7.5, 9.6, '• Variant-specific detector weights', ha='center', fontsize=9)
ax.text(7.5, 9.3, '• Confidence-based adjustment', ha='center', fontsize=9)
ax.text(7.5, 9.0, '• Conflict resolution mechanisms', ha='center', fontsize=9)
ax.text(7.5, 8.7, '• ToxicBERT + RoBERTa + ToxicChat', ha='center', fontsize=9)

# Arrow down from Components to Component 3
arrow3 = FancyArrowPatch((5, 8.5), (5, 7.8),
                        arrowstyle='->', mutation_scale=30, linewidth=3, color='#424242')
ax.add_patch(arrow3)

# ===================== COMPONENT 3 =====================
comp3_box = FancyBboxPatch((0.3, 5.3), 4.4, 2.2, boxstyle="round,pad=0.15",
                          edgecolor='#F57C00', facecolor='#FFE0B2', linewidth=3)
ax.add_patch(comp3_box)
ax.text(2.5, 7.1, 'COMPONENT 3', ha='center', fontsize=12, fontweight='bold', color='#F57C00')
ax.text(2.5, 6.8, 'Advanced Aggregation', ha='center', fontsize=11, fontweight='bold')
ax.text(2.5, 6.4, '• Weighted averaging', ha='center', fontsize=9)
ax.text(2.5, 6.1, '• Consensus scoring', ha='center', fontsize=9)
ax.text(2.5, 5.8, '• Majority voting with confidence', ha='center', fontsize=9)
ax.text(2.5, 5.5, '• Ensemble of all 3 methods', ha='center', fontsize=9)

# Arrow Component 3 to Component 4
arrow4 = FancyArrowPatch((4.7, 6.4), (5.3, 6.4),
                        arrowstyle='->', mutation_scale=30, linewidth=3, color='#424242')
ax.add_patch(arrow4)

# ===================== COMPONENT 4 =====================
comp4_box = FancyBboxPatch((5.3, 5.3), 4.4, 2.2, boxstyle="round,pad=0.15",
                          edgecolor='#7B1FA2', facecolor='#E1BEE7', linewidth=3)
ax.add_patch(comp4_box)
ax.text(7.5, 7.1, 'COMPONENT 4', ha='center', fontsize=12, fontweight='bold', color='#7B1FA2')
ax.text(7.5, 6.8, 'Adaptive Thresholding', ha='center', fontsize=11, fontweight='bold')
ax.text(7.5, 6.4, '• Per-variant thresholds', ha='center', fontsize=9)
ax.text(7.5, 6.1, '• Confidence-based adjustment', ha='center', fontsize=9)
ax.text(7.5, 5.8, '• Policy-specific calibration', ha='center', fontsize=9)
ax.text(7.5, 5.5, '• Direct: 0.75 | Para: 0.62 | Jail: 0.58', ha='center', fontsize=9)

# Arrow down to Output
arrow5 = FancyArrowPatch((5, 5.3), (5, 4.6),
                        arrowstyle='->', mutation_scale=30, linewidth=3, color='#424242')
ax.add_patch(arrow5)

# Output Layer - Decision
output_box = FancyBboxPatch((0.5, 3.3), 4, 1.2, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='#C8E6C9', linewidth=2)
ax.add_patch(output_box)
ax.text(2.5, 4.1, 'OUTPUT: REJECT', ha='center', va='center',
        fontsize=13, fontweight='bold', color='#2E7D32')
ax.text(2.5, 3.7, '(Attack Blocked)', ha='center', fontsize=10, style='italic')

# Alternative output
output_box2 = FancyBboxPatch((5.5, 3.3), 4, 1.2, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor='#FFCDD2', linewidth=2)
ax.add_patch(output_box2)
ax.text(7.5, 4.1, 'OUTPUT: ACCEPT', ha='center', va='center',
        fontsize=13, fontweight='bold', color='#C62828')
ax.text(7.5, 3.7, '(Attack Succeeded - Rare)', ha='center', fontsize=10, style='italic')

# Performance Metrics Box
metrics_box = FancyBboxPatch((0.5, 0.3), 9, 2.5, boxstyle="round,pad=0.15",
                            edgecolor='#1976D2', facecolor='#E8F5E9', linewidth=3)
ax.add_patch(metrics_box)
ax.text(5, 2.5, 'PERFORMANCE METRICS (v2.0 Improvements)', ha='center',
        fontsize=13, fontweight='bold', color='#1976D2')

# Metrics table
metrics_data = [
    ['Variant', 'v1.0 ASR', 'v2.0 ASR', 'Improvement'],
    ['Direct', '2.4%', '1.8%', '↓0.6pp (27%)'],
    ['Paraphrase', '18.4%', '9.3%', '↓9.1pp (50%)'],
    ['Jailbreak', '28.7%', '11.3%', '↓17.4pp (61%)']
]

y_start = 1.9
for i, row in enumerate(metrics_data):
    x_positions = [1.2, 3.5, 5.8, 8]
    for j, text in enumerate(row):
        weight = 'bold' if i == 0 else 'normal'
        color = '#1976D2' if i == 0 else 'black'
        if i > 0 and j == 3:  # Improvement column
            color = '#2E7D32'
            weight = 'bold'
        ax.text(x_positions[j], y_start - i*0.4, text, ha='center',
               fontsize=10, fontweight=weight, color=color)

# Legend
legend_y = 0.5
ax.text(0.8, legend_y, '⬤', fontsize=20, color='#1976D2')
ax.text(1.2, legend_y, 'Input Processing', fontsize=9)
ax.text(3.2, legend_y, '⬤', fontsize=20, color='#388E3C')
ax.text(3.6, legend_y, 'Detector Ensemble', fontsize=9)
ax.text(5.8, legend_y, '⬤', fontsize=20, color='#F57C00')
ax.text(6.2, legend_y, 'Aggregation', fontsize=9)
ax.text(8, legend_y, '⬤', fontsize=20, color='#7B1FA2')
ax.text(8.4, legend_y, 'Decision Logic', fontsize=9)

plt.tight_layout()
plt.savefig('SEMANTIC_SMOOTHING_v2.0_ARCHITECTURE.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Architecture diagram saved: SEMANTIC_SMOOTHING_v2.0_ARCHITECTURE.png")
plt.close()
