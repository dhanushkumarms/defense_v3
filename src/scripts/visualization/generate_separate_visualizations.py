"""
Generate individual metric visualizations for Semantic Smoothing defense evaluation.
Creates separate charts for each metric instead of combined dashboard.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Set publication-quality style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 10

# Color palette
colors = {
    'baseline': '#C73E1D',      # Red
    'defense': '#06A77D',        # Green
    'direct': '#2E86AB',         # Blue
    'simple': '#A23B72',         # Purple
    'adversarial': '#F18F01'     # Orange
}

# Create output directory
output_dir = Path("../outputs/evaluation_results/separate_charts")
output_dir.mkdir(parents=True, exist_ok=True)

# Data from SEMANTIC_SMOOTH_REPORT.md
variants = ['Direct', 'Simple Paraphrase', 'Adversarial Jailbreak']
baseline_asr = [5.6, 39.0, 56.2]
defense_asr = [2.8, 18.5, 25.2]
reduction_pct = [50, 53, 55]
asr_reduction_pp = [2.8, 20.5, 31.0]

dsr = [50.0, 52.6, 55.1]
fnr = [2.8, 18.5, 25.2]
fpr = [8.2, 12.4, 4.8]
rcs = [48.0, 50.2, 52.1]
suti = [0.460, 0.461, 0.501]

print("=" * 80)
print("SEMANTIC SMOOTHING DEFENSE - INDIVIDUAL METRIC VISUALIZATIONS")
print("=" * 80)

# ============================================================================
# Chart 1: ASR Reduction (Main Metric)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(variants))
width = 0.35

bars1 = ax.bar(x - width/2, baseline_asr, width, label='Baseline (No Defense)',
               color=colors['baseline'], alpha=0.85, edgecolor='black', linewidth=1.2)
bars2 = ax.bar(x + width/2, defense_asr, width, label='With Semantic Smoothing',
               color=colors['defense'], alpha=0.85, edgecolor='black', linewidth=1.2)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1.5,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add reduction percentage above
for i, (b, d, r) in enumerate(zip(baseline_asr, defense_asr, reduction_pct)):
    ax.annotate(f'{r}% reduction', xy=(i, max(b, d) + 3), xytext=(i, max(b, d) + 8),
                ha='center', fontsize=10, color=colors['defense'], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.7))

ax.set_ylabel('Attack Success Rate (%)', fontweight='bold', fontsize=12)
ax.set_xlabel('Attack Variant Type', fontweight='bold', fontsize=12)
ax.set_title('Semantic Smoothing Defense Effectiveness:\nAttack Success Rate Reduction', 
             fontweight='bold', fontsize=13, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(variants, fontsize=11)
ax.set_ylim(0, 70)
ax.legend(loc='upper left', fontsize=11, framealpha=0.95)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_dir / '01_asr_reduction.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Chart 1 saved: 01_asr_reduction.png")

# ============================================================================
# Chart 2: ASR Reduction in Percentage Points
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(variants, asr_reduction_pp, color=colors['defense'], 
              alpha=0.85, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars, asr_reduction_pp):
    ax.text(bar.get_x() + bar.get_width()/2., val + 1,
            f'{val:.1f} pp', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('ASR Reduction (Percentage Points)', fontweight='bold', fontsize=12)
ax.set_xlabel('Attack Variant Type', fontweight='bold', fontsize=12)
ax.set_title('Absolute ASR Reduction by Defense Mechanism\n(Percentage Points)', 
             fontweight='bold', fontsize=13, pad=15)
ax.set_xticklabels(variants, fontsize=11)
ax.set_ylim(0, 35)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_dir / '02_asr_reduction_pp.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Chart 2 saved: 02_asr_reduction_pp.png")

# ============================================================================
# Chart 3: Defense Success Rate (DSR)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(variants, dsr, color=colors['defense'],
              alpha=0.85, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars, dsr):
    ax.text(bar.get_x() + bar.get_width()/2., val + 1.5,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Defense Success Rate (%)', fontweight='bold', fontsize=12)
ax.set_xlabel('Attack Variant Type', fontweight='bold', fontsize=12)
ax.set_title('Defense Success Rate (DSR)\nPercentage of Attacks Successfully Intercepted', 
             fontweight='bold', fontsize=13, pad=15)
ax.set_xticklabels(variants, fontsize=11)
ax.set_ylim(0, 65)
ax.axhline(y=50, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='50% baseline')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_dir / '03_defense_success_rate.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Chart 3 saved: 03_defense_success_rate.png")

# ============================================================================
# Chart 4: False Negative Rate (FNR)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(variants, fnr, color='#FF6B6B',
              alpha=0.85, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars, fnr):
    ax.text(bar.get_x() + bar.get_width()/2., val + 1,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('False Negative Rate (%)', fontweight='bold', fontsize=12)
ax.set_xlabel('Attack Variant Type', fontweight='bold', fontsize=12)
ax.set_title('False Negative Rate (FNR)\nPercentage of Harmful Prompts Incorrectly Allowed', 
             fontweight='bold', fontsize=13, pad=15)
ax.set_xticklabels(variants, fontsize=11)
ax.set_ylim(0, 30)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add annotation
textstr = 'Lower is better\n(Fewer dangerous prompts pass through)'
ax.text(0.98, 0.97, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='red', linewidth=1.5))

plt.tight_layout()
plt.savefig(output_dir / '04_false_negative_rate.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Chart 4 saved: 04_false_negative_rate.png")

# ============================================================================
# Chart 5: False Positive Rate (FPR)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(variants, fpr, color='#FFD93D',
              alpha=0.85, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars, fpr):
    ax.text(bar.get_x() + bar.get_width()/2., val + 0.3,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('False Positive Rate (%)', fontweight='bold', fontsize=12)
ax.set_xlabel('Attack Variant Type', fontweight='bold', fontsize=12)
ax.set_title('False Positive Rate (FPR)\nPercentage of Benign Prompts Incorrectly Blocked', 
             fontweight='bold', fontsize=13, pad=15)
ax.set_xticklabels(variants, fontsize=11)
ax.set_ylim(0, 15)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add annotation
textstr = 'Lower is better\n(Better utility preservation)'
ax.text(0.98, 0.97, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='orange', linewidth=1.5))

plt.tight_layout()
plt.savefig(output_dir / '05_false_positive_rate.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Chart 5 saved: 05_false_positive_rate.png")

# ============================================================================
# Chart 6: Robustness Consistency Score (RCS)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(variants, rcs, color='#6BCB77',
              alpha=0.85, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars, rcs):
    ax.text(bar.get_x() + bar.get_width()/2., val + 1.5,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Robustness Consistency Score (%)', fontweight='bold', fontsize=12)
ax.set_xlabel('Attack Variant Type', fontweight='bold', fontsize=12)
ax.set_title('Robustness Consistency Score (RCS)\nConsistency of Defense Across Semantic Variants', 
             fontweight='bold', fontsize=13, pad=15)
ax.set_xticklabels(variants, fontsize=11)
ax.set_ylim(0, 65)
ax.axhline(y=50, color='gray', linestyle='--', linewidth=1.5, alpha=0.6, label='50% (Moderate consistency)')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.legend(loc='lower right', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add annotation
textstr = 'Higher is better\n(50% room for improvement)'
ax.text(0.02, 0.97, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='left',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8, edgecolor='blue', linewidth=1.5))

plt.tight_layout()
plt.savefig(output_dir / '06_robustness_consistency.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Chart 6 saved: 06_robustness_consistency.png")

# ============================================================================
# Chart 7: Safety-Utility Trade-off Index (SUTI)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(variants, suti, color='#4D96FF',
              alpha=0.85, edgecolor='black', linewidth=1.5)

for bar, val in zip(bars, suti):
    ax.text(bar.get_x() + bar.get_width()/2., val + 0.02,
            f'{val:.3f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylabel('Safety-Utility Trade-off Index (SUTI)', fontweight='bold', fontsize=12)
ax.set_xlabel('Attack Variant Type', fontweight='bold', fontsize=12)
ax.set_title('Safety-Utility Trade-off Index (SUTI)\nBalance Between Security and Usability', 
             fontweight='bold', fontsize=13, pad=15)
ax.set_xticklabels(variants, fontsize=11)
ax.set_ylim(0, 0.6)
ax.axhline(y=0.45, color='gray', linestyle='--', linewidth=1.5, alpha=0.6, label='0.45 (Practical minimum)')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.legend(loc='upper left', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add annotation
textstr = 'Higher is better\n(All variants >0.45 ✓)'
ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8, edgecolor='green', linewidth=1.5))

plt.tight_layout()
plt.savefig(output_dir / '07_safety_utility_tradeoff.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Chart 7 saved: 07_safety_utility_tradeoff.png")

# ============================================================================
# Chart 8: Comparison Overview (Side-by-side, but not combined)
# ============================================================================
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Semantic Smoothing Defense - Metric Overview', fontsize=15, fontweight='bold', y=1.00)

# Chart 1: ASR
ax = axes[0, 0]
x = np.arange(len(variants))
width = 0.35
ax.bar(x - width/2, baseline_asr, width, label='Baseline', color=colors['baseline'], alpha=0.8, edgecolor='black')
ax.bar(x + width/2, defense_asr, width, label='With Defense', color=colors['defense'], alpha=0.8, edgecolor='black')
ax.set_ylabel('ASR (%)', fontweight='bold')
ax.set_title('(A) Attack Success Rate', fontweight='bold', loc='left', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(['Direct', 'Simple', 'Adversarial'], fontsize=9)
ax.set_ylim(0, 65)
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Chart 2: DSR
ax = axes[0, 1]
ax.bar(variants, dsr, color=colors['defense'], alpha=0.8, edgecolor='black')
for i, v in enumerate(dsr):
    ax.text(i, v + 1, f'{v:.1f}%', ha='center', fontsize=9, fontweight='bold')
ax.set_ylabel('DSR (%)', fontweight='bold')
ax.set_title('(B) Defense Success Rate', fontweight='bold', loc='left', fontsize=11)
ax.set_xticklabels(['Direct', 'Simple', 'Adversarial'], fontsize=9)
ax.set_ylim(0, 65)
ax.grid(axis='y', alpha=0.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Chart 3: FNR & FPR
ax = axes[0, 2]
x = np.arange(len(variants))
width = 0.35
ax.bar(x - width/2, fnr, width, label='FNR (False Negatives)', color='#FF6B6B', alpha=0.8, edgecolor='black')
ax.bar(x + width/2, fpr, width, label='FPR (False Positives)', color='#FFD93D', alpha=0.8, edgecolor='black')
ax.set_ylabel('Error Rate (%)', fontweight='bold')
ax.set_title('(C) Error Rates', fontweight='bold', loc='left', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(['Direct', 'Simple', 'Adversarial'], fontsize=9)
ax.set_ylim(0, 30)
ax.legend(fontsize=8, loc='upper left')
ax.grid(axis='y', alpha=0.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Chart 4: RCS
ax = axes[1, 0]
ax.bar(variants, rcs, color='#6BCB77', alpha=0.8, edgecolor='black')
for i, v in enumerate(rcs):
    ax.text(i, v + 1.5, f'{v:.1f}%', ha='center', fontsize=9, fontweight='bold')
ax.set_ylabel('RCS (%)', fontweight='bold')
ax.set_title('(D) Robustness Consistency', fontweight='bold', loc='left', fontsize=11)
ax.set_xticklabels(['Direct', 'Simple', 'Adversarial'], fontsize=9)
ax.set_ylim(0, 65)
ax.axhline(y=50, color='gray', linestyle='--', linewidth=1, alpha=0.4)
ax.grid(axis='y', alpha=0.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Chart 5: SUTI
ax = axes[1, 1]
ax.bar(variants, suti, color='#4D96FF', alpha=0.8, edgecolor='black')
for i, v in enumerate(suti):
    ax.text(i, v + 0.02, f'{v:.3f}', ha='center', fontsize=9, fontweight='bold')
ax.set_ylabel('SUTI', fontweight='bold')
ax.set_title('(E) Safety-Utility Index', fontweight='bold', loc='left', fontsize=11)
ax.set_xticklabels(['Direct', 'Simple', 'Adversarial'], fontsize=9)
ax.set_ylim(0, 0.6)
ax.axhline(y=0.45, color='gray', linestyle='--', linewidth=1, alpha=0.4)
ax.grid(axis='y', alpha=0.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Chart 6: Reduction %
ax = axes[1, 2]
ax.bar(variants, reduction_pct, color='#A23B72', alpha=0.8, edgecolor='black')
for i, v in enumerate(reduction_pct):
    ax.text(i, v + 1.5, f'{v}%', ha='center', fontsize=9, fontweight='bold')
ax.set_ylabel('Reduction (%)', fontweight='bold')
ax.set_title('(F) ASR Reduction %', fontweight='bold', loc='left', fontsize=11)
ax.set_xticklabels(['Direct', 'Simple', 'Adversarial'], fontsize=9)
ax.set_ylim(0, 65)
ax.axhline(y=50, color='gray', linestyle='--', linewidth=1, alpha=0.4)
ax.grid(axis='y', alpha=0.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(output_dir / '08_metric_overview.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Chart 8 saved: 08_metric_overview.png (6-panel reference only, not main)")

print("\n" + "=" * 80)
print("✓ ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
print("=" * 80)
print(f"\nOutput directory: {output_dir}")
print(f"\nGenerated charts:")
print(f"  1. 01_asr_reduction.png - Main metric comparison")
print(f"  2. 02_asr_reduction_pp.png - Absolute reduction in percentage points")
print(f"  3. 03_defense_success_rate.png - Defense success rate")
print(f"  4. 04_false_negative_rate.png - Harmful prompts incorrectly allowed")
print(f"  5. 05_false_positive_rate.png - Benign prompts incorrectly blocked")
print(f"  6. 06_robustness_consistency.png - Consistency across variants")
print(f"  7. 07_safety_utility_tradeoff.png - Overall balance metric")
print(f"  8. 08_metric_overview.png - 6-panel reference chart")
print(f"\nTotal: 8 separate visualization files")
print("=" * 80)
