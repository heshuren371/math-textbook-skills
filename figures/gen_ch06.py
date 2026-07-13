#!/usr/bin/env python3
"""第6章：三角函数（上）——正弦与余弦矢量图"""
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
# 图1：单位圆——sin和cos的几何定义
# ============================================================
fig, ax = plt.subplots(figsize=(7, 7))
theta = np.linspace(0, 2*np.pi, 400)
ax.plot(np.cos(theta), np.sin(theta), 'b-', lw=2, label='单位圆 x²+y²=1')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title('单位圆——sin 和 cos 的几何定义', fontsize=16)

# 画一个角度（60度）
angle = np.pi/3
ax.plot([0, np.cos(angle)], [0, np.sin(angle)], 'r-', lw=2)
ax.plot([0, np.cos(angle)], [0, 0], 'g--', lw=1.5, label='cos(θ)=邻边/斜边')
ax.plot([np.cos(angle), np.cos(angle)], [0, np.sin(angle)], 'orange', lw=1.5, ls='--', label='sin(θ)=对边/斜边')
# 标注
ax.scatter([np.cos(angle)], [np.sin(angle)], color='red', s=100, zorder=5)
ax.annotate(f'P({np.cos(angle):.2f}, {np.sin(angle):.2f})',
            (np.cos(angle), np.sin(angle)), xytext=(10, 5),
            textcoords='offset points', fontsize=12)
ax.annotate('θ=60°', (0.2, 0.1), fontsize=13)
# 弧线
arc_theta = np.linspace(0, angle, 100)
ax.plot(0.3*np.cos(arc_theta), 0.3*np.sin(arc_theta), 'k-', lw=1.5)
ax.legend(fontsize=12, loc='upper left')
save('ch06_unit_circle')

# ============================================================
# 图2：y=sin(x) 的图像——标注周期、振幅、关键点
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
x = np.linspace(-2*np.pi, 2*np.pi, 1000)
ax.plot(x, np.sin(x), '#2b83ba', lw=2.5, label='y = sin(x)')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.grid(True, alpha=0.3)
ax.set_title('正弦函数 y = sin(x)', fontsize=16)
ax.set_xlabel('x')
ax.set_ylabel('y')
# 标注关键点
key_x = [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
key_y = [0, 1, 0, -1, 0, 1, 0, -1, 0]
for kx, ky in zip(key_x, key_y):
    ax.scatter([kx], [ky], color='red', s=60, zorder=5)
# 标注周期
ax.annotate('周期 T=2π', xy=(0, -1.3), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
# 标注振幅
ax.annotate('振幅=1', xy=(np.pi, 1.2), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
ax.legend(fontsize=12)
# 画刻度标签
ax.set_xticks([-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π'])
save('ch06_sine_wave')

# ============================================================
# 图3：y=cos(x) 的图像
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
x = np.linspace(-2*np.pi, 2*np.pi, 1000)
ax.plot(x, np.cos(x), '#d7191c', lw=2.5, label='y = cos(x)')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.grid(True, alpha=0.3)
ax.set_title('余弦函数 y = cos(x)', fontsize=16)
ax.set_xlabel('x')
ax.set_ylabel('y')
# 关键点
key_x = [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
key_y = [1, 0, -1, 0, 1, 0, -1, 0, 1]
for kx, ky in zip(key_x, key_y):
    ax.scatter([kx], [ky], color='red', s=60, zorder=5)
ax.set_xticks([-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π'])
ax.legend(fontsize=12)
save('ch06_cosine_wave')

# ============================================================
# 图4：sin 和 cos 对比——相位差 π/2
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
x = np.linspace(-np.pi, 2*np.pi, 1000)
ax.plot(x, np.sin(x), '#2b83ba', lw=2.5, label='y = sin(x)')
ax.plot(x, np.cos(x), '#d7191c', lw=2.5, label='y = cos(x)')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-np.pi, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.grid(True, alpha=0.3)
ax.set_title('sin(x) 与 cos(x)——相位差 π/2', fontsize=16)
ax.set_xlabel('x')
ax.set_ylabel('y')
# 标注相位差
ax.annotate('sin 比 cos\n领先 π/2', xy=(np.pi/2, 0.5), fontsize=13,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π'])
ax.legend(fontsize=12, loc='upper right')
save('ch06_sine_cosine_compare')

# ============================================================
# 图5：不同振幅和周期的正弦波
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
x = np.linspace(0, 2*np.pi, 1000)
ax.plot(x, np.sin(x), '#2b83ba', lw=2.5, label='y = sin(x)')
ax.plot(x, 2*np.sin(x), '#d7191c', lw=2, label='y = 2sin(x)（振幅=2）')
ax.plot(x, np.sin(2*x), '#fdae61', lw=2, label='y = sin(2x)（周期=π）')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-2.5, 2.5)
ax.grid(True, alpha=0.3)
ax.set_title('振幅与周期的变化', fontsize=16)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
ax.legend(fontsize=12)
save('ch06_amplitude_period')

print('\n第6章图像全部生成完成！')
