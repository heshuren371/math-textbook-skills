---
name: latex-figure-drawing
description: 用 Python + matplotlib 生成精确的数学图形，导出为 PDF 矢量图供 LaTeX 插入，避免手写 tikz 坐标误差。涵盖几何图（角度/三角形/平行线/立体）和函数图的成熟模式。
emoji: 📊
color: "#1565C0"
---

# LaTeX 数学图绘制工具

## 核心决策：Python 画图 > 手写 TikZ

本 session 中第12章的手写 TikZ 图被用户三次指出拥挤/看不清（刻度重叠、Δ标注挡住、文字挤在一起）。第14章的初始 TikZ 版本同样存在角标错位、字母重叠等问题。

**结论：对所有带坐标轴的函数图、有角度弧线的几何图、涉及多层标注的示意图，优先用 Python + matplotlib 生成矢量 PDF，再用 `\includegraphics` 插入**。手写 TikZ 只保留给极简单的无坐标图（如箭头示意图、长方形分割）。

Python 方案优势：
- 坐标精确到浮点数，不会算错
- 标注位置可微调（`xshift`, `yshift`, `xytext`）
- 颜色/线型/字体统一控制
- 修改时只改 Python 参数后重跑，不碰 LaTeX 源码
- 导出为 PDF 矢量格式，LaTeX 插入无失真

## 字体配置（macOS 中文支持）

```python
import matplotlib
matplotlib.use('Agg')            # 后台模式（无 GUI）
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['PingFang SC', 'Heiti SC', 'STHeiti', 'Arial Unicode MS'],
    'font.size': 12,
    'axes.linewidth': 1.0,
    'axes.unicode_minus': False,   # 避免负号显示为方框
})
```

注意必须先设 `matplotlib.use('Agg')`——在无显示器终端中运行时，不设这个会报错。

## 保存函数

```python
import os
def save(fig, name, out_dir='figures'):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    fig.savefig(path + '.pdf', format='pdf', bbox_inches='tight', pad_inches=0.08)
    fig.savefig(path + '.png', format='png', dpi=200, bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)
    print(f'  ✓ {name}')
```

同时保存 PDF（矢量供 LaTeX）和 PNG（供快速预览）。`pad_inches=0.08` 留少量边距避免裁切，dpi=200 保证预览清晰度。

**⚠️ 边距控制**：`bbox_inches='tight'` 会让每张图的最终尺寸不同（取决于标注文字的分布）。如果要求所有图在 LaTeX 中插入时大小一致，改用固定 `set_xlim`/`set_ylim` + `figsize`，并控制 `pad_inches` 而非依赖 tight。

## 绘图规范标准（教材级）

所有教材图遵循统一视觉规范，避免同一张书中出现风格割裂：

```python
C_MAIN = '#000000'   # 主体线（三角形边、坐标轴）
C_AUX  = '#555555'   # 辅助线（虚线、标注线）
C_BLUE = '#1a5276'   # 蓝色标注（角1、同位角）
C_RED  = '#922b21'   # 红色标注（角2、内错角）
C_FILL = '#eaf2f8'   # 浅色填充背景
```

**线宽层次**：
- 主体图形：`lw=2.0`（三角形边、坐标轴、平行线）
- 辅助线/标注线：`lw=1.0`（距离标记、半径标注）
- 被遮挡边：`lw=1.2, linestyle='--'`（3D 图中被前面的面挡住的边）
- 角弧线：`lw=1.5`

**字体**：
- 中文标签：`fontsize=11`
- 数学符号：`fontsize=12`
- 公式框内：`fontsize=12, bbox=dict(boxstyle='round,pad=0.25')`

**标注间距**：文字与图形边缘间距 ≥ 0.15 坐标单位，避免拥挤重叠。

## 几何图绘制模式

### 角度弧线（Arc patch）

```python
from matplotlib.patches import Arc
arc = Arc((cx, cy),            # 圆心坐标
          2*r, 2*r,            # width, height（半径的两倍）
          theta1=start_deg,    # 起始角度（度制，逆时针）
          theta2=end_deg,      # 终止角度
          lw=1.5, color='blue')
ax.add_patch(arc)
```

**常用角度弧线参数：**
- `theta1=0, theta2=60` → 从水平向右到 60° 的弧（锐角标注）
- `theta1=270, theta2=315` → 向下偏右的弧（内错角标注）
- `theta1=180, theta2=135` → 向左上方的弧（补角标注）
- 注意 Arc 的 `(cx,cy)` 不在 (0,0) 时，需要计算精确角度

### 三角形（Polygon patch）

```python
from matplotlib.patches import Polygon
verts = [(0,0), (2.5,0), (1.5,1.8)]  # 三个顶点 (x,y) 元组
tri = Polygon(verts, closed=True, fill=None, edgecolor='black', lw=1.5)
ax.add_patch(tri)
```

`fill=None` 或 `fill=False` 画空心三角形。如需填充用 `facecolor='#ccccff', alpha=0.5`。

### 直角标记

```python
s = 0.3  # 直角符号边长
ax.plot([x, x+s], [y, y], 'k-', lw=1)      # 水平短线
ax.plot([x, x], [y, y+s], 'k-', lw=1)      # 垂直短线
```

### 箭头射线

```python
ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
```

`''` 表示无文字标注的纯箭头。`xy` 是箭头指向位置，`xytext` 是箭头起始位置。

### 双行标签（不重叠）

```python
ax.text(x, y, f'{title}\n{sub}', ha='center', va='top', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none'))
```

双行标签合并为一个节点，用 `align=center` 或 `\n` 分行。加 `bbox` 白色背景遮住下方内容，避免视觉干扰。

### 立体图（mplot3d + 斜二测画法）

对于长方体、柱体、锥体等三维图形，有两种方法：

**方法 A：matplotlib 的 mplot3d（推荐用于简单立体）**
```python
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111, projection='3d')
```

**方法 B：2D 斜二测画法（更可控）**
画一个前面矩形 + 后面矩形偏移 + 连接线，模拟三维：
```python
# 前面 4×2
ax.plot([0,4,4,0,0],[0,0,2,2,0],'k-',lw=2)
# 后面（偏移 (1,1)）
ax.plot([1,5,5,1,1],[1,1,3,3,1],'k-',lw=1)
# 连接线
for (x,y),(x2,y2) in [((0,0),(1,1)),((4,0),(5,1)),((4,2),(5,3)),((0,2),(1,3))]:
    ax.plot([x,x2],[y,y2],'k-',lw=0.8)
```

方法 B 不需要 3D 渲染，不会出现 z-order 问题，适合教材示意图。

### 圆柱/圆锥（椭圆 + 侧线）

```python
from matplotlib.patches import Ellipse
ell = Ellipse((cx, cy), width, height, facecolor='#ccccff', edgecolor='black', lw=1.5)
ax.add_patch(ell)
```

圆柱 = 上下椭圆 + 两侧竖直线；圆锥 = 底椭圆 + 两侧线交于一点；球体 = 圆 + 半径箭头。

## 函数图绘制模式

```python
x = np.linspace(-1, 5, 200)
fig, ax = plt.subplots(figsize=(5, 4))
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.plot(x, 2*x + 1, 'r-', label='$y = 2x + 1$', lw=2)
ax.plot(x, -x + 4, 'b-', label='$y = -x + 4$', lw=2)
ax.axhline(y=5, color='gray', linestyle='--', lw=0.8)

ax.set_xlim(-1, 5); ax.set_ylim(-1, 7)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.legend(fontsize=10)
```

**关键设置：**
- `spines[].set_position('zero')` — 将坐标轴移到中心（y=0, x=0），而非图边缘。适合第12章函数图
- `spines[].set_color('none')` — 隐藏上/右框线
- 线宽 `lw=2` 函数线、`lw=0.8` 辅助线（区分主次）

## 多函数对比图模式

教材中经常需要把多个函数放在一起对比（六种基本函数、变换前后）。以下四种模式来自 `gen_ch02.py` 实战：

### 模式A：多面板网格（subplot）

用 `plt.subplots(rows, cols)` 创建子图网格，每个子图展示一个函数：

```python
fig, axes = plt.subplots(2, 3, figsize=(14, 9))
funcs = [
    ('y = x',     lambda x: x,        (-3, 3), (-3, 3)),
    ('y = x²',    lambda x: x**2,     (-3, 3), (-1, 10)),
    ('y = 1/x',   lambda x: 1/x,      (-3, 3), (-5, 5), True),  # True=跳过x=0
    ('y = |x|',   lambda x: np.abs(x), (-3, 3), (-0.5, 3.5)),
]
for ax, (title, f, xr, yr, *skip) in zip(axes.flat, funcs):
    xs = np.linspace(xr[0], xr[1], 500)
    ys = np.array([f(x) for x in xs])
    if skip and skip[0]:
        ys[np.abs(xs) < 0.01] = np.nan
    ax.plot(xs, ys, 'b-', lw=2)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_xlim(*xr); ax.set_ylim(*yr)
    ax.set_title(title, fontsize=15)
    ax.grid(True, alpha=0.3)
plt.tight_layout()
```

### 模式B：叠加对比（同一坐标系多条曲线）

适合展示平移/对称/翻折变换，配合标注箭头：

```python
x = np.linspace(-4, 6, 400)
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, x**2,     'b-',  lw=2, label='y = x²（原函数）')
ax.plot(x, (x-2)**2, 'r-',  lw=2, label='y = (x-2)²（右移2）')
ax.plot(x, x**2 + 3, 'g-',  lw=2, label='y = x² + 3（上移3）')
ax.annotate('顶点 (0,0)', (0, 0), xytext=(10, -30),
            textcoords='offset points', fontsize=11,
            arrowprops=dict(arrowstyle='->', color='blue'))
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
```

### 模式C：翻折变换（fill_between 高亮）

```python
x = np.linspace(-3, 3, 500)
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, x**2 - 1, 'b--', lw=1.5, label='y = x² - 1')
ax.plot(x, np.abs(x**2 - 1), 'r-', lw=2.5, label='y = |x² - 1|')
x_fill = np.linspace(-1, 1, 200)
ax.fill_between(x_fill, 0, -(x_fill**2 - 1), color='red', alpha=0.15)
ax.legend(fontsize=12)
```

`fill_between(x, y_lower, y_upper)` 填充 `y_lower` 和 `y_upper` 之间的区域。

### 模式D：垂线检验法对比（左右子图）

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
x = np.linspace(-2, 2, 400)
ax1.plot(x, x**2, 'b-', lw=2)
ax1.axvline(1, color='red', ls='--', alpha=0.7)
ax1.set_title('[是] 函数\\n每条竖线只交1个点', fontsize=13)
ax1.grid(True, alpha=0.3)
theta = np.linspace(0, 2*np.pi, 400)
ax2.plot(2*np.cos(theta), 2*np.sin(theta), 'r-', lw=2)
ax2.axvline(0.5, color='red', ls='--', alpha=0.7)
ax2.set_title('[不是] 函数\\n竖线 x=0.5 交了2个点', fontsize=13)
ax2.grid(True, alpha=0.3)
ax2.set_aspect('equal')  # 圆必须等比例
plt.tight_layout()
```

## 标注交点

```python
ax.plot(2, 5, 'go', markersize=8)          # 绿色实心圆
ax.annotate('$(2, 5)$', xy=(2, 5),         # 标注文字
            xytext=(2.3, 5.3),              # 文字偏移位置
            arrowprops=dict(arrowstyle='->', lw=0.5))
```

## LaTeX 与 Python 图对接注意事项

### 数字与中文括号的间距（详见 memory 教训）

在 LaTeX 正文中，`600（6` 渲染后看起来像 `6006`，因为中文左括号 `（` 紧贴数字，在 PDF 字体下难以区分。

**解决方法：** 把算式放进数学模式，再用中文括号写说明：
```latex
% ❌ 错误
注意 0.6 \times 1000 = 600（6 的小数点右移三位...

% ✅ 正确
注意 \( 0.6 \times 1000 = 600 \)（6 的小数点右移三位...
```

注意 `\)（` ——数学模式的右括号紧接中文左括号，中间无空格。这在 PDF 渲染中能清晰区分数字和说明文字。

### 图文件名管理

- 每章一个 `gen_chNN.py` 脚本，生成该章所有图
- 图文件名格式：`chNN_descriptive_name.pdf`
- 确保 `.pdf` 和 `.png` 同时保存（PDF 供 LaTeX 插入，PNG 供快速预览）

```latex
% 单张图
\includegraphics[width=0.38\textwidth]{figures/ch14_angle_demo.pdf}

% 三张并排（用 hfill 自动间距）
\begin{center}
\includegraphics[width=0.28\textwidth]{figures/a.pdf}\hfill
\includegraphics[width=0.28\textwidth]{figures/b.pdf}\hfill
\includegraphics[width=0.28\textwidth]{figures/c.pdf}
\end{center}
```

`\hfill` 优于 `\qquad`——弹性间距自动适应页面宽度，不会因文字长度不同而溢出或重叠。

## 几何正确性检查清单（必须通过才能保存）

绘图是教材的数学对象，逻辑错误会导致学生学到错误的几何关系。每张图交付前必须通过以下检查：

### 角度类图
- [ ] 角度弧线的 `theta1`/`theta2` 是根据截线与平行线的**实际夹角**计算的，不是凭感觉填写
- [ ] 同位角弧线在两个交点的**同一方位**（均为平行线上方、截线右侧，或均为平行线下方、截线左侧）
- [ ] 内错角弧线在**平行线内侧**，形成 Z 字形，角度值与同位角互补（和为180°）
- [ ] 直角标记的两条小线组成90°角，且与三角形边缘相切而不是悬空

### 三角形类图
- [ ] 三角形三个顶点坐标与文字标签完全对应（不能标签写 A=(0,0) 实际画的是折线）
- [ ] 面积法证明图中四个直角三角形**全等**，两条直角边分别为 a 和 b（不能同一个三角形两条边都是 a 或都是 b）
- [ ] 面积法证明图中间留下的四边形是**边长为 c 的正方形**（验证三角形全等时那条斜边都是 c）

### 3D 立体图
- [ ] 圆柱/圆锥的侧面连接线**精确连接**椭圆长轴端点与顶点/另一椭圆长轴端点
- [ ] 圆柱/圆锥底面椭圆被遮挡的后半部分画**虚线**`linestyle='--'`
- [ ] 斜二测画法中被前面挡住的边画虚线，可见边画实线

## 统计图（Statistical Charts）绘制模式

统计章节（如第18章）使用图表而非几何图。同样用 matplotlib 生成矢量 PDF，但使用不同的 API。

### 条形图（Bar Chart）

```python
months = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
counts = [2, 1, 3, 1, 2, 1, 4, 1, 1, 1, 1, 1]
fig, ax = plt.subplots(figsize=(6, 3.5))
bars = ax.bar(months, counts, color='#85c1e9', edgecolor=C_MAIN, lw=1.0, width=0.7)
ax.set_ylabel('人数', fontsize=11)
ax.set_xticklabels(months, fontsize=9, rotation=45)
for bar, cnt in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            str(cnt), ha='center', va='bottom', fontsize=9)
```

**要点**：`ax.bar()` 返回 BarContainer；柱顶标注用 `bar.get_x() + bar.get_width()/2` 居中；分类数据用 `rotation=45` 处理长标签。

### 折线图（Line Chart）

```python
temps = [-2, 0, 8, 16, 22, 28, 30, 29, 24, 17, 8, 0]
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(months, temps, '-o', color=C_BLUE, lw=2.0, ms=5, mfc='white')
ax.grid(True, linestyle='--', alpha=0.4)
ax.annotate('最高 30°C', xy=(6, 30), xytext=(7, 29), ha='left', fontsize=9, color=C_RED)
```

**要点**：`'-o'` 实线+圆点；`mfc='white'` 圆点填白；`grid(True, linestyle='--', alpha=0.4)` 半透明网格线。

### 扇形图/饼图（Pie Chart）

```python
labels = ['食品', '住房', '交通', '教育', '医疗', '娱乐', '其他']
sizes = [30, 25, 12, 14, 8, 7, 4]
explode = (0.05, 0.05, 0, 0, 0, 0, 0)
fig, ax = plt.subplots(figsize=(5, 4))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, autopct='%1.0f%%',
    startangle=90, explode=explode,
    wedgeprops={'edgecolor': C_MAIN, 'linewidth': 1.0})
for t in autotexts:
    t.set_fontsize(9)
```

**要点**：`autopct='%1.0f%%'` 整数百分比；`startangle=90` 从12点方向开始；`wedgeprops` 保证边框风格统一。

### 频数直方图（Histogram）

```python
bins = [155, 160, 165, 170, 175]
fig, ax = plt.subplots(figsize=(6, 3.5))
n, bins, patches = ax.hist(heights, bins=bins, color='#85c1e9', edgecolor=C_MAIN, lw=1.2)
ax.set_xticks([157.5, 162.5, 167.5, 172.5])           # 组中值
ax.set_xticklabels(['155-160','160-165','165-170','170-175'], fontsize=9)
for i, (left, right) in enumerate(zip(bins[:-1], bins[1:])):
    mid = (left + right) / 2
    ax.text(mid, n[i] + 0.3, str(int(n[i])), ha='center', fontsize=10)
```

**要点**：`ax.hist()` 返回 `(n, bins, patches)`，`n` 即为频数数组；`set_xticks` 在组中值处设刻度；频数标注直接从 `n[i]` 获取。

## 数轴图解集表示（Number Line / Inequality Visualization）

当教材内容涉及不等式解集的数轴表示时（如第20章不等式），不可用手写的 ASCII 艺术（`\xrightarrow{\quad\circ\quad}`）。一位成人学习者的明确反馈：「这个数轴画的让我非常不满意」。

数轴图的核心是**空心圈（不含=）vs 实心点（含=）**的视觉对比，以及不等式组的**多层重叠高亮**。

### 基础绘制函数

```python
def draw_axis(ax, xmin, xmax):
    """画一条带箭头的数轴"""
    ax.plot([xmin, xmax], [0, 0], '-', color=C_MAIN, lw=1.2)
    ax.plot([xmax-0.1, xmax], [0.05, 0], '-', color=C_MAIN, lw=1.0)
    ax.plot([xmax-0.1, xmax], [-0.05, 0], '-', color=C_MAIN, lw=1.0)
    for tick in range(int(xmin)+1, int(xmax)):
        ax.plot(tick, 0, '|', color=C_AUX, ms=4, mew=0.8)

def open_circle(ax, x, y=0, r=0.09):
    """空心圈——不含该点（> 或 <）"""
    ax.add_patch(plt.Circle((x, y), r, fill=False, edgecolor=C_RED, lw=2.0, zorder=5))

def closed_circle(ax, x, y=0, r=0.09):
    """实心点——含该点（>= 或 <=）"""
    ax.add_patch(plt.Circle((x, y), r, fill=True, facecolor=C_RED, edgecolor=C_RED, lw=2.0, zorder=5))

def ray_right(ax, x_start, x_end, y=0, color=C_RED):
    """向右的加粗解集线段"""
    ax.plot([x_start, x_end], [y, y], '-', color=color, lw=3.5, solid_capstyle='butt')

def ray_left(ax, x_start, x_end, y=0, color=C_RED):
    """向左的加粗解集线段"""
    ax.plot([x_start, x_end], [y, y], '-', color=color, lw=3.5, solid_capstyle='butt')
```

### 三种标准图

**图1：单不等式解集** — `figsize=(5.5, 1.6)`，ylim=(-0.5,0.9)，在目标点画圈+射线+标签

**图2：不等式组重叠** — `figsize=(6.5, 2.8)`，ylim=(-1.2,1.0)。第一条条件画数轴上方(y=0.55)，第二条画下方(y=-0.55)，重叠区域在数轴上(y=0)加粗红色段，解集在下方向白底圆角框标注

**图3：四种基本类型一览** — `figsize=(7, 4.8)`，4个子图垂直排列，标题用`① 大大取大`等

### ⚠️ Unicode 代替 mathtext（关键 pitfall）

**matplotlib 内置 mathtext 不支持 `\ge`、`\le` 命令。** 这是本会话中 gen_ch20_numlines.py 第一次运行到 `ax.text(4, 0.55, '$x \ge 2$', ...)` 时直接崩溃的根因：

```
ParseFatalException: Unknown symbol: \ge, found '\'  (at char 2), (line:1, col:3)
```

**规则：数轴图所有文本标注使用纯 Unicode 字符。**

```python
# ❌ 错误：mathtext 不认 \ge \le
ax.text(4, 0.38, '$x \\ge 2$', ha='center', fontsize=12)

# ✅ 正确：直接用 Unicode
ax.text(4, 0.38, 'x ≥ 2', ha='center', fontsize=12, fontweight='bold')
ax.text(3, -0.3, '解集: 2 < x ≤ 4', ha='center', fontsize=11)
```

Unicode 常用字符：`≥` `≤` `≠` `×` `→` `±` `≈` `²` `³`。PingFang SC 原生支持全部。

只有在需要下标（`x₁`）、分式、根号等 mathtext 独有功能时才用 `$...$`，数轴图中极少出现。

参考脚本：`references/gen_ch20_numlines.py` — 完整的 ch20 数轴图生成，含四种类型对比。

## 常见几何错误 pitfalls

| 错误模式 | 典型表现 | 如何检查 |
|---|---|---|
| **同位角弧线角度凭感觉** | `theta1=45, theta2=90` 而截线其实是 40° | 手动计算截线斜率 `m=tan(θ)`，确认交点处同位角从平行线水平方向开始。使用 `np.arctan2(dy,dx)` 计算精确角度 |
| **面积法证明三角形放置错误** | 四个三角形不全等，中间不是正方形 | 验证每个三角形的两条直角边一为 a 一为 b，斜边都为 `sqrt(a²+b²)` |
| **圆柱/圆锥连接线脱离椭圆** | 母线 y 坐标不在椭圆边界上 | 验证连接线起点 `(x,y)` 满足 `(x-cx)²/r² + (y-cy)²/(h/2)² = 1` |
| **三角形标签与坐标脱节** | 标签说 A=(0,0) 但实际绘制的顶点不在 (0,0) | 通过列表 `verts = [(0,0), (2,0), (1,2)]` 绘制，确保标签与顶点一一对应 |
| **角弧开口不等于实际角度** | 小三角形标记角 C 的开口 53° 但实际角度 74° | 计算实际夹角 `arctan2(dy1,dx1) - arctan2(dy2,dx2)`，确保标记形状与实际角一致 |
| **数字紧贴中文括号** | `600（6` 在 PDF 渲染中容易误读为 `6006` | 把算式放进数学模式 `\\(...\\)` 再接中文说明，避免自然语言数字与中文括号直接相邻 |
| **图尺寸因 tight bbox 不可控** | 每张图插入 LaTeX 后实际大小不同，排版混乱 | 固定 `figsize`，用 `set_xlim`/`set_ylim` 统一定义画布范围，配合 `pad_inches=0.08` 而非依赖 `bbox_inches='tight'` |

## 顶点标注最佳实践（2026-07-13 修复案例）

用户反馈「有几个U型函数的顶点是错的」——来自第2章函数图的实际教训：

### 顶点标注四原则

1. **用 `ax.scatter()` 打点加黑边框**：`ax.scatter([x], [y], color='...', s=150, zorder=5, edgecolors='black', linewidths=1)`
   - `edgecolors='black'` 使顶点标记在任何背景色下都清晰可见
   - 大尺寸（`s=150` 或更大）确保顶点不会被曲线遮挡
   - `zorder=5` 确保标记在曲线上方

2. **`xytext` 偏移量避免文字覆盖曲线**：
   - 顶点在坐标轴上方（y>0 区域）：用 `xytext=(12, -25)` 偏移到下方
   - 顶点在坐标轴下方（y<0 区域）：用 `xytext=(12, 8)` 偏移到上方
   - 偏移量要足够大（≥ 15 点），否则文字与曲线或坐标轴重叠

3. **多曲线对比时，顶点颜色与曲线颜色一致**：
   ```python
   verts = [(0,0,'b'), (2,0,'r'), (0,3,'g')]
   for vx, vy, c in verts:
       ax.scatter([vx], [vy], color=c, s=150, zorder=5, edgecolors='black')
       ax.annotate(f'({vx},{vy})', (vx, vy), xytext=(12, -25),
                   textcoords='offset points', fontsize=13,
                   color=c, fontweight='bold')
   ```

4. **不要在原点额外标注"O"**：坐标轴的交点已经表示了原点的位置。加标字母"O"会导致用户看到"两个O点"——一个来自坐标轴交点，一个来自标注文字。如果必须标注原点，用坐标值 `(0,0)` 且确保不与坐标轴刻度标签重叠。

### 避免「坐标系有两个O点」的规则

- 不要在坐标轴交叉点处标注字母 "O" 或文字 "原点"
- 坐标轴标签 `ax.set_xlabel('x')` 和 `ax.set_ylabel('y')` 已经定义了轴的标识
- 刻度标签中的数字 `0` 在某些字体下看起来像大写 `O`，但这是正常的
- 如果需要强调原点位置，用一个小圆点 `ax.scatter([0], [0], color='black', s=40, zorder=5)` 即可

### 参考实现

完整案例见 `gen_ch02_v2.py`（第2章矢量图v2版），该版本修复了：
- 顶点标注偏移问题：改用大红点+黑边+精确偏移
- O点重复问题：移除所有原点的"O"文字标注
- 垂线检验法图：用颜色区分（绿色"是函数"/红色"不是函数"）替代不可显示的✓✗符号

---

## 函数图顶点标注和安全清单补充

在「安全清单（交付前检查）」末尾补充以下两项检查：

- [ ] 函数图的所有顶点已用 `ax.scatter()` 打点标记（大红点+黑边），`xytext` 偏移量足够大（≥15点），文字不与曲线或坐标轴重叠
- [ ] 原点处没有额外标注字母"O"或文字"原点"——坐标轴交点本身已经表示了原点位置

- [ ] 以上几何正确性检查清单已通过
- [ ] LaTeX 文档用 `xelatex` 编译（非 pdflatex，后者不支持中文）
- [ ] 每个 `\includegraphics` 路径正确（相对路径从 book.tex 所在目录出发）
- [ ] 编译后打开 PDF 目测所有图的位置、标注、颜色是否正确
- [ ] matplotlib `rcParams` 中已设 `axes.unicode_minus: False`（否则负号显示为方框）
- [ ] 中文标签在 PDF 中正常显示（不出现 □ 框）
- [ ] 所有图的 `figsize`、`xlim`、`ylim` 已统一设置，插入 LaTeX 后大小一致
- [ ] 三角形/立体图中的标签与实际绘制的顶点坐标完全对应
- [ ] 角度弧线的 `theta1`/`theta2` 是根据实际几何关系计算而来，非凭感觉填写

## 参考实现

`templates/drawing_template.py` — 标准绘图模板，含统一配置、保存函数、颜色常量。新图直接复制此文件修改。

`references/geometry_correctness_checklist.md` — 几何正确性验证的详细说明，包含各类图的验证方法与代码片段。

`references/gen_ch14_example.py` — 完整的第14章图生成脚本，涵盖：
- 角度弧线（Arc）
- 三角形分类（Polygon）
- 三角形内角标注（角度弧线 + 直角符号）
- 同位角/内错角图（截线 + 平行线 + 多层弧线）
- 平行/垂直线图

`references/gen_ch16_example.py` — 完整的第16章图生成脚本，涵盖：
- 直角三角形标注（a/b/c）
- 面积切割法证明（4个彩色三角形 + 小正方形）
- 梯子靠墙应用图
- 数轴上的 √2

`references/gen_ch20_numlines.py` — 第20章数轴图生成脚本，涵盖：
- 空心圈 vs 实心点对比（单不等式解集）
- 不等式组重叠高亮（双条件取交集）
- 四种基本类型一览（大大取大/小小取小/大小取中间/大小无解）
- **重要教训**：所有文本用 Unicode（`≥` `≤`）而非 mathtext（`\ge` `\le`），后者在 matplotlib 内置解析器中不兼容
