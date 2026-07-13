#!/usr/bin/env python3
"""第3章：幂函数与多项式——矢量图生成脚本"""
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
# 图1：正整数幂函数对比（n=1,2,3,4）
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-2, 2, 400)
powers = [(1, 'y = x\xb9', '#2b83ba'),
          (2, 'y = x\xb2', '#d7191c'),
          (3, 'y = x\xb3', '#fdae61'),
          (4, 'y = x\xb4', '#5e3c99')]
for n, label, color in powers:
    ax.plot(x, x**n, color=color, lw=2.5, label=label)
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 4)
ax.grid(True, alpha=0.3)
ax.set_title('正整数幂函数对比', fontsize=16)
ax.legend(fontsize=12, loc='upper left')
# 标公共点(1,1)
ax.scatter([1], [1], color='black', s=80, zorder=5, edgecolors='black')
ax.annotate('(1,1)', (1,1), xytext=(8,5), textcoords='offset points', fontsize=12)
# 标原点
ax.scatter([0], [0], color='black', s=40, zorder=5)
save('ch03_positive_powers')

# ============================================================
# 图2：负整数幂函数（n=-1, -2）和分数幂（n=1/2, 1/3）
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 左图：负整数幂
x1 = np.linspace(-3, 3, 2000)
x1_pos = x1[x1 > 0.05]
x1_neg = x1[x1 < -0.05]
for x_range, label_suffix, linestyle in [(x1_pos, '(x>0)', '-'), (x1_neg, '(x<0)', '--')]:
    if len(x_range) == 0:
        continue
    y1 = 1/x_range
    y2 = 1/(x_range**2)
    ax1.plot(x_range, y1, '#d7191c', lw=2.5, label=f'y=1/x {label_suffix}' if label_suffix=='(x>0)' else None)
    ax1.plot(x_range, y2, '#2b83ba', lw=2, label=f'y=1/x\xb2 {label_suffix}' if label_suffix=='(x>0)' else None,
             linestyle=linestyle)
ax1.axhline(0, color='gray', lw=0.8)
ax1.axvline(0, color='gray', lw=0.8)
ax1.set_xlim(-3, 3)
ax1.set_ylim(-5, 5)
ax1.grid(True, alpha=0.3)
ax1.set_title('负整数幂', fontsize=16)
ax1.legend(fontsize=11)
ax1.set_xlabel('x')
ax1.set_ylabel('y')

# 右图：分数幂（定义域x>=0）
x2 = np.linspace(0, 4, 400)
ax2.plot(x2, x2**0.5, '#d7191c', lw=2.5, label='y = x^(1/2) = sqrt(x)')
ax2.plot(x2, x2**(1/3), '#2b83ba', lw=2.5, label='y = x^(1/3) = cbrt(x)')
ax2.plot(x2, x2**(1/4), '#fdae61', lw=2, label='y = x^(1/4)')
ax2.plot(x2, x2, 'k--', lw=1, alpha=0.5, label='y = x（参考线）')
ax2.axhline(0, color='gray', lw=0.8)
ax2.axvline(0, color='gray', lw=0.8)
ax2.set_xlim(-0.2, 4)
ax2.set_ylim(-0.2, 2.5)
ax2.grid(True, alpha=0.3)
ax2.set_title('分数幂（n>0）', fontsize=16)
ax2.legend(fontsize=11)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
# 标(1,1)
ax2.scatter([1], [1], color='black', s=80, zorder=5)
ax2.annotate('(1,1)', (1,1), xytext=(8,5), textcoords='offset points', fontsize=12)

plt.tight_layout()
save('ch03_power_variants')

# ============================================================
# 图3：多项式 f(x) = (x+2)(x-1)(x-3) 
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-3, 4, 400)
y = (x+2)*(x-1)*(x-3)
ax.plot(x, y, '#2b83ba', lw=2.5, label='f(x) = (x+2)(x-1)(x-3)')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
# 标根
for root, color_root in [(-2, 'red'), (1, 'red'), (3, 'red')]:
    ax.scatter([root], [0], color=color_root, s=150, zorder=5, edgecolors='black')
    ax.annotate(f'x={root}', (root, 0), xytext=(0, -35),
                textcoords='offset points', fontsize=13, color='red',
                fontweight='bold', ha='center',
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
ax.set_xlim(-3.5, 4.5)
ax.set_ylim(-8, 10)
ax.grid(True, alpha=0.3)
ax.set_title('三次多项式 f(x) = (x+2)(x-1)(x-3)', fontsize=15)
ax.legend(fontsize=12)
save('ch03_cubic_polynomial')

# ============================================================
# 图4：重根现象 —— f(x) = (x-1)(x-2)^2
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-0.5, 4, 400)
y = (x-1)*(x-2)**2
ax.plot(x, y, '#d7191c', lw=2.5, label='f(x) = (x-1)(x-2)^2')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
# 标根
roots = [(1, '单根（穿过）'), (2, '重根（弹回）')]
for r, desc in roots:
    ax.scatter([r], [0], color='red', s=150, zorder=5, edgecolors='black')
    ax.annotate(f'x={r}\\n{desc}', (r, 0), xytext=(0, -40),
                textcoords='offset points', fontsize=12, color='red',
                ha='center',
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
ax.set_xlim(-0.5, 4)
ax.set_ylim(-2, 4)
ax.grid(True, alpha=0.3)
ax.set_title('重根的效果——f(x) = (x-1)(x-2)\xb2', fontsize=15)
ax.legend(fontsize=12, loc='upper left')
save('ch03_double_root')

# ============================================================
# 图5：正偶次幂 vs 正奇次幂的行为
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

x_left = np.linspace(-2.5, 2.5, 400)
ax1.plot(x_left, x_left**4, '#2b83ba', lw=2.5, label='y = x^4')
ax1.plot(x_left, x_left**6, '#d7191c', lw=2, label='y = x^6')
ax1.axhline(0, color='gray', lw=0.8)
ax1.axvline(0, color='gray', lw=0.8)
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-1, 20)
ax1.grid(True, alpha=0.3)
ax1.set_title('偶次幂：两端都向上', fontsize=15)
ax1.legend(fontsize=12)
ax1.set_xlabel('x')
ax1.set_ylabel('y')

x_right = np.linspace(-2.5, 2.5, 400)
ax2.plot(x_right, x_right**3, '#2b83ba', lw=2.5, label='y = x^3')
ax2.plot(x_right, x_right**5, '#d7191c', lw=2, label='y = x^5')
ax2.axhline(0, color='gray', lw=0.8)
ax2.axvline(0, color='gray', lw=0.8)
ax2.set_xlim(-2.5, 2.5)
ax2.set_ylim(-20, 20)
ax2.grid(True, alpha=0.3)
ax2.set_title('奇次幂：一端向下、一端向上', fontsize=15)
ax2.legend(fontsize=12)
ax2.set_xlabel('x')
ax2.set_ylabel('y')

plt.tight_layout()
save('ch03_even_vs_odd')

print('\n第3章图像全部生成完成！')
