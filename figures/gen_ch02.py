#!/usr/bin/env python3
"""第2章：函数的图像——矢量图生成脚本"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# ── 全局设置 ──
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
    print(f'  ✓ {name}.pdf')

# ============================================================
# 图1：描点法画 y = x²
# ============================================================
fig, ax = plt.subplots(figsize=(7, 6))
ax.set_xlim(-4, 4)
ax.set_ylim(-1, 10)
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.grid(True, alpha=0.3)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('描点法画 y = x²')

# 曲线
xs = np.linspace(-3.5, 3.5, 200)
ax.plot(xs, xs**2, 'b-', lw=2, label='y = x²')

# 描点
points = [(-3,9), (-2,4), (-1,1), (0,0), (1,1), (2,4), (3,9)]
px, py = zip(*points)
ax.scatter(px, py, color='red', s=60, zorder=5, label='描点')
for x, y in points:
    ax.annotate(f'({x},{y})', (x, y), xytext=(5, 10),
                textcoords='offset points', fontsize=11, color='red')

ax.legend(fontsize=12)
save('ch02_sketch_x2')

# ============================================================
# 图2：六种基本函数对比（2×3子图）
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(14, 9))
funcs = [
    ('y = x', lambda x: x, (-3, 3), (-3, 3)),
    ('y = x²', lambda x: x**2, (-3, 3), (-1, 10)),
    ('y = x³', lambda x: x**3, (-3, 3), (-10, 10)),
    ('y = 1/x', lambda x: 1/x, (-3, 3), (-5, 5), True),
    ('y = |x|', lambda x: np.abs(x), (-3, 3), (-0.5, 3.5)),
    ('y = √x', lambda x: np.sqrt(x) if x >= 0 else np.nan, (-0.5, 5), (-0.5, 2.5)),
]

for ax, (title, f, xr, yr, *args) in zip(axes.flat, funcs):
    skip_zero = args[0] if args else False
    xs = np.linspace(xr[0], xr[1], 1000)
    ys = np.array([f(x) for x in xs])
    if skip_zero:
        ys[np.abs(xs) < 0.01] = np.nan
    ax.plot(xs, ys, 'b-', lw=2)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_xlim(*xr)
    ax.set_ylim(*yr)
    ax.set_title(title, fontsize=15)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

plt.tight_layout()
save('ch02_six_basic_funcs')

# ============================================================
# 图3：平移变换 —— y = x² → y = (x-2)² → y = x² + 3
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-4, 6, 400)
ax.plot(x, x**2, 'b-', lw=2, label='y = x²（原函数）')
ax.plot(x, (x-2)**2, 'r-', lw=2, label='y = (x-2)²（右移2）')
ax.plot(x, x**2 + 3, 'g-', lw=2, label='y = x² + 3（上移3）')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-3, 6)
ax.set_ylim(-1, 12)
ax.grid(True, alpha=0.3)
ax.set_title('图像的平移变换', fontsize=16)
ax.legend(fontsize=12)
ax.annotate('顶点 (0,0)', (0,0), xytext=(10,-30), textcoords='offset points',
            fontsize=11, arrowprops=dict(arrowstyle='->', color='blue'))
ax.annotate('顶点 (2,0)', (2,0), xytext=(10,-30), textcoords='offset points',
            fontsize=11, arrowprops=dict(arrowstyle='->', color='red'))
ax.annotate('顶点 (0,3)', (0,3), xytext=(10,10), textcoords='offset points',
            fontsize=11, arrowprops=dict(arrowstyle='->', color='green'))
save('ch02_translation')

# ============================================================
# 图4：对称变换 —— y = x² → y = -x²
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-3, 3, 400)
ax.plot(x, x**2, 'b-', lw=2, label='y = x²（开口向上）')
ax.plot(x, -x**2, 'r-', lw=2, label='y = -x²（开口向下）')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-10, 10)
ax.grid(True, alpha=0.3)
ax.set_title('图像的对称变换（关于 x 轴对称）', fontsize=16)
ax.legend(fontsize=12)
# 画对称连线
ax.plot([2, 2], [4, -4], 'k--', lw=0.8, alpha=0.6)
ax.plot([1, 1], [1, -1], 'k--', lw=0.8, alpha=0.6)
ax.annotate('(2,4)', (2,4), xytext=(5,5), textcoords='offset points', fontsize=11)
ax.annotate('(2,-4)', (2,-4), xytext=(5,5), textcoords='offset points', fontsize=11)
save('ch02_symmetry')

# ============================================================
# 图5：翻折变换 —— y = x²-1 和 y = |x²-1|
# ============================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(-3, 3, 500)
ax.plot(x, x**2 - 1, 'b--', lw=1.5, label='y = x² - 1（原函数）')
ax.plot(x, np.abs(x**2 - 1), 'r-', lw=2.5, label='y = |x² - 1|（翻折后）')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
# 填充翻折区域
x_fill = np.linspace(-1, 1, 200)
y_fill = x_fill**2 - 1
ax.fill_between(x_fill, 0, -y_fill, color='red', alpha=0.15)
ax.set_xlim(-3, 3)
ax.set_ylim(-1.5, 5)
ax.grid(True, alpha=0.3)
ax.set_title('图像的翻折变换——y = |f(x)|', fontsize=16)
ax.legend(fontsize=12)
ax.annotate('x 轴下方的部分\n翻折到上方', (0, -0.5), xytext=(80, -20),
            textcoords='offset points', fontsize=11,
            arrowprops=dict(arrowstyle='->', color='red'),
            bbox=dict(boxstyle='round', facecolor='pink', alpha=0.3))
save('ch02_abs_flip')

# ============================================================
# 图6：从图像读函数信息——定义域、值域、零点
# ============================================================
fig, ax = plt.subplots(figsize=(7, 5))
x = np.linspace(-2, 2, 400)
y = x**3 - x
ax.plot(x, y, 'b-', lw=2.5, label='f(x) = x³ - x')
ax.axhline(0, color='gray', lw=0.8)
ax.axvline(0, color='gray', lw=0.8)
# 标零点
zeros = [-1, 0, 1]
for z in zeros:
    ax.scatter([z], [0], color='red', s=80, zorder=5)
    ax.annotate(f'零点 x={z}', (z, 0), xytext=(10, -35),
                textcoords='offset points', fontsize=11,
                arrowprops=dict(arrowstyle='->', color='red'))
# 标定义域和值域
ax.annotate('定义域: R', xy=(1.5, 1.5), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
ax.annotate('值域: R', xy=(1.5, 1), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-1.5, 1.5)
ax.grid(True, alpha=0.3)
ax.set_title('从图像读信息：定义域·值域·零点', fontsize=15)
ax.legend(fontsize=12)
save('ch02_read_from_graph')

# ============================================================
# 图7：垂线检验法
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 左：是函数
x = np.linspace(-2, 2, 400)
ax1.plot(x, x**2, 'b-', lw=2)
ax1.axvline(1, color='red', ls='--', alpha=0.7)
ax1.set_title('[是] 函数\n每条竖线只交1个点', fontsize=13)
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-0.5, 4.5)
ax1.grid(True, alpha=0.3)

# 右：不是函数（圆）
theta = np.linspace(0, 2*np.pi, 400)
ax2.plot(2*np.cos(theta), 2*np.sin(theta), 'r-', lw=2)
ax2.axvline(0.5, color='red', ls='--', alpha=0.7)
ax2.set_title('[不是] 函数\n竖线 x=0.5 交了2个点', fontsize=13)
ax2.set_xlim(-2.5, 2.5)
ax2.set_ylim(-2.5, 2.5)
ax2.grid(True, alpha=0.3)
ax2.set_aspect('equal')

plt.tight_layout()
save('ch02_vertical_line_test')

# ============================================================
# 图8：y=1/x 的详细图（加渐近线）
# ============================================================
fig, ax = plt.subplots(figsize=(7, 6))
x = np.linspace(-5, 5, 2000)
y = 1/x
y[np.abs(x) < 0.02] = np.nan
ax.plot(x, y, 'b-', lw=2, label='y = 1/x')
ax.axhline(0, color='gray', lw=0.8, ls='--')
ax.axvline(0, color='gray', lw=0.8, ls='--')
# 渐近线标注
ax.annotate('水平渐近线 y=0', xy=(3.5, 0.1), fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
ax.annotate('垂直渐近线 x=0', xy=(0.2, 3), fontsize=12, rotation=90,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.grid(True, alpha=0.3)
ax.set_title('y = 1/x 的图像与渐近线', fontsize=16)
ax.legend(fontsize=12)
save('ch02_reciprocal')

print('\n全部图像生成完成！')
