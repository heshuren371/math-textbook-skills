# 含参三角函数不等式恒成立

## 问题特征

\(f(x)=(1-a-x)\sin x-(1+a+x)\cos x\ge0\) 在 \([0,\pi]\) 上恒成立，求 \(a\)。

## 核心变换

\[
f(x)=(\sin x-\cos x)-(x+a)(\sin x+\cos x)
\]

利用 \(\sin x\pm\cos x=\sqrt2\sin(x\pm\pi/4)\) 可进一步化为：
\[
f(x)=\sqrt2\sin\!\Bigl(x-\frac\pi4\Bigr)-(x+a)\sqrt2\sin\!\Bigl(x+\frac\pi4\Bigr).
\]

## 区间符号分析

| 区间 | \(\sin x+\cos x\) | \(\sin x-\cos x\) | 处理方法 |
|------|:-----------------:|:-----------------:|---------|
| \((0,\pi/4)\) | \(+\) | \(-\) | 不等式两端均负，化为 \(a\le H(x)\) |
| \((\pi/4,3\pi/4)\) | \(+\) | \(+\) | 化为 \(a\le H(x)\) |
| \((3\pi/4,\pi)\) | \(-\) | \(+\) | 除以负数翻转不等号，得 \(a\ge H(x)\) |

其中 \(H(x)=\dfrac{\sin x-\cos x}{\sin x+\cos x}-x\).

## 关键恒等式

\[
\frac{\sin x-\cos x}{\sin x+\cos x}
=\frac{\tan x-1}{\tan x+1}
=\tan\!\Bigl(x-\frac\pi4\Bigr).
\]

故 \(H(x)=\tan(x-\pi/4)-x\).

## \(H(x)\) 的性质

\[
H'(x)=\sec^2\!\Bigl(x-\frac\pi4\Bigr)-1
=\tan^2\!\Bigl(x-\frac\pi4\Bigr)\ge0,
\]

\(H\) 在定义区间内严格增。

- \(H(0)=\tan(-\pi/4)-0=-1\)
- \(H(\pi)=\tan(3\pi/4)-\pi=-1-\pi\)

## 最终参数范围

\[
\begin{cases}
x\in[0,3\pi/4): & a\le H(x)\Rightarrow a\le\min H(x)=H(0)=-1\\[4pt]
x\in(3\pi/4,\pi]: & a\ge H(x)\Rightarrow a\ge\max H(x)=H(\pi)=-1-\pi
\end{cases}
\]

\[
\boxed{a\in[-1-\pi,\,-1]}
\]

## 本模式可迁移的其他题型

- \(g(x)=(p-x)\sin x-(q+x)\cos x\) 型：提取 \((\sin x\pm\cos x)\) 后分析
- 含 \(\sin x,\cos x\) 的线性组合：统一写成 \(A\sin(x+\varphi)\) 形式
