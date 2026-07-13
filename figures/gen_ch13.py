#!/usr/bin/env python3
"""第13章：函数在无穷远处的极限——矢量图"""
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

# 1: 水平渐近线 —— 1/x → 0
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(-10, -0.1, 1000)
ax.plot(x, 1/x, '#2b83ba', lw=2, label='y=1/x')
x = np.linspace(0.1, 10, 1000)
ax.plot(x, 1/x, '#2b83ba', lw=2)
ax.axhline(0, color='red', ls='--', lw=1.5, alpha=0.7, label='y=0（水平渐近线）')
ax.set_xlim(-10, 10)
ax.set_ylim(-3, 3)
ax.grid(True, alpha=0.3)
ax.set_title('水平渐近线  lim_{x→∞} 1/x = 0', fontsize=15)
ax.legend(fontsize=12)
ax.set_xlabel('x')
ax.set_ylabel('y')
save('ch13_horizontal_asymptote')

# 2: 不同增长速度对比
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0.1, 10, 400)
ax.plot(x, np.log(x), '#2b83ba', lw=2, label='ln(x)')
ax.plot(x, x**0.5, '#fdae61', lw=2, label='sqrt(x)')
ax.plot(x, x, '#aaaaaa', lw=1, ls='--', label='x')
ax.plot(x, x**2, '#d7191c', lw=2, label='x^2')
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.grid(True, alpha=0.3)
ax.set_title('x→∞时不同函数的增长速度', fontsize=15)
ax.legend(fontsize=11)
ax.set_xlabel('x')
ax.set_ylabel('y')
save('ch13_growth_rates')

# 3: 函数趋于无穷
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0.1, 5, 400)
ax.plot(x, 1/x, '#2b83ba', lw=2, label='y=1/x → ∞ (x→0⁺)')
ax.axvline(0, color='red', ls='--', lw=1.5, alpha=0.7, label='垂直渐近线 x=0')
ax.set_xlim(-0.5, 5)
ax.set_ylim(-5, 20)
ax.grid(True, alpha=0.3)
ax.set_title('垂直渐近线  lim_{x→0⁺} 1/x = ∞', fontsize=15)
ax.legend(fontsize=12)
ax.set_xlabel('x')
ax.set_ylabel('y')
save('ch13_vertical_asymptote')

print('\n第13章图像全部生成完成！')
