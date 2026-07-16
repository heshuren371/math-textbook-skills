# math-textbook-authoring

Pipeline for authoring math textbooks — takes a syllabus, generates LaTeX chapters with consistent formatting, produces vector figures, runs domain-specific audits, and compiles to PDF.

## What's here

| File | Purpose |
|------|---------|
| **[SKILL.md](SKILL.md)** | The skill — load this into Hermes Agent, Claude Code, or Codex CLI |
| **[book.pdf](book.pdf)** | Example output: 257-page mathematical analysis textbook |
| `mathbook-pipeline.py` | Automation pipeline (init → chapter → audit → fix → build) |
| `book.tex` | LaTeX master file |
| `figures/` | 57 vector figures with generation scripts |
| `shared/preamble.tex` | LaTeX preamble |

## Quick Start

```bash
# Install LaTeX compiler
brew install tectonic

# Clone and try the example
git clone https://github.com/heshuren371/math-textbook-skills.git
cd math-textbook-skills
tectonic book.tex    # → book.pdf (257 pages, ~30s first compile)

# Start your own textbook
python3 mathbook-pipeline.py init "My Textbook"
python3 mathbook-pipeline.py chapter new ch01 "First Chapter"
```

## Use as a Skill

**Hermes Agent:**
```bash
cp SKILL.md ~/.hermes/profiles/<profile>/skills/mathematics/math-textbook-authoring/
```

**Claude Code:**
```bash
claude-code --instructions SKILL.md
```

**Codex CLI:**
```bash
codex run --instructions SKILL.md
```

## How it works

```
Syllabus → Chapter Template → Write Content → Generate Figures → Audit → Fix → Compile → PDF
```

The pipeline (`mathbook-pipeline.py`) automates the mechanical parts: chapter scaffolding, domain-specific checks (ε-N/ε-δ completeness, axiom coverage), and auto-fixes for 11 common LaTeX errors.

The skill (`SKILL.md`) guides the AI through content generation: reader portrait, cognitive dependency mapping, chapter structure, figure generation, and delivery checklist.

## License

MIT
