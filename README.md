# Math Textbook Authoring

Turn a math syllabus into a structured LaTeX textbook with consistent chapter formatting, domain-specific proof/style audits, and a verifiable delivery checklist. Works for analysis, algebra, topology, number theory, or any structured math subject.

```yaml
name: math-textbook-authoring
description: "Use when the user wants to turn a math syllabus/outline into a structured LaTeX textbook — generates consistent chapter templates, applies domain-specific proof coverage audits (analysis/topology/algebra/number-theory), and enforces a delivery checklist before compilation. Do NOT use for one-off LaTeX documents, non-math writing, or textbooks where the user has no syllabus."
```

## What it does

- **Guided workflow** — reader portrait → syllabus parsing → scaffold generation → chapter template → domain audit → delivery checklist
- **Domain-specific audits** — 5 built-in (structural, analysis, topology, algebra, number-theory), extensible
- **No hardcoded content** — exercise count, proof depth, figure style all negotiated per reader portrait
- **Platform-agnostic** — works with any LLM agent (Hermes, Codex, Claude Code, ChatGPT, etc.)

## Example output

This skill has produced a 257-page mathematical analysis textbook (30 chapters, 900+ exercises, 57 figures) and a linear algebra chapter (6 pages, 8 exercises). The template is cross-domain — topology, algebra, and number-theory textbooks use the same structure with different audit criteria.

## Installation

### Hermes Agent

```bash
cp SKILL.md ~/.hermes/profiles/<profile>/skills/mathematics/math-textbook-authoring/SKILL.md
```

Then load it: `skill_view(name='math-textbook-authoring')`

### Claude Code

Copy the skill to your project's skills directory — Claude auto-invokes it:

```bash
mkdir -p .claude/skills
cp SKILL.md .claude/skills/math-textbook-authoring.md
```

Then just say what you need: `"I have a linear algebra syllabus — help me structure the LaTeX."`

### Codex CLI

Codex reads `AGENTS.md` in your repo. Reference the skill there:

```bash
echo '[instructions](SKILL.md)' >> AGENTS.md
```

Or pipe it directly: `codex exec "$(cat SKILL.md) 帮我搭线性代数教材的章节结构"`

### Copy-paste

Open the skill file and paste its contents into your agent's system prompt, or reference it in your project's `CLAUDE.md` / `AGENTS.md`.

## Usage

1. Provide a syllabus (chapter list with topics)
2. The skill guides you through reader profiling, scaffold generation, chapter templating, domain audits, and a delivery checklist
3. Output: structured LaTeX files ready to compile

No syllabus? The skill can help you define one from a course name or topic list.

## File structure

```
textbooks/
├── trigonometry/       # Named after the subject
│   ├── book.tex
│   ├── shared/preamble.tex
│   ├── chapters/
│   ├── figures/
│   └── book.pdf
└── linear-algebra/     # Another subject, separate directory
    ├── book.tex
    └── ...
```

## Test prompts

**Should trigger:**
- "I have a syllabus for a topology textbook. Can you help me structure the LaTeX?"
- "帮我写一本线性代数教材，我有大纲。先帮我搭章节结构。"

**Should NOT trigger:**
- "Fix this LaTeX document, it won't compile" → use a LaTeX cleanup skill
- "Explain what compactness means in topology" → pure Q&A

**Should stop:**
- "Write me a textbook" (no syllabus) → the skill asks for a syllabus first

## License

广东工业大学

## 贡献

感谢好兄弟刘勇江的细心指导与建议。
