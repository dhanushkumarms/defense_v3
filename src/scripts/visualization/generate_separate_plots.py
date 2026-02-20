"""
Generate Separate Visualization Plots for Semantic Smoothing v2.0

Creates individual PNG files for each metric:
1. ASR Comparison (v1.0 vs v2.0)
2. DSR Comparison (v1.0 vs v2.0)
3. FNR v2.0
4. FPR v2.0
5. RCS v2.0
6. SUTI v2.0
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 300

# Data
variants_list = ['Direct', 'Paraphrase', 'Jailbreak']

# v1.0 data
v1_asr = [2.4, 18.4, 28.7]
v1_dsr = [97.6, 81.6, 71.3]

# v2.0 data
v2_asr = [1.8, 9.3, 11.3]
v2_dsr = [98.2, 90.7, 88.7]
v2_fnr = [1.8, 9.3, 11.3]
v2_fpr = [0.0, 0.0, 0.0]
v2_rcs = [98.2, 90.7, 88.7]
v2_suti = [0.982, 0.907, 0.887]

# 1. ASR Comparison
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(variants_list))
width = 0.35
ax.bar(x - width/2, v1_asr, width, label='v1.0 Baseline', color='#ff9999', alpha=0.8, edgecolor='black', linewidth=1.5)
ax.bar(x + width/2, v2_asr, width, label='v2.0 Upgraded', color='#2ca02c', alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Attack Success Rate (%)', fontweight='bold', fontsize=12)
ax.set_title('Attack Success Rate - v1.0 vs v2.0 Comparison\n(Lower = Better)', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(variants_list, fontweight='bold')
ax.legend(loc='upper right', fontsize=11)
ax.grid(axis='y', alpha=0.3)
for i, (v1, v2) in enumerate(zip(v1_asr, v2_asr)):
    ax.text(i - width/2, v1 + 0.5, f'{v1:.1f}%', ha='center', fontweight='bold', fontsize=10)
    ax.text(i + width/2, v2 + 0.5, f'{v2:.1f}%', ha='center', fontweight='bold', fontsize=10)
plt.tight_layout()
plt.savefig('PLOT_1_ASR_COMPARISON.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Generated: PLOT_1_ASR_COMPARISON.png")

# 2. DSR Comparison
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, v1_dsr, width, label='v1.0 Baseline', color='#ff9999', alpha=0.8, edgecolor='black', linewidth=1.5)
ax.bar(x + width/2, v2_dsr, width, label='v2.0 Upgraded', color='#2ca02c', alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Defense Success Rate (%)', fontweight='bold', fontsize=12)
ax.set_title('Defense Success Rate - v1.0 vs v2.0 Comparison\n(Higher = Better)', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(variants_list, fontweight='bold')
ax.set_ylim(60, 105)
ax.legend(loc='lower right', fontsize=11)
ax.grid(axis='y', alpha=0.3)
for i, (v1, v2) in enumerate(zip(v1_dsr, v2_dsr)):
    ax.text(i - width/2, v1 + 1, f'{v1:.1f}%', ha='center', fontweight='bold', fontsize=10)
    ax.text(i + width/2, v2 + 1, f'{v2:.1f}%', ha='center', fontweight='bold', fontsize=10)
plt.tight_layout()
plt.savefig('PLOT_2_DSR_COMPARISON.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Generated: PLOT_2_DSR_COMPARISON.png")

# 3. FNR v2.0
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(variants_list, v2_fnr, color='#ff7f0e', alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('False Negative Rate (%)', fontweight='bold', fontsize=12)
ax.set_title('False Negative Rate - Semantic Smoothing v2.0\n(Lower = Better)', fontweight='bold', fontsize=14)
ax.set_xticklabels(variants_list, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, v2_fnr)):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.3, f'{val:.1f}%', ha='center', fontweight='bold', fontsize=10)
plt.tight_layout()
plt.savefig('PLOT_3_FNR_v2.0.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Generated: PLOT_3_FNR_v2.0.png")

# 4. FPR v2.0
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(variants_list, v2_fpr, color='#9467bd', alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('False Positive Rate (%)', fontweight='bold', fontsize=12)
ax.set_title('False Positive Rate - Semantic Smoothing v2.0\n(Lower = Better)', fontweight='bold', fontsize=14)
ax.set_xticklabels(variants_list, fontweight='bold')
ax.set_ylim(0, 0.1)
ax.grid(axis='y', alpha=0.3)
ax.text(0.5, 0.05, 'Perfect Score: 0.0% across all variants', 
        transform=ax.transAxes, ha='center', fontsize=12, 
        bbox=dict(boxstyle='round', facecolor='#90EE90', alpha=0.7))
plt.tight_layout()
plt.savefig('PLOT_4_FPR_v2.0.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Generated: PLOT_4_FPR_v2.0.png")

# 5. RCS v2.0
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(variants_list, v2_rcs, color='#17becf', alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Robustness Consistency Score (%)', fontweight='bold', fontsize=12)
ax.set_title('Robustness Consistency Score - Semantic Smoothing v2.0\n(Higher = Better)', fontweight='bold', fontsize=14)
ax.set_xticklabels(variants_list, fontweight='bold')
ax.set_ylim(80, 105)
ax.grid(axis='y', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, v2_rcs)):
    ax.text(bar.get_x() + bar.get_width()/2, val + 1, f'{val:.1f}%', ha='center', fontweight='bold', fontsize=10)
plt.tight_layout()
plt.savefig('PLOT_5_RCS_v2.0.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Generated: PLOT_5_RCS_v2.0.png")

# 6. SUTI v2.0
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(variants_list, v2_suti, color='#bcbd22', alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Safety-Utility Trade-off Index', fontweight='bold', fontsize=12)
ax.set_title('Safety-Utility Trade-off Index - Semantic Smoothing v2.0\n(Higher = Better, Max = 1.0)', fontweight='bold', fontsize=14)
ax.set_xticklabels(variants_list, fontweight='bold')
ax.set_ylim(0.8, 1.05)
ax.grid(axis='y', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, v2_suti)):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.01, f'{val:.3f}', ha='center', fontweight='bold', fontsize=10)
plt.tight_layout()
plt.savefig('PLOT_6_SUTI_v2.0.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("✓ Generated: PLOT_6_SUTI_v2.0.png")

print("\n" + "="*70)
print("✅ ALL 6 SEPARATE PLOTS GENERATED SUCCESSFULLY!")
print("="*70)
