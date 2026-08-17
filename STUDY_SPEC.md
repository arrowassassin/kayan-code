# Study Curriculum Authoring Spec

Chapters live at `study/<section-dir>/<nn>-<slug>.mdx`. Each file starts with
frontmatter:

```
---
title: Short chapter name
section: 2 · Algorithm Patterns     <- EXACT section label, shared by the section's files
order: 21                            <- global ordering integer (see ranges below)
minutes: 25                          <- honest reading time
---
```

Sections, dirs and order ranges:
- `00-foundations` → `0 · Foundations` (orders 1–9)
- `01-data-structures` → `1 · Data Structures` (10–19)
- `02-patterns` → `2 · Algorithm Patterns` (20–29)
- `03-graphs` → `3 · Graphs` (30–39)
- `04-dp` → `4 · Dynamic Programming` (40–49)
- `05-google` → `5 · The Google Loop` (50–59)
- `06-system-design` → `6 · System Design` (60–69)
- `07-behavioral` → `7 · Behavioral (G&L)` (70–79)

## Voice and depth (this is the whole point)

Explain like the reader is a bright freshman meeting the idea for the FIRST
time — everyday analogy first, then the mechanism, then the code — but carry
the content ALL THE WAY to a senior-SDE bar: invariants, why-it-works
arguments, complexity, failure modes, and the follow-up trade-offs a Google
interviewer probes. Simple words, zero dumbing-down. Read
`study/00-foundations/01-big-o.mdx` first and match its voice exactly.

Rules:
- Analogy → intuition → mechanism → runnable-quality Python → complexity with
  the ONE spoken sentence justification → traps → "what the interviewer asks
  next".
- Use ```mermaid diagrams wherever structure/flow genuinely helps (state
  machines, tree shapes, request flows, partition diagrams). Dark-theme
  friendly; keep node text short. Not every chapter needs one — but visual
  topics (graphs, trees, system design flows, DP tables) should have 1–3.
- Tables for comparisons (structure ops, consistency levels, pattern
  signatures).
- Cross-link practice: reference bank problems as markdown links like
  `[Insert Interval](/problems/0057-insert-interval)` — slugs are the dirs in
  `problems/`. Every DS/algo chapter ends with a **Practice ladder**: 3–6
  bank problems ordered easy→hard, each with one line on what it trains.
- Python is the reference language; idiomatic, `heapq`/`deque`/`defaultdict`
  freely.
- No filler, no "in this chapter we will". Start teaching in sentence one.
- 900–1800 words per chapter (system-design walkthroughs may run longer).
- Facts about Google's process: state the well-established shape, and where
  candidate reports vary, say so plainly ("teams differ; expect X or Y").
  Never invent specific insider numbers.

The reader's context: Snowflake Applied AI round 2 next, AND a Google Senior
SDE (L5) loop — the curriculum serves both; Google-specific chapters carry
the L5 senior bar (ambiguity handling, follow-up escalation, code quality,
communication) explicitly.
