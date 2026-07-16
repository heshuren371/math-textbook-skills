---
name: math-textbook-authoring
description: "Use when the user wants to turn a math syllabus/outline into a structured LaTeX textbook — generates consistent chapter templates, applies domain-specific proof coverage audits (analysis/topology/algebra/number-theory), and enforces a delivery checklist before compilation. Unlike a general-purpose writing assistant, this skill provides the structural framework, format standards, and audit criteria. Do NOT use for one-off LaTeX documents, non-math writing, or textbooks where the user has no syllabus."
emoji: 📘
tags: [latex, math, textbook, structure, education, audit]
---

# Math Textbook Authoring

Turn a math syllabus into a structured LaTeX textbook with consistent chapter formatting, domain-appropriate proof/style audits, and a verifiable delivery checklist. The skill provides the **scaffold** — chapter structure, audit criteria, output format — but does not dictate content (exercise count, proof complexity, figure choice). Those are negotiated with the user based on their reader portrait and syllabus.

## When to use

- User has a math syllabus and wants consistent LaTeX chapter structure
- User needs domain-specific audits (proof coverage, formalism checks)
- User wants a delivery checklist before finalizing a textbook
- The textbook covers a structured math field (analysis, algebra, geometry, topology, number theory, etc.)

## Workflow

```
1. (If no syllabus) Help user define one from course name or topic list
2. Collect reader portrait
3. Parse syllabus
4. Generate LaTeX scaffold
5. For each chapter: build from template
6. Run domain audit
7. Apply delivery checklist
8. Compile
```

## Step 2: Reader Portrait

Before generating anything, collect these from the user:

- **Math background** — prerequisites they can assume; concepts they tend to forget
- **Goal** — exam prep, self-study, reference text, course material
- **Time budget** — how much the reader can spend per session
- **Attitude** — math-anxious, neutral, willing to grind
- **Target level** — what the reader should be able to do after each chapter
- **Exercise preference** — competition problems, self-check with answers, or none
- **Figure style** — conceptual diagrams, numerical plots, or no figures

These answers determine chapter depth, exercise density, and figure complexity.

## Step 3: Parse Syllabus

From the user's syllabus, extract:

- **Chapter list** with titles and topics
- **Dependencies** between chapters (prerequisite ordering)
- **Domain tags** per chapter (analysis, algebra, topology, number-theory)
- **Special requirements** (proof-heavy, computation-heavy, application-driven)

Group chapters by domain for shared audit criteria.

## Step 4: Generate LaTeX Scaffold

Name the project directory after the book title or subject. This keeps multiple textbooks organized:

```
textbooks/                    # Optional parent folder for all textbooks
├── trigonometry/             # Named after the subject
│   ├── book.tex
│   ├── shared/preamble.tex
│   ├── chapters/ch01.tex
│   ├── figures/
│   └── book.pdf
└── linear-algebra/           # Another subject, separate directory
    ├── book.tex
    ├── shared/preamble.tex
    ├── chapters/ch01.tex
    ├── figures/
    └── book.pdf
```

Convention: `kebab-case` directory name matching the book title (e.g., `real-analysis`, `abstract-algebra`, `probability-and-statistics`). Ask the user to confirm the directory name before generating.

**Document class**: recommend `ctexbook` (Chinese), `book` (English), `memoir` (customizable). Let the user decide.

**Theorem environments**: define `definition`, `theorem`, `lemma`, `corollary`, `proof`, `example`, `remark` via `\newtheorem` or `amsthm`. Use `tcolorbox` for visual distinction if needed.

**Preamble defaults**: `amsmath`, `amssymb`, `amsthm`, `graphicx`, `hyperref`, `geometry`. Extend per user request.

**TOC formatting**: Avoid tcolorbox colors bleeding into the table of contents. Use `hidelinks` to suppress link borders:
```latex
\usepackage[hidelinks, colorlinks=false]{hyperref}
```

## Step 5: Chapter Template

Each chapter follows this **configurable** structure. Adjust depth and sections based on the reader portrait:

```
\chapter{Title}

\section{Application context}
  — What the reader can do after mastering this chapter.
  — bridge from previous chapter (omit for chapter 1).

\section{Prerequisites}
  — Concepts assumed; link to earlier chapters for review.
  — Skip for chapters where all prerequisites are in the same book.

\section{Core content}
  Custom structure per subject. General pattern:
  1. Intuition / motivation
  2. Formal definitions
  3. Examples (worked, with commentary)
  4. Theorems and proofs (see domain audit for coverage expectations)
  5. Figures / diagrams (conceptual or computational)

\section{Chapter summary}
  — What was covered, in one paragraph.
  — Bridge sentence to next chapter.

\section{Exercises}
  Count and difficulty negotiated with user in Step 2.
  Consider tiered groups: basic check → application → extension.
```

Shape exercise count, proof depth, and figure choice from the reader portrait and syllabus. The template is a container — it provides structure, not content defaults.

## Step 6: Domain Audits

After generating each chapter, run the matching audit. Each audit produces a checklist of items the user (or the model) should verify.

### `structural` — default for any chapter
- [ ] Every `\begin{...}` has a matching `\end{...}`
- [ ] Math mode used correctly (`\(...\)` inline, `\[...\]` display)
- [ ] No Unicode in LaTeX math mode (use `\to`, `\checkmark`, etc.)
- [ ] Citation keys match bibliography entries

### `analysis` — real/complex analysis
- [ ] Every `\lim` statement has ε-N (sequences) or ε-δ (functions) proof or a citation to a source that does
- [ ] `\limsup`/`\liminf` used consistently with their formal definitions
- [ ] Continuity proofs mention the specific definition used (ε-δ, sequential)
- [ ] Convergence claims specify whether they refer to pointwise, uniform, or norm convergence

### `topology` — general/point-set topology
- [ ] Every claim about open/closed sets explicitly mentions the ambient topology
- [ ] Compactness arguments specify the definition used (open-cover, sequential for metric, etc.)
- [ ] Connectedness claims distinguish between connected, path-connected, and locally connected
- [ ] Continuous function claims reference the definition used (preimage of open is open, etc.)

### `algebra` — group/ring/field theory
- [ ] Every claim about a subgroup/normal subgroup explicitly verifies the closure conditions
- [ ] Homomorphism claims check the identity-preserving and operation-preserving properties
- [ ] For rings: distinguish between ring homomorphisms and algebra homomorphisms
- [ ] Quotient structures verified: well-definedness of the operation

### `number-theory` — elementary/analytic number theory
- [ ] Prime distribution claims cite the range (effective bound or asymptotic)
- [ ] Dirichlet convolution and Möbius inversion are properly introduced if used
- [ ] Modular arithmetic: specify the modulus explicitly in every equivalence
- [ ] Asymptotic notation explained on first use (O, o, ~, ≪)

To add a custom domain, define a new audit checklist in the skill body or in a separate reference file. The checklists above are starting points — prune or extend per user need.

## Step 7: Delivery Checklist

Before marking the textbook ready, run this checklist:

```
[ ] Chapter dependency order validated (no forward references to undefined content)
[ ] Theorem/proof coverage audit passed for target domain
[ ] No placeholder text ("TODO", "FIXME", "insert proof here")
[ ] All figures referenced in the text exist or are noted as to-be-created
[ ] User confirmed all content parameters (exercise count, figure style, depth)
[ ] Compiles to PDF without errors; output renders correctly
```

## Compilation

The agent should **describe** the compile command but not assume a specific LaTeX distribution:

```bash
# Pick one:
pdflatex book.tex && pdflatex book.tex   # (run twice for cross-refs)
tectonic book.tex                         # single-pass, handles most packages
xelatex book.tex                          # for Chinese (ctexbook) or custom fonts
lualatex book.tex                         # for OpenType fonts
```

Recommend `latexmk -pdf book.tex` for automatic re-run management if available.

For figures, recommend:
- **Vector graphics**: matplotlib (`plt.savefig('fig.pdf')`), TikZ for simple diagrams
- **Raster**: only when necessary (photographs, screenshots)
- Ask the user what tools they have. If they have matplotlib, recommend vector PDF output.

## Example Output

This skill has been used to produce a 257-page mathematical analysis textbook (30 chapters, 900+ exercises, 57 figures) and a linear algebra chapter (20+ pages, 6 figures, 30 exercises). The structure is cross-domain — topology, algebra, and number-theory textbooks use the same template with different audit criteria.

## Test Prompts

**Should trigger:**
- "I have a syllabus for a topology textbook. Can you help me structure the LaTeX?"
- "帮我写一本线性代数教材，我有大纲。先帮我搭章节结构。"

**Should NOT trigger:**
- "Fix this LaTeX document, it won't compile" → use a LaTeX cleanup skill
- "Explain what compactness means in topology" → pure Q&A, not textbook authoring

**Should stop:**
- "Write me a textbook" (no syllabus) → ask for syllabus first
- "Generate chapter 5" without a project scaffold → guide user through setup first
