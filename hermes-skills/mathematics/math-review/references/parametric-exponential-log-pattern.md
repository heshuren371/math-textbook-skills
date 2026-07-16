# Parametric Exponential + Logarithm Inequality Pattern

## Trigger

Problems of the form: \(f(x)=ae^{x-1}-\ln x+\ln a\ge 1\) for all \(x>0\), find \(a\) (or min integer \(m\)).

## Standard Workflow

### Step 1 — Necessity via special point

Plug \(x=1\):

\[
f(1)=a+\ln a-1\ge 1\;\Longrightarrow\;a+\ln a\ge 2.
\]

Since \(a+\ln a\) is strictly increasing, \(a\ge 1\).

### Step 2 — Critical point analysis

\[
f'(x)=ae^{x-1}-\frac1x,\qquad f''(x)=ae^{x-1}+\frac1{x^2}>0.
\]

\(f'(x)=0\) has unique solution \(x_0\) with \(a x_0 e^{x_0-1}=1\).  
If \(a\ge 1\) then \(x_0\le 1\).

### Step 3 — Parameter elimination

From \(f'(x_0)=0\): \(ae^{x_0-1}=1/x_0\) ⇒ \(\ln a = 1-x_0-\ln x_0\).

\[
f(x_0)=\frac1{x_0}-\ln x_0+1-x_0-\ln x_0 = \frac1{x_0}-x_0+1-2\ln x_0.
\]

### Step 4 — Reduce to single variable

\(h(x)=\dfrac1x-x-2\ln x\), \(h'(x)=-\dfrac1{x^2}-1-\dfrac2x<0\), \(h(1)=0\).  
\(a\ge 1\) ⇒ \(x_0\le 1\) ⇒ \(h(x_0)\ge 0\) ⇒ \(f(x_0)\ge 1\).

## Pitfalls

- Parameter elimination works **only** at the critical point \(x_0\).
- Special-point necessity ≠ sufficiency — always prove the full range.
- Integer optimization: check the integer above the real threshold.
