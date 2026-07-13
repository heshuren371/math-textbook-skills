"""
数学教材图绘制模板—复制此文件后修改，保持统一风格。

规范要点：
- figsize 固定，用 set_xlim/set_ylim 控制坐标范围
- 主体线 lw=2.0，辅助线 lw=1.0，遮挡线 linestyle='--'
- 中文：PingFang SC，数学：STIXGeneral
- 保存时同时出 PDF + PNG，dpi=200
- 标注文字与图形间距 ≥ 0.15 坐标单位
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Polygon, Ellipse
import os

OUT = '/Users/heshuren/math-notes-zhongce/figures'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['PingFang SC', 'Heiti SC', 'STHeiti', 'Arial Unicode MS'],
    'mathtext.fontset': 'stix',
    'font.size': 11,
    'axes.unicode_minus': False,
})

# ── 颜色常量 ──
C_MAIN = '#000000'   # 主体线
C_AUX  = '#555555'   # 辅助线
C_BLUE = '#1a5276'   # 蓝色标注
C_RED  = '#922b21'   # 红色标注
C_FILL = '#eaf2f8'   # 填充背景

# ── 保存函数 ──
def save(fig, name, out_dir=OUT):
    """保存图片为 PDF + PNG。
    
    注意：bbox_inches='tight' 会让每张图的最终尺寸不同，
    如果需要所有图在 LaTeX 中插入时大小一致，
    应用固定 figsize + set_xlim/set_ylim 而非依赖 tight。"""
    path = os.path.join(out_dir, name)
    fig.savefig(path + '.pdf', format='pdf', bbox_inches='tight', pad_inches=0.08)
    fig.savefig(path + '.png', format='png', dpi=200, bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)
    print(f'  ✓ {name}')

def new_fig(w=5.0, h=3.8):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect('equal')
    return fig, ax

# ── 常用绘图函数 ──
def draw_angle_arc(ax, cx, cy, r, theta1, theta2, **kw):
    """
    绘制角度弧线，验证 theta1/theta2 与实际几何关系一致。
    
    theta1/theta2 是以水平向右为 0°、逆时针方向为正的角度（单位：度）。
    必须根据实际几何关系计算，不能凭感觉填写。
    """
    arc = Arc((cx, cy), 2*r, 2*r, theta1=theta1, theta2=theta2,
              lw=kw.get('lw', 1.5), color=kw.get('color', C_BLUE))
    ax.add_patch(arc)

def draw_right_angle(ax, x, y, s=0.3, orientation='br'):
    """绘制直角标记。orientation: 'br'=bottom-right, 'bl', 'tr', 'tl'"""
    dx = s if 'r' in orientation else -s
    dy = s if 't' in orientation else -s
    ax.plot([x, x+dx], [y, y], '-', color=C_MAIN, lw=1.2)
    ax.plot([x, x], [y, y+dy], '-', color=C_MAIN, lw=1.2)

def draw_triangle(ax, verts, **kw):
    """
    绘制三角形，验证顶点与标签对应。
    
    verts 必须是三个 (x,y) 元组的列表，
    标签必须与此列表完全对应，不能凭感觉写其他坐标。
    """
    tri = Polygon(verts, closed=True, fill=kw.get('fill', None),
                  edgecolor=kw.get('edgecolor', C_MAIN),
                  lw=kw.get('lw', 2.0))
    if 'facecolor' in kw:
        tri.set_facecolor(kw['facecolor'])
        tri.set_alpha(kw.get('alpha', 0.5))
    ax.add_patch(tri)

# ── 示例：在此处编写具体图形 ──
def example_demo():
    fig, ax = new_fig(4, 3)
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 4)
    ax.axis('off')

    # 主体图形：直角三角形
    draw_triangle(ax, [(0, 0), (4, 0), (0, 3)])
    draw_right_angle(ax, 0, 0, s=0.4)

    # 标注（与顶点完全对应）
    ax.text(2, -0.35, '$a$', ha='center', fontsize=12)
    ax.text(-0.35, 1.5, '$b$', va='center', fontsize=12)
    ax.text(1.7, 1.7, '$c$', fontsize=12, rotation=-37)

    save(fig, 'example_demo')

if __name__ == '__main__':
    example_demo()
