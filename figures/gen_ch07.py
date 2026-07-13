#!/usr/bin/env python3
"""第7章：三角函数（下）——正切、恒等式、反三角"""
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
# 图1：y=tan(x) 的图像
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
x = np.linspace(-2*np.pi, 2*np.pi, 2000)
y = np.tan(x)
# 处理渐近线
mask = np.abs(np.cos(x)) > 1e-10
x_plot = x[mask]
y_plot = y[mask]
ax.plot(x_plot, y_plot, '#d7191c', lw=2, label='y = tan(x)')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-5, 5)
ax.grid(True, alpha=0.3)
ax.set_title('正切函数 y = tan(x)', fontsize=16)
ax.set_xlabel('x')
ax.set_ylabel('y')
# 画渐近线
for k in range(-2, 3):
    ax.axvline((k+0.5)*np.pi, color='gray', ls='--', lw=0.8, alpha=0.5)
ax.set_xticks([-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π'])
ax.annotate('渐近线 x=π/2', xy=(np.pi/2, 3.5), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
ax.legend(fontsize=12)
ax.set_ylim(-5, 5)
save('ch07_tangent')

# ============================================================
# 图2：sin, cos, tan 对比
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
x = np.linspace(-np.pi, 2*np.pi, 2000)
ax.plot(x, np.sin(x), '#2b83ba', lw=2, label='sin(x)')
ax.plot(x, np.cos(x), '#fdae61', lw=2, label='cos(x)')
# tan 单独画（需要处理渐近线）
x_tan = np.linspace(-np.pi, 2*np.pi, 2000)
mask = np.abs(np.cos(x_tan)) > 1e-10
ax.plot(x_tan[mask], np.tan(x_tan)[mask], '#d7191c', lw=2, label='tan(x)')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-np.pi, 2*np.pi)
ax.set_ylim(-3, 3)
ax.grid(True, alpha=0.3)
ax.set_title('sin(x)、cos(x)、tan(x) 对比', fontsize=16)
ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π'])
ax.legend(fontsize=12)
save('ch07_sin_cos_tan')

# ============================================================
# 图3：arcsin(x) 和 arccos(x) 反三角函数
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 左：arcsin
x = np.linspace(-1, 1, 400)
ax1.plot(x, np.arcsin(x), '#2b83ba', lw=2.5, label='y = arcsin(x)')
ax1.axhline(0, color='gray', lw=0.8)
ax1.axvline(0, color='gray', lw=0.8)
ax1.set_xlim(-1.2, 1.2)
ax1.set_ylim(-np.pi/2-0.2, np.pi/2+0.2)
ax1.grid(True, alpha=0.3)
ax1.set_title('y = arcsin(x)', fontsize=16)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
# 标注值域
ax1.annotate('值域[-π/2, π/2]', xy=(0, -1.2), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
ax1.set_yticks([-np.pi/2, -np.pi/4, 0, np.pi/4, np.pi/2])
ax1.set_yticklabels(['-π/2', '-π/4', '0', 'π/4', 'π/2'])

# 右：arccos
ax2.plot(x, np.arccos(x), '#d7191c', lw=2.5, label='y = arccos(x)')
ax2.axhline(0, color='gray', lw=0.8)
ax2.axvline(0, color='gray', lw=0.8)
ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-0.2, np.pi+0.2)
ax2.grid(True, alpha=0.3)
ax2.set_title('y = arccos(x)', fontsize=16)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.annotate('值域[0, π]', xy=(0, 2.5), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
ax2.set_yticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax2.set_yticklabels(['0', 'π/4', 'π/2', '3π/4', 'π'])

plt.tight_layout()
save('ch07_arcsin_arccos')

# ============================================================
# 图4：arctan(x)
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-10, 10, 1000)
ax.plot(x, np.arctan(x), '#5e3c99', lw=2.5, label='y = arctan(x)')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.axhline(np.pi/2, color='gray', ls='--', lw=0.8, alpha=0.5)
ax.axhline(-np.pi/2, color='gray', ls='--', lw=0.8, alpha=0.5)
ax.set_xlim(-10, 10)
ax.set_ylim(-2, 2)
ax.grid(True, alpha=0.3)
ax.set_title('y = arctan(x)——值域(-π/2, π/2)', fontsize=16)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.annotate('水平渐近线 y=π/2', xy=(5, 1.7), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))
ax.annotate('水平渐近线 y=-π/2', xy=(5, -1.7), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))
ax.legend(fontsize=12)
save('ch07_arctan')

print('\n第7章图像全部生成完成！')
