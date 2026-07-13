#!/usr/bin/env python3
"""第10章：数列极限的直观——矢量图"""
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
# 图1：收敛数列 a_n = 1/n → 0
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
n = np.arange(1, 21)
a_n = 1/n
ax.scatter(n, a_n, color='#2b83ba', s=80, zorder=5)
ax.plot(n, a_n, '#2b83ba', lw=1, ls='--', alpha=0.3)
ax.axhline(0, color='red', ls='-', lw=2, alpha=0.7, label='极限 L = 0')
ax.set_title('收敛数列  a_n = 1/n → 0', fontsize=16)
ax.set_xlabel('n')
ax.set_ylabel('a_n')
ax.set_xticks(n[::2])
ax.grid(True, alpha=0.3)
ax.legend(fontsize=12)
ax.set_ylim(-0.05, 1.1)
ax.annotate('n 越大，a_n 越接近 0', xy=(15, 0.3), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
save('ch10_convergent')

# ============================================================
# 图2：发散数列 a_n = n → ∞
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
n = np.arange(1, 11)
a_n = n
ax.scatter(n, a_n, color='#d7191c', s=80, zorder=5)
ax.plot(n, a_n, '#d7191c', lw=1, ls='--', alpha=0.3)
ax.set_title('发散数列  a_n = n → ∞', fontsize=16)
ax.set_xlabel('n')
ax.set_ylabel('a_n')
ax.set_xticks(n)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 12)
save('ch10_divergent')

# ============================================================
# 图3：振荡发散 a_n = (-1)^n
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
n = np.arange(1, 16)
a_n = (-1)**n
ax.scatter(n, a_n, color='#5e3c99', s=100, zorder=5)
ax.plot(n, a_n, '#5e3c99', lw=1, ls='--', alpha=0.3)
ax.axhline(0, color='gray', lw=0.8)
ax.set_title('振荡发散  a_n = (-1)^n（不趋近任何数）', fontsize=16)
ax.set_xlabel('n')
ax.set_ylabel('a_n')
ax.set_xticks(n)
ax.grid(True, alpha=0.3)
ax.set_ylim(-1.5, 1.5)
ax.annotate('在 -1 和 1 之间来回跳\n永远不固定', xy=(10, 0.5), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightpink', alpha=0.3))
save('ch10_oscillating_divergent')

# ============================================================
# 图4：极限的"ε带形"几何意义
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
N = 30
n = np.arange(1, N+1)
a_n = 1/n + 0.5*np.sin(n/2)/n  # 趋近0，带点波动
# 实际用 1/n 来展示，更清晰
a_n = 1/n
ax.scatter(n, a_n, color='#2b83ba', s=60, zorder=5, label='a_n')
L = 0
eps = 0.15
# 画ε带
ax.fill_between(range(1, N+1), L-eps, L+eps, color='red', alpha=0.1, label=f'ε={eps} 的带')
# 标出N
ax.axhline(L, color='red', lw=2, alpha=0.7)
ax.axhline(L+eps, color='red', ls='--', lw=1, alpha=0.5)
ax.axhline(L-eps, color='red', ls='--', lw=1, alpha=0.5)
# 从第10项开始就在带内了
ax.axvline(7, color='green', ls='-', lw=1.5, alpha=0.7, label='N=7 之后都在带内')
ax.set_title('极限的"ε带"——N 之后所有项都在带内', fontsize=15)
ax.set_xlabel('n')
ax.set_ylabel('a_n')
ax.set_xlim(0, N+1)
ax.set_ylim(-0.1, 1.1)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='upper right')
ax.annotate(f'n≥7 时\n|a_n-0|<{eps}', xy=(15, 0.05), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
save('ch10_epsilon_band')

print('\n第10章图像全部生成完成！')
