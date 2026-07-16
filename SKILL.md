---
name: math-textbook-authoring
description: "Pipeline for authoring math textbooks — takes a syllabus, generates LaTeX chapters with consistent structure, produces vector figures (matplotlib), runs domain-specific audits, and compiles to PDF. Configurable for any math subject."
emoji: 📘
tags: [latex, math, textbook, pipeline, matplotlib, education]
---

# Math Textbook Authoring

Turn a syllabus into a compiled LaTeX textbook with generated figures, automated audits, and consistent chapter formatting. Works for analysis, algebra, topology, number theory, or any structured math subject.

## Quick Start

```bash
brew install tectonic               # LaTeX compiler (or apt install texlive-full)
python3 mathbook-pipeline.py init "My Textbook"
python3 mathbook-pipeline.py chapter new ch01 "Title"
# Write content → audit → fix → compile
python3 mathbook-pipeline.py audit [domain] ch01
python3 mathbook-pipeline.py fix all ch01
tectonic book.tex                   # → book.pdf
```

## Pipeline

```
init                    Create project skeleton (book.tex, shared/, figures/, chapter dirs)
chapter new chXX "T"    Create chapter template
audit [domain] [ch]     Check for domain-specific errors
fix [layer] [ch]        Auto-fix errors
build                   Compile to PDF
```

## Chapter Template

Each chapter follows this configurable structure:

1. **Application context** — what the reader can do after this chapter
2. **Prerequisites** — concepts needed (skip for non-first chapters)
3. **Core content** — intuition → definitions → examples → theorems → figures
4. **Symbol cards** — new notation with pronunciation guides
5. **Numerical verification** — Python snippet verifying key claims
6. **Chapter summary** — progress check + bridge to next chapter
7. **Exercises** — configurable count and difficulty distribution

## Figure Generation

**Prefer matplotlib → PDF vector over hand-written TikZ.** TikZ is error-prone for coordinate axes, angle arcs, or multi-layer annotations. Matplotlib gives pixel-perfect positioning with tunable parameters.

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.sans-serif': ['DejaVu Sans'],  # or 'PingFang SC' for Chinese
    'font.size': 12,
    'axes.unicode_minus': False,
})

def save(fig, name, out_dir='figures'):
    import os
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    fig.savefig(path + '.pdf', format='pdf', bbox_inches='tight', pad_inches=0.08)
    fig.savefig(path + '.png', format='png', dpi=200, bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)
```

Insert in LaTeX: `\includegraphics{figures/chXX_figN.pdf}`

## Domain Audits

Plug in domain-specific checks. Built-in domains:

| Domain | Checks |
|--------|--------|
| `structural` | Environment pairing, math mode, Unicode characters |
| `analysis` | ε-N/ε-δ proof coverage for every `\lim` |
| `topology` | Open/closed sets, compactness, connectedness |
| `algebra` | Group/ring/field axioms, homomorphism properties |
| `number-theory` | Prime distribution, multiplicative functions |

Add custom domains in `mathbook-pipeline.py`'s `AUDIT_DOMAINS` dict.

## Fix Layers

| Layer | What it fixes |
|-------|---------------|
| `syntax` | LaTeX syntax (missing braces, wrong brackets) |
| `pairing` | Unclosed `\begin{...}` / `\end{...}` |
| `unicode` | Non-LaTeX chars (`→` → `\to`, `✓` → `\checkmark`) |
| `mathmode` | Chinese text in `\[...\]` → wrap with `\text{}` |
| `all` | Run all layers |

## LaTeX Compilation Traps

| # | Problem | Error | Fix |
|---|---------|-------|-----|
| 1 | `\begin{examplebox}[...}` has `}` instead of `]` | `Argument of \examplebox has an extra }` | `}` → `]` |
| 2 | `^` `_` `\frac` in box title | `Missing $ inserted` | Simplify or wrap in `{...}` |
| 3 | `\blacksquare` outside math mode | `Missing $ inserted` | `\(\blacksquare\)` |
| 4 | Missing `\end{exercise}` | Unclosed environment | Match every `\begin` |
| 5 | `\end{section}` used | `Undefined control sequence` | Delete it |
| 6 | `\verb` inside tabular/box | Compilation error | Use `\texttt` |
| 7 | `openright` in documentclass | Blank pages | Switch to `openany` |
| 8 | Unicode: `→` `✓` `✗` `℃` `【` `】` | `Missing character` | Use LaTeX commands |
| 9 | `\frac{...]{...}` bracket mismatch | `File ended while scanning \frac` | `]` → `}` |
| 10 | `\]` before `\end{cases}` | `Missing $ inserted` | `\end{cases}` first |
| 11 | `\end{aligned}` after `\]` | `Bad math environment delimiter` | `\]` last |

Auto-fix: `python3 mathbook-pipeline.py fix all`

## Configuration

Set in `mathbook-pipeline.py` or environment:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `EXERCISES_PER_CHAPTER` | varies | Exercise count per chapter |
| `LANGUAGE` | `zh` | `zh` (ctex) or `en` |
| `MATHBOOK_DOMAIN` | `analysis` | Default audit domain |

## Delivery Checklist

```
[ ] Every \lim has proof or citation (analysis domain)
[ ] No "obviously" / "trivially" / "omitted" in proofs
[ ] All \begin{...} match \end{...}
[ ] Chinese in math mode uses \text{}
[ ] Compiles: tectonic book.tex → book.pdf (zero errors)
[ ] Figures generate without errors
```

## Example Output

See `book.pdf` — a 257-page mathematical analysis textbook (30 chapters, 900+ exercises, 57 figures) built with this pipeline.

## Installation (Hermes Agent)

```bash
git clone https://github.com/heshuren371/math-textbook-skills.git
cp math-textbook-skills/SKILL.md ~/.hermes/profiles/<your-profile>/skills/mathematics/math-textbook-authoring/
```

## Installation (Claude Code / Codex CLI)

```bash
claude-code --instructions math-textbook-skills/SKILL.md
codex run --instructions math-textbook-skills/SKILL.md
```
