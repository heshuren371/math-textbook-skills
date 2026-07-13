#!/usr/bin/env python3
"""第9章：数列基础——矢量图"""
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
# 图1：函数 vs 数列 对比（连续vs离散）
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 左：连续函数 y = x²
x = np.linspace(0, 5, 200)
ax1.plot(x, x**2, 'b-', lw=2, label='y = x²（连续）')
ax1.set_title('连续函数', fontsize=15)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=12)

# 右：数列 a_n = n²（离散）
n = np.arange(1, 6)
ax2.scatter(n, n**2, color='red', s=100, zorder=5, label='a_n = n²（离散）')
ax2.plot(n, n**2, 'r--', lw=1, alpha=0.3)
ax2.set_title('数列（离散点）', fontsize=15)
ax2.set_xlabel('n（项数）')
ax2.set_ylabel('a_n')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=12)
ax2.set_xticks([1,2,3,4,5])

plt.tight_layout()
save('ch09_continuous_vs_discrete')

# ============================================================
# 图2：等差数列 vs 等比数列
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

n = np.arange(1, 8)
# 左：等差 a_n = 2n - 1（奇数序列）
ax1.scatter(n, 2*n-1, color='#2b83ba', s=100, zorder=5)
ax1.plot(n, 2*n-1, '#2b83ba', lw=1.5, ls='--', alpha=0.3)
ax1.set_title('等差数列 a_n = 2n-1（公差=2）', fontsize=14)
ax1.set_xlabel('n')
ax1.set_ylabel('a_n')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(n)

# 右：等比 a_n = 2^(n-1)
ax2.scatter(n, 2**(n-1), color='#d7191c', s=100, zorder=5)
ax2.plot(n, 2**(n-1), '#d7191c', lw=1.5, ls='--', alpha=0.3)
ax2.set_title('等比数列 a_n = 2^(n-1)（公比=2）', fontsize=14)
ax2.set_xlabel('n')
ax2.set_ylabel('a_n')
ax2.grid(True, alpha=0.3)
ax2.set_xticks(n)

plt.tight_layout()
save('ch09_arithmetic_geometric')

# ============================================================
# 图3：摆动数列 a_n = (-1)^n / n
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
n = np.arange(1, 15)
a_n = (-1)**n / n
ax.scatter(n, a_n, color='#5e3c99', s=100, zorder=5)
ax.plot(n, a_n, '#5e3c99', lw=1, ls='--', alpha=0.3)
ax.axhline(0, color='gray', lw=0.8)
ax.set_title('摆动数列 a_n = (-1)^n / n', fontsize=16)
ax.set_xlabel('n')
ax.set_ylabel('a_n')
ax.grid(True, alpha=0.3)
ax.set_xticks(n)
# 标注趋近于0
ax.annotate('当 n 增大时\n振幅越来越小', xy=(12, -0.05), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
save('ch09_oscillating')

# ============================================================
# 图4：单调有界数列 a_n = 1 - 1/n
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
n = np.arange(1, 12)
a_n = 1 - 1/n
ax.scatter(n, a_n, color='#2b83ba', s=100, zorder=5, label='a_n = 1 - 1/n')
ax.plot(n, a_n, '#2b83ba', lw=1.5, ls='--', alpha=0.3)
ax.axhline(1, color='red', ls='--', lw=1, alpha=0.7, label='上界 y=1')
ax.set_title('单调递增有上界的数列', fontsize=16)
ax.set_xlabel('n')
ax.set_ylabel('a_n')
ax.grid(True, alpha=0.3)
ax.set_xticks(n)
ax.legend(fontsize=12)
ax.set_ylim(0, 1.2)
save('ch09_monotonic_bounded')

print('\n第9章图像全部生成完成！')
