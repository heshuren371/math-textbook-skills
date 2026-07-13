"""
mathplot.py — 一键配置 Matplotlib 中文 + 数学风格

用法:
    import mathplot    # 自动启用中文 + 默认样式
    from mathplot import savefig, figure, subplots, demo
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ── 查找系统中可用的中文字体 ──
_CANDIDATES = ['PingFang SC', 'Heiti SC', 'Hiragino Sans GB',
               'STKaiti', 'STSong', 'SimSun', 'SimHei']
_FOUND = None
for c in _CANDIDATES:
    try:
        fp = fm.findfont(c, fallback_to_default=False)
        if 'DejaVu' not in fp:
            _FOUND = c
            break
    except Exception:
        continue

if _FOUND:
    plt.rcParams['font.sans-serif'] = [_FOUND] + plt.rcParams['font.sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
else:
    print('⚠️ mathplot: 未找到中文字体')

# ── 默认样式 ──
plt.rcParams.update({
    'figure.figsize': (8, 5), 'figure.dpi': 120, 'savefig.dpi': 150,
    'font.size': 11, 'axes.titlesize': 13, 'axes.labelsize': 11,
    'legend.fontsize': 9, 'xtick.labelsize': 9, 'ytick.labelsize': 9,
    'axes.grid': True, 'grid.alpha': 0.3,
})


def savefig(path, dpi=150):
    plt.savefig(path, dpi=dpi, bbox_inches='tight')
    print(f'  📈 已保存: {path} ({dpi}dpi)')


def subplots(*args, **kwargs):
    return plt.subplots(*args, **kwargs)


def demo():
    import numpy as np
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    x = np.linspace(-3, 3, 300)
    axes[0].plot(x, np.exp(x), 'b-', label='exp(x)', linewidth=2)
    axes[0].plot(x, np.log(np.maximum(x, 1e-10)), 'r-', label='log(x)', linewidth=2)
    axes[0].plot(x, 1/(1+np.exp(-x)), 'g-', label='sigmoid(x)', linewidth=2)
    axes[0].axhline(0, color='gray', lw=0.5)
    axes[0].axvline(0, color='gray', lw=0.5)
    axes[0].set_title('常用函数曲线')
    axes[0].legend()
    xs = np.linspace(-4, 4, 200)
    ys = np.linspace(-4, 4, 200)
    X, Y = np.meshgrid(xs, ys)
    Z = (1.5 - X + X*Y)**2 + (2.25 - X + X*Y**2)**2 + (2.625 - X + X*Y**3)**2
    axes[1].contour(X, Y, np.log(Z+1e-10), levels=20, cmap='viridis', linewidths=0.8)
    axes[1].set_title('Beale 函数 (log 等高线)')
    plt.tight_layout()
    savefig('/tmp/mathplot-demo.png')
    plt.close()
