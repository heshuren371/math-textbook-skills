#!/usr/bin/env python3
"""第15-16章：连续函数——矢量图"""
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

# 1: 连续 vs 间断
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
x = np.linspace(-2, 2, 400)
ax1.plot(x, x**2, '#2b83ba', lw=2.5)
ax1.set_title('连续函数 —— 一笔画', fontsize=15)
ax1.grid(True, alpha=0.3)

x = np.linspace(-2, -0.01, 200)
ax2.plot(x, x, '#d7191c', lw=2.5)
x = np.linspace(0.01, 2, 200)
ax2.plot(x, x+1, '#d7191c', lw=2.5)
ax2.scatter([0], [0], color='white', s=100, edgecolors='#d7191c', linewidths=2, zorder=5)
ax2.scatter([0], [1], color='#d7191c', s=100, zorder=5)
ax2.set_title('间断函数 —— 笔要断开', fontsize=15)
ax2.grid(True, alpha=0.3)
plt.tight_layout()
save('ch15_continuous_vs_discontinuous')

# 2: 介值定理
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0, 5, 400)
y = 0.5*(x-2.5)**3 + 2
ax.plot(x, y, '#2b83ba', lw=2.5)
ax.axhline(1, color='red', ls='--', alpha=0.7)
ax.axhline(3, color='red', ls='--', alpha=0.7)
ax.axvline(0.6, color='gray', ls=':', alpha=0.5)
ax.axvline(4.4, color='gray', ls=':', alpha=0.5)
ax.scatter([0.6, 4.4], [1, 3], color='red', s=80, zorder=5)
ax.annotate('f(a)=1', (0.6, 0.8), fontsize=12)
ax.annotate('f(b)=3', (4.4, 3.2), fontsize=12)
# 中间值2
ax.axhline(2, color='green', ls='--', alpha=0.5)
ax.scatter([2.5], [2], color='green', s=80, zorder=5)
ax.annotate('存在c使f(c)=2', (2.5, 2.2), fontsize=12)
ax.set_title('介值定理：连续函数取遍中间所有值', fontsize=14)
ax.grid(True, alpha=0.3)
save('ch16_intermediate_value')

print('完成')
