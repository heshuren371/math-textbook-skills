# External Document Parsing: MinerU as Math Content Input Pipeline

## Overview

This user (高考数学/竞赛数学 reviewer) uses [MinerU](https://mineru.net) (OpenDataLab's document parsing engine, 73.5k ⭐ on GitHub) to convert images/PDFs/scanned math problems into structured Markdown/JSON, then passes the extracted content to the mathematician for rigorous analysis.

**Workflow:**

```
用户 → 上传图片/PDF/扫描件 → mineru.net (GPU-backed OCR+VLM)
                                        ↓
                              Markdown/JSON（含 LaTeX 公式、HTML 表格）
                                        ↓
                              数学家数学分析（正确性、完整性、边界处理）
```

## Why MinerU for Math Input

| Feature | Benefit for Math Review |
|---------|------------------------|
| **公式 → LaTeX** | 数学表达式直接可读，无需手工转写 |
| **109 种语言 OCR** | 中英文混排数学题完整识别 |
| **表格 → HTML** | 复杂统计/列表题结构保留 |
| **版面还原** | 多栏/页眉页脚自动处理，输出按阅读顺序 |
| **无需本地安装** | mineru.net 在线版直接上传，GPU 加速 |

## Output Format Recommendation

**Always prefer Markdown over JSON** when passing MinerU output to the mathematician.

| Dimension | Markdown ✅ | JSON |
|-----------|-----------|------|
| LaTeX formula readability | Directly visible ✅ | Buried in string fields |
| Review speed | Zero processing ✅ | Needs parsing first |
| Table readability | Markdown table ✅ | HTML/nested arrays |
| Layout metadata | None (not needed) | Lots (noise) |
| Pass to AI analysis | Clean context ✅ | Extra noise fields |

JSON's strengths (bbox coordinates, confidence scores, page numbers) are not useful for math content analysis.

## Fallback Strategy: MinerU + LaTeX Live Dual Engine

When MinerU fails on complex formulas (matrices, multi-line equations, nested integrals), use a **secondary specialized formula OCR tool** as fallback:

```
MinerU full-page parse → inspect formula output → errors/missing?
                                                      ↓
                                                    yes ↓
                          Manual crop formula region → LaTeX Live → replace in Markdown
```

### Quantitative Analysis

If MinerU formula accuracy = 90% and LaTeX Live accuracy = 95%:

\[
\text{Final accuracy} = 0.9 \times 1 + 0.1 \times 0.95 = \mathbf{99.5\%}
\]

This is a **cascaded classifier with fallback** — from 90% to 99.5% is a qualitative leap.

### Trigger Strategy

| Trigger type | Condition |
|-------------|-----------|
| **Automatic** | Complex matrices, determinants, large equation systems |
| **Automatic** | Nested formulas containing `\int`, `\sum`, `\prod` |
| **Manual check** | Obvious garbled output (e.g., `\operatorname` split) |
| **Manual check** | Misplaced super/subscripts (`x^2` rendered as `x2`) |
| **Manual check** | Multi-line formulas merged into one line (`\begin{cases}` lost) |

### How to Apply

Do a **targeted replacement** in the MinerU Markdown — don't regenerate the whole document. The workflow takes ~2-5 minutes per complex PDF.

### Worth It Assessment

| Scenario | Worth it? |
|----------|-----------|
| 高考/竞赛 test paper (5-10 formulas total) | **Highly worth it** — 30s manual check |
| 300-page textbook | **Not worth it** — fix the first-stage pipeline instead |

## Installation (Local, if needed)

```bash
pip install uv -i https://mirrors.aliyun.com/pypi/simple
uv pip install -U "mineru[all]" -i https://mirrors.aliyun.com/pypi/simple
export MINERU_MODEL_SOURCE=modelscope   # 无法访问 huggingface 时
mineru -p <input_path> -o <output_path>
```

**System requirements (pipeline backend, pure CPU):**
- Python 3.10–3.13
- RAM: ≥16GB (recommended 32GB)
- Disk: ≥20GB free (model downloads)
- GPU optional (pipeline runs on CPU)

**Our environment:** macOS (Apple Silicon), 16GB RAM, Python 3.11.15, no GPU → pipeline backend works but slow for large images.

## When to Recommend

- User sends a screenshot/photo of a math problem
- User has a scanned PDF with mixed text/formulas/tables
- User needs formula LaTeX extraction
- Document has complex layout (multi-column, headers/footers)
- User prefers not to type out the problem manually

## Alternatives (if MinerU isn't suitable)

| Tool | Strength | Weakness |
|------|----------|----------|
| **MinerU (web)** | Best for complex docs, formula LaTeX | Requires upload to external service |
| **MinerU + LaTeX Live (fallback)** | 99.5% formula accuracy achievable | Requires manual cropping for errors |
| **GPT-4o / Claude vision** | General-purpose image understanding | May hallucinate formulas |
| **pymupdf / marker-pdf** | Lightweight local PDF text extraction | Limited formula/table recognition |
| **Manual input** | Most reliable | User effort |

## Source

MinerU GitHub: https://github.com/opendatalab/MinerU
Online demo: https://mineru.net
