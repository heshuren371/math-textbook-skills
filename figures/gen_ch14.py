#!/usr/bin/env python3
"""第14章：ε-δ定义——矢量图"""
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

# 1: ε-δ 几何意义
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-1, 3, 400)
y = x**2 - x + 1
ax.plot(x, y, '#2b83ba', lw=2.5, label='f(x)')
L, a = 1, 1
eps, delta = 0.3, 0.35
ax.axhline(L, color='red', lw=1.5, alpha=0.7)
ax.axhline(L+eps, color='red', ls='--', lw=1, alpha=0.5)
ax.axhline(L-eps, color='red', ls='--', lw=1, alpha=0.5)
ax.axvline(a-delta, color='green', ls='--', lw=1, alpha=0.5)
ax.axvline(a+delta, color='green', ls='--', lw=1, alpha=0.5)
ax.fill_betweenx([L-eps, L+eps], a-delta, a+delta, color='yellow', alpha=0.15)
ax.scatter([a], [L], color='red', s=100, zorder=5)
ax.annotate('ε', xy=(2.5, L+eps+0.05), fontsize=16)
ax.annotate('δ', xy=(a+delta/2, L-0.3), fontsize=16)
ax.set_xlim(-1, 3)
ax.set_ylim(0, 3)
ax.grid(True, alpha=0.3)
ax.set_title('ε-δ 定义：|x-a|<δ ⇒ |f(x)-L|<ε', fontsize=14)
ax.legend(fontsize=12)
save('ch14_epsilon_delta')
print('完成')
