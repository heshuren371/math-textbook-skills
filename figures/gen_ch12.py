#!/usr/bin/env python3
"""第12章：极限存在判别法——矢量图"""
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
# 图1：单调有界原理 —— a_n = 1-1/n 单调递增有上界
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
n = np.arange(1, 15)
a_n = 1 - 1/n
ax.scatter(n, a_n, color='#2b83ba', s=100, zorder=5, label='a_n = 1 - 1/n')
ax.plot(n, a_n, '#2b83ba', lw=1, ls='--', alpha=0.3)
ax.axhline(1, color='red', ls='-', lw=2, alpha=0.7, label='上界 y=1')
ax.fill_between(range(1, 16), 0, 1, color='green', alpha=0.05)
ax.set_title('单调递增有上界 ⇒ 收敛', fontsize=16)
ax.set_xlabel('n')
ax.set_ylabel('a_n')
ax.set_xlim(0, 16)
ax.set_ylim(0, 1.2)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=12)
ax.annotate('往上走，但不超过 1\n→ 极限存在', xy=(10, 0.4), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
save('ch12_monotone_bounded')

# ============================================================
# 图2：夹逼定理 —— 三个数列夹在一起
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
N = 30
n = np.arange(1, N+1)
lower = 1/n * (-1)**0  # 1/n
upper = 1/n + 0.5
mid = (lower + upper) / 2 + 0.2 * np.sin(n/3)/n

ax.scatter(n, lower, color='#2b83ba', s=30, alpha=0.7, label='b_n (下界)')
ax.scatter(n, upper, color='#d7191c', s=30, alpha=0.7, label='c_n (上界)')
ax.scatter(n, mid, color='#5e3c99', s=40, alpha=0.9, label='a_n (被夹住)')

ax.fill_between(range(1, N+1), lower, upper, color='gray', alpha=0.08)
ax.axhline(0, color='red', ls='-', lw=1, alpha=0.5)
ax.set_title('夹逼定理：若 b_n → L, c_n → L, 则 a_n → L', fontsize=14)
ax.set_xlabel('n')
ax.set_ylabel('a_n')
ax.set_xlim(0, N+1)
ax.set_ylim(-0.1, 1.0)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='upper right')
save('ch12_squeeze_theorem')

print('\n第12章图像全部生成完成！')
