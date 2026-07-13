# TikZ 数学图形排版质量规范

> 从 `数学基础重建` 教材系列开发中积累的排版经验。这些规则被违反了至少 6 次才形成。

## 基础原则

数学教材中的 TikZ 图不是装饰——它们承载教学内容。一个被遮挡的标注 = 一个学不会的概念。

## 规则 1：刻度数字与标注文字分侧

**最常见错误**：Δ 标注和刻度数字都在坐标轴同一侧，重叠。

```latex
% ❌ 错——Δx=1 在 x 轴下方，刻度 1,2 也在 x 轴下方，文字重叠
\draw[<->] (1,0) -- (2,0) node[midway,below] {\(\Delta x=1\)};
\foreach \x in {1,2} \draw (\x,0) node[below] {\x};

% ✅ 对——Δx=1 放 x 轴上方，刻度数字放下方
\draw[<->] (1,0) -- (2,0) node[midway,above] {\(\Delta x=1\)};
\foreach \x in {1,2} \draw (\x,0) node[below] {\x};
```

## 规则 2：刻度字体必须缩小

坐标轴刻度数字必须用 `\footnotesize` 或 `\scriptsize`，默认字体太大。

```latex
% ✅ 正确——5个以下的函数图用 \scriptsize
\foreach \x in {1,2,3,4,5}
  \draw (\x,0.06) -- (\x,-0.06) node[below,font=\scriptsize] {\x};

% ✅ 大于 10 个刻度（如 y 轴 2,4,6,8,10）用 \footnotesize
\foreach \y in {2,4,6,8,10}
  \draw (0.06,\y) -- (-0.06,\y) node[left,font=\footnotesize] {\y};
```

## 规则 3：Δ 标注从箭头线分离

`midway,right` 会让文字紧贴箭头线。加 `xshift` 和 `pos` 偏移。

```latex
% ❌ 错——紧贴箭头线，看不清
\draw[<->] (2,0) -- (2,2) node[midway,right] {\(\Delta y=2\)};

% ✅ 对——右移 4pt，位置偏下 65% 处
\draw[<->] (2,0) -- (2,2) node[pos=0.65,right,xshift=4pt,font=\scriptsize] {\(\Delta y=2\)};
```

## 规则 4：几何图的分类标签不要叠加

三个并列的三角形各自下方有标签时，用单节点 `align=center` 双行，不要用两个独立节点分两行。间距用 `\hfill` 不要用 `\qquad`。

```latex
% ✅ 正确——align=center 节点自动分行，\hfill 弹性分布
\begin{center}
\begin{tikzpicture}[scale=0.8]
  \draw[thick] (0,0) -- (2.5,0) -- (1.5,1.8) -- cycle;
  \node[below,align=center,font=\scriptsize] at (1.25,-0.3)
    {不等边三角形\\[2pt] 三边各不相等};
\end{tikzpicture}
\hfill
\begin{tikzpicture}[scale=0.8]
  ...
```

## 规则 5：几何图中角弧线必须对齐实际交点

同位角/内错角图的弧线必须从截线与平行线的实际交点位置画起，不能随意选坐标。

```latex
% ✅ 两条平行线 y=2 和 y=-2，截线 (-3,-3)→(3,3) 斜率=1
% 截线与上平行线交于 (2,2)，与下平行线交于 (-2,-2)
% 同位角：弧线从 (1.5,1.5) 开始 — 在交点附近
\draw[blue,thick] (1.5,1.5) arc (225:270:0.5);
% （arc (225:270:0.5) 在 225°到270°的弧，从 ("225°位置", y) 开始）
```

## 规则 6：避免非 \texttt{lstlisting} 中的 `#` 字符

LaTeX 中 `#` 是宏参数字符。章节标题中写 `### 有限小数` 会编译报错。

```latex
% ❌ 错
\section{### 有限小数}

% ✅ 对
\subsection{有限小数}
```

## 规则 7：中文左括号 `（` 不要紧贴数字

`600（6）` 在 PDF 中会被误读为 `6006`。

```latex
% ❌ 错——600紧贴（
注意 0.6 \times 1000 = 600（6 的小数点右移三位）

% ✅ 对——用数学模式隔开
注意 \( 0.6 \times 1000 = 600 \)（6 的小数点右移三位）
```

## 规则 8：避免深层嵌套的 tikz 条件

第6章用 27 个 `\ifnum...\else\ifnum` 嵌套来画 1-100 质数表——TeX 引擎报 100 个错误后中止编译。

```latex
% ❌ 错——27 层嵌套 ifnum
\ifnum\n=2 ...\else\ifnum\n=3 ...\else\ifnum\n=5 ...\else...

% ✅ 对——用 tabular 环境 + \mathbf{} 标记质数
\begin{array}{cccccccccc}
1 & \mathbf{2} & \mathbf{3} & 4 & \mathbf{5} & 6 & ...
\end{array}
```

**通用教训**：TikZ 中的复杂循环和条件分支应控制在 5 层以内。超过这个深度，用 LaTeX 的 tabular/array 替代。

## 规则 9：排版后必须肉眼检查

编译成功后，打开 PDF 检查：
1. 所有标注文字是否清晰可读（不被遮挡、不重叠）
2. 刻度数字大小是否合适
3. 几何图中的角标注位置是否正确
4. 相邻图形之间的间距是否足够
5. 数字和后随 `（` 是否分开了
