"""
geometry3d.py — 立体几何 3D 可视化工具模板

用法:
    from geometry3d import Geometry3DPlotter
    # 或直接运行: python3 geometry3d.py

功能:
    - 自动配置中文 (PingFang SC / Heiti SC / …)
    - 绘制顶点 + 标签 (含防重叠偏移)
    - 绘制棱 (线段)
    - 绘制半透明面 (Poly3DCollection)
    - 绘制向量 (quiver, 法向量或方向向量)
    - 标记线段上的参数点 (G = B + t*(F-B))
    - 二面角法向量示意

参考:
    math-output-format/references/3d-geometry-reconstruction.md
    用于高考/竞赛立体几何题的坐标验证和可视化
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.lines import Line2D

# ── 中文配置 ──
_CANDIDATES = ['PingFang SC', 'Heiti SC', 'Hiragino Sans GB',
               'STKaiti', 'STSong', 'SimSun', 'SimHei']
_FOUND = None
for c in _CANDIDATES:
    try:
        fp = matplotlib.font_manager.findfont(c, fallback_to_default=False)
        if 'DejaVu' not in fp:
            _FOUND = c
            break
    except Exception:
        continue
if _FOUND:
    plt.rcParams['font.sans-serif'] = [_FOUND] + plt.rcParams['font.sans-serif']
    plt.rcParams['axes.unicode_minus'] = False


class Geometry3DPlotter:
    """立体几何 3D 绘图器

    Example:
        pts = {'A': [0,0,0], 'B': [1,1.732,0], 'C': [3,1.732,0], 'D': [2,0,0],
               'E': [2,0,3.464], 'F': [2,1.732,1.732]}
        G = np.array([1.5, 1.732, 0.866])  # 参数点

        plotter = Geometry3DPlotter(pts)
        plotter.add_edges([('A','B'),('B','C'),('C','D'),('D','A')])
        plotter.add_point('G', G, color='red')
        plotter.add_face([pts['A'], pts['D'], pts['E']], color='#FF6B6B', alpha=0.2)
        plotter.add_vector(origin=np.array([1.5,0.866,0.433]),
                           vector=np.array([0,-1,2]), color='red', label='n₁')
        plotter.show(elev=22, azim=-60)
    """

    def __init__(self, points, title='立体几何 3D 视图', figsize=(12, 10)):
        """
        Args:
            points: dict {name: np.array([x, y, z])}
            title: 图标题
            figsize: 画布大小
        """
        self.points = {k: np.array(v, dtype=float) for k, v in points.items()}
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        self.ax.set_xlabel('X', fontsize=12, labelpad=10)
        self.ax.set_ylabel('Y', fontsize=12, labelpad=10)
        self.ax.set_zlabel('Z', fontsize=12, labelpad=10)
        self.ax.grid(True, alpha=0.25)

        # 默认标签偏移 (防止重叠)
        self._label_offsets = {}
        # 自定义图例句柄
        self._legend_handles = []

    def set_label_offsets(self, offsets):
        """设置标签偏移量
        Args:
            offsets: {name: (dx, dy, dz)}
        """
        self._label_offsets = offsets

    def add_edges(self, edge_pairs, color='#2C3E50', linewidth=2.5,
                  linestyle='-', label=None):
        """绘制棱 (线段列表)

        Args:
            edge_pairs: [(name1, name2), ...]
            color: 线条颜色
            linewidth: 线宽
            linestyle: 线型
            label: 图例标签 (仅首条线段会被加到图例)
        """
        for i, (s, t) in enumerate(edge_pairs):
            xs = [self.points[s][0], self.points[t][0]]
            ys = [self.points[s][1], self.points[t][1]]
            zs = [self.points[s][2], self.points[t][2]]
            lbl = label if (i == 0 and label) else None
            line = self.ax.plot(xs, ys, zs, color=color, linewidth=linewidth,
                                linestyle=linestyle, solid_capstyle='round',
                                label=lbl)
        if label:
            self._legend_handles.append(
                Line2D([0], [0], color=color, linewidth=linewidth,
                       linestyle=linestyle, label=label))

    def add_face(self, vertices, color='gray', alpha=0.15,
                 edgecolor='#888', linewidth=1.0, label=None):
        """绘制半透明面

        Args:
            vertices: 顶点列表 [np.array, np.array, ...] 或 [[x,y,z], ...]
            color: 填充色
            alpha: 透明度
            edgecolor: 边色 (None = 不描边)
            linewidth: 边线宽
        """
        verts = [np.array(v, dtype=float) for v in vertices]
        poly = Poly3DCollection([verts], alpha=alpha, color=color,
                                 edgecolor=edgecolor, linewidth=linewidth)
        self.ax.add_collection3d(poly)

    def add_point(self, name, pos, color='#1a1a2e', size=100,
                  edgecolors='white', zorder=5, label=None):
        """添加一个点并标注文字

        Args:
            name: 标签文字
            pos: np.array([x, y, z])
            color: 点颜色
            size: 点大小
            edgecolors: 描边色
            zorder: 层级
            label: 图例标签
        """
        if isinstance(pos, (list, tuple)):
            pos = np.array(pos)
        self.ax.scatter(*pos, color=color, s=size, zorder=zorder,
                        edgecolors=edgecolors, linewidth=1, label=label)
        offset = self._label_offsets.get(name, (0.15, 0.15, 0))
        self.ax.text(pos[0] + offset[0], pos[1] + offset[1],
                     pos[2] + offset[2], name,
                     fontsize=14, fontweight='bold', color='#1a1a2e')

    def add_vertices(self, colors=None, sizes=None):
        """批量绘制所有顶点

        Args:
            colors: dict {name: color} 或 None (统一黑色)
            sizes: dict {name: size} 或 None (统一 100)
        """
        if colors is None:
            colors = {}
        if sizes is None:
            sizes = {}
        for name, pos in self.points.items():
            c = colors.get(name, '#1a1a2e')
            s = sizes.get(name, 100)
            self.add_point(name, pos, color=c, size=s)

    def add_vector(self, origin, vector, color='red', linewidth=2.5,
                   alpha=0.8, arrow_length_ratio=0.2, label=None):
        """绘制向量 (quiver)

        Args:
            origin: 起点 np.array([x, y, z])
            vector: 向量 np.array([dx, dy, dz])
            color: 颜色
            linewidth: 线宽
            alpha: 透明度
            arrow_length_ratio: 箭头大小比
            label: 图例标签
        """
        self.ax.quiver(origin[0], origin[1], origin[2],
                       vector[0], vector[1], vector[2],
                       color=color, linewidth=linewidth, alpha=alpha,
                       arrow_length_ratio=arrow_length_ratio, label=label)
        if label:
            m = '>' if arrow_length_ratio > 0 else 'o'
            self._legend_handles.append(
                Line2D([0], [0], color=color, linewidth=linewidth,
                       marker=m, markersize=8, label=label))

    def add_param_point_on_segment(self, name, start, end, t,
                                    color='#E74C3C', size=150):
        """在线段上添加参数点 G = start + t*(end-start)

        Args:
            name: 标签名
            start: 起点名 (str)
            end: 终点名 (str)
            t: 参数 t ∈ [0,1]
            color: 点颜色
            size: 点大小
        Returns:
            np.array: 点坐标
        """
        s = self.points[start]
        e = self.points[end]
        pos = s + t * (e - s)
        self.add_point(name, pos, color=color, size=size,
                       edgecolors='white')
        return pos

    def set_limits(self, xlim=None, ylim=None, zlim=None):
        """设定坐标轴范围"""
        if xlim:
            self.ax.set_xlim(*xlim)
        if ylim:
            self.ax.set_ylim(*ylim)
        if zlim:
            self.ax.set_zlim(*zlim)

    def add_legend(self, loc='upper right', fontsize=10):
        """添加图例"""
        if self._legend_handles:
            self.ax.legend(handles=self._legend_handles, loc=loc,
                          fontsize=fontsize, framealpha=0.9)

    def show(self, elev=25, azim=-60, save_path=None, dpi=200):
        """显示/保存 3D 图

        Args:
            elev: 仰角
            azim: 方位角
            save_path: 保存路径 (None=不保存)
            dpi: 分辨率
        """
        self.ax.view_init(elev=elev, azim=azim)
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
            print(f'✅ 已保存: {save_path} ({dpi}dpi)')
        plt.close()


# ═══════════════════════════════════════════════
# 演示: 多面体 ABCDEF + 二面角 D-AG-E (BG=1)
# ═══════════════════════════════════════════════
if __name__ == '__main__':
    sqrt3 = np.sqrt(3)

    # 顶点坐标
    pts = {
        'A': (0, 0, 0),
        'B': (1, sqrt3, 0),
        'C': (3, sqrt3, 0),
        'D': (2, 0, 0),
        'E': (2, 0, 2*sqrt3),
        'F': (2, sqrt3, sqrt3),
    }

    plotter = Geometry3DPlotter(pts, title='多面体 ABCDEF 及二面角 D-AG-E')

    # 标签偏移 (防重叠)
    plotter.set_label_offsets({
        'A': (-0.4, -0.3, 0), 'B': (0, 0.35, 0),
        'C': (0.3, 0.35, 0), 'D': (0.3, -0.3, 0),
        'E': (0.3, -0.3, 0.1), 'F': (-0.1, 0.3, 0.3),
    })

    # 绘制顶点
    plotter.add_vertices()

    # 绘制半透明面
    plotter.add_face([pts['A'], pts['B'], pts['C'], pts['D']],
                     color='gray', alpha=0.12, label='底面 ABCD')
    plotter.add_face([pts['A'], pts['D'], pts['E']],
                     color='#FF6B6B', alpha=0.20)
    plotter.add_face([pts['B'], pts['C'], pts['F']],
                     color='#4ECDC4', alpha=0.25)
    plotter.add_face([pts['D'], pts['E'], pts['F']],
                     color='#FFE66D', alpha=0.18)
    plotter.add_face([pts['A'], pts['B'], pts['F']],
                     color='#95E1D3', alpha=0.18)
    plotter.add_face([pts['A'], pts['E'], pts['F']],
                     color='#F38181', alpha=0.18)
    plotter.add_face([pts['C'], pts['D'], pts['E']],
                     color='#AA96DA', alpha=0.18)
    plotter.add_face([pts['B'], pts['C'], pts['E']],
                     color='#C9B1FF', alpha=0.10)

    # 绘制棱
    plotter.add_edges([
        ('A','B'),('B','C'),('C','D'),('D','A'),  # 底面
        ('D','E'),                                  # 垂直棱
        ('A','F'),('B','F'),('C','F'),             # 侧棱
        ('E','F'),('B','E'),('C','E'),             # 顶棱
    ], label='棱')

    # G 点 (BG = 1, t=1/2)
    G = plotter.add_param_point_on_segment('G', 'B', 'F', 0.5)

    # AG 虚线
    plotter.add_edges([('A', 'G')], color='#E74C3C', linewidth=2.5,
                      linestyle='--', label='AG (二面角的棱)')

    # 法向量 (从 AG 中点发出)
    M_AG = (np.array(pts['A']) + G) / 2
    n1 = np.cross(np.array(pts['D']) - np.array(pts['A']), G - np.array(pts['A']))
    n1 = n1 / np.linalg.norm(n1) * 0.8
    n2 = np.cross(np.array(pts['E']) - np.array(pts['A']), G - np.array(pts['A']))
    n2 = n2 / np.linalg.norm(n2) * 0.8

    plotter.add_vector(M_AG, n1, color='#C0392B', label='n₁ (DAG法向)')
    plotter.add_vector(M_AG, n2, color='#2980B9', label='n₂ (EAG法向)')

    plotter.set_limits(xlim=(-0.5, 3.5), ylim=(-0.8, 2.8), zlim=(-0.5, 4.0))
    plotter.add_legend()
    plotter.show(elev=22, azim=-65, save_path='/tmp/geometry3d-demo.png')
