#!/usr/bin/env python3
"""第11章：ε-N 语言——矢量图"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['PingFang SC', 'Heiti SC'],
    'font.size': 14,
    'axes.unicode_minus': False,
    'figure.dpi': 150,
})
OUT = '/Users/heshuren/math-analysis/figures'
os.makedirs(OUT, exist_ok=True)

def save(name):
    plt.savefig(f'{OUT}/{name}.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print(f'  OK {name}.pdf')

# ============================================================
# 图1：ε-N 定义核心图示 —— 更小的ε需要更大的N
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

N = 30
ns = np.arange(1, N+1)
a_n = 1/ns

for ax, eps, n_label in [(ax1, 0.2, 5), (ax2, 0.1, 10)]:
    ax.scatter(ns, a_n, color='#2b83ba', s=50, zorder=5)
    ax.plot(ns, a_n, '#2b83ba', lw=1, alpha=0.3)
    ax.axhline(0, color='red', lw=2)
    ax.fill_between(range(1, N+1), -eps, eps, color='red', alpha=0.1)
    ax.axhline(eps, color='red', ls='--', lw=1, alpha=0.5)
    ax.axhline(-eps, color='red', ls='--', lw=1, alpha=0.5)
    ax.axvline(n_label, color='green', ls='-', lw=1.5, alpha=0.7)
    ax.annotate(f'N={n_label}', xy=(n_label, 0.6), fontsize=13,
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    ax.set_title(f'ε={eps}：需要 N={n_label}', fontsize=15)
    ax.set_xlabel('n')
    ax.set_ylabel('a_n')
    ax.set_xlim(0, N+1)
    ax.set_ylim(-0.15, 1.1)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
save('ch11_epsilon_N_demo')

# ============================================================
# 图2：ε-N 证明的"阶梯"图 —— 直观展示 |a_n - L| < ε
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
N = 30
ns = np.arange(1, N+1)
a_n = 1/(ns+10)  # 收敛到0
ax.scatter(ns, a_n, color='#2b83ba', s=50, zorder=5)
ax.plot(ns, a_n, '#2b83ba', lw=1, alpha=0.3)
L = 0
eps = 0.05
ax.axhline(L, color='red', lw=2, label=f'L = {L}')
ax.axhline(L+eps, color='red', ls='--', lw=1, alpha=0.5, label=f'ε = {eps}')
ax.axhline(L-eps, color='red', ls='--', lw=1, alpha=0.5)
# 找出第一个进入带内的n
for i, val in enumerate(a_n, 1):
    if abs(val - L) < eps:
        ax.axvline(i, color='green', ls='-', lw=1.5, alpha=0.7, label=f'N={i}')
        ax.annotate(f'n≥{i} 后\n都在带内', xy=(i, 0.08), fontsize=12,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
        break
ax.set_xlabel('n')
ax.set_ylabel('a_n')
ax.set_xlim(0, N+1)
ax.set_ylim(-0.02, 0.35)
ax.grid(True, alpha=0.3)
ax.set_title('ε-N 证明：找到 N 使得 n ≥ N 时 |a_n - L| < ε', fontsize=14)
ax.legend(fontsize=11)
save('ch11_epsilon_N_proof')

print('\n第11章图像全部生成完成！')
