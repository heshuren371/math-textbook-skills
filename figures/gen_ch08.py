#!/usr/bin/env python3
"""第8章：函数的四大性质——矢量图"""
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
# 图1：单调递增 vs 单调递减
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

x = np.linspace(-2, 2, 400)
ax1.plot(x, x**3, '#2b83ba', lw=2.5)
ax1.axhline(0, color='gray', lw=0.8)
ax1.axvline(0, color='gray', lw=0.8)
ax1.set_title('单调递增 —— x 越大 y 越大', fontsize=15)
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-3, 3)
ax1.grid(True, alpha=0.3)
# 标注
ax1.annotate('x₁<x₂ ⇒ f(x₁)<f(x₂)', xy=(-1, 0), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

x = np.linspace(-2, 2, 400)
ax2.plot(x, -x**3, '#d7191c', lw=2.5)
ax2.axhline(0, color='gray', lw=0.8)
ax2.axvline(0, color='gray', lw=0.8)
ax2.set_title('单调递减 —— x 越大 y 越小', fontsize=15)
ax2.set_xlim(-2.5, 2.5)
ax2.set_ylim(-3, 3)
ax2.grid(True, alpha=0.3)
ax2.annotate('x₁<x₂ ⇒ f(x₁)>f(x₂)', xy=(-1, 0), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightpink', alpha=0.3))

plt.tight_layout()
save('ch08_monotonic')

# ============================================================
# 图2：有界函数 vs 无界函数
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

x = np.linspace(-2, 2, 400)
ax1.plot(x, np.sin(x), '#2b83ba', lw=2.5, label='sin(x)')
ax1.axhline(1, color='red', ls='--', lw=1, alpha=0.7, label='y=1')
ax1.axhline(-1, color='red', ls='--', lw=1, alpha=0.7, label='y=-1')
ax1.axhline(0, color='gray', lw=0.8)
ax1.axvline(0, color='gray', lw=0.8)
ax1.set_title('有界函数 —— |sin(x)| ≤ 1', fontsize=15)
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-1.8, 1.8)
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=12)

x = np.linspace(-2, 2, 400)
ax2.plot(x, x**3, '#d7191c', lw=2.5, label='x³')
ax2.axhline(0, color='gray', lw=0.8)
ax2.axvline(0, color='gray', lw=0.8)
ax2.set_title('无界函数 —— x³ 无上下界', fontsize=15)
ax2.set_xlim(-2.5, 2.5)
ax2.set_ylim(-3, 3)
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=12)

plt.tight_layout()
save('ch08_bounded')

# ============================================================
# 图3：反函数关于 y=x 对称
# ============================================================
fig, ax = plt.subplots(figsize=(7, 7))
x1 = np.linspace(0.05, 3, 400)
ax.plot(x1, np.log(x1), '#d7191c', lw=2.5, label='y = ln(x)')
x2 = np.linspace(-1, 2, 400)
ax.plot(x2, np.exp(x2), '#2b83ba', lw=2.5, label='y = e^x')
x_line = np.linspace(-1, 3, 100)
ax.plot(x_line, x_line, 'k--', lw=1, alpha=0.5, label='y = x')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-1, 3)
ax.set_ylim(-1, 3)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title('反函数关于 y=x 对称', fontsize=16)
ax.legend(fontsize=12)
ax.annotate('(1,0) 和 (0,1) 对称', xy=(0.15, 0.15), fontsize=12)
save('ch08_inverse_function')

print('\n第8章图像全部生成完成！')
